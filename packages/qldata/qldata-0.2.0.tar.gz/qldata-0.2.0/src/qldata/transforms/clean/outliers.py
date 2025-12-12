"""Outlier detection and removal."""

from typing import Any

import pandas as pd


def detect_outliers_zscore(
    data: pd.DataFrame,
    column: str,
    threshold: float = 3.0,
) -> pd.Series:
    """Detect outliers using a robust z-score (median/MAD) method.

    Args:
        data: DataFrame with data
        column: Column to check for outliers
        threshold: Z-score threshold (default: 3.0)

    Returns:
        Boolean Series indicating outliers

    Example:
        >>> data = pd.DataFrame({'price': [100, 101, 102, 200, 103]})
        >>> outliers = detect_outliers_zscore(data, 'price', threshold=2.0)
        >>> outliers[3]
        True
    """
    if column not in data.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")

    values = data[column]
    median = values.median()
    mad = (values - median).abs().median()

    if mad == 0:
        return pd.Series([False] * len(data), index=data.index)

    # Modified z-score using MAD for robustness against extreme values
    z_scores = 0.6745 * (values - median).abs() / mad
    mask = z_scores > threshold
    return pd.Series(mask.tolist(), index=data.index, dtype=bool)


def detect_outliers_iqr(
    data: pd.DataFrame,
    column: str,
    multiplier: float = 1.5,
) -> pd.Series:
    """Detect outliers using IQR (Interquartile Range) method.

    Args:
        data: DataFrame with data
        column: Column to check for outliers
        multiplier: IQR multiplier (default: 1.5)

    Returns:
        Boolean Series indicating outliers

    Example:
        >>> data = pd.DataFrame({'price': [100, 101, 102, 200, 103]})
        >>> outliers = detect_outliers_iqr(data, 'price')
        >>> outliers[3]
        True
    """
    if column not in data.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")

    values = data[column]
    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    mask = (values < lower_bound) | (values > upper_bound)
    return pd.Series(mask.tolist(), index=data.index, dtype=bool)


def remove_outliers(
    data: pd.DataFrame, columns: list[str] | str | None = None, method: str = "iqr", **kwargs: Any
) -> pd.DataFrame:
    """Remove outliers from data.

    Args:
        data: DataFrame with data
        columns: Columns to check (default: auto-detect all numeric columns)
        method: Detection method ('zscore' or 'iqr')
        **kwargs: Additional arguments for detection method

    Returns:
        DataFrame with outliers removed

    Example:
        >>> data = pd.DataFrame({
        ...     'close': [100, 101, 102, 200, 103, 104],
        ...     'volume': [1000, 1100, 1050, 1200, 1150, 1080]
        ... })
        >>> clean = remove_outliers(data, columns='close', method='iqr')
        >>> len(clean)
        5
    """
    if columns is None:
        # Auto-detect all numeric columns
        numeric_cols = data.select_dtypes(include=["number"]).columns.tolist()
        columns = numeric_cols if numeric_cols else []
    elif isinstance(columns, str):
        columns = [columns]

    if not columns:
        return data

    # Detect outliers in each column
    outlier_mask = pd.Series([False] * len(data), index=data.index)

    for column in columns:
        if column not in data.columns:
            continue

        if method == "zscore":
            threshold = kwargs.get("threshold", 3.0)
            col_outliers = detect_outliers_zscore(data, column, threshold)
        elif method == "iqr":
            multiplier = kwargs.get("multiplier", 1.5)
            col_outliers = detect_outliers_iqr(data, column, multiplier)
        else:
            raise ValueError(f"Unknown method: {method}. Use 'zscore' or 'iqr'")

        outlier_mask |= col_outliers

    # Remove outliers
    return data[~outlier_mask]
