"""Gap detection in time series data."""

from dataclasses import dataclass
from datetime import datetime, timedelta

import pandas as pd

from qldata.models.timeframe import Timeframe


@dataclass
class Gap:
    """Represents a gap in time series data."""

    start: datetime
    end: datetime
    expected_bars: int
    gap_type: str = "missing"  # "missing", "market_closed", "holiday"

    @property
    def duration(self) -> timedelta:
        """Get gap duration."""
        return self.end - self.start

    def __str__(self) -> str:
        """String representation."""
        return f"Gap({self.gap_type}): {self.start} to {self.end} ({self.expected_bars} bars)"


def detect_gaps(
    data: pd.DataFrame,
    timeframe: Timeframe,
    max_gap_bars: int = 5,
) -> list[Gap]:
    """Detect gaps in time series data.

    Args:
        data: DataFrame with DatetimeIndex
        timeframe: Expected data timeframe
        max_gap_bars: Maximum bars gap to report (default: 5)

    Returns:
        List of detected gaps

    Example:
        >>> data = pd.DataFrame({
        ...     'close': [100, 101, 102, 103]
        ... }, index=pd.date_range('2024-01-01', periods=4, freq='1h'))
        >>> # Remove middle bar to create gap
        >>> data_with_gap = data.drop(data.index[2])
        >>> gaps = detect_gaps(data_with_gap, Timeframe.HOUR_1)
        >>> len(gaps)
        1
    """
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data must have DatetimeIndex")

    if data.empty:
        return []

    gaps = []
    interval_seconds = timeframe.to_seconds()

    # Check gaps between consecutive timestamps
    for i in range(len(data) - 1):
        current_time = data.index[i]
        next_time = data.index[i + 1]

        time_diff = (next_time - current_time).total_seconds()

        # If gap is larger than expected interval
        if time_diff > interval_seconds * 1.5:  # Allow some tolerance
            missed_bars = int(time_diff / interval_seconds) - 1

            if missed_bars >= max_gap_bars:
                gap = Gap(
                    start=current_time, end=next_time, expected_bars=missed_bars, gap_type="missing"
                )
                gaps.append(gap)

    return gaps


def count_gaps(data: pd.DataFrame, timeframe: Timeframe) -> int:
    """Count number of gaps in data.

    Args:
        data: DataFrame with DatetimeIndex
        timeframe: Expected data timeframe

    Returns:
        Number of gaps detected
    """
    gaps = detect_gaps(data, timeframe, max_gap_bars=1)
    return len(gaps)


def has_gaps(data: pd.DataFrame, timeframe: Timeframe) -> bool:
    """Check if data has any gaps.

    Args:
        data: DataFrame with DatetimeIndex
        timeframe: Expected data timeframe

    Returns:
        True if gaps exist
    """
    return count_gaps(data, timeframe) > 0
