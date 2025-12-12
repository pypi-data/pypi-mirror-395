"""Streaming API entry point."""

from __future__ import annotations

from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Any

import pandas as pd

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
    from types import TracebackType


def _interval_to_seconds(interval: str | Timeframe | float | int) -> float:
    """Normalize interval to seconds."""
    if isinstance(interval, float | int):
        return float(interval)
    if isinstance(interval, Timeframe):
        # Special case: tick has no fixed interval, use 1.0 for streaming compatibility
        if interval == Timeframe.TICK:
            return 1.0
        return float(interval.to_seconds())
    # assume string timeframe like "1s", "1m", "4h", "1d"
    tf = Timeframe.from_string(interval)
    # Special case: tick has no fixed interval, use 1.0 for streaming compatibility
    if tf == Timeframe.TICK:
        return 1.0
    return float(tf.to_seconds())


def _window_to_seconds(value: str | float | int) -> float:
    """Convert a window spec to seconds."""
    if isinstance(value, float | int):
        return float(value)
    spec = value.strip().lower()
    if spec.endswith("ms"):
        return float(spec[:-2]) / 1000
    if spec.endswith("s"):
        return float(spec[:-1])
    if spec.endswith("m"):
        return float(spec[:-1]) * 60
    if spec.endswith("h"):
        return float(spec[:-1]) * 3600
    if spec.endswith("d"):
        return float(spec[:-1]) * 86400
    return float(spec)


