"""Resilience configuration for streaming sessions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ResilienceConfig:
    """Configuration for stream resilience features.

    All features are enabled by default for reliable streaming.
    Set individual flags to False to disable specific features.

    Attributes:
        rate_limiting: Enable rate limit tracking (default: True)
        sequence_tracking: Enable gap/duplicate detection (default: True)
        time_sync: Enable exchange time synchronization (default: True)
        journal_path: Path for data journaling (default: None, opt-in)
        gap_threshold: Sequence gap size that triggers resync (default: 100)
        time_sync_interval: Seconds between time sync polls (default: 300)
    """

    rate_limiting: bool = True
    sequence_tracking: bool = True
    time_sync: bool = True
    journal_path: Path | None = None
    gap_threshold: int = 100
    time_sync_interval: float = 300.0

    def __post_init__(self) -> None:
        """Normalize journal path input."""
        if isinstance(self.journal_path, str):
            self.journal_path = Path(self.journal_path)

    @classmethod
    def disabled(cls) -> ResilienceConfig:
        """Create config with all resilience features disabled."""
        return cls(
            rate_limiting=False,
            sequence_tracking=False,
            time_sync=False,
        )

    @classmethod
    def for_exchange(cls, exchange: str) -> ResilienceConfig:
        """Create config with exchange-specific defaults."""
        # All exchanges use same defaults for now
        # Can customize per-exchange in future
        return cls()


# Exchange-specific rate limit defaults
EXCHANGE_RATE_LIMITS = {
    "binance": {
        "default": {"limit": 1200, "window_seconds": 60},
        "orders": {"limit": 100, "window_seconds": 10},
    },
    "bybit": {
        "default": {"limit": 120, "window_seconds": 60},
        "orders": {"limit": 100, "window_seconds": 60},
    },
}


def get_rate_limit_config(exchange: str, endpoint: str = "default") -> dict:
    """Get rate limit config for an exchange endpoint."""
    exchange_limits = EXCHANGE_RATE_LIMITS.get(exchange, EXCHANGE_RATE_LIMITS["binance"])
    return exchange_limits.get(endpoint, exchange_limits["default"])
