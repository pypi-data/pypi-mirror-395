"""Data validation utilities for financial time series."""

import pandas as pd

from qldata.common.dataframe.schema import DataFrameSchema
from qldata.common.dataframe.timestamps import TimestampOps


def detect_ohlcv_columns(data: pd.DataFrame) -> dict[str, str | None]:
    """Auto-detect OHLCV columns in DataFrame."""
    return DataFrameSchema.detect(data).to_dict()


def remove_invalid_prices(
    data: pd.DataFrame, price_columns: list[str] | None = None
) -> pd.DataFrame:
    """Remove rows with zero or negative prices.

    Args:
        data: DataFrame with price data
        price_columns: Columns to check (auto-detects OHLC if None)

    Returns:
        DataFrame with invalid prices removed

    Example:
        >>> df = pd.DataFrame({
        ...     'open': [100, 0, -5, 102],
        ...     'high': [101, 101, 104, 103],
        ...     'close': [100.5, 100, 103, 102.5]
        ... })
        >>> clean = remove_invalid_prices(df)
        >>> len(clean)
        2
    """
    if price_columns is None:
        schema = DataFrameSchema.detect(data)
        price_columns = schema.price_columns

    if not price_columns:
        return data

    # Create mask for valid prices (all must be > 0)
    valid_mask = pd.Series([True] * len(data), index=data.index)

    for col in price_columns:
        if col in data.columns:
            valid_mask &= data[col] > 0

    return data[valid_mask]


def validate_ohlc_relationships(data: pd.DataFrame) -> pd.DataFrame:
    """Validate OHLC relationships and remove invalid rows.

    Checks:
    - High >= Low
    - High >= Open
    - High >= Close
    - Low <= Open
    - Low <= Close

    Args:
        data: DataFrame with OHLC columns

    Returns:
        DataFrame with invalid OHLC relationships removed

    Example:
        >>> df = pd.DataFrame({
        ...     'open': [100, 100],
        ...     'high': [101, 95],  # Second row invalid (high < open)
        ...     'low': [99, 94],
        ...     'close': [100.5, 96]
        ... })
        >>> clean = validate_ohlc_relationships(df)
        >>> len(clean)
        1
    """
    schema = DataFrameSchema.detect(data)
    o_col = schema.open
    h_col = schema.high
    l_col = schema.low
    c_col = schema.close

    # Only validate if all OHLC columns exist
    if not all([o_col, h_col, l_col, c_col]):
        return data

    # Check all relationships
    valid_mask = (
        (data[h_col] >= data[l_col])  # High >= Low
        & (data[h_col] >= data[o_col])  # High >= Open
        & (data[h_col] >= data[c_col])  # High >= Close
        & (data[l_col] <= data[o_col])  # Low <= Open
        & (data[l_col] <= data[c_col])  # Low <= Close
    )

    return data[valid_mask]


def add_timestamp_sorting(data: pd.DataFrame) -> pd.DataFrame:
    """Sort DataFrame by timestamp index in ascending order.

    Args:
        data: DataFrame with DatetimeIndex

    Returns:
        Sorted DataFrame

    Example:
        >>> df = pd.DataFrame(
        ...     {'price': [102, 100, 101]},
        ...     index=pd.to_datetime(['2024-01-03', '2024-01-01', '2024-01-02'])
        ... )
        >>> sorted_df = add_timestamp_sorting(df)
        >>> sorted_df.index[0]
        Timestamp('2024-01-01 00:00:00')
    """
    return TimestampOps.sort_by_timestamp(data)


__all__ = [
    "detect_ohlcv_columns",
    "remove_invalid_prices",
    "validate_ohlc_relationships",
    "add_timestamp_sorting",
]
