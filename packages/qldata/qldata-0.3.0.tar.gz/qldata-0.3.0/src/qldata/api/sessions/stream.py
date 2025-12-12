"""Live streaming session management."""

from __future__ import annotations

import logging
from contextlib import AbstractContextManager
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd

from qldata.api.config.resilience import EXCHANGE_RATE_LIMITS, ResilienceConfig
from qldata.models.timeframe import Timeframe
from qldata.resilience.rate_limit import RateLimitConfig, RateLimitManager
from qldata.resilience.sequence import SequenceResult, SequenceTracker
from qldata.stores.journal import DataJournal

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import TracebackType

logger = logging.getLogger(__name__)


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
        on_data: Callable[[pd.DataFrame], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_close: Callable[[], None] | None = None,
        *,
        window_seconds: float | None = None,
        max_rows: int | None = None,
        resample_to: str | None = None,
        clean_fn: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
        resilience: ResilienceConfig | bool = True,
        source: str = "binance",
        # Optional component overrides
        rate_limiter: RateLimitManager | None = None,
        sequence_tracker: dict[str, SequenceTracker] | None = None,
        journal: Any | None = None,  # DataJournal or path string
    ) -> None:
        self._adapter = adapter
        self._symbols = symbols
        self._stream_type = stream_type
        self._interval = interval
        self._on_data = on_data
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
        self._source = source

        # Initialize resilience config
        if resilience is False:
            self._resilience = ResilienceConfig.disabled()
        elif resilience is True:
            self._resilience = ResilienceConfig.for_exchange(source)
        else:
            self._resilience = resilience

        # Rate limiter: use provided or create default
        if rate_limiter is not None:
            self._rate_limiter = rate_limiter
        elif self._resilience.rate_limiting:
            limits_config = EXCHANGE_RATE_LIMITS.get(source, EXCHANGE_RATE_LIMITS["binance"])
            limits = {
                k: RateLimitConfig(limit=v["limit"], window_seconds=v["window_seconds"])
                for k, v in limits_config.items()
            }
            self._rate_limiter = RateLimitManager(limits=limits)
        else:
            self._rate_limiter = None

        # Sequence trackers: use provided or create defaults
        if sequence_tracker is not None:
            self._sequence_trackers = sequence_tracker
        elif self._resilience.sequence_tracking:
            self._sequence_trackers = {}
            for symbol in symbols:
                self._sequence_trackers[symbol] = SequenceTracker(
                    symbol, stream_type, gap_threshold=self._resilience.gap_threshold
                )
        else:
            self._sequence_trackers = {}

        # Journal: use provided instance or create from path
        self._journal = None
        if journal is not None:
            if isinstance(journal, str):
                self._journal = DataJournal(Path(journal))
            else:
                self._journal = journal
        elif self._resilience.journal_path is not None:
            self._journal = DataJournal(self._resilience.journal_path)

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
        """Most recent batch received (set when no on_data callback is provided)."""
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

            # Sequence tracking
            if self._resilience.sequence_tracking and "symbol" in df.columns:
                symbol = df["symbol"].iloc[0] if not df.empty else None
                if symbol and symbol in self._sequence_trackers:
                    # Extract sequence from message (trade ID or update ID)
                    seq = msg.get("t") or msg.get("u") or msg.get("T")
                    if seq:
                        result = self._sequence_trackers[symbol].record(seq)
                        if result == SequenceResult.GAP:
                            logger.warning(
                                f"Sequence gap detected for {symbol}, "
                                f"gaps: {self._sequence_trackers[symbol].get_gaps()}"
                            )
                        elif result == SequenceResult.DUPLICATE:
                            logger.debug(f"Duplicate message for {symbol}, seq={seq}")
                            return  # Skip duplicates

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

            if self._on_data:
                self._on_data(df)
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
