"""Gap filling strategies."""

import pandas as pd


def fill_forward(data: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Forward fill missing values.

    Args:
        data: DataFrame with data
        columns: Columns to fill (default: all columns)

    Returns:
        DataFrame with gaps filled
    """
    if columns is None:
        return data.ffill()
    return data.copy().assign(**{col: data[col].ffill() for col in columns if col in data.columns})


def fill_backward(data: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Backward fill missing values.

    Args:
        data: DataFrame with data
        columns: Columns to fill (default: all columns)

    Returns:
        DataFrame with gaps filled
    """
    if columns is None:
        return data.bfill()
    return data.copy().assign(**{col: data[col].bfill() for col in columns if col in data.columns})


def fill_interpolate(
    data: pd.DataFrame,
    columns: list[str] | None = None,
    method: str = "linear",
) -> pd.DataFrame:
    """Interpolate missing values.

    Args:
        data: DataFrame with data
        columns: Columns to fill (default: numeric columns)
        method: Interpolation method (default: 'linear')

    Returns:
        DataFrame with gaps filled
    """
    if columns is None:
        return data.interpolate(method=method)

    result = data.copy()
    for col in columns:
        if col in data.columns:
            result[col] = data[col].interpolate(method=method)

    return result
