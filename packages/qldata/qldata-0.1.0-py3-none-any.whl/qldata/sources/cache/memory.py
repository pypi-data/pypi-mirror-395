from datetime import datetime
from functools import lru_cache
from typing import Any

import pandas as pd

from qldata.models.timeframe import Timeframe
from qldata.sources.base.source import DataSource


class MemoryCache(DataSource):
    """In-memory cache wrapper for data sources with statistics.

    Wraps another DataSource and caches results with LRU eviction.
    Tracks cache hits, misses, and other statistics.
    """

    def __init__(self, source: DataSource, max_size: int = 1000) -> None:
        """Initialize memory cache.

        Args:
            source: Underlying data source
            max_size: Maximum cache size
        """
        self._source = source
        self._max_size = max_size
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "errors": 0,
        }

        # Create cached version of get_bars
        self._cached_get_bars = lru_cache(maxsize=max_size)(self._get_bars_impl)

    @staticmethod
    def _make_hashable(value: Any) -> Any:
        """Convert potentially unhashable values into a hashable representation."""
        if isinstance(value, dict):
            return tuple(sorted((k, MemoryCache._make_hashable(v)) for k, v in value.items()))
        if isinstance(value, (list, tuple, set)):
            return tuple(MemoryCache._make_hashable(v) for v in value)
        return value

    def _get_bars_impl(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Timeframe,
        kwargs_key: tuple[tuple[str, Any], ...] | None = None,
    ) -> pd.DataFrame:
        """Implementation of get_bars (for caching).

        Args:
            symbol: Symbol ticker
            start: Start datetime
            end: End datetime
            timeframe: Bar timeframe
            kwargs_key: Hashable representation of additional kwargs

        Returns:
            DataFrame with OHLCV data
        """
        try:
            extra_kwargs = dict(kwargs_key or ())
            return self._source.get_bars(symbol, start, end, timeframe, **extra_kwargs)
        except Exception:
            self._stats["errors"] += 1
            raise

    @staticmethod
    def _normalize_dt(dt: datetime) -> datetime:
        """Normalize datetime for cache keys to avoid microsecond bloat."""
        return dt.replace(microsecond=0)

    def get_bars(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Timeframe,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Get bar data with caching.

        Args:
            symbol: Symbol ticker
            start: Start datetime
            end: End datetime
            timeframe: Bar timeframe
            **kwargs: Additional parameters

        Returns:
            DataFrame with OHLCV data
        """
        # Track cache info before call
        cache_info_before = self._cached_get_bars.cache_info()

        # Use cached version
        key_start = self._normalize_dt(start)
        key_end = self._normalize_dt(end)
        kwargs_key = tuple(
            sorted((k, self._make_hashable(v)) for k, v in kwargs.items())
        )
        result = self._cached_get_bars(symbol, key_start, key_end, timeframe, kwargs_key)

        # Track cache info after call
        cache_info_after = self._cached_get_bars.cache_info()

        # Update statistics
        if cache_info_after.hits > cache_info_before.hits:
            self._stats["hits"] += 1
        else:
            self._stats["misses"] += 1

        # Track evictions
        if cache_info_after.currsize < cache_info_before.currsize:
            self._stats["evictions"] += 1

        return result

    def clear_cache(self) -> None:
        """Clear the cache and reset statistics."""
        self._cached_get_bars.cache_clear()

    def get_cache_info(self) -> dict[str, Any]:
        """Get cache information.

        Returns:
            Dictionary with cache statistics
        """
        cache_info = self._cached_get_bars.cache_info()

        hit_rate = (
            cache_info.hits / (cache_info.hits + cache_info.misses)
            if (cache_info.hits + cache_info.misses) > 0
            else 0.0
        )

        return {
            "hits": cache_info.hits,
            "misses": cache_info.misses,
            "hit_rate": hit_rate,
            "current_size": cache_info.currsize,
            "max_size": cache_info.maxsize,
            "evictions": self._stats["evictions"],
            "errors": self._stats["errors"],
        }

    def get_stats(self) -> dict[str, Any]:
        """Get detailed statistics.

        Returns:
            Dictionary with cache statistics
        """
        return {
            **self.get_cache_info(),
            "total_requests": self._stats["hits"] + self._stats["misses"],
        }

    def __repr__(self) -> str:
        """String representation."""
        info = self.get_cache_info()
        return (
            f"MemoryCache(max_size={info['max_size']}, "
            f"current_size={info['current_size']}, "
            f"hit_rate={info['hit_rate']:.2%})"
        )
