"""Timezone handling utilities."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Common market timezones
US_EASTERN = ZoneInfo("America/New_York")
US_CENTRAL = ZoneInfo("America/Chicago")
LONDON = ZoneInfo("Europe/London")
TOKYO = ZoneInfo("Asia/Tokyo")
UTC = timezone.utc


def ensure_timezone(dt: datetime, tz: ZoneInfo | timezone = UTC) -> datetime:
    """Ensure datetime has timezone info.

    If datetime is naive, assume it's in the given timezone.
    If datetime already has timezone, return as-is.

    Args:
        dt: Input datetime
        tz: Timezone to assume if dt is naive (default: UTC)

    Returns:
        Timezone-aware datetime
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    return dt


def to_utc(dt: datetime) -> datetime:
    """Convert datetime to UTC.

    Args:
        dt: Input datetime (naive or aware)

    Returns:
        Datetime in UTC timezone
    """
    dt = ensure_timezone(dt)
    return dt.astimezone(UTC)


def to_timezone(dt: datetime, tz: ZoneInfo | timezone) -> datetime:
    """Convert datetime to specific timezone.

    Args:
        dt: Input datetime
        tz: Target timezone

    Returns:
        Datetime in target timezone
    """
    dt = ensure_timezone(dt)
    return dt.astimezone(tz)
