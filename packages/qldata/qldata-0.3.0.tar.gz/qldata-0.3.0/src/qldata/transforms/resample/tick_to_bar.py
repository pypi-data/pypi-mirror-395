"""Tick to bar conversion."""

import pandas as pd

from qldata.models.timeframe import Timeframe
from qldata.transforms.resample.aggregations import aggregate_ohlcv


def ticks_to_bars(
    ticks: pd.DataFrame,
    timeframe: Timeframe,
    symbol: str | None = None,
) -> pd.DataFrame:
    """Convert tick data to bars.

    Args:
        ticks: DataFrame with tick data (indexed by timestamp, with 'price' and 'volume')
        timeframe: Target bar timeframe
        symbol: Optional symbol (if not in DataFrame)

    Returns:
        DataFrame with OHLCV bar data

    Example:
        >>> ticks = pd.DataFrame({
        ...     'timestamp': pd.date_range('2024-01-01', periods=1000, freq='1s'),
        ...     'price': [100 + i*0.01 for i in range(1000)],
        ...     'volume': [1000] * 1000
        ... }).set_index('timestamp')
        >>> bars = ticks_to_bars(ticks, Timeframe.MIN_1)
        >>> len(bars)
        17
    """
    if not isinstance(ticks.index, pd.DatetimeIndex):
        raise ValueError("Ticks must have DatetimeIndex")

    if "price" not in ticks.columns or "volume" not in ticks.columns:
        raise ValueError("Ticks must have 'price' and 'volume' columns")

    # Get pandas resample rule
    rule = timeframe.to_pandas_rule()

    # Resample and aggregate
    bars = ticks.resample(rule).apply(lambda group: pd.Series(aggregate_ohlcv(group)))

    # Drop rows with no data (NaN open)
    bars = bars.dropna(subset=["open"])

    # Add symbol if provided
    if symbol:
        bars["symbol"] = symbol

    return bars
