"""Time parsing utilities."""

from datetime import datetime, timedelta, timezone
from typing import cast

import pandas as pd


def parse_datetime(value: str | datetime | pd.Timestamp) -> datetime:
    """Parse flexible datetime input.

    Handles:
    - ISO strings: "2024-01-01", "2024-01-01 09:30:00"
    - datetime objects
    - pandas Timestamps
    - Relative: "today", "yesterday", "-7d", "-3M"

    Args:
        value: Input to parse

    Returns:
        Parsed datetime object

    Raises:
        ValueError: If input cannot be parsed
    """
    if isinstance(value, datetime):
        return value

    if isinstance(value, pd.Timestamp):
        return cast(datetime, value.to_pydatetime())

    if isinstance(value, str):
        # Relative dates
        if value.lower() == "today":
            return datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        if value.lower() == "yesterday":
            return (datetime.now(timezone.utc) - timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

        # Relative offset: "-7d", "-3M", "-1y"
        if value.startswith("-"):
            return _parse_relative(value)

        # ISO-like string
        parsed = cast(pd.Timestamp, pd.to_datetime(value))
        if isinstance(parsed, pd.Timestamp):
            return datetime.fromtimestamp(parsed.timestamp())
        raise ValueError(f"Cannot parse datetime: {value}")

    raise ValueError(f"Cannot parse datetime: {value}")


def _parse_relative(value: str) -> datetime:
    """Parse relative date string like '-7d', '-3M', '-1y'.

    Args:
        value: Relative time string

    Returns:
        Datetime offset from now

    Raises:
        ValueError: If format is invalid
    """
    value = value.strip()
    if not value.startswith("-"):
        raise ValueError(f"Relative date must start with '-', got: {value}")

    # Parse number and unit
    number_str = value[1:-1]
    unit = value[-1].lower()

    try:
        number = int(number_str)
    except ValueError as e:
        raise ValueError(f"Invalid relative date format: {value}") from e

    now = datetime.now(timezone.utc)

    if unit == "d":
        return now - timedelta(days=number)
    elif unit == "w":
        return now - timedelta(weeks=number)
    elif unit == "m":
        # Approximate: 30 days per month
        return now - timedelta(days=number * 30)
    elif unit == "y":
        # Approximate: 365 days per year
        return now - timedelta(days=number * 365)
    else:
        raise ValueError(f"Invalid time unit: {unit}. Use d/w/m/y")
