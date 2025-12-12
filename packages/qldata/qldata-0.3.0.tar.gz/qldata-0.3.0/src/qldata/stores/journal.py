"""Write-ahead log for stream data replay.

Provides durable journaling of stream data for crash recovery
and replay capabilities.
"""

from __future__ import annotations

import json
import logging
import os
import struct
import time
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger(__name__)

# Journal file format:
# Each entry: [4 bytes: length][payload bytes][4 bytes: checksum]
# Payload: JSON encoded {stream_id, seq, ts, data}

HEADER_SIZE = 4
CHECKSUM_SIZE = 4


def _crc32(data: bytes) -> int:
    """Calculate CRC32 checksum."""
    import zlib

    return zlib.crc32(data) & 0xFFFFFFFF


@dataclass
class JournalEntry:
    """A single entry in the data journal.

    Attributes:
        stream_id: Identifier for the stream (e.g., "binance:BTCUSDT:depth")
        sequence: Sequence number within the stream
        timestamp: When the data was received
        data: The actual data payload
    """

    stream_id: str
    sequence: int
    timestamp: datetime
    data: dict[str, Any]

    def to_bytes(self) -> bytes:
        """Serialize entry to bytes."""
        payload = {
            "stream_id": self.stream_id,
            "seq": self.sequence,
            "ts": self.timestamp.isoformat(),
            "data": self.data,
        }
        return json.dumps(payload, separators=(",", ":")).encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> JournalEntry:
        """Deserialize entry from bytes."""
        payload = json.loads(data.decode("utf-8"))
        return cls(
            stream_id=payload["stream_id"],
            sequence=payload["seq"],
            timestamp=datetime.fromisoformat(payload["ts"]),
            data=payload["data"],
        )


@dataclass
class Checkpoint:
    """Checkpoint marking last processed sequence per stream.

    Attributes:
        stream_id: Stream identifier
        sequence: Last processed sequence
        timestamp: When checkpoint was created
    """

    stream_id: str
    sequence: int
    timestamp: datetime


