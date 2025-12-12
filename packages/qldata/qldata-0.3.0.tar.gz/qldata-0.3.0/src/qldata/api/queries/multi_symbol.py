"""Fluent query builder for multiple symbols."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import pandas as pd

from qldata.api.queries.symbol import SymbolQuery
from qldata.common.logger import get_logger
from qldata.common.strings import normalize_symbol
from qldata.common.time import parse_datetime
from qldata.config import get_config
from qldata.errors.data import NoDataFound
from qldata.errors.source import SourceError
from qldata.models.timeframe import Timeframe

if TYPE_CHECKING:
    from qldata.config.manager import ConfigManager

logger = get_logger(__name__)


class MultiSymbolQuery:
    """Fluent query builder for multiple symbols.

    Provides explicit methods for handling multiple symbols.
    Always returns dict or MultiIndex DataFrame.
    """

    def __init__(self, tickers: list[str], config: "ConfigManager | None" = None) -> None:
        """Initialize query for multiple symbols.

        Args:
            tickers: List of symbol tickers
            config: Optional injected ConfigManager for testing/overrides
        """
        if not tickers:
            raise ValueError("Must provide at least one symbol")
        self._symbols = [normalize_symbol(t) for t in tickers]
        self._config = config or get_config()
        self._start: datetime | None = None
        self._end: datetime | None = None
        self._timeframe: Timeframe = Timeframe.DAY_1
        self._source: str | None = None
        self._category: str | None = None
        self._validate: bool | None = False
        self._transforms: list[Any] = []
        self._data_dir: Path | None = None
        self._store_type: str | None = None

    # Time range methods (same as SymbolQuery)
    def between(self, start: str | datetime, end: str | datetime) -> "MultiSymbolQuery":
        """Set explicit date range."""
        self._start = parse_datetime(start) if isinstance(start, str) else start
        self._end = parse_datetime(end) if isinstance(end, str) else end
        return self

    def since(self, start: str | datetime) -> "MultiSymbolQuery":
        """Set start date, end defaults to now."""
        self._start = parse_datetime(start) if isinstance(start, str) else start
        self._end = datetime.now(timezone.utc)
        return self

    def last(
        self, n: int, unit: Literal["days", "hours", "minutes"] = "days"
    ) -> "MultiSymbolQuery":
        """Get last N time units ending now.

        Args:
            n: Number of time units
            unit: Time unit, defaults to "days"

        Examples:
            >>> qd.data(["BTCUSDT", "SOLUSDT"]).last(30).resolution("1d").get()
        """
        is_local = self._source in {"file", "local"}
        self._end = datetime.now() if is_local else datetime.now(timezone.utc)

        if unit == "days":
            self._start = self._end - timedelta(days=n)
        elif unit == "hours":
            self._start = self._end - timedelta(hours=n)
        elif unit == "minutes":
            self._start = self._end - timedelta(minutes=n)
        else:
            raise ValueError(f"unit must be 'days', 'hours', or 'minutes', got {unit}")

        return self

    # Resolution/Timeframe methods
    def resolution(self, interval: str | Timeframe) -> "MultiSymbolQuery":
        """Set bar resolution/interval.

        Args:
            interval: Time interval string (e.g., "1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M")
                     or Timeframe enum

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(30).resolution("1d").get()
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(24).resolution("1h").get()
        """
        self._timeframe = Timeframe.from_string(interval) if isinstance(interval, str) else interval
        return self

    # Data source
    def from_source(
        self, source: str, category: str | None = None, **kwargs: Any
    ) -> "MultiSymbolQuery":
        """Specify data source."""
        valid_sources = ["binance", "bybit", "local"]
        if source not in valid_sources:
            raise ValueError(f"source must be one of {valid_sources}, got {source}")
        self._source = source
        if category:
            self._category = category
        if "data_dir" in kwargs and kwargs["data_dir"] is not None:
            self._data_dir = Path(kwargs["data_dir"]).expanduser().resolve()
        if "store_type" in kwargs and kwargs["store_type"] is not None:
            self._store_type = kwargs["store_type"]
        return self

    def category(self, name: str) -> "MultiSymbolQuery":
        """Specify market category for the chosen source (binance/bybit)."""
        self._category = name
        return self

    # Data cleaning and validation
    def clean(
        self,
        remove_outliers: bool = False,
        remove_invalid_prices: bool = False,
        validate_ohlc: bool = False,
        dropna_subset: list[str] | None = None,
        dropna_how: str = "any",
    ) -> "MultiSymbolQuery":
        """Apply adaptive data cleaning pipeline to all symbols.

        Default behavior (conservative, safe for all data types):
        - Sorts by timestamp
        - Removes duplicate timestamps (keeps last)
        - Drops rows with NaN in OHLCV columns (if present), or completely empty rows otherwise

        Args:
            remove_outliers: Remove statistical outliers from numeric columns (default: False)
            remove_invalid_prices: Remove zero/negative prices (default: False)
            validate_ohlc: Validate OHLC relationships (default: False)
            dropna_subset: Override columns for NaN checking (default: auto-detect OHLCV)
            dropna_how: 'any' or 'all' for dropna behavior (default: 'any')

        Returns:
            Self for method chaining

        Examples:
            >>> # Basic cleaning
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(30).resolution("1d").clean().get()

            >>> # Aggressive cleaning
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(30).resolution("1d").clean(remove_outliers=True, validate_ohlc=True).get()
        """
        from qldata.transforms.clean import (
            add_timestamp_sorting,
            detect_ohlcv_columns,
            remove_duplicates,
            validate_ohlc_relationships,
        )
        from qldata.transforms.clean import (
            remove_invalid_prices as rm_invalid,
        )
        from qldata.transforms.clean import (
            remove_outliers as rm_outliers,
        )

        # 1. Sort by timestamp
        self._transforms.append(add_timestamp_sorting)

        # 2. Remove duplicates (keep last)
        self._transforms.append(lambda df: remove_duplicates(df, keep="last"))

        # 3. Adaptive NaN dropping
        if dropna_subset is None:
            # Auto-detect: check for OHLCV columns
            def adaptive_dropna(df):
                ohlcv = detect_ohlcv_columns(df)
                ohlcv_cols = [v for v in ohlcv.values() if v is not None]

                if ohlcv_cols:
                    # Drop if any OHLCV is NaN
                    return df.dropna(subset=ohlcv_cols, how="any")
                else:
                    # Custom data: drop only completely empty rows
                    return df.dropna(how="all")

            self._transforms.append(adaptive_dropna)
        else:
            # User-specified subset
            self._transforms.append(lambda df: df.dropna(subset=dropna_subset, how=dropna_how))

        # 4. Optional: Remove invalid prices
        if remove_invalid_prices:
            self._transforms.append(rm_invalid)

        # 5. Optional: Validate OHLC relationships
        if validate_ohlc:
            self._transforms.append(validate_ohlc_relationships)

        # 6. Optional: Remove outliers
        if remove_outliers:

            def drop_volume_outliers(df: pd.DataFrame) -> pd.DataFrame:
                cleaned = rm_outliers(df, columns="volume")
                if "volume" in cleaned.columns:
                    median_vol = cleaned["volume"].median()
                    cleaned = cleaned[cleaned["volume"] <= median_vol * 5]
                return cleaned

            self._transforms.append(drop_volume_outliers)

        return self

    # Validation
    def validate(self, enabled: bool = True) -> "MultiSymbolQuery":
        """Enable/disable data validation."""
        self._validate = enabled
        return self

    # Convenience transform methods
    def fill_forward(self) -> "MultiSymbolQuery":
        """Forward fill missing values (propagate last valid observation).

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(30).resolution("1d").fill_forward().get()
        """
        from qldata.transforms import fill_forward as ff

        self._transforms.append(ff)
        return self

    def fill_backward(self) -> "MultiSymbolQuery":
        """Backward fill missing values (use next valid observation).

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(30).resolution("1d").fill_backward().get()
        """
        from qldata.transforms import fill_backward as fb

        self._transforms.append(fb)
        return self

    def interpolate(self, method: str = "linear") -> "MultiSymbolQuery":
        """Interpolate missing values.

        Args:
            method: Interpolation method ('linear', 'time', 'polynomial', etc.)

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(30).resolution("1d").interpolate().get()
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(30).resolution("1d").interpolate(method='time').get()
        """
        from qldata.transforms import fill_interpolate

        self._transforms.append(lambda df: fill_interpolate(df, method=method))
        return self

    def resample(self, to_timeframe: str) -> "MultiSymbolQuery":
        """Resample data to a different timeframe.

        Args:
            to_timeframe: Target timeframe (e.g., "1h", "1d", "1w")

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(30).resolution("1m").resample("1h").get()
            >>> qd.data(["BTCUSDT", "ETHUSDT"]).last(7).resolution("1m").resample("5m").get()
        """
        from qldata.transforms import resample as rs

        def resample_transform(df):
            required = ["open", "high", "low", "close", "volume"]
            if not all(col in df.columns for col in required):
                close_series = df["close"] if "close" in df.columns else pd.Series([], dtype=float)
                if "open" not in df.columns:
                    df["open"] = close_series
                if "high" not in df.columns:
                    df["high"] = close_series
                if "low" not in df.columns:
                    df["low"] = close_series
                if "close" not in df.columns:
                    df["close"] = close_series
                if "volume" not in df.columns:
                    df["volume"] = 0
            return rs(df, self._timeframe, to_timeframe)

        self._transforms.append(resample_transform)
        return self

    # Execution - single entry point
    def get(
        self,
        format: Literal["dict", "combined"] = "dict",
        parallel: bool = True,
        workers: int = 4,
    ) -> dict[str, pd.DataFrame] | pd.DataFrame:
        """Execute query and return data.

        Args:
            format: "dict" (default) returns mapping of symbol -> DataFrame; "combined" returns MultiIndex DataFrame
            parallel: Whether to fetch in parallel when multiple symbols
            workers: Number of worker threads when parallel is enabled
        """
        # Set defaults
        if self._source == "local":
            if self._start is None:
                self._start = datetime.min
            if self._end is None:
                self._end = datetime.max
        else:
            if self._start is None:
                self._start = datetime.now(timezone.utc) - timedelta(days=30)
            if self._end is None:
                self._end = datetime.now(timezone.utc)

        # Fetch data
        if self._source == "local":
            data_dict = self._load_from_storage()
        elif parallel and len(self._symbols) > 1:
            data_dict = self._fetch_parallel(workers)
        else:
            data_dict = self._fetch_sequential()

        # Apply transforms across all symbols
        for transform in self._transforms:
            data_dict = {sym: transform(df) for sym, df in data_dict.items()}

        # Validate if requested
        if self._validate or (self._validate is None and get_config().is_validation_enabled()):
            from qldata.validation.checks.price import validate_bars

            data_dict = {sym: validate_bars(df) for sym, df in data_dict.items()}

        if format == "dict":
            return data_dict
        if format == "combined":
            if not data_dict or all(df.empty for df in data_dict.values()):
                return pd.DataFrame()
            return pd.concat(data_dict, names=["symbol", "timestamp"])
        raise ValueError("format must be 'dict' or 'combined'")

    def _fetch_sequential(self) -> dict[str, pd.DataFrame]:
        """Fetch symbols sequentially."""
        data_dict = {}

        for symbol in self._symbols:
            query = SymbolQuery(symbol, config=self._config)
            query._start = self._start
            query._end = self._end
            query._timeframe = self._timeframe
            query._source = self._source
            query._category = self._category
            query._validate = self._validate
            query._data_dir = self._data_dir
            query._store_type = self._store_type

            try:
                data_dict[symbol] = query.get()
            except NoDataFound as e:
                logger.warning(f"No data found for {symbol}: {e}")
                data_dict[symbol] = pd.DataFrame()
            except (SourceError, ConnectionError, TimeoutError) as e:
                logger.error(f"Failed to fetch {symbol}: {e}")
                data_dict[symbol] = pd.DataFrame()
            except Exception:
                logger.exception(f"Unexpected error fetching {symbol}")
                data_dict[symbol] = pd.DataFrame()

        return data_dict

    def _fetch_parallel(self, workers: int) -> dict[str, pd.DataFrame]:
        """Fetch symbols in parallel using threads."""
        results: dict[str, pd.DataFrame] = {}

        def build_query(symbol: str) -> SymbolQuery:
            q = SymbolQuery(symbol)
            q._start = self._start
            q._end = self._end
            q._timeframe = self._timeframe
            q._source = self._source
            q._category = self._category
            q._validate = self._validate
            q._data_dir = self._data_dir
            q._store_type = self._store_type
            return q

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_symbol = {
                executor.submit(build_query(symbol).get): symbol for symbol in self._symbols
            }

            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    results[symbol] = future.result()
                except NoDataFound as e:
                    logger.warning(f"No data found for {symbol}: {e}")
                    results[symbol] = pd.DataFrame()
                except (SourceError, ConnectionError, TimeoutError) as e:
                    logger.error(f"Failed to fetch {symbol}: {e}")
                    results[symbol] = pd.DataFrame()
                except Exception:  # pragma: no cover - defensive
                    logger.exception(f"Unexpected error fetching {symbol}")
                    results[symbol] = pd.DataFrame()

        return results

    def _load_from_storage(self) -> dict[str, pd.DataFrame]:
        """Load multiple symbols from storage."""
        store = (
            self._create_custom_store()
            if (self._data_dir or self._store_type)
            else self._config.get_default_store()
        )

        if self._timeframe is None:
            raise ValueError(
                "Must specify timeframe when loading from storage: use .resolution(...)"
            )

        data_dict: dict[str, pd.DataFrame] = {}
        for symbol in self._symbols:
            try:
                data_dict[symbol] = store.read_bars(
                    symbol,
                    self._start,  # type: ignore
                    self._end,  # type: ignore
                    self._timeframe,
                )
            except NoDataFound as e:
                logger.warning(f"No stored data found for {symbol}: {e}")
                data_dict[symbol] = pd.DataFrame()
            except Exception as e:
                logger.error(f"Error loading {symbol} from storage: {e}")
                data_dict[symbol] = pd.DataFrame()
        return data_dict

    def _create_custom_store(self):
        """Create a store using overrides."""
        from qldata.stores.factory import StoreFactory

        data_dir = self._data_dir or self._config.get_data_dir()
        store_type = self._store_type or self._config.get_store_type()

        return StoreFactory.create(store_type, data_dir)

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"MultiSymbolQuery(symbols={self._symbols}, "
            f"start={self._start}, end={self._end}, "
            f"resolution={self._timeframe})"
        )
