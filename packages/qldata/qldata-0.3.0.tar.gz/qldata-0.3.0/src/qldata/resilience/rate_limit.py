"""Rate limit management for API requests.

Provides token bucket rate limiting with per-endpoint tracking,
header-based limit updates, and backpressure signaling.
"""

from __future__ import annotations

import asyncio
import logging
import time
from contextlib import suppress
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


@dataclass
class RateLimitConfig:
    """Configuration for a rate-limited endpoint.

    Attributes:
        limit: Maximum requests allowed in the window
        window_seconds: Time window for the limit
        weight: Default weight per request (some endpoints cost more)
    """

    limit: int = 1200
    window_seconds: float = 60.0
    weight: int = 1


@dataclass
class RateLimitState:
    """Current state of rate limiting for an endpoint.

    Attributes:
        tokens: Remaining request tokens
        limit: Maximum tokens (from config or headers)
        reset_at: When tokens reset (epoch timestamp)
        updated_at: Last update time
    """

    tokens: int
    limit: int
    reset_at: float
    updated_at: float = field(default_factory=time.time)


class RateLimitManager:
    """Manages rate limits across multiple endpoints.

    Uses a token bucket algorithm with support for:
    - Per-endpoint limits and weights
    - Exchange header-based limit updates
    - Backpressure callbacks when limits approach
    - Async waiting for token availability

    Example:
        >>> manager = RateLimitManager({
        ...     "klines": RateLimitConfig(limit=1200, window_seconds=60),
        ...     "orders": RateLimitConfig(limit=100, window_seconds=10, weight=5),
        ... })
        >>> if manager.acquire("klines"):
        ...     response = fetch_klines()
        ...     manager.update_from_headers("klines", response.headers)
    """

    def __init__(
        self,
        limits: dict[str, RateLimitConfig] | None = None,
        default_limit: int = 1200,
        default_window: float = 60.0,
    ) -> None:
        """Initialize rate limit manager.

        Args:
            limits: Per-endpoint rate limit configurations
            default_limit: Default limit for unknown endpoints
            default_window: Default window in seconds for unknown endpoints
        """
        self._configs: dict[str, RateLimitConfig] = limits or {}
        self._default_limit = default_limit
        self._default_window = default_window
        self._states: dict[str, RateLimitState] = {}
        self._lock = asyncio.Lock()

        # Callbacks
        self._on_limit_approaching: list[Callable[[str, float], None]] = []
        self._on_limit_exceeded: list[Callable[[str], None]] = []

        # Threshold for "approaching" callback (percentage of limit used)
        self._approach_threshold = 0.8

    def _get_config(self, endpoint: str) -> RateLimitConfig:
        """Get config for endpoint, using defaults if not defined."""
        if endpoint in self._configs:
            return self._configs[endpoint]
        return RateLimitConfig(
            limit=self._default_limit,
            window_seconds=self._default_window,
        )

    def _get_or_create_state(self, endpoint: str) -> RateLimitState:
        """Get or initialize state for an endpoint."""
        if endpoint not in self._states:
            config = self._get_config(endpoint)
            self._states[endpoint] = RateLimitState(
                tokens=config.limit,
                limit=config.limit,
                reset_at=time.time() + config.window_seconds,
            )
        return self._states[endpoint]

    def _maybe_reset(self, endpoint: str) -> None:
        """Reset tokens if window has passed."""
        state = self._get_or_create_state(endpoint)
        now = time.time()

        if now >= state.reset_at:
            config = self._get_config(endpoint)
            state.tokens = state.limit
            state.reset_at = now + config.window_seconds
            state.updated_at = now
            logger.debug(f"Rate limit reset for {endpoint}: {state.tokens} tokens")

    def acquire(self, endpoint: str, weight: int | None = None) -> bool:
        """Try to acquire tokens for a request.

        Args:
            endpoint: API endpoint name
            weight: Request weight (uses config default if not specified)

        Returns:
            True if tokens acquired, False if rate limited
        """
        self._maybe_reset(endpoint)

        config = self._get_config(endpoint)
        state = self._get_or_create_state(endpoint)
        cost = weight if weight is not None else config.weight

        if state.tokens >= cost:
            state.tokens -= cost
            state.updated_at = time.time()

            # Check if approaching limit
            used_ratio = 1 - (state.tokens / state.limit)
            if used_ratio >= self._approach_threshold:
                for callback in self._on_limit_approaching:
                    try:
                        callback(endpoint, used_ratio)
                    except Exception as e:
                        logger.warning(f"Error in limit approaching callback: {e}")

            logger.debug(f"Acquired {cost} tokens for {endpoint}, {state.tokens} remaining")
            return True

        # Rate limited
        for callback in self._on_limit_exceeded:
            try:
                callback(endpoint)
            except Exception as e:
                logger.warning(f"Error in limit exceeded callback: {e}")

        logger.warning(f"Rate limited on {endpoint}: need {cost}, have {state.tokens}")
        return False

    async def acquire_async(
        self,
        endpoint: str,
        weight: int | None = None,
        max_wait: float = 60.0,
    ) -> bool:
        """Acquire tokens, waiting if necessary.

        Args:
            endpoint: API endpoint name
            weight: Request weight
            max_wait: Maximum seconds to wait for tokens

        Returns:
            True if tokens acquired, False if timed out
        """
        async with self._lock:
            if self.acquire(endpoint, weight):
                return True

            wait = self.wait_time(endpoint)
            if wait > max_wait:
                logger.warning(f"Wait time {wait:.1f}s exceeds max {max_wait:.1f}s for {endpoint}")
                return False

            logger.debug(f"Waiting {wait:.1f}s for rate limit on {endpoint}")
            await asyncio.sleep(wait)

            return self.acquire(endpoint, weight)

    def wait_time(self, endpoint: str) -> float:
        """Get seconds until tokens are available.

        Args:
            endpoint: API endpoint name

        Returns:
            Seconds to wait (0 if tokens available now)
        """
        self._maybe_reset(endpoint)
        state = self._get_or_create_state(endpoint)

        if state.tokens > 0:
            return 0.0

        return max(0.0, state.reset_at - time.time())

    def tokens_remaining(self, endpoint: str) -> int:
        """Get remaining tokens for an endpoint.

        Args:
            endpoint: API endpoint name

        Returns:
            Number of tokens remaining
        """
        self._maybe_reset(endpoint)
        return self._get_or_create_state(endpoint).tokens

    def update_from_headers(
        self,
        endpoint: str,
        headers: dict[str, Any],
        *,
        limit_key: str = "X-RateLimit-Limit",
        remaining_key: str = "X-RateLimit-Remaining",
        reset_key: str = "X-RateLimit-Reset",
    ) -> None:
        """Update rate limit state from response headers.

        Exchanges typically return rate limit info in headers.
        This method parses common header formats.

        Args:
            endpoint: API endpoint name
            headers: Response headers dict
            limit_key: Header key for limit
            remaining_key: Header key for remaining
            reset_key: Header key for reset time
        """
        state = self._get_or_create_state(endpoint)

        # Case-insensitive header lookup
        headers_lower = {k.lower(): v for k, v in headers.items()}

        if limit_key.lower() in headers_lower:
            with suppress(ValueError, TypeError):
                state.limit = int(headers_lower[limit_key.lower()])

        if remaining_key.lower() in headers_lower:
            with suppress(ValueError, TypeError):
                state.tokens = int(headers_lower[remaining_key.lower()])

        if reset_key.lower() in headers_lower:
            with suppress(ValueError, TypeError):
                reset_val = headers_lower[reset_key.lower()]
                # Handle both Unix timestamp and seconds-until-reset
                if isinstance(reset_val, int | float):
                    if reset_val > 1e9:  # Unix timestamp
                        state.reset_at = float(reset_val)
                    else:  # Seconds until reset
                        state.reset_at = time.time() + float(reset_val)
                else:
                    state.reset_at = float(reset_val)

        state.updated_at = time.time()
        logger.debug(
            f"Updated rate limit for {endpoint} from headers: "
            f"{state.tokens}/{state.limit}, resets in {state.reset_at - time.time():.1f}s"
        )

    def update_binance_headers(self, endpoint: str, headers: dict[str, Any]) -> None:
        """Update from Binance-style headers.

        Binance uses:
        - X-MBX-USED-WEIGHT-1M: Weight used in last minute
        """
        state = self._get_or_create_state(endpoint)
        headers_lower = {k.lower(): v for k, v in headers.items()}

        weight_key = "x-mbx-used-weight-1m"
        if weight_key in headers_lower:
            try:
                used = int(headers_lower[weight_key])
                state.tokens = max(0, state.limit - used)
                state.updated_at = time.time()
                logger.debug(f"Binance weight update for {endpoint}: used {used}, remaining {state.tokens}")
            except (ValueError, TypeError):
                pass

    def on_limit_approaching(self, callback: Callable[[str, float], None]) -> None:
        """Register callback when rate limit is approaching.

        Args:
            callback: Function(endpoint, used_ratio) called when threshold exceeded
        """
        self._on_limit_approaching.append(callback)

    def on_limit_exceeded(self, callback: Callable[[str], None]) -> None:
        """Register callback when rate limit is exceeded.

        Args:
            callback: Function(endpoint) called when rate limited
        """
        self._on_limit_exceeded.append(callback)

    def set_approach_threshold(self, threshold: float) -> None:
        """Set the threshold for 'approaching limit' callbacks.

        Args:
            threshold: Ratio (0-1) of limit usage that triggers callback
        """
        if not 0 < threshold < 1:
            raise ValueError("Threshold must be between 0 and 1")
        self._approach_threshold = threshold

    def reset(self, endpoint: str | None = None) -> None:
        """Reset rate limit state.

        Args:
            endpoint: Specific endpoint to reset, or None for all
        """
        if endpoint:
            if endpoint in self._states:
                del self._states[endpoint]
        else:
            self._states.clear()

    def get_status(self) -> dict[str, dict[str, Any]]:
        """Get current status of all tracked endpoints.

        Returns:
            Dict mapping endpoint to status info
        """
        now = time.time()
        status = {}

        for endpoint, state in self._states.items():
            status[endpoint] = {
                "tokens": state.tokens,
                "limit": state.limit,
                "reset_in_seconds": max(0, state.reset_at - now),
                "usage_ratio": 1 - (state.tokens / state.limit) if state.limit > 0 else 1.0,
            }

        return status
