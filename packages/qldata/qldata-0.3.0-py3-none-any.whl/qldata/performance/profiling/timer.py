"""Timing utilities for performance profiling."""

import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import ParamSpec, TypeVar

from qldata.logging import get_logger

logger = get_logger(__name__)


@contextmanager
def timer(name: str = "Operation") -> Iterator[None]:
    """Context manager for timing code blocks.

    Args:
        name: Name of operation being timed

    Example:
        >>> with timer("Data loading"):
        ...     data = qd.get("BTCUSDT", "2024-01-01", "2024-12-01", "1d")
        Data loading took 0.123s
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.info(f"{name} took {elapsed:.3f}s")


P = ParamSpec("P")
R = TypeVar("R")


def timed(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to time function execution.

    Args:
        func: Function to time

    Returns:
        Wrapped function

    Example:
        >>> @timed
        ... def expensive_operation():
        ...     time.sleep(1)
        >>> expensive_operation()
        expensive_operation took 1.001s
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} took {elapsed:.3f}s")
        return result

    return wrapper


class Timer:
    """Simple timer class for manual timing.

    Example:
        >>> timer = Timer()
        >>> timer.start()
        >>> # ... do work ...
        >>> print(f"Elapsed: {timer.elapsed():.2f}s")
    """

    def __init__(self) -> None:
        """Initialize timer."""
        self._start_time: float | None = None
        self._end_time: float | None = None

    def start(self) -> None:
        """Start the timer."""
        self._start_time = time.perf_counter()
        self._end_time = None

    def stop(self) -> float:
        """Stop the timer and return elapsed time.

        Returns:
            Elapsed seconds
        """
        if self._start_time is None:
            raise RuntimeError("Timer not started")

        self._end_time = time.perf_counter()
        return self.elapsed()

    def elapsed(self) -> float:
        """Get elapsed time.

        Returns:
            Elapsed seconds
        """
        if self._start_time is None:
            raise RuntimeError("Timer not started")

        end = self._end_time if self._end_time is not None else time.perf_counter()
        return end - self._start_time
