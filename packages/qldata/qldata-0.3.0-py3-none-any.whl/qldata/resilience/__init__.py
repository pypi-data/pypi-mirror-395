"""Resilience package for robust application development."""

from qldata.resilience.connection import ConnectionState, ConnectionStateManager
from qldata.resilience.core import (
    HeartbeatMonitor,
    MessageDeduplicator,
    ReconnectionManager,
)
from qldata.resilience.rate_limit import RateLimitConfig, RateLimitManager, RateLimitState
from qldata.resilience.sequence import Gap, OrderBookSyncer, SequenceResult, SequenceTracker
from qldata.resilience.time_sync import TimeSyncManager, TimeSyncResult

__all__ = [
    # Core
    "ReconnectionManager",
    "HeartbeatMonitor",
    "MessageDeduplicator",
    "ConnectionStateManager",
    "ConnectionState",
    # Rate limiting
    "RateLimitManager",
    "RateLimitConfig",
    "RateLimitState",
    # Sequence tracking
    "SequenceTracker",
    "SequenceResult",
    "Gap",
    "OrderBookSyncer",
    # Time sync
    "TimeSyncManager",
    "TimeSyncResult",
]

