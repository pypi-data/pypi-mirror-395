"""Streaming query builder."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from qldata.api.sessions.stream import StreamSession, _interval_to_seconds, _window_to_seconds
from qldata.models.timeframe import Timeframe
from qldata.transforms.clean import (
    add_timestamp_sorting,
    detect_ohlcv_columns,
    remove_duplicates,
    validate_ohlc_relationships,
)
from qldata.transforms.clean import (
    remove_invalid_prices as clean_remove_invalid_prices,
)
from qldata.transforms.clean import (
    remove_outliers as clean_remove_outliers,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    import pandas as pd

    from qldata.api.config.resilience import ResilienceConfig
    from qldata.resilience import RateLimitManager, SequenceTracker
else:
    from qldata.api.config.resilience import ResilienceConfig


class StreamQuery:
    """Fluent builder for streaming sessions."""

    def __init__(
        self,
        api: Any,  # StreamingAPI
        symbols: list[str],
        source: str,
        category: str | None,
        interval: float,
        kline_interval: str | None,
        on_data: Callable[[pd.DataFrame], None] | None,
        on_error: Callable[[Exception], None] | None,
        on_close: Callable[[], None] | None,
        resilience: ResilienceConfig | bool = True,
        rate_limiter: RateLimitManager | None = None,
        sequence_tracker: dict[str, SequenceTracker] | None = None,
        journal: Any | None = None,
    ) -> None:
        if not isinstance(resilience, bool | ResilienceConfig):
            raise TypeError("resilience must be a bool or ResilienceConfig")

        self._api = api
        self._symbols = symbols
        self._source = source
        self._category = category
        self._interval_seconds = interval
        self._kline_interval = kline_interval
        self._on_data = on_data
        self._on_error = on_error
        self._on_close = on_close
        self._pipes: list[Callable[[pd.DataFrame], pd.DataFrame]] = []
        self._window_seconds: float | None = None
        self._max_rows: int | None = None
        self._resample_to: str | None = None
        self._clean_fn: Callable[[pd.DataFrame], pd.DataFrame] | None = None
        self._resilience = resilience
        self._rate_limiter = rate_limiter
        self._sequence_tracker = sequence_tracker
        self._journal = journal

    def resolution(self, interval: str | Timeframe | float | int) -> StreamQuery:
        """Set streaming interval or request tick data.

        For live sources this selects kline streams when supported (e.g., "1m", "5m", "1h").
        Use "tick" or Timeframe.TICK to explicitly request raw trade data (default behavior).

        Args:
            interval: Resolution ("tick", "1s", "1m", "1h", etc.) or numeric seconds
        """
        self._interval_seconds = _interval_to_seconds(interval)
        # Keep the raw string for kline-capable sources
        if isinstance(interval, Timeframe):
            self._kline_interval = interval.value if interval != Timeframe.TICK else None
        elif isinstance(interval, int | float):
            # Numeric intervals imply tick cadence, not kline
            self._kline_interval = None
        else:
            # String interval - check if it's "tick"
            self._kline_interval = None if interval == "tick" else interval
        return self

    def on_data(self, callback: Callable[[pd.DataFrame], None]) -> StreamQuery:
        """Set data callback.

        Args:
            callback: Function to handle incoming data batches
        """
        self._on_data = callback
        return self

    def on_error(self, callback: Callable[[Exception], None]) -> StreamQuery:
        """Set error callback."""
        self._on_error = callback
        return self

    def on_close(self, callback: Callable[[], None]) -> StreamQuery:
        """Set close callback."""
        self._on_close = callback
        return self

    def pipe(self, func: Callable[[pd.DataFrame], pd.DataFrame]) -> StreamQuery:
        """Attach a transform to run on each batch before callbacks."""
        self._pipes.append(func)
        return self

    def buffer(
        self, *, window: str | float | int | None = None, size: int | None = None
    ) -> StreamQuery:
        """Keep a rolling buffer (by time window and/or row count) before emitting."""
        self._window_seconds = _window_to_seconds(window) if window is not None else None
        self._max_rows = size
        return self

    def resample(self, to_timeframe: str) -> StreamQuery:
        """Resample buffered ticks to a coarser timeframe (requires buffer to accumulate)."""
        self._resample_to = to_timeframe
        # Auto-buffer if none set: keep 2x target window, capped minimum
        if self._window_seconds is None:
            window_sec = _window_to_seconds(to_timeframe)
            self._window_seconds = max(window_sec * 2, window_sec + 30)
        return self

    def clean(
        self,
        remove_outliers: bool = False,
        remove_invalid_prices: bool = False,
        validate_ohlc: bool = False,
        dropna_subset: list[str] | None = None,
        dropna_how: str = "any",
    ) -> StreamQuery:
        """Cleaning step applied after buffering/resampling."""

        def cleaner(df: pd.DataFrame) -> pd.DataFrame:
            transforms: list[Callable[[pd.DataFrame], pd.DataFrame]] = []
            transforms.append(add_timestamp_sorting)
            transforms.append(lambda d: remove_duplicates(d, keep="last"))

            if dropna_subset is None:

                def adaptive_dropna(d: pd.DataFrame) -> pd.DataFrame:
                    ohlcv = detect_ohlcv_columns(d)
                    cols = [v for v in ohlcv.values() if v is not None]
                    if cols:
                        return d.dropna(subset=cols, how="any")
                    return d.dropna(how=dropna_how)

                transforms.append(adaptive_dropna)
            else:
                transforms.append(lambda d: d.dropna(subset=dropna_subset, how=dropna_how))

            if remove_invalid_prices:
                transforms.append(clean_remove_invalid_prices)
            if validate_ohlc:
                transforms.append(validate_ohlc_relationships)
            if remove_outliers:
                transforms.append(lambda d: clean_remove_outliers(d, columns=None))

            for t in transforms:
                df = t(df)
            return df

        self._clean_fn = cleaner
        return self

    def get(self, *, start: bool = True) -> StreamSession:
        """Instantiate a StreamSession (optionally auto-start).

        Args:
            start: If True (default), start streaming immediately.
        """
        adapter = self._api._create_adapter(self._source, self._category)

        # Determine stream type
        stream_type = "trades" if self._kline_interval is None else "klines"

        session = StreamSession(
            adapter,
            self._symbols,
            stream_type,
            self._kline_interval,
            self._on_data,
            self._on_error,
            self._on_close,
            window_seconds=self._window_seconds,
            max_rows=self._max_rows,
            resample_to=self._resample_to,
            clean_fn=self._clean_fn,
            resilience=self._resilience,
            source=self._source,
            rate_limiter=self._rate_limiter,
            sequence_tracker=self._sequence_tracker,
            journal=self._journal,
        )
        for pipe in self._pipes:
            session.pipe(pipe)
        if start:
            session.start()
        return session
