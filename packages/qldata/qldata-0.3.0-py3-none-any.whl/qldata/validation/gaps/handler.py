"""Gap handling strategies."""

import pandas as pd

from qldata.models.timeframe import Timeframe
from qldata.validation.gaps.detector import detect_gaps


def fill_gaps(
    data: pd.DataFrame,
    timeframe: Timeframe,
    method: str = "forward",
) -> pd.DataFrame:
    """Fill gaps in time series data.

    Args:
        data: DataFrame with DatetimeIndex
        timeframe: Data timeframe
        method: Fill method ('forward', 'backward', 'interpolate', 'zero')

    Returns:
        DataFrame with gaps filled

    Example:
        >>> data = pd.DataFrame({
        ...     'close': [100, 101, 103]
        ... }, index=pd.to_datetime(['2024-01-01 09:00', '2024-01-01 10:00', '2024-01-01 12:00']))
        >>> filled = fill_gaps(data, Timeframe.HOUR_1, method='forward')
        >>> len(filled)
        3
    """
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data must have DatetimeIndex")

    if data.empty:
        return data

    # Create complete time range
    start = data.index[0]
    end = data.index[-1]
    freq = timeframe.to_pandas_rule()

    complete_index = pd.date_range(start=start, end=end, freq=freq)

    # Reindex to complete range
    reindexed = data.reindex(complete_index)

    # Fill based on method
    if method == "forward":
        filled = reindexed.ffill()
    elif method == "backward":
        filled = reindexed.bfill()
    elif method == "interpolate":
        filled = reindexed.interpolate(method="linear")
    elif method == "zero":
        filled = reindexed.fillna(0)
    else:
        raise ValueError(f"Unknown fill method: {method}")

    return filled


def remove_gaps(
    data: pd.DataFrame,
    timeframe: Timeframe,
    max_gap_bars: int = 5,
) -> pd.DataFrame:
    """Remove sections with large gaps.

    Useful for removing entire sections of missing data.

    Args:
        data: DataFrame with DatetimeIndex
        timeframe: Data timeframe
        max_gap_bars: Maximum gap size to keep (default: 5)

    Returns:
        DataFrame with gap sections removed
    """
    gaps = detect_gaps(data, timeframe, max_gap_bars=max_gap_bars)

    if not gaps:
        return data

    # Remove data around large gaps
    result = data.copy()

    for gap in gaps:
        # Remove the bars immediately before and after large gaps
        # This helps ensure clean continuous data
        mask = (result.index >= gap.start) & (result.index <= gap.end)
        result = result[~mask]

    return result
