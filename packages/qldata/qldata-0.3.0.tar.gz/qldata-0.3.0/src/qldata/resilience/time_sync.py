"""Exchange time synchronization.

Provides clock drift calculation and timestamp correction
for accurate order book and trade timestamps.
"""

from __future__ import annotations

import asyncio
import logging
import statistics
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)


@dataclass
class TimeSyncResult:
    """Result of a time synchronization attempt.

    Attributes:
        server_time_ms: Server time in milliseconds
        local_time_ms: Local time when response received (ms)
        round_trip_ms: Round trip time in milliseconds
        drift_ms: Estimated clock drift (positive = local ahead)
    """

    server_time_ms: int
    local_time_ms: int
    round_trip_ms: float
    drift_ms: float


class TimeSyncManager:
    """Manages time synchronization with exchange servers.

    Exchanges often require accurate timestamps for:
    - Signed requests (within X ms of server time)
    - Accurate event ordering
    - Latency calculations

    Uses multiple samples to estimate clock drift, accounting
    for network latency variations.

    Example:
        >>> async def get_server_time():
        ...     resp = await client.get("/api/v3/time")
        ...     return resp["serverTime"]
        >>>
        >>> sync = TimeSyncManager()
        >>> drift = await sync.sync(get_server_time)
        >>> corrected = sync.correct_timestamp(datetime.now(timezone.utc))
    """

    def __init__(
        self,
        poll_interval: float = 60.0,
        sample_count: int = 5,
        max_history: int = 100,
    ) -> None:
        """Initialize time sync manager.

        Args:
            poll_interval: Seconds between automatic syncs
            sample_count: Number of samples per sync
            max_history: Maximum drift history to keep
        """
        self._poll_interval = poll_interval
        self._sample_count = sample_count
        self._max_history = max_history

        self._drift_ms: float = 0.0
        self._last_sync: float | None = None
        self._history: deque[TimeSyncResult] = deque(maxlen=max_history)
        self._latency_history: deque[float] = deque(maxlen=max_history)

        self._sync_task: asyncio.Task | None = None
        self._running = False

        # Callbacks
        self._on_drift_exceeded: list[tuple[float, Callable[[float], None]]] = []

    async def sync(
        self,
        fetch_server_time: Callable[[], Awaitable[int]],
        samples: int | None = None,
    ) -> float:
        """Perform time synchronization.

        Takes multiple samples and uses median to estimate drift,
        which is robust against network jitter.

        Args:
            fetch_server_time: Async function returning server time in ms
            samples: Number of samples (uses default if not specified)

        Returns:
            Estimated clock drift in milliseconds (positive = local ahead)
        """
        sample_count = samples or self._sample_count
        results: list[TimeSyncResult] = []

        for i in range(sample_count):
            try:
                result = await self._single_sync(fetch_server_time)
                results.append(result)
                self._history.append(result)
                self._latency_history.append(result.round_trip_ms)

                # Small delay between samples
                if i < sample_count - 1:
                    await asyncio.sleep(0.1)

            except Exception as e:
                logger.warning(f"Time sync sample {i + 1} failed: {e}")

        if not results:
            logger.error("All time sync samples failed")
            return self._drift_ms

        # Use median drift (robust to outliers)
        drifts = [r.drift_ms for r in results]
        self._drift_ms = statistics.median(drifts)
        self._last_sync = time.time()

        logger.info(
            f"Time sync complete: drift={self._drift_ms:.1f}ms, "
            f"avg_latency={statistics.mean(r.round_trip_ms for r in results):.1f}ms"
        )

        # Check drift thresholds
        for threshold_ms, callback in self._on_drift_exceeded:
            if abs(self._drift_ms) > threshold_ms:
                try:
                    callback(self._drift_ms)
                except Exception as e:
                    logger.warning(f"Error in drift callback: {e}")

        return self._drift_ms

    async def _single_sync(
        self,
        fetch_server_time: Callable[[], Awaitable[int]],
    ) -> TimeSyncResult:
        """Perform single time sync sample."""
        local_before = int(time.time() * 1000)
        server_time = await fetch_server_time()
        local_after = int(time.time() * 1000)

        round_trip = local_after - local_before
        # Estimate server time at midpoint of request
        local_midpoint = local_before + round_trip // 2
        drift = local_midpoint - server_time

        return TimeSyncResult(
            server_time_ms=server_time,
            local_time_ms=local_midpoint,
            round_trip_ms=round_trip,
            drift_ms=drift,
        )

    async def start_polling(
        self,
        fetch_server_time: Callable[[], Awaitable[int]],
    ) -> None:
        """Start automatic time sync polling.

        Args:
            fetch_server_time: Async function returning server time in ms
        """
        if self._running:
            return

        self._running = True

        async def poll_loop() -> None:
            while self._running:
                try:
                    await self.sync(fetch_server_time)
                except Exception as e:
                    logger.error(f"Time sync poll failed: {e}")
                await asyncio.sleep(self._poll_interval)

        self._sync_task = asyncio.create_task(poll_loop())
        logger.info(f"Started time sync polling (interval={self._poll_interval}s)")

    def stop_polling(self) -> None:
        """Stop automatic time sync polling."""
        self._running = False
        if self._sync_task:
            self._sync_task.cancel()
            self._sync_task = None
        logger.info("Stopped time sync polling")

    def server_time(self) -> datetime:
        """Get estimated current server time.

        Returns:
            Estimated server time as datetime
        """
        local_now_ms = int(time.time() * 1000)
        server_now_ms = local_now_ms - int(self._drift_ms)
        return datetime.fromtimestamp(server_now_ms / 1000, tz=timezone.utc)

    def server_time_ms(self) -> int:
        """Get estimated current server time in milliseconds.

        Returns:
            Estimated server time in milliseconds
        """
        return int(time.time() * 1000) - int(self._drift_ms)

    def correct_timestamp(self, local_ts: datetime) -> datetime:
        """Correct a local timestamp to server time.

        Args:
            local_ts: Local datetime to correct

        Returns:
            Corrected datetime (estimated server time)
        """
        local_ms = int(local_ts.timestamp() * 1000)
        server_ms = local_ms - int(self._drift_ms)
        return datetime.fromtimestamp(server_ms / 1000, tz=timezone.utc)

    def correct_timestamp_ms(self, local_ms: int) -> int:
        """Correct a local timestamp (ms) to server time.

        Args:
            local_ms: Local time in milliseconds

        Returns:
            Corrected time in milliseconds
        """
        return local_ms - int(self._drift_ms)

    @property
    def drift_ms(self) -> float:
        """Current estimated clock drift in milliseconds.

        Positive = local clock is ahead of server.
        """
        return self._drift_ms

    @property
    def last_sync(self) -> datetime | None:
        """Time of last successful sync."""
        if self._last_sync is None:
            return None
        return datetime.fromtimestamp(self._last_sync, tz=timezone.utc)

    @property
    def avg_latency_ms(self) -> float | None:
        """Average round-trip latency in milliseconds."""
        if not self._latency_history:
            return None
        return statistics.mean(self._latency_history)

    @property
    def latency_std_ms(self) -> float | None:
        """Standard deviation of latency in milliseconds."""
        if len(self._latency_history) < 2:
            return None
        return statistics.stdev(self._latency_history)

    def on_drift_exceeded(
        self,
        threshold_ms: float,
        callback: Callable[[float], None],
    ) -> None:
        """Register callback for when drift exceeds threshold.

        Args:
            threshold_ms: Drift threshold in milliseconds
            callback: Function(drift_ms) to call
        """
        self._on_drift_exceeded.append((threshold_ms, callback))

    def needs_sync(self, max_age_seconds: float = 300.0) -> bool:
        """Check if sync is needed.

        Args:
            max_age_seconds: Maximum age of last sync

        Returns:
            True if sync hasn't happened or is too old
        """
        if self._last_sync is None:
            return True
        return time.time() - self._last_sync > max_age_seconds

    def get_stats(self) -> dict:
        """Get synchronization statistics.

        Returns:
            Dict with drift, latency, and sync info
        """
        return {
            "drift_ms": self._drift_ms,
            "last_sync": self._last_sync,
            "avg_latency_ms": self.avg_latency_ms,
            "latency_std_ms": self.latency_std_ms,
            "sample_count": len(self._history),
            "is_polling": self._running,
        }
