"""Duplicate removal."""

import pandas as pd


def remove_duplicates(
    data: pd.DataFrame,
    keep: str = "last",
) -> pd.DataFrame:
    """Remove duplicate timestamps.

    Args:
        data: DataFrame with timestamp index
        keep: Which duplicate to keep ('first', 'last', or 'mean')

    Returns:
        DataFrame with duplicates removed

    Example:
        >>> data = pd.DataFrame({
        ...     'timestamp': ['2024-01-01', '2024-01-01', '2024-01-02'],
        ...     'close': [100, 101, 102]
        ... }).set_index('timestamp')
        >>> clean = remove_duplicates(data, keep='last')
        >>> len(clean)
        2
    """
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data must have DatetimeIndex")

    if keep == "mean":
        # Group by index and take mean
        return data.groupby(data.index).mean()
    elif keep in ("first", "last"):
        # Use pandas duplicated
        return data[~data.index.duplicated(keep=keep)]
    else:
        raise ValueError(f"Invalid keep value: {keep}. Use 'first', 'last', or 'mean'")
