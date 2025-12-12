# src/qldata/common/rate_limiter.py
"""Rate limiting for API calls."""

import time
from collections import deque
from collections.abc import Callable
from functools import wraps
from threading import Lock
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class RateLimiter:
    """Rate limiter using sliding window algorithm.

    Thread-safe rate limiter that tracks calls within a time window.

    Example:
        >>> limiter = RateLimiter(max_calls=10, period=60)
        >>> @limiter
        ... def api_call():
        ...     return "data"
    """

    def __init__(self, max_calls: int, period: float) -> None:
        """Initialize rate limiter.

        Args:
            max_calls: Maximum number of calls allowed
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: deque[float] = deque()
        self.lock = Lock()

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorator to rate limit a function.

        Args:
            func: Function to rate limit

        Returns:
            Wrapped function
        """

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            self._acquire_slot()
            return func(*args, **kwargs)

        return wrapper

    def _acquire_slot(self) -> None:
        """Wait for an available slot and record the call."""
        while True:
            with self.lock:
                now = time.time()

                # Remove calls outside the time window
                while self.calls and self.calls[0] <= now - self.period:
                    self.calls.popleft()

                if len(self.calls) < self.max_calls:
                    self.calls.append(now)
                    return

                # Compute how long to wait before retrying
                sleep_time = max(0.0, self.period - (now - self.calls[0]))

            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                time.sleep(0)

    def wait_if_needed(self) -> None:
        """Manually wait if rate limit is reached."""
        while True:
            with self.lock:
                now = time.time()

                # Remove old calls
                while self.calls and self.calls[0] <= now - self.period:
                    self.calls.popleft()

                if len(self.calls) < self.max_calls:
                    return

                sleep_time = max(0.0, self.period - (now - self.calls[0]))

            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                time.sleep(0)

    def get_stats(self) -> dict[str, Any]:
        """Get rate limiter statistics.

        Returns:
            Dictionary with stats
        """
        with self.lock:
            now = time.time()
            # Clean up old calls
            while self.calls and self.calls[0] <= now - self.period:
                self.calls.popleft()

            return {
                "current_calls": len(self.calls),
                "max_calls": self.max_calls,
                "period": self.period,
                "available_calls": self.max_calls - len(self.calls),
                "time_until_reset": (self.period - (now - self.calls[0]) if self.calls else 0),
            }

    def reset(self) -> None:
        """Reset the rate limiter."""
        with self.lock:
            self.calls.clear()


class AdaptiveRateLimiter(RateLimiter):
    """Rate limiter that adapts based on errors.

    Automatically backs off when rate limit errors are detected.
    """

    def __init__(
        self,
        max_calls: int,
        period: float,
        backoff_factor: float = 0.5,
        max_backoff: float = 300,
    ) -> None:
        """Initialize adaptive rate limiter.

        Args:
            max_calls: Initial maximum calls
            period: Time period in seconds
            backoff_factor: Factor to reduce rate on errors (0.5 = 50%)
            max_backoff: Maximum period after backoff
        """
        super().__init__(max_calls, period)
        self.initial_max_calls = max_calls
        self.initial_period = period
        self.backoff_factor = backoff_factor
        self.max_backoff = max_backoff
        self.consecutive_errors = 0

    def on_rate_limit_error(self) -> None:
        """Called when a rate limit error occurs."""
        with self.lock:
            self.consecutive_errors += 1
            # Reduce allowed calls
            new_max = max(1, int(self.max_calls * self.backoff_factor))
            # Increase period
            new_period = min(self.max_backoff, self.period * (1 / self.backoff_factor))

            self.max_calls = new_max
            self.period = new_period

    def on_success(self) -> None:
        """Called on successful request."""
        with self.lock:
            if self.consecutive_errors > 0:
                self.consecutive_errors = 0
                # Gradually restore to initial limits
                self.max_calls = min(
                    self.initial_max_calls, int(self.max_calls * 1.1)  # 10% increase
                )
                self.period = max(self.initial_period, self.period * 0.9)  # 10% decrease


__all__ = ["RateLimiter", "AdaptiveRateLimiter"]
