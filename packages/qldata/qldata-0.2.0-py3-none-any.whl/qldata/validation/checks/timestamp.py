"""Timestamp validation checks."""

from datetime import datetime, timezone

import pandas as pd

from qldata.validation.core import Severity, ValidationReport


def check_chronological_order(
    data: pd.DataFrame,
    report: ValidationReport,
) -> pd.DataFrame:
    """Check if timestamps are in chronological order.

    Args:
        data: DataFrame with DatetimeIndex
        report: ValidationReport to add issues to

    Returns:
        DataFrame sorted by timestamp
    """
    if not isinstance(data.index, pd.DatetimeIndex):
        report.add_issue(
            Severity.ERROR,
            "chronological_order",
            "Data does not have DatetimeIndex",
        )
        return data

    # Check if sorted
    is_sorted = data.index.is_monotonic_increasing

    if not is_sorted:
        report.add_issue(
            Severity.WARNING,
            "chronological_order",
            "Timestamps are not in chronological order",
            suggestion="Sorting data by timestamp",
        )
        return data.sort_index()

    return data


def check_future_dates(
    data: pd.DataFrame,
    report: ValidationReport,
) -> pd.DataFrame:
    """Check for future timestamps.

    Args:
        data: DataFrame with DatetimeIndex
        report: ValidationReport to add issues to

    Returns:
        DataFrame with future dates removed
    """
    if not isinstance(data.index, pd.DatetimeIndex):
        return data

    now = datetime.now(timezone.utc)
    future_dates = data.index > pd.Timestamp(now)

    if future_dates.any():
        count = future_dates.sum()
        report.add_issue(
            Severity.ERROR,
            "future_dates",
            f"{count} timestamps in the future",
            suggestion="Remove or check data source clock",
        )
        return data[~future_dates]

    return data


def check_duplicates(
    data: pd.DataFrame,
    report: ValidationReport,
) -> pd.DataFrame:
    """Check for duplicate timestamps.

    Args:
        data: DataFrame with DatetimeIndex
        report: ValidationReport to add issues to

    Returns:
        DataFrame with duplicates removed (keeping last)
    """
    if not isinstance(data.index, pd.DatetimeIndex):
        return data

    has_dupes = data.index.duplicated().any()

    if has_dupes:
        count = data.index.duplicated().sum()
        report.add_issue(
            Severity.WARNING,
            "duplicate_timestamps",
            f"{count} duplicate timestamps found",
            suggestion="Keeping last occurrence",
        )
        return data[~data.index.duplicated(keep="last")]

    return data
