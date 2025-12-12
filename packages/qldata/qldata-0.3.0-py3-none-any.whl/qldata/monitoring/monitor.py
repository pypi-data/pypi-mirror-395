"""Data quality monitoring for streaming data."""

import time
from collections import deque
from datetime import datetime, timezone

import numpy as np


class DataQualityMonitor:
    """Monitor streaming data quality in real-time.

    Tracks latency, throughput, and staleness of streaming data.
    """

    def __init__(self, stale_threshold_seconds: int = 30):
        """Initialize monitor.

        Args:
            stale_threshold_seconds: Seconds without data before considered stale
        """
        self._latencies: deque[float] = deque(maxlen=1000)  # Last 1000 latencies
        self._message_count = 0
        self._last_message_time: datetime | None = None
        self._start_time = time.time()
        self._stale_threshold = stale_threshold_seconds

        # Error tracking
        self._error_count = 0
        self._last_error: Exception | None = None

        # Gap tracking
        self._gaps_detected = 0

    def record_message(self, message_timestamp: datetime | None = None) -> None:
        """Record receipt of a message.

        Args:
            message_timestamp: Timestamp from the message (for latency calc)
        """
        now = datetime.now(timezone.utc)

        # Calculate latency if timestamp provided
        if message_timestamp:
            latency_ms = (now - message_timestamp).total_seconds() * 1000
            self._latencies.append(latency_ms)

        self._message_count += 1
        self._last_message_time = now

    def record_error(self, error: Exception) -> None:
        """Record an error.

        Args:
            error: Exception that occurred
        """
        self._error_count += 1
        self._last_error = error

    def record_gap(self) -> None:
        """Record a detected data gap."""
        self._gaps_detected += 1

    def get_metrics(self) -> dict:
        """Get current quality metrics.

        Returns:
            Dictionary with quality metrics
        """
        uptime = time.time() - self._start_time

        metrics = {
            "total_messages": self._message_count,
            "uptime_seconds": uptime,
            "throughput": self._message_count / uptime if uptime > 0 else 0,
            "is_stale": self.is_stale(),
            "seconds_since_last_message": self.seconds_since_last_message(),
            "error_count": self._error_count,
            "gaps_detected": self._gaps_detected,
        }

        # Latency metrics (if we have latencies)
        if self._latencies:
            metrics.update(
                {
                    "latency_p50": float(np.percentile(self._latencies, 50)),
                    "latency_p95": float(np.percentile(self._latencies, 95)),
                    "latency_p99": float(np.percentile(self._latencies, 99)),
                    "latency_max": float(max(self._latencies)),
                    "latency_avg": float(np.mean(self._latencies)),
                }
            )
        else:
            metrics.update(
                {
                    "latency_p50": None,
                    "latency_p95": None,
                    "latency_p99": None,
                    "latency_max": None,
                    "latency_avg": None,
                }
            )

        return metrics

    def is_stale(self) -> bool:
        """Check if data is stale (no recent updates).

        Returns:
            True if no messages received within threshold
        """
        if not self._last_message_time:
            return False

        elapsed = (datetime.now(timezone.utc) - self._last_message_time).total_seconds()
        return elapsed > self._stale_threshold

    def seconds_since_last_message(self) -> float | None:
        """Get seconds since last message.

        Returns:
            Seconds since last message, or None if no messages
        """
        if not self._last_message_time:
            return None

        return (datetime.now(timezone.utc) - self._last_message_time).total_seconds()

    def reset(self) -> None:
        """Reset all metrics."""
        self._latencies.clear()
        self._message_count = 0
        self._last_message_time = None
        self._start_time = time.time()
        self._error_count = 0
        self._last_error = None
        self._gaps_detected = 0

    def get_health_status(self) -> str:
        """Get overall health status.

        Returns:
            "healthy", "degraded", or "unhealthy"
        """
        if self.is_stale():
            return "unhealthy"

        metrics = self.get_metrics()

        # Check latency if available
        if metrics["latency_p95"] is not None and metrics["latency_p95"] > 1000:
            return "degraded"

        # Check error rate
        if self._error_count > 0:
            error_rate = self._error_count / max(self._message_count, 1)
            if error_rate > 0.01:  # > 1% errors
                return "degraded"

        return "healthy"

    def __repr__(self) -> str:
        metrics = self.get_metrics()
        return (
            f"DataQualityMonitor("
            f"messages={metrics['total_messages']}, "
            f"throughput={metrics['throughput']:.1f}/s, "
            f"stale={metrics['is_stale']}, "
            f"health={self.get_health_status()}"
            f")"
        )
