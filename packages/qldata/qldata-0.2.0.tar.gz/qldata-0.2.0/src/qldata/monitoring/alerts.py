"""Alert system for data quality monitoring."""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Alert:
    """Represents a monitoring alert."""

    severity: str  # "info", "warning", "error", "critical"
    message: str
    timestamp: datetime
    metric_name: str
    metric_value: float
    threshold: float


class AlertManager:
    """Manage alerts for data quality issues.

    Provides callbacks for various alert conditions.
    """

    def __init__(self) -> None:
        self._high_latency_callbacks: list[Callable[[float], None]] = []
        self._stale_data_callbacks: list[Callable[[], None]] = []
        self._low_throughput_callbacks: list[Callable[[float], None]] = []
        self._connection_lost_callbacks: list[Callable[[], None]] = []
        self._reconnected_callbacks: list[Callable[[int], None]] = []

        # Alert history
        self._alerts: list[Alert] = []
        self._max_history = 100

    def on_high_latency(self, callback: Callable[[float], None]) -> None:
        """Register callback for high latency alerts.

        Args:
            callback: Function(latency_ms) to call when latency is high
        """
        self._high_latency_callbacks.append(callback)

    def on_stale_data(self, callback: Callable[[], None]) -> None:
        """Register callback for stale data alerts.

        Args:
            callback: Function to call when data becomes stale
        """
        self._stale_data_callbacks.append(callback)

    def on_low_throughput(self, callback: Callable[[float], None]) -> None:
        """Register callback for low throughput alerts.

        Args:
            callback: Function(throughput) to call when throughput is low
        """
        self._low_throughput_callbacks.append(callback)

    def on_connection_lost(self, callback: Callable[[], None]) -> None:
        """Register callback for connection loss.

        Args:
            callback: Function to call when connection is lost
        """
        self._connection_lost_callbacks.append(callback)

    def on_reconnected(self, callback: Callable[[int], None]) -> None:
        """Register callback for successful reconnection.

        Args:
            callback: Function(attempts) to call when reconnected
        """
        self._reconnected_callbacks.append(callback)

    def check_latency(
        self, latency_ms: float, warning_threshold: float = 500, error_threshold: float = 1000
    ) -> Alert | None:
        """Check latency and trigger alerts if needed.

        Args:
            latency_ms: Current latency in milliseconds
            warning_threshold: Warning threshold in ms
            error_threshold: Error threshold in ms

        Returns:
            Alert if threshold exceeded, None otherwise
        """
        alert = None

        if latency_ms > error_threshold:
            alert = Alert(
                severity="error",
                message=f"High latency: {latency_ms:.1f}ms (threshold: {error_threshold}ms)",
                timestamp=datetime.now(timezone.utc),
                metric_name="latency",
                metric_value=latency_ms,
                threshold=error_threshold,
            )
            self._record_alert(alert)
            self._notify(self._high_latency_callbacks, latency_ms)

        elif latency_ms > warning_threshold:
            alert = Alert(
                severity="warning",
                message=f"Elevated latency: {latency_ms:.1f}ms (threshold: {warning_threshold}ms)",
                timestamp=datetime.now(timezone.utc),
                metric_name="latency",
                metric_value=latency_ms,
                threshold=warning_threshold,
            )
            self._record_alert(alert)

        return alert

    def check_stale_data(self, is_stale: bool) -> Alert | None:
        """Check if data is stale and trigger alerts.

        Args:
            is_stale: Whether data is currently stale

        Returns:
            Alert if stale, None otherwise
        """
        if is_stale:
            alert = Alert(
                severity="critical",
                message="Data stream is stale - no updates received",
                timestamp=datetime.now(timezone.utc),
                metric_name="stale",
                metric_value=1.0,
                threshold=1.0,
            )
            self._record_alert(alert)
            self._notify(self._stale_data_callbacks)
            return alert

        return None

    def check_throughput(
        self, current_tps: float, expected_tps: float, tolerance: float = 0.5
    ) -> Alert | None:
        """Check if throughput is below expected.

        Args:
            current_tps: Current transactions per second
            expected_tps: Expected TPS
            tolerance: Acceptable ratio (0.5 = 50% of expected is threshold)

        Returns:
            Alert if throughput too low, None otherwise
        """
        threshold = expected_tps * tolerance

        if current_tps < threshold:
            alert = Alert(
                severity="warning",
                message=f"Low throughput: {current_tps:.1f}/s (expected: {expected_tps:.1f}/s)",
                timestamp=datetime.now(timezone.utc),
                metric_name="throughput",
                metric_value=current_tps,
                threshold=threshold,
            )
            self._record_alert(alert)
            self._notify(self._low_throughput_callbacks, current_tps)
            return alert

        return None

    def notify_connection_lost(self) -> None:
        """Notify that connection was lost."""
        alert = Alert(
            severity="error",
            message="WebSocket connection lost",
            timestamp=datetime.now(timezone.utc),
            metric_name="connection",
            metric_value=0.0,
            threshold=1.0,
        )
        self._record_alert(alert)
        self._notify(self._connection_lost_callbacks)

    def notify_reconnected(self, attempts: int) -> None:
        """Notify successful reconnection.

        Args:
            attempts: Number of attempts it took to reconnect
        """
        alert = Alert(
            severity="info",
            message=f"Reconnected successfully after {attempts} attempts",
            timestamp=datetime.now(timezone.utc),
            metric_name="reconnection",
            metric_value=float(attempts),
            threshold=float(attempts),
        )
        self._record_alert(alert)
        self._notify(self._reconnected_callbacks, attempts)

    def get_recent_alerts(self, limit: int = 10) -> list[Alert]:
        """Get recent alerts.

        Args:
            limit: Maximum number of alerts to return

        Returns:
            List of recent alerts
        """
        return self._alerts[-limit:]

    def clear_alerts(self) -> None:
        """Clear alert history."""
        self._alerts.clear()

    def _record_alert(self, alert: Alert) -> None:
        """Record an alert in history."""
        self._alerts.append(alert)

        # Trim history if needed
        if len(self._alerts) > self._max_history:
            self._alerts = self._alerts[-self._max_history :]

        # Log the alert
        log_method = getattr(logger, alert.severity, logger.info)
        log_method(alert.message)

    def _notify(self, callbacks: list[Callable[..., None]], *args: Any) -> None:
        """Notify callbacks with arguments."""
        for callback in callbacks:
            try:
                callback(*args)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

    def __repr__(self) -> str:
        return f"AlertManager(alerts={len(self._alerts)})"