class StreamSession(AbstractContextManager["StreamSession"]):
    """Manage a live streaming session using adapter WebSocket methods."""

    def __init__(
        self,
        adapter: Any,  # BinanceAdapter or BybitAdapter
        symbols: list[str],
        stream_type: str,  # "trades", "klines", "ticker"
        interval: str | None,  # For klines
        on_tick: Callable[[pd.DataFrame], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_close: Callable[[], None] | None = None,
        *,
        window_seconds: float | None = None,
        max_rows: int | None = None,
        resample_to: str | None = None,
        clean_fn: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
    ) -> None:
        self._adapter = adapter
        self._symbols = symbols
        self._stream_type = stream_type
        self._interval = interval
        self._on_tick = on_tick
        self._on_error = on_error
        self._on_close = on_close
        self._pipes: list[Callable[[pd.DataFrame], pd.DataFrame]] = []
        self._latest: pd.DataFrame | None = None
        self._new_data_available: bool = False
        self._buffers: dict[str, pd.DataFrame] = {}
        self._window_seconds = window_seconds
        self._max_rows = max_rows
        self._resample_to = resample_to
        self._clean_fn = clean_fn
        self._stream_keys: list[str] = []

    def start(self) -> StreamSession:
        """Start streaming."""
        if not self._symbols:
            raise ValueError("At least one symbol is required to start a stream")

        # Start appropriate stream type for each symbol
        for symbol in self._symbols:
            try:
                if self._stream_type == "trades":
                    key = self._adapter.stream_trades(symbol, self._handle_message)
                elif self._stream_type == "klines" and self._interval:
                    key = self._adapter.stream_klines(symbol, self._interval, self._handle_message)
                elif self._stream_type == "ticker":
                    key = self._adapter.stream_ticker(symbol, self._handle_message)
                else:
                    raise ValueError(f"Unknown stream type: {self._stream_type}")

                # Binance returns keys, Bybit doesn't - handle both
                if key:
                    self._stream_keys.append(key)
            except Exception as e:
                self._handle_error(e)

        return self

    def stop(self) -> None:
        """Stop streaming."""
        try:
            self._adapter.stop_all_streams()
        except Exception as e:
            if self._on_error:
                self._on_error(e)

        if self._on_close:
            self._on_close()

    def subscribe(self, symbols: list[str]) -> StreamSession:
        """Subscribe to additional symbols."""
        for symbol in symbols:
            if symbol not in self._symbols:
                self._symbols.append(symbol)
                # Start stream for new symbol
                try:
                    if self._stream_type == "trades":
                        key = self._adapter.stream_trades(symbol, self._handle_message)
                    elif self._stream_type == "klines" and self._interval:
                        key = self._adapter.stream_klines(symbol, self._interval, self._handle_message)
                    elif self._stream_type == "ticker":
                        key = self._adapter.stream_ticker(symbol, self._handle_message)

                    if key:
                        self._stream_keys.append(key)
                except Exception as e:
                    self._handle_error(e)
        return self

    def unsubscribe(self, symbols: list[str] | None = None) -> StreamSession:
        """Unsubscribe from symbols (stops all and restarts without those symbols)."""
        if symbols is None:
            self._symbols = []
            self.stop()
        else:
            # Remove from list
            self._symbols = [s for s in self._symbols if s not in symbols]
            # Restart streams
            self.stop()
            if self._symbols:
                self.start()
        return self

    def pipe(self, func: Callable[[pd.DataFrame], pd.DataFrame]) -> StreamSession:
        """Attach a transform to run on each batch before callbacks."""
        self._pipes.append(func)
        return self

    @property
    def latest(self) -> pd.DataFrame | None:
        """Most recent batch received (set when no on_tick callback is provided)."""
        return self._latest

    @property
    def has_new_data(self) -> bool:
        """Whether a new batch has arrived since the last consume_latest() call."""
        return self._new_data_available

    def consume_latest(self) -> pd.DataFrame | None:
        """Return the latest batch and reset the new-data flag."""
        latest = self._latest
        self._new_data_available = False
        return latest

    def _handle_message(self, msg: dict) -> None:
        """Handle incoming WebSocket message from adapter."""
        try:
            # Convert message to DataFrame
            df = self._message_to_dataframe(msg)

            if df is None or df.empty:
                return

            # Apply pipeline
            self._handle_tick(df)

        except Exception as exc:
            self._handle_error(exc)

    def _message_to_dataframe(self, msg: dict) -> pd.DataFrame | None:
        """Convert adapter WebSocket message to DataFrame.

        Adapters return raw exchange messages, we normalize them.
        """
        try:
            # Binance trade message
            if "e" in msg and msg["e"] == "trade":
                return pd.DataFrame([{
                    "timestamp": pd.to_datetime(msg.get("E", msg.get("T")), unit="ms"),
                    "symbol": msg.get("s"),
                    "price": float(msg.get("p", 0)),
                    "volume": float(msg.get("q", 0)),
                    "bid": None,
                    "ask": None,
                }])

            # Binance kline message
            elif "e" in msg and msg["e"] == "kline":
                k = msg.get("k", {})
                return pd.DataFrame([{
                    "timestamp": pd.to_datetime(k.get("T"), unit="ms"),
                    "symbol": k.get("s"),
                    "open": float(k.get("o", 0)),
                    "high": float(k.get("h", 0)),
                    "low": float(k.get("l", 0)),
                    "close": float(k.get("c", 0)),
                    "volume": float(k.get("v", 0)),
                    "price": float(k.get("c", 0)),
                    "bid": None,
                    "ask": None,
                }])

            # Bybit messages (simplified - may need adjustment based on actual format)
            elif "topic" in msg:
                data = msg.get("data", {})
                if isinstance(data, list):
                    data = data[0] if data else {}

                return pd.DataFrame([{
                    "timestamp": pd.to_datetime(data.get("t", data.get("T")), unit="ms"),
                    "symbol": msg.get("topic", "").split(".")[-1],
                    "price": float(data.get("price", data.get("close", 0))),
                    "volume": float(data.get("volume", data.get("v", 0))),
                    "bid": None,
                    "ask": None,
                }])

            # Generic fallback
            return None

        except Exception:
            return None

    def _handle_tick(self, df: pd.DataFrame) -> None:
        try:
            for pipe in self._pipes:
                df = pipe(df)

            df = self._apply_buffer(df)
            df = self._apply_resample(df)
            if self._clean_fn:
                df = self._clean_fn(df)

            if self._on_tick:
                self._on_tick(df)
            else:
                # If no callback set, retain latest batch for pull-style access
                self._latest = df
                self._new_data_available = True
        except Exception as exc:
            self._handle_error(exc)

    def _handle_error(self, exc: Exception) -> None:
        if self._on_error:
            self._on_error(exc)
        else:
            raise

    def _apply_buffer(self, df: pd.DataFrame) -> pd.DataFrame:
        """Maintain per-symbol rolling buffers if configured."""
        if self._window_seconds is None and self._max_rows is None:
            return df

        combined: list[pd.DataFrame] = []
        cutoff_ts: float | None = None
        if self._window_seconds is not None:
            cutoff_ts = pd.Timestamp.utcnow().timestamp() - self._window_seconds

        for symbol, group in df.groupby("symbol"):
            existing = self._buffers.get(symbol)
            merged = group if existing is None else pd.concat([existing, group])
            merged = merged.sort_values("timestamp")

            if cutoff_ts is not None:
                merged = merged[merged["timestamp"].astype("int64") / 1_000_000_000 >= cutoff_ts]

            if self._max_rows is not None and len(merged) > self._max_rows:
                merged = merged.iloc[-self._max_rows :]

            self._buffers[symbol] = merged
            combined.append(merged)

        return pd.concat(combined, ignore_index=True) if combined else df

    def _apply_resample(self, df: pd.DataFrame) -> pd.DataFrame:
        """Resample buffered data if configured."""
        if self._resample_to is None or df.empty:
            return df

        out: list[pd.DataFrame] = []
        for symbol, group in df.groupby("symbol"):
            g = group.copy()
            g = g.set_index("timestamp")
            resampled = (
                g.resample(self._resample_to)
                .agg({"price": "last", "volume": "sum", "bid": "last", "ask": "last"})
                .dropna(how="all")
            )
            if resampled.empty:
                continue
            resampled["symbol"] = symbol
            out.append(resampled.reset_index())

        if not out:
            return pd.DataFrame(columns=df.columns)

        return pd.concat(out, ignore_index=True)

    def __enter__(self) -> StreamSession:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.stop()


class StreamQuery:
    """Fluent builder for streaming sessions."""

    def __init__(
        self,
        api: StreamingAPI,
        symbols: list[str],
        source: str,
        category: str | None,
        interval: float,
        kline_interval: str | None,
        on_tick: Callable[[pd.DataFrame], None] | None,
        on_error: Callable[[Exception], None] | None,
        on_close: Callable[[], None] | None,
    ) -> None:
        self._api = api
        self._symbols = symbols
        self._source = source
        self._category = category
        self._interval_seconds = interval
        self._kline_interval = kline_interval
        self._on_tick = on_tick
        self._on_error = on_error
        self._on_close = on_close
        self._pipes: list[Callable[[pd.DataFrame], pd.DataFrame]] = []
        self._window_seconds: float | None = None
        self._max_rows: int | None = None
        self._resample_to: str | None = None
        self._clean_fn: Callable[[pd.DataFrame], pd.DataFrame] | None = None

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

    def on_tick(self, callback: Callable[[pd.DataFrame], None]) -> StreamQuery:
        """Set tick callback."""
        self._on_tick = callback
        return self

    def on_data(self, callback: Callable[[pd.DataFrame], None]) -> StreamQuery:
        """Set data callback (alias for on_tick, more intuitive for aggregated data)."""
        return self.on_tick(callback)

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
            self._on_tick,
            self._on_error,
            self._on_close,
            window_seconds=self._window_seconds,
            max_rows=self._max_rows,
            resample_to=self._resample_to,
            clean_fn=self._clean_fn,
        )
        for pipe in self._pipes:
            session.pipe(pipe)
        if start:
            session.start()
        return session


