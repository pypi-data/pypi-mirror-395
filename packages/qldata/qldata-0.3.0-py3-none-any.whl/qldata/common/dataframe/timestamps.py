"""Shared timestamp operations for DataFrames."""

from datetime import datetime

import pandas as pd


class TimestampOps:
    """Centralized helpers for timestamp handling on DataFrames."""

    @staticmethod
    def ensure_datetime_index(df: pd.DataFrame, column: str | None = None) -> pd.DataFrame:
        """Ensure the DataFrame has a DatetimeIndex, setting from a column if provided."""
        if isinstance(df.index, pd.DatetimeIndex):
            return df

        target_column = column or ("timestamp" if "timestamp" in df.columns else None)
        if target_column and target_column in df.columns:
            df = df.set_index(target_column)
        else:
            raise ValueError("Cannot create DatetimeIndex: no timestamp column found")

        df.index = pd.to_datetime(df.index)
        return df

    @staticmethod
    def validate_datetime_index(df: pd.DataFrame) -> None:
        """Validate that a DataFrame uses a DatetimeIndex."""
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame must have DatetimeIndex")

    @staticmethod
    def sort_by_timestamp(df: pd.DataFrame) -> pd.DataFrame:
        """Return DataFrame sorted by timestamp."""
        TimestampOps.validate_datetime_index(df)
        return df.sort_index()

    @staticmethod
    def filter_date_range(df: pd.DataFrame, start: datetime, end: datetime) -> pd.DataFrame:
        """Filter to a closed date range."""
        TimestampOps.validate_datetime_index(df)
        idx = df.index

        # Align tz-awareness between index and boundaries to avoid pandas comparison errors
        if idx.tz is None:
            if start.tzinfo is not None:
                start = start.replace(tzinfo=None)
            if end.tzinfo is not None:
                end = end.replace(tzinfo=None)
        else:
            tz = idx.tz
            start = start.replace(tzinfo=tz) if start.tzinfo is None else start.astimezone(tz)
            end = end.replace(tzinfo=tz) if end.tzinfo is None else end.astimezone(tz)

        return df[(idx >= start) & (idx <= end)]

    @staticmethod
    def remove_duplicate_timestamps(df: pd.DataFrame, keep: str = "last") -> pd.DataFrame:
        """Remove duplicate timestamps, keeping the specified occurrence."""
        TimestampOps.validate_datetime_index(df)
        return df[~df.index.duplicated(keep=keep)]


__all__ = ["TimestampOps"]
