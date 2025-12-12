"""Decorator utilities for adding resilience to adapters."""

from collections.abc import Callable
from functools import wraps
from typing import TypeVar

try:
    from tenacity import (
        retry,
        retry_if_exception_type,
        stop_after_attempt,
        wait_exponential,
    )

    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False

from qldata.errors import NetworkError, RateLimitError

F = TypeVar("F", bound=Callable)


def with_rate_limit_retry(max_retries: int = 3, multiplier: int = 2, min_wait: int = 4, max_wait: int = 60):
    """Decorator to handle rate limiting with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        multiplier: Exponential backoff multiplier
        min_wait: Minimum wait time in seconds
        max_wait: Maximum wait time in seconds

    Example:
        >>> @with_rate_limit_retry(max_retries=3)
        ... def fetch_data():
        ...     # This will retry up to 3 times on RateLimitError
        ...     pass
    """

    def decorator(func: F) -> F:
        if not TENACITY_AVAILABLE:
            # If tenacity not available, return function as-is
            return func

        @retry(
            stop=stop_after_attempt(max_retries),
            wait=wait_exponential(multiplier=multiplier, min=min_wait, max=max_wait),
            retry=retry_if_exception_type(RateLimitError),
            reraise=True,
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


def with_network_retry(max_retries: int = 3, multiplier: int = 1, min_wait: int = 2, max_wait: int = 10):
    """Decorator to handle transient network errors.

    Args:
        max_retries: Maximum number of retry attempts
        multiplier: Exponential backoff multiplier
        min_wait: Minimum wait time in seconds
        max_wait: Maximum wait time in seconds

    Example:
        >>> @with_network_retry(max_retries=3)
        ... def fetch_data():
        ...     # This will retry up to 3 times on NetworkError
        ...     pass
    """

    def decorator(func: F) -> F:
        if not TENACITY_AVAILABLE:
            return func

        @retry(
            stop=stop_after_attempt(max_retries),
            wait=wait_exponential(multiplier=multiplier, min=min_wait, max=max_wait),
            retry=retry_if_exception_type((NetworkError, ConnectionError)),
            reraise=True,
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator
