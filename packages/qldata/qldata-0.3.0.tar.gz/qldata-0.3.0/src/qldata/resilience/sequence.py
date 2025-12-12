"""Sequence tracking for WebSocket streams.

Provides gap detection, duplicate filtering, and order book
snapshot/delta reconciliation for reliable live data.
"""

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

logger = logging.getLogger(__name__)


class SequenceResult(Enum):
    """Result of recording a sequence number."""

    OK = "ok"  # Normal, in-order message
    GAP = "gap"  # Gap detected (missed messages)
    DUPLICATE = "duplicate"  # Already seen this sequence
    OUT_OF_ORDER = "out_of_order"  # Arrived late but still valid
    RESET = "reset"  # Sequence was reset (reconnection)


@dataclass
class Gap:
    """Represents a gap in sequence numbers.

    Attributes:
        start: First missing sequence number
        end: Last missing sequence number (inclusive)
        detected_at: When gap was detected
    """

    start: int
    end: int
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def size(self) -> int:
        """Number of missing messages."""
        return self.end - self.start + 1


class SequenceTracker:
    """Tracks sequence numbers to detect gaps and duplicates.

    Used for WebSocket streams that include sequence numbers,
    allowing detection of missed messages and triggering resyncs.

    Example:
        >>> tracker = SequenceTracker("BTCUSDT", "depth")
        >>> result = tracker.record(100)
        >>> result = tracker.record(101)  # OK
        >>> result = tracker.record(105)  # GAP - missed 102, 103, 104
        >>> if tracker.needs_resync():
        ...     request_snapshot()
    """

    def __init__(
        self,
        symbol: str,
        stream_type: str,
        *,
        max_out_of_order: int = 10,
        gap_threshold: int = 100,
        history_size: int = 1000,
    ) -> None:
        """Initialize sequence tracker.

        Args:
            symbol: Trading symbol
            stream_type: Type of stream (e.g., "depth", "trades")
            max_out_of_order: Maximum out-of-order messages before gap
            gap_threshold: Gap size that triggers resync
            history_size: Number of recent sequences to track
        """
        self.symbol = symbol
        self.stream_type = stream_type
        self._max_out_of_order = max_out_of_order
        self._gap_threshold = gap_threshold
        self._history_size = history_size

        self._last_seq: int | None = None
        self._seen: set[int] = set()
        self._pending: dict[int, datetime] = {}  # Out-of-order messages waiting
        self._gaps: list[Gap] = []
        self._total_gaps = 0
        self._total_duplicates = 0
        self._needs_resync = False

    def record(self, seq: int) -> SequenceResult:
        """Record a sequence number and detect issues.

        Args:
            seq: Sequence number from WebSocket message

        Returns:
            SequenceResult indicating what happened
        """
        now = datetime.now(timezone.utc)

        # First message
        if self._last_seq is None:
            self._last_seq = seq
            self._seen.add(seq)
            logger.debug(f"[{self.symbol}:{self.stream_type}] First sequence: {seq}")
            return SequenceResult.OK

        # Check for duplicate
        if seq in self._seen:
            self._total_duplicates += 1
            logger.debug(f"[{self.symbol}:{self.stream_type}] Duplicate: {seq}")
            return SequenceResult.DUPLICATE

        # Normal in-order
        expected = self._last_seq + 1
        if seq == expected:
            self._last_seq = seq
            self._add_to_seen(seq)
            self._process_pending()
            return SequenceResult.OK

        # Sequence reset (jumped backwards significantly)
        if seq < self._last_seq - self._history_size:
            logger.warning(
                f"[{self.symbol}:{self.stream_type}] Sequence reset detected: "
                f"{self._last_seq} -> {seq}"
            )
            self.reset(seq)
            return SequenceResult.RESET

        # Out of order (arrived late)
        if seq < expected:
            self._add_to_seen(seq)
            logger.debug(f"[{self.symbol}:{self.stream_type}] Out of order: {seq} (expected {expected})")
            return SequenceResult.OUT_OF_ORDER

        # Gap detected
        gap_size = seq - expected
        if gap_size > 0:
            gap = Gap(start=expected, end=seq - 1, detected_at=now)
            self._gaps.append(gap)
            self._total_gaps += gap_size
            logger.warning(
                f"[{self.symbol}:{self.stream_type}] Gap detected: "
                f"missing {gap.start}-{gap.end} ({gap.size} messages)"
            )

            # Check if resync needed
            if gap_size >= self._gap_threshold:
                self._needs_resync = True
                logger.error(
                    f"[{self.symbol}:{self.stream_type}] Large gap ({gap_size}), resync required"
                )

            self._last_seq = seq
            self._add_to_seen(seq)
            return SequenceResult.GAP

        # Should not reach here
        self._last_seq = seq
        self._add_to_seen(seq)
        return SequenceResult.OK

    def _add_to_seen(self, seq: int) -> None:
        """Add to seen set, maintaining max size."""
        self._seen.add(seq)
        # Prune old entries if too large
        if len(self._seen) > self._history_size * 2:
            min_keep = max(self._seen) - self._history_size
            self._seen = {s for s in self._seen if s >= min_keep}

    def _process_pending(self) -> None:
        """Process any pending out-of-order messages."""
        while self._last_seq is not None and (self._last_seq + 1) in self._pending:
            next_seq = self._last_seq + 1
            del self._pending[next_seq]
            self._last_seq = next_seq
            logger.debug(f"[{self.symbol}:{self.stream_type}] Processed pending: {next_seq}")

    def get_gaps(self) -> list[Gap]:
        """Get list of detected gaps.

        Returns:
            List of Gap objects
        """
        return self._gaps.copy()

    def get_unfilled_gaps(self) -> list[Gap]:
        """Get gaps that haven't been filled.

        Returns:
            Gaps where messages are still missing
        """
        unfilled = []
        for gap in self._gaps:
            missing = [s for s in range(gap.start, gap.end + 1) if s not in self._seen]
            if missing:
                unfilled.append(Gap(start=min(missing), end=max(missing), detected_at=gap.detected_at))
        return unfilled

    def needs_resync(self) -> bool:
        """Check if stream needs resynchronization.

        Returns:
            True if large gap detected requiring snapshot resync
        """
        return self._needs_resync

    def mark_synced(self) -> None:
        """Mark stream as synchronized (after snapshot applied)."""
        self._needs_resync = False
        self._gaps.clear()
        logger.info(f"[{self.symbol}:{self.stream_type}] Marked as synced")

    def reset(self, from_seq: int | None = None) -> None:
        """Reset tracker state.

        Args:
            from_seq: New starting sequence number
        """
        self._seen.clear()
        self._pending.clear()
        self._gaps.clear()
        self._needs_resync = False

        if from_seq is not None:
            self._last_seq = from_seq
            self._seen.add(from_seq)
        else:
            self._last_seq = None

        logger.info(f"[{self.symbol}:{self.stream_type}] Reset to seq={from_seq}")

    @property
    def last_sequence(self) -> int | None:
        """Get last recorded sequence number."""
        return self._last_seq

    @property
    def total_gaps(self) -> int:
        """Total number of gap instances detected."""
        return self._total_gaps

    @property
    def total_duplicates(self) -> int:
        """Total number of duplicates detected."""
        return self._total_duplicates

    def get_stats(self) -> dict:
        """Get tracker statistics.

        Returns:
            Dict with gap and duplicate counts
        """
        return {
            "symbol": self.symbol,
            "stream_type": self.stream_type,
            "last_sequence": self._last_seq,
            "total_gaps": self._total_gaps,
            "total_duplicates": self._total_duplicates,
            "unfilled_gaps": len(self.get_unfilled_gaps()),
            "needs_resync": self._needs_resync,
        }


