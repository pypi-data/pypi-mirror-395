"""Bar to bar resampling."""

import pandas as pd

from qldata.models.timeframe import Timeframe
from qldata.transforms.resample.aggregations import aggregate_bars


def resample_bars(
    bars: pd.DataFrame,
    from_timeframe: Timeframe,
    to_timeframe: Timeframe,
) -> pd.DataFrame:
    """Resample bars to different timeframe.

    Args:
        bars: DataFrame with OHLCV bar data (indexed by timestamp)
        from_timeframe: Current timeframe
        to_timeframe: Target timeframe

    Returns:
        DataFrame with resampled OHLCV data

    Raises:
        ValueError: If trying to resample to lower timeframe

    Example:
        >>> bars_1m = pd.DataFrame({
        ...     'timestamp': pd.date_range('2024-01-01', periods=60, freq='1min'),
        ...     'open': [100 + i*0.1 for i in range(60)],
        ...     'high': [100 + i*0.1 + 0.5 for i in range(60)],
        ...     'low': [100 + i*0.1 - 0.3 for i in range(60)],
        ...     'close': [100 + i*0.1 + 0.2 for i in range(60)],
        ...     'volume': [1000] * 60
        ... }).set_index('timestamp')
        >>> bars_1h = resample_bars(bars_1m, Timeframe.MIN_1, Timeframe.HOUR_1)
        >>> len(bars_1h)
        1
    """
    if not isinstance(bars.index, pd.DatetimeIndex):
        raise ValueError("Bars must have DatetimeIndex")

    required_cols = ["open", "high", "low", "close", "volume"]
    if not all(col in bars.columns for col in required_cols):
        raise ValueError(f"Bars must have columns: {required_cols}")

    # Check that we're upsampling (higher timeframe)
    from_seconds = from_timeframe.to_seconds()
    to_seconds = to_timeframe.to_seconds()

    if to_seconds < from_seconds:
        raise ValueError(
            f"Cannot resample from {from_timeframe} to {to_timeframe}. "
            "Can only resample to higher timeframes (e.g., 1m → 1h, not 1h → 1m)"
        )

    # Get pandas resample rule
    rule = to_timeframe.to_pandas_rule()

    # Resample and aggregate
    resampled = bars.resample(rule).apply(lambda group: pd.Series(aggregate_bars(group)))

    # Drop rows with no data
    resampled = resampled.dropna(subset=["open"])

    # Preserve symbol column if it exists
    if "symbol" in bars.columns:
        # Get the first symbol value for each resampled period
        symbols = bars["symbol"].resample(rule).first()
        resampled["symbol"] = symbols

    return resampled