class StreamingAPI:
    """Single entry point for live streaming data."""

    def __call__(
        self,
        symbols: str | list[str],
        *,
        source: str,
        category: str | None = None,
        interval: float = 1.0,
        on_tick: Callable[[pd.DataFrame], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_close: Callable[[], None] | None = None,
        **_kwargs: Any,
    ) -> StreamQuery:
        """Create a streaming builder.

        Args:
            symbols: Single symbol or list of symbols
            source: Streaming source identifier ("binance", "bybit")
            category: Required for bybit ("spot", "linear", "inverse"); optional for binance
            interval: Tick interval (seconds) or timeframe-like string
            on_tick: Callback invoked with each batch (DataFrame)
            on_error: Callback invoked on exceptions inside the pipeline
            on_close: Callback invoked when stream stops
        """
        symbol_list = [symbols] if isinstance(symbols, str) else symbols
        if not symbol_list:
            raise ValueError("Must provide at least one symbol for streaming")
        normalized_category = self._normalize_category(source, category)
        normalized_symbols = _normalize_symbols(symbol_list, source, normalized_category)
        kline_interval: str | None
        if isinstance(interval, Timeframe):
            kline_interval = interval.value
        elif isinstance(interval, int | float):
            kline_interval = None
        else:
            kline_interval = interval
        return StreamQuery(
            self,
            normalized_symbols,
            source,
            normalized_category,
            _interval_to_seconds(interval),
            kline_interval,
            on_tick,
            on_error,
            on_close,
        )

    def _create_adapter(self, source: str, category: str | None) -> Any:
        """Create adapter for streaming."""
        if source == "binance":
            from qldata.adapters import BinanceAdapter

            return BinanceAdapter(category=category or "spot")
        if source == "bybit":
            from qldata.adapters import BybitAdapter

            return BybitAdapter(category=category or "linear")
        raise ValueError(
            f"Streaming source '{source}' is not supported (available: 'binance', 'bybit')"
        )

    def _normalize_category(self, source: str, category: str | None) -> str | None:
        """Validate and normalize category per streaming source."""
        if source == "bybit":
            if category is None:
                raise ValueError(
                    "category is required for bybit streaming ('spot', 'linear', 'inverse')"
                )
            valid = {"spot", "linear", "inverse"}
            if category not in valid:
                raise ValueError(
                    f"Invalid category '{category}' for bybit streaming. Choose from {sorted(valid)}"
                )
            return category

        if source == "binance":
            if category is None:
                return "spot"
            valid = {"spot", "usdm", "coinm"}
            if category not in valid:
                raise ValueError(
                    f"Invalid category '{category}' for binance streaming. Choose from {sorted(valid)}"
                )
            return category

        return None


def _normalize_symbols(symbols: list[str], source: str, category: str | None) -> list[str]:
    """Normalize and validate symbols for streaming sources."""
    normed: list[str] = []
    for sym in symbols:
        cleaned = sym.upper().replace("/", "").replace("-", "")

        if source == "binance":
            normed.append(cleaned)
            continue

        if source == "bybit":
            if category == "inverse":
                if not cleaned.endswith("USD"):
                    raise ValueError(
                        f"Bybit inverse symbols must end with 'USD' (e.g., BTCUSD); got '{sym}'"
                    )
            else:  # spot or linear
                if not cleaned.endswith("USDT"):
                    raise ValueError(
                        f"Bybit {category} symbols must end with 'USDT' (e.g., BTCUSDT); got '{sym}'"
                    )
            normed.append(cleaned)
            continue

        normed.append(cleaned)

    return normed


# Singleton
stream = StreamingAPI()


__all__ = ["StreamingAPI", "StreamSession", "StreamQuery", "stream"]
