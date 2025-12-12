"""Centralized logging infrastructure for qldata.

Provides consistent logging across all modules with performance tracking.
"""

import functools
import logging
import time
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing data")
    """
    return logging.getLogger(f"qldata.{name}")


def timed(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to log function execution time.

    Logs at DEBUG level with function name and duration.

    Example:
        >>> @timed
        ... def fetch_data():
        ...     return data
    """
    logger = logging.getLogger(f"qldata.{func.__module__}")

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(f"{func.__name__} took {elapsed:.3f}s")
        return result

    return wrapper


def log_operation(operation: str, **context: Any) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to log operations with context.

    Args:
        operation: Operation description
        **context: Additional context to log

    Example:
        >>> @log_operation("fetch_bars", source="binance")
        ... def fetch_bars(symbol):
        ...     return data
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        logger = logging.getLogger(f"qldata.{func.__module__}")

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            ctx_str = ", ".join(f"{k}={v}" for k, v in context.items())
            logger.debug(f"{operation} started ({ctx_str})")

            try:
                result = func(*args, **kwargs)
                logger.debug(f"{operation} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{operation} failed: {e}")
                raise

        return wrapper

    return decorator


__all__ = ["get_logger", "timed", "log_operation"]