class DataJournal:
    """Write-ahead log for stream data with replay support.

    Provides durable storage of stream data for:
    - Crash recovery (replay missed data)
    - Debugging (replay historical streams)
    - Auditing (complete data trail)

    Example:
        >>> journal = DataJournal(Path("./data/journal"))
        >>> journal.append("binance:BTCUSDT:depth", {"b": [[50000, 1]], "a": []}, seq=100)
        >>> journal.checkpoint("binance:BTCUSDT:depth", 100)
        >>>
        >>> # After restart
        >>> for entry in journal.replay("binance:BTCUSDT:depth", from_seq=95):
        ...     process(entry.data)
    """

    def __init__(
        self,
        path: Path | str,
        max_size_mb: int = 100,
        sync_interval: int = 100,
    ) -> None:
        """Initialize data journal.

        Args:
            path: Directory for journal files
            max_size_mb: Maximum journal file size before rotation
            sync_interval: Entries between fsync calls
        """
        self._path = Path(path)
        self._path.mkdir(parents=True, exist_ok=True)

        self._max_size_bytes = max_size_mb * 1024 * 1024
        self._sync_interval = sync_interval

        self._current_file: Path | None = None
        self._file_handle: Any | None = None
        self._handle_stack: ExitStack | None = None
        self._entries_since_sync = 0
        self._total_entries = 0

        # Checkpoints per stream
        self._checkpoints: dict[str, Checkpoint] = {}
        self._checkpoint_file = self._path / "checkpoints.json"
        self._load_checkpoints()

    def _get_current_file(self) -> Path:
        """Get current journal file, creating if needed."""
        if self._current_file is None:
            self._current_file = self._path / f"journal_{int(time.time())}.bin"

        # Check size and rotate if needed
        if (
            self._current_file.exists()
            and self._current_file.stat().st_size >= self._max_size_bytes
        ):
            self._close_file()
            self._current_file = self._path / f"journal_{int(time.time())}.bin"

        return self._current_file

    def _open_file(self) -> Any:
        """Open current journal file for appending."""
        if self._file_handle is None:
            file_path = self._get_current_file()
            if self._handle_stack is None:
                self._handle_stack = ExitStack()
            self._file_handle = self._handle_stack.enter_context(file_path.open("ab"))
            logger.debug(f"Opened journal file: {file_path}")
        return self._file_handle

    def _close_file(self) -> None:
        """Close current journal file."""
        if self._file_handle is not None:
            self._file_handle.flush()
            os.fsync(self._file_handle.fileno())
            self._file_handle.close()
            self._file_handle = None
        if self._handle_stack is not None:
            self._handle_stack.close()
            self._handle_stack = None
            logger.debug(f"Closed journal file: {self._current_file}")

    def append(
        self,
        stream_id: str,
        data: dict[str, Any],
        seq: int,
        timestamp: datetime | None = None,
    ) -> None:
        """Append data to the journal.

        Args:
            stream_id: Stream identifier
            data: Data payload to store
            seq: Sequence number
            timestamp: Data timestamp (uses current time if not specified)
        """
        entry = JournalEntry(
            stream_id=stream_id,
            sequence=seq,
            timestamp=timestamp or datetime.now(timezone.utc),
            data=data,
        )

        payload = entry.to_bytes()
        checksum = _crc32(payload)

        # Write: length | payload | checksum
        handle = self._open_file()
        handle.write(struct.pack("<I", len(payload)))
        handle.write(payload)
        handle.write(struct.pack("<I", checksum))

        self._entries_since_sync += 1
        self._total_entries += 1

        # Periodic sync
        if self._entries_since_sync >= self._sync_interval:
            handle.flush()
            os.fsync(handle.fileno())
            self._entries_since_sync = 0

    def replay(
        self,
        stream_id: str,
        from_seq: int | None = None,
        to_seq: int | None = None,
    ) -> Iterator[JournalEntry]:
        """Replay journal entries for a stream.

        Args:
            stream_id: Stream identifier to replay
            from_seq: Start sequence (inclusive), or None for all
            to_seq: End sequence (inclusive), or None for all

        Yields:
            JournalEntry objects in order
        """
        # Get all journal files sorted by time
        journal_files = sorted(self._path.glob("journal_*.bin"))

        for journal_file in journal_files:
            yield from self._read_file(journal_file, stream_id, from_seq, to_seq)

    def _read_file(
        self,
        file_path: Path,
        stream_id: str | None,
        from_seq: int | None,
        to_seq: int | None,
    ) -> Iterator[JournalEntry]:
        """Read entries from a journal file."""
        try:
            with open(file_path, "rb") as f:
                while True:
                    # Read length
                    length_bytes = f.read(HEADER_SIZE)
                    if len(length_bytes) < HEADER_SIZE:
                        break

                    length = struct.unpack("<I", length_bytes)[0]

                    # Read payload
                    payload = f.read(length)
                    if len(payload) < length:
                        logger.warning(f"Truncated entry in {file_path}")
                        break

                    # Read and verify checksum
                    checksum_bytes = f.read(CHECKSUM_SIZE)
                    if len(checksum_bytes) < CHECKSUM_SIZE:
                        logger.warning(f"Missing checksum in {file_path}")
                        break

                    expected_checksum = struct.unpack("<I", checksum_bytes)[0]
                    actual_checksum = _crc32(payload)

                    if expected_checksum != actual_checksum:
                        logger.warning(f"Checksum mismatch in {file_path}, skipping entry")
                        continue

                    # Parse entry
                    try:
                        entry = JournalEntry.from_bytes(payload)
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.warning(f"Failed to parse entry: {e}")
                        continue

                    # Filter by stream and sequence
                    if stream_id is not None and entry.stream_id != stream_id:
                        continue
                    if from_seq is not None and entry.sequence < from_seq:
                        continue
                    if to_seq is not None and entry.sequence > to_seq:
                        continue

                    yield entry

        except FileNotFoundError:
            pass
        except Exception as e:
            logger.error(f"Error reading journal file {file_path}: {e}")

    def checkpoint(self, stream_id: str, seq: int) -> None:
        """Record a checkpoint for a stream.

        Args:
            stream_id: Stream identifier
            seq: Last processed sequence number
        """
        self._checkpoints[stream_id] = Checkpoint(
            stream_id=stream_id,
            sequence=seq,
            timestamp=datetime.now(timezone.utc),
        )
        self._save_checkpoints()
        logger.debug(f"Checkpoint saved for {stream_id}: seq={seq}")

    def last_checkpoint(self, stream_id: str) -> int | None:
        """Get last checkpoint sequence for a stream.

        Args:
            stream_id: Stream identifier

        Returns:
            Last checkpointed sequence, or None if no checkpoint
        """
        if stream_id in self._checkpoints:
            return self._checkpoints[stream_id].sequence
        return None

    def _load_checkpoints(self) -> None:
        """Load checkpoints from file."""
        if not self._checkpoint_file.exists():
            return

        try:
            with open(self._checkpoint_file) as f:
                data = json.load(f)
                for stream_id, cp_data in data.items():
                    self._checkpoints[stream_id] = Checkpoint(
                        stream_id=stream_id,
                        sequence=cp_data["sequence"],
                        timestamp=datetime.fromisoformat(cp_data["timestamp"]),
                    )
            logger.info(f"Loaded {len(self._checkpoints)} checkpoints")
        except Exception as e:
            logger.warning(f"Failed to load checkpoints: {e}")

    def _save_checkpoints(self) -> None:
        """Save checkpoints to file."""
        data = {
            cp.stream_id: {
                "sequence": cp.sequence,
                "timestamp": cp.timestamp.isoformat(),
            }
            for cp in self._checkpoints.values()
        }

        try:
            with open(self._checkpoint_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save checkpoints: {e}")

    def rotate(self) -> Path | None:
        """Rotate to a new journal file.

        Returns:
            Path to the rotated (old) file, or None if no file was active
        """
        old_file = self._current_file
        self._close_file()
        self._current_file = None
        logger.info(f"Rotated journal, archived: {old_file}")
        return old_file

    def cleanup(self, max_age_hours: int = 24) -> int:
        """Remove old journal files.

        Args:
            max_age_hours: Maximum age of files to keep

        Returns:
            Number of files removed
        """
        cutoff = time.time() - (max_age_hours * 3600)
        removed = 0

        for journal_file in self._path.glob("journal_*.bin"):
            # Extract timestamp from filename
            try:
                file_ts = int(journal_file.stem.split("_")[1])
                if file_ts < cutoff:
                    journal_file.unlink()
                    removed += 1
                    logger.info(f"Removed old journal: {journal_file}")
            except (ValueError, IndexError):
                pass

        return removed

    def close(self) -> None:
        """Close the journal and save state."""
        self._close_file()
        self._save_checkpoints()
        logger.info("Journal closed")

    def get_stats(self) -> dict:
        """Get journal statistics.

        Returns:
            Dict with file and entry counts
        """
        journal_files = list(self._path.glob("journal_*.bin"))
        total_size = sum(f.stat().st_size for f in journal_files if f.exists())

        return {
            "file_count": len(journal_files),
            "total_size_mb": total_size / (1024 * 1024),
            "total_entries": self._total_entries,
            "checkpoint_count": len(self._checkpoints),
            "current_file": str(self._current_file) if self._current_file else None,
        }

    def __enter__(self) -> DataJournal:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
