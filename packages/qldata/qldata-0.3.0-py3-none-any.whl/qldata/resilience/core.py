"""Enhanced resilience utilities for WebSocket connections."""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from contextlib import suppress
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class ReconnectionManager:
    """Manages automatic reconnection with exponential backoff.

    Handles reconnection attempts with configurable backoff and max retries.
    """

    def __init__(
        self,
        max_retries: int = 10,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
    ):
        """Initialize reconnection manager.

        Args:
            max_retries: Maximum reconnection attempts (0 = infinite)
            base_delay: Initial delay in seconds
            max_delay: Maximum delay between retries
            backoff_factor: Exponential backoff multiplier
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

        self._attempt = 0
        self._on_retry_callbacks: list[Callable[[int], None]] = []
        self._on_success_callbacks: list[Callable[[], None]] = []
        self._on_failure_callbacks: list[Callable[[], None]] = []

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number.

        Args:
            attempt: Attempt number (0-indexed)

        Returns:
            Delay in seconds
        """
        delay = self.base_delay * (self.backoff_factor**attempt)
        return min(delay, self.max_delay)

    async def reconnect(self, connect_func: Callable[[], Awaitable[None]]) -> bool:
        """Execute reconnection with exponential backoff.

        Args:
            connect_func: Async function to call for reconnection

        Returns:
            True if reconnected successfully, False otherwise
        """
        self._attempt = 0

        while self.max_retries == 0 or self._attempt < self.max_retries:
            if self._attempt > 0:
                delay = self.calculate_delay(self._attempt - 1)
                logger.info(f"Reconnection attempt {self._attempt + 1}, waiting {delay:.1f}s...")

                # Notify retry callbacks
                for retry_callback in self._on_retry_callbacks:
                    try:
                        retry_callback(self._attempt + 1)
                    except Exception as e:
                        logger.error(f"Error in retry callback: {e}")

                await asyncio.sleep(delay)

            try:
                # Attempt connection
                await connect_func()

                logger.info(f"Reconnected successfully after {self._attempt + 1} attempts")

                # Notify success callbacks
                for success_callback in self._on_success_callbacks:
                    try:
                        success_callback()
                    except Exception as e:
                        logger.error(f"Error in success callback: {e}")

                self._attempt = 0
                return True

            except Exception as e:
                self._attempt += 1
                logger.warning(f"Reconnection attempt {self._attempt} failed: {e}")

        # Max retries exceeded
        logger.error(f"Failed to reconnect after {self._attempt} attempts")

        # Notify failure callbacks
        for failure_callback in self._on_failure_callbacks:
            try:
                failure_callback()
            except Exception as e:
                logger.error(f"Error in failure callback: {e}")

        return False

    def on_retry(self, callback: Callable[[int], None]) -> None:
        """Register callback for retry attempts.

        Args:
            callback: Function(attempt_number) to call
        """
        self._on_retry_callbacks.append(callback)

    def on_success(self, callback: Callable[[], None]) -> None:
        """Register callback for successful reconnection."""
        self._on_success_callbacks.append(callback)

    def on_failure(self, callback: Callable[[], None]) -> None:
        """Register callback for reconnection failure."""
        self._on_failure_callbacks.append(callback)

    def reset(self) -> None:
        """Reset attempt counter."""
        self._attempt = 0


class HeartbeatMonitor:
    """Monitors connection health via heartbeats.

    Detects stale connections and triggers reconnection if needed.
    """

    def __init__(self, timeout_seconds: float = 30.0, ping_interval: float = 10.0):
        """Initialize heartbeat monitor.

        Args:
            timeout_seconds: Seconds without heartbeat before timeout
            ping_interval: Seconds between ping messages
        """
        self.timeout_seconds = timeout_seconds
        self.ping_interval = ping_interval

        self._last_heartbeat: datetime | None = None
        self._monitoring_task: asyncio.Task | None = None
        self._on_timeout_callbacks: list[Callable[[], None]] = []

    def record_heartbeat(self) -> None:
        """Record a heartbeat (pong received)."""
        self._last_heartbeat = datetime.now(timezone.utc)

    def is_alive(self) -> bool:
        """Check if connection is alive.

        Returns:
            True if heartbeat within timeout, False otherwise
        """
        if not self._last_heartbeat:
            return True  # No heartbeats yet

        elapsed = (datetime.now(timezone.utc) - self._last_heartbeat).total_seconds()
        return elapsed < self.timeout_seconds

    def seconds_since_heartbeat(self) -> float | None:
        """Get seconds since last heartbeat.

        Returns:
            Seconds since last heartbeat, or None if no heartbeats
        """
        if not self._last_heartbeat:
            return None

        return (datetime.now(timezone.utc) - self._last_heartbeat).total_seconds()

    async def start_monitoring(self, ping_func: Callable[[], Awaitable[None]]) -> None:
        """Start monitoring heartbeats.

        Args:
            ping_func: Async function to send ping
        """
        self._last_heartbeat = datetime.now(timezone.utc)

        async def monitor() -> None:
            while True:
                await asyncio.sleep(self.ping_interval)

                # Send ping
                try:
                    await ping_func()
                except Exception as e:
                    logger.error(f"Error sending ping: {e}")

                # Check timeout
                if not self.is_alive():
                    logger.warning("Heartbeat timeout detected")

                    # Notify callbacks
                    for callback in self._on_timeout_callbacks:
                        try:
                            callback()
                        except Exception as e:
                            logger.error(f"Error in timeout callback: {e}")

                    break

        self._monitoring_task = asyncio.create_task(monitor())

    async def stop_monitoring(self) -> None:
        """Stop monitoring heartbeats."""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._monitoring_task
            self._monitoring_task = None

    def on_timeout(self, callback: Callable[[], None]) -> None:
        """Register callback for heartbeat timeout.

        Args:
            callback: Function to call on timeout
        """
        self._on_timeout_callbacks.append(callback)


class MessageDeduplicator:
    """Deduplicates messages using sequence numbers.

    Prevents processing duplicate messages during reconnections.
    """

    def __init__(self, buffer_size: int = 1000):
        """Initialize deduplicator.

        Args:
            buffer_size: Number of recent sequence numbers to track
        """
        self.buffer_size = buffer_size
        self._seen_sequences: set[int] = set()
        self._sequence_queue: list[int] = []

    def is_duplicate(self, sequence: int) -> bool:
        """Check if sequence number has been seen.

        Args:
            sequence: Sequence number

        Returns:
            True if duplicate, False otherwise
        """
        return sequence in self._seen_sequences

    def record(self, sequence: int) -> bool:
        """Record a sequence number.

        Args:
            sequence: Sequence number

        Returns:
            True if new (not duplicate), False if duplicate
        """
        if sequence in self._seen_sequences:
            return False

        self._seen_sequences.add(sequence)
        self._sequence_queue.append(sequence)

        # Trim buffer if needed
        if len(self._sequence_queue) > self.buffer_size:
            old_seq = self._sequence_queue.pop(0)
            self._seen_sequences.discard(old_seq)

        return True

    def reset(self) -> None:
        """Clear all tracked sequences."""
        self._seen_sequences.clear()
        self._sequence_queue.clear()
