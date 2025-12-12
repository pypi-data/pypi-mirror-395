"""Fluent query builder for single symbols."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import pandas as pd

from qldata.api.queries.helpers import _get_adapter
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


class SymbolQuery:
    """Fluent query builder for a single symbol.

    Provides explicit, chainable methods for building queries.
    Always returns a single DataFrame.
    """

    def __init__(self, ticker: str, config: "ConfigManager | None" = None) -> None:
        """Initialize query for a symbol.

        Args:
            ticker: Symbol ticker (e.g., "BTCUSDT")
            config: Optional injected ConfigManager for testing/overrides
        """
        self._symbol = normalize_symbol(ticker)
        self._config = config or get_config()
        self._start: datetime | None = None
        self._end: datetime | None = None
        self._timeframe: Timeframe = Timeframe.DAY_1
        self._source: str | None = None
        self._validate: bool | None = False
        self._category: str | None = None
        self._transforms: list[Any] = []
        self._data_dir: Path | None = None
        self._store_type: str | None = None
        self._file_path: Path | None = None

    # Time range methods
    def between(self, start: str | datetime, end: str | datetime) -> "SymbolQuery":
        """Set explicit date range.

        Args:
            start: Start date/time
            end: End date/time

        Examples:
            >>> qd.symbol("BTCUSDT").between("2024-01-01", "2024-12-01")
            >>> qd.symbol("BTCUSDT").between("2024-01-01", "now")
        """
        self._start = parse_datetime(start) if isinstance(start, str) else start
        self._end = parse_datetime(end) if isinstance(end, str) else end
        return self

    def since(self, start: str | datetime) -> "SymbolQuery":
        """Set start date, end defaults to now.

        Args:
            start: Start date/time

        Examples:
            >>> qd.symbol("BTCUSDT").since("2024-01-01")
        """
        self._start = parse_datetime(start) if isinstance(start, str) else start
        self._end = datetime.now(timezone.utc)
        return self

    def last(self, n: int, unit: Literal["days", "hours", "minutes"] = "days") -> "SymbolQuery":
        """Get last N time units ending now.

        Unified method for recent periods with sensible defaults.

        Args:
            n: Number of time units
            unit: Time unit ("days", "hours", or "minutes"), defaults to "days"

        Examples:
            >>> qd.data("BTCUSDT").last(30)              # last 30 days
            >>> qd.data("BTCUSDT").last(24, "hours")     # last 24 hours
            >>> qd.data("BTCUSDT").last(60, "minutes")   # last 60 minutes
        """
        # Use naive timestamps for local/file sources to match stored data
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

    def recent(self, bars: int) -> "SymbolQuery":
        """Get most recent N bars.

        Args:
            bars: Number of bars to fetch

        Examples:
            >>> qd.data("BTCUSDT").recent(100).resolution("1h").get()
        """
        if bars <= 0:
            raise ValueError(f"bars must be positive, got {bars}")

        # Estimate time needed (with 2x buffer for weekends/holidays)
        seconds_per_bar = self._timeframe.to_seconds()
        total_seconds = bars * seconds_per_bar * 2

        self._end = datetime.now(timezone.utc)
        self._start = self._end - timedelta(seconds=total_seconds)
        return self

    # Resolution/Timeframe methods
    def resolution(self, interval: str | Timeframe) -> "SymbolQuery":
        """Set bar resolution/interval.

        Args:
            interval: Time interval string (e.g., "1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M")
                     or Timeframe enum

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data("BTCUSDT").last(7).resolution("1h").get()
            >>> qd.data("BTCUSDT").last(30).resolution("15m").get()
            >>> qd.data("BTCUSDT").between("2024-01-01", "2024-02-01").resolution("1d").get()
        """
        self._timeframe = Timeframe.from_string(interval) if isinstance(interval, str) else interval
        return self

    # Data source
    def from_source(self, source: str, category: str | None = None, **kwargs: Any) -> "SymbolQuery":
        """Specify data source or file path.

        Args:
            source: Broker name ("binance", "bybit"), storage alias ("local"),
                or file path (csv/parquet)
            category: Market category for brokers
            **kwargs: Optional data_dir/store_type for storage
        """
        if self._is_file_path(source):
            self._source = "file"
            self._file_path = Path(source).expanduser().resolve()
            return self

        valid_sources = ["binance", "bybit", "local"]
        if source not in valid_sources:
            raise ValueError(f"source must be one of {valid_sources} or a file path, got {source}")

        if category:
            self._category = category
        self._source = source

        if "data_dir" in kwargs and kwargs["data_dir"] is not None:
            self._data_dir = Path(kwargs["data_dir"]).expanduser().resolve()
        if "store_type" in kwargs and kwargs["store_type"] is not None:
            self._store_type = kwargs["store_type"]
        return self

    @staticmethod
    def _is_file_path(source: str) -> bool:
        """Check if source looks like a file path."""
        if any(source.endswith(ext) for ext in [".csv", ".parquet", ".pq"]):
            return True
        return Path(source).expanduser().resolve().exists()

    # Validation
    # Data cleaning and validation
    def clean(
        self,
        remove_outliers: bool = False,
        remove_invalid_prices: bool = False,
        validate_ohlc: bool = False,
        dropna_subset: list[str] | None = None,
        dropna_how: str = "any",
    ) -> "SymbolQuery":
        """Apply adaptive data cleaning pipeline.

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
            >>> # Basic cleaning (conservative)
            >>> qd.data("BTCUSDT").last(30).resolution("1d").clean().get()

            >>> # Crypto with invalid price removal
            >>> qd.data("BTCUSDT", source="binance").last(7).resolution("1h").clean(remove_invalid_prices=True).get()

            >>> # Aggressive cleaning
            >>> qd.data("BTCUSDT").last(30).resolution("1d").clean(remove_outliers=True, validate_ohlc=True).get()

            >>> # Custom data with specific columns
            >>> qd.data("custom", source="file.csv").clean(dropna_subset=['dataA', 'dataB']).get()
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

    def validate(self, enabled: bool = True) -> "SymbolQuery":
        """Enable/disable data validation.

        Args:
            enabled: Whether to validate data

        Examples:
            >>> qd.data("BTCUSDT").last(30).validate(True).resolution("1d").get()
        """
        self._validate = enabled
        return self

    # Transforms
    def transform(self, func: Any) -> "SymbolQuery":
        """Add a transform function to apply to data.

        Args:
            func: Function that takes DataFrame and returns DataFrame

        Examples:
            >>> qd.data("BTCUSDT").last(30).transform(remove_outliers).resolution("1d").get()
        """
        self._transforms.append(func)
        return self

    # Convenience transform methods
    def fill_forward(self) -> "SymbolQuery":
        """Forward fill missing values (propagate last valid observation).

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data("BTCUSDT").last(30).resolution("1d").fill_forward().get()
        """
        from qldata.transforms import fill_forward as ff

        self._transforms.append(ff)
        return self

    def fill_backward(self) -> "SymbolQuery":
        """Backward fill missing values (use next valid observation).

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data("BTCUSDT").last(30).resolution("1d").fill_backward().get()
        """
        from qldata.transforms import fill_backward as fb

        self._transforms.append(fb)
        return self

    def interpolate(self, method: str = "linear") -> "SymbolQuery":
        """Interpolate missing values.

        Args:
            method: Interpolation method ('linear', 'time', 'polynomial', etc.)

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data("BTCUSDT").last(30).resolution("1d").interpolate().get()
            >>> qd.data("BTCUSDT").last(30).resolution("1d").interpolate(method='time').get()
        """
        from qldata.transforms import fill_interpolate

        self._transforms.append(lambda df: fill_interpolate(df, method=method))
        return self

    def resample(self, to_timeframe: str) -> "SymbolQuery":
        """Resample data to a different timeframe.

        Args:
            to_timeframe: Target timeframe (e.g., "1h", "1d", "1w")

        Returns:
            Self for method chaining

        Examples:
            >>> qd.data("BTCUSDT").last(30).resolution("1m").resample("1h").get()
            >>> qd.data("BTCUSDT").last(7).resolution("1m").resample("5m").get()
        """
        from qldata.transforms import resample as rs

        def resample_transform(df):
            required = ["open", "high", "low", "close", "volume"]
            if not all(col in df.columns for col in required):
                # Fill missing OHLC from close; volume defaults to 0 if missing
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

    # Execution
    def get(self) -> pd.DataFrame:
        """Execute query and return DataFrame (primary execution method)."""
        # Set defaults
        if self._source in {"file", "local"}:
            if self._start is None:
                self._start = datetime.min
            if self._end is None:
                self._end = datetime.max
        else:
            if self._start is None:
                self._start = datetime.now(timezone.utc) - timedelta(days=30)
            if self._end is None:
                self._end = datetime.now(timezone.utc)

        # Get data
        if self._source == "file":
            data = self._load_from_file()
        elif self._source == "local":
            data = self._load_from_storage()
        else:
            data = self._fetch_from_source() if self._source else self._fetch_from_default()

        # Apply transforms
        for transform in self._transforms:
            data = transform(data)

        # Validate if requested
        if self._validate or (self._validate is None and get_config().is_validation_enabled()):
            from qldata.validation.checks.price import validate_bars

            data = validate_bars(data)

        return data

    def _fetch_from_default(self) -> pd.DataFrame:
        """Fetch from default configured source."""
        source = self._config.get_default_source()
        return source.get_bars(
            self._symbol,
            self._start,  # type: ignore
            self._end,  # type: ignore
            self._timeframe,
        )

    def _fetch_from_source(self) -> pd.DataFrame:
        """Fetch from specified source."""
        if self._source == "local":
            return self._load_from_storage()
        if self._source not in {"binance", "bybit"}:
            raise ValueError(f"Unknown source: {self._source}")

        source = _get_adapter(self._source, self._category)

        try:
            data = source.get_bars(
                self._symbol,
                self._start,  # type: ignore
                self._end,  # type: ignore
                self._timeframe,
            )
        except NoDataFound:
            raise
        except Exception as exc:
            raise SourceError(f"Failed to fetch {self._symbol} from {self._source}: {exc}") from exc

        if not isinstance(data, pd.DataFrame) or data.empty:
            raise NoDataFound(f"No data returned for {self._symbol} from {self._source}")

        return data

    def _load_from_file(self) -> pd.DataFrame:
        """Load data from a CSV/Parquet file."""
        if self._file_path is None:
            raise ValueError("File path not set for file source")

        file_path = self._file_path
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix in (".parquet", ".pq"):
            data = pd.read_parquet(file_path)
        elif file_path.suffix == ".csv":
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("Loaded data must have a DatetimeIndex")

        # Filter by requested time window
        return data[(data.index >= self._start) & (data.index <= self._end)]

    def _load_from_storage(self) -> pd.DataFrame:
        """Load data from configured or custom storage."""
        store = (
            self._create_custom_store()
            if (self._data_dir or self._store_type)
            else self._config.get_default_store()
        )

        if self._timeframe is None:
            raise ValueError(
                "Must specify timeframe when loading from storage: use .resolution(...)"
            )

        return store.read_bars(
            self._symbol,
            self._start,  # type: ignore
            self._end,  # type: ignore
            self._timeframe,
        )

    def _create_custom_store(self):
        """Create a store using overrides."""
        from qldata.stores.factory import StoreFactory

        data_dir = self._data_dir or self._config.get_data_dir()
        store_type = self._store_type or self._config.get_store_type()

        return StoreFactory.create(store_type, data_dir)

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"SymbolQuery(symbol={self._symbol}, "
            f"start={self._start}, end={self._end}, "
            f"resolution={self._timeframe})"
        )