class OrderBookSyncer:
    """Manages order book synchronization via snapshot + delta updates.

    Handles the common exchange pattern where you receive:
    1. Initial snapshot with full order book
    2. Delta updates for price level changes

    The syncer ensures deltas are applied in order and triggers
    resync when gaps are detected.

    Example:
        >>> syncer = OrderBookSyncer("BTCUSDT")
        >>> syncer.apply_snapshot(initial_book, last_update_id=1000)
        >>> for delta in websocket_updates:
        ...     book = syncer.apply_delta(delta)
        ...     if book:
        ...         process(book)
        ...     elif syncer.needs_resync():
        ...         request_new_snapshot()
    """

    def __init__(
        self,
        symbol: str,
        *,
        buffer_size: int = 100,
    ) -> None:
        """Initialize order book syncer.

        Args:
            symbol: Trading symbol
            buffer_size: Max deltas to buffer before snapshot
        """
        self.symbol = symbol
        self._buffer_size = buffer_size

        self._bids: dict[Decimal, Decimal] = {}  # price -> quantity
        self._asks: dict[Decimal, Decimal] = {}
        self._last_update_id: int | None = None
        self._snapshot_update_id: int | None = None
        self._synced = False
        self._buffer: deque[dict] = deque(maxlen=buffer_size)

    def apply_snapshot(
        self,
        bids: list[tuple[Decimal, Decimal]],
        asks: list[tuple[Decimal, Decimal]],
        last_update_id: int,
    ) -> None:
        """Apply a full order book snapshot.

        Args:
            bids: List of (price, quantity) tuples
            asks: List of (price, quantity) tuples
            last_update_id: Snapshot's last update ID
        """
        self._bids = dict(bids)
        self._asks = dict(asks)
        self._snapshot_update_id = last_update_id
        self._last_update_id = last_update_id
        self._synced = True

        # Process buffered deltas
        processed = 0
        while self._buffer:
            delta = self._buffer.popleft()
            if self._should_apply_delta(delta):
                self._apply_delta_internal(delta)
                processed += 1

        logger.info(
            f"[{self.symbol}] Snapshot applied: {len(self._bids)} bids, {len(self._asks)} asks, "
            f"update_id={last_update_id}, processed {processed} buffered deltas"
        )

    def apply_delta(self, delta: dict) -> dict | None:
        """Apply a delta update to the order book.

        Args:
            delta: Delta update with structure:
                {
                    "U": first_update_id,
                    "u": last_update_id,
                    "b": [[price, qty], ...],  # bid updates
                    "a": [[price, qty], ...],  # ask updates
                }

        Returns:
            Current book state as dict if synced, None if buffering/needs resync
        """
        # Buffer if no snapshot yet
        if not self._synced:
            self._buffer.append(delta)
            return None

        # Check if delta is applicable
        if not self._should_apply_delta(delta):
            # Gap detected or old delta
            first_id = delta.get("U", delta.get("first_update_id", 0))
            if first_id > (self._last_update_id or 0) + 1:
                logger.warning(
                    f"[{self.symbol}] Delta gap: expected {self._last_update_id + 1}, "  # type: ignore
                    f"got {first_id}"
                )
                self._synced = False
            return None

        self._apply_delta_internal(delta)
        return self.get_book()

    def _should_apply_delta(self, delta: dict) -> bool:
        """Check if delta should be applied.

        Binance rule: first delta after snapshot should have
        U <= lastUpdateId + 1 AND u >= lastUpdateId + 1
        """
        if self._snapshot_update_id is None:
            return False

        first_id = delta.get("U", delta.get("first_update_id", 0))
        last_id = delta.get("u", delta.get("last_update_id", 0))

        # For first delta after snapshot
        if self._last_update_id == self._snapshot_update_id:
            return first_id <= self._snapshot_update_id + 1 <= last_id

        # For subsequent deltas
        expected = (self._last_update_id or 0) + 1
        return first_id == expected

    def _apply_delta_internal(self, delta: dict) -> None:
        """Apply delta to internal book state."""
        # Apply bid updates
        for update in delta.get("b", delta.get("bids", [])):
            price = Decimal(str(update[0]))
            qty = Decimal(str(update[1]))
            if qty == 0:
                self._bids.pop(price, None)
            else:
                self._bids[price] = qty

        # Apply ask updates
        for update in delta.get("a", delta.get("asks", [])):
            price = Decimal(str(update[0]))
            qty = Decimal(str(update[1]))
            if qty == 0:
                self._asks.pop(price, None)
            else:
                self._asks[price] = qty

        self._last_update_id = delta.get("u", delta.get("last_update_id"))

    def is_synced(self) -> bool:
        """Check if order book is synchronized.

        Returns:
            True if snapshot applied and no gaps
        """
        return self._synced

    def needs_resync(self) -> bool:
        """Check if resync is needed.

        Returns:
            True if gap detected or not synced
        """
        return not self._synced

    def get_book(self) -> dict:
        """Get current order book state.

        Returns:
            Dict with bids, asks, and metadata
        """
        sorted_bids = sorted(self._bids.items(), key=lambda x: x[0], reverse=True)
        sorted_asks = sorted(self._asks.items(), key=lambda x: x[0])

        return {
            "symbol": self.symbol,
            "bids": [(float(p), float(q)) for p, q in sorted_bids],
            "asks": [(float(p), float(q)) for p, q in sorted_asks],
            "last_update_id": self._last_update_id,
            "synced": self._synced,
        }

    def get_best_bid(self) -> tuple[Decimal, Decimal] | None:
        """Get best bid (highest price).

        Returns:
            (price, quantity) or None if empty
        """
        if not self._bids:
            return None
        price = max(self._bids.keys())
        return (price, self._bids[price])

    def get_best_ask(self) -> tuple[Decimal, Decimal] | None:
        """Get best ask (lowest price).

        Returns:
            (price, quantity) or None if empty
        """
        if not self._asks:
            return None
        price = min(self._asks.keys())
        return (price, self._asks[price])

    def reset(self) -> None:
        """Reset syncer state."""
        self._bids.clear()
        self._asks.clear()
        self._last_update_id = None
        self._snapshot_update_id = None
        self._synced = False
        self._buffer.clear()
        logger.info(f"[{self.symbol}] OrderBookSyncer reset")
