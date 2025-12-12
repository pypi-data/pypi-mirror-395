"""Streaming API entry point."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from qldata.api.sessions.query import StreamQuery
from qldata.api.sessions.stream import _interval_to_seconds
from qldata.models.timeframe import Timeframe

if TYPE_CHECKING:
    from collections.abc import Callable

    import pandas as pd

    from qldata.api.config.resilience import ResilienceConfig
    from qldata.resilience import RateLimitManager, SequenceTracker
else:
    from qldata.api.config.resilience import ResilienceConfig


class StreamingAPI:
    """Single entry point for live streaming data."""

    def __call__(
        self,
        symbols: str | list[str],
        *,
        source: str,
        category: str | None = None,
        interval: float = 1.0,
        on_data: Callable[[pd.DataFrame], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_close: Callable[[], None] | None = None,
        resilience: ResilienceConfig | bool = True,
        rate_limiter: RateLimitManager | None = None,
        sequence_tracker: dict[str, SequenceTracker] | None = None,
        journal: Any | None = None,
    ) -> StreamQuery:
        """Create a streaming builder.

        Args:
            symbols: Single symbol or list of symbols
            source: Streaming source identifier ("binance", "bybit")
            category: Required for bybit ("spot", "linear", "inverse"); optional for binance
            interval: Tick interval (seconds) or timeframe-like string
            on_data: Callback invoked with each batch (DataFrame)
            on_error: Callback invoked on exceptions inside the pipeline
            on_close: Callback invoked when stream stops
            resilience: Enable resilience features (default: True). Pass False to disable.
            rate_limiter: Custom RateLimitManager instance (overrides default)
            sequence_tracker: Custom SequenceTracker dict keyed by symbol (overrides default)
            journal: DataJournal instance or path string for journaling
        """
        if not isinstance(resilience, bool | ResilienceConfig):
            raise TypeError("resilience must be a bool or ResilienceConfig")

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
            on_data,
            on_error,
            on_close,
            resilience=resilience,
            rate_limiter=rate_limiter,
            sequence_tracker=sequence_tracker,
            journal=journal,
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


# Default singleton instance
stream = StreamingAPI()
