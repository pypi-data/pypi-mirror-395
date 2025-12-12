"""Timeframe definitions and utilities."""

from enum import Enum


class Timeframe(Enum):
    """Standard timeframe definitions for market data.

    Supports common intervals from ticks to monthly bars.
    """

    TICK = "tick"
    SEC_1 = "1s"
    SEC_5 = "5s"
    SEC_15 = "15s"
    SEC_30 = "30s"
    MIN_1 = "1m"
    MIN_2 = "2m"
    MIN_3 = "3m"
    MIN_5 = "5m"
    MIN_15 = "15m"
    MIN_30 = "30m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"
    DAY_1 = "1d"
    DAY_3 = "3d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"

    @classmethod
    def from_string(cls, s: str) -> "Timeframe":
        """Parse string to Timeframe enum.

        Args:
            s: Timeframe string (e.g., "1h", "5m", "1d")

        Returns:
            Timeframe enum value

        Raises:
            ValueError: If timeframe string is not recognized
        """
        normalized = s.strip()
        for tf in cls:
            if tf.value.lower() == normalized.lower():
                return tf

        # Provide helpful error message with suggestions
        available = [tf.value for tf in cls if tf != cls.TICK]
        raise ValueError(
            f"Unknown timeframe: '{s}'. " f"Available intervals: {', '.join(available)}"
        )

    @classmethod
    def from_minutes(cls, minutes: int) -> "Timeframe":
        """Create timeframe from minutes.

        Args:
            minutes: Number of minutes (1, 2, 3, 5, 15, or 30)

        Returns:
            Timeframe enum

        Raises:
            ValueError: If minutes value not supported

        Examples:
            >>> Timeframe.from_minutes(5)
            Timeframe.MIN_5
        """
        mapping = {
            1: cls.MIN_1,
            2: cls.MIN_2,
            3: cls.MIN_3,
            5: cls.MIN_5,
            15: cls.MIN_15,
            30: cls.MIN_30,
        }

        if minutes not in mapping:
            raise ValueError(
                f"Unsupported minutes value: {minutes}. " f"Supported: {list(mapping.keys())}"
            )

        return mapping[minutes]

    @classmethod
    def from_hours(cls, hours: int) -> "Timeframe":
        """Create timeframe from hours.

        Args:
            hours: Number of hours (1, 2, 4, 6, 8, or 12)

        Returns:
            Timeframe enum

        Raises:
            ValueError: If hours value not supported

        Examples:
            >>> Timeframe.from_hours(4)
            Timeframe.HOUR_4
        """
        mapping = {
            1: cls.HOUR_1,
            2: cls.HOUR_2,
            4: cls.HOUR_4,
            6: cls.HOUR_6,
            8: cls.HOUR_8,
            12: cls.HOUR_12,
        }

        if hours not in mapping:
            raise ValueError(
                f"Unsupported hours value: {hours}. " f"Supported: {list(mapping.keys())}"
            )

        return mapping[hours]

    @classmethod
    def from_days(cls, days: int) -> "Timeframe":
        """Create timeframe from days.

        Args:
            days: Number of days (1 or 3)

        Returns:
            Timeframe enum

        Raises:
            ValueError: If days value not supported

        Examples:
            >>> Timeframe.from_days(1)
            Timeframe.DAY_1
        """
        mapping = {
            1: cls.DAY_1,
            3: cls.DAY_3,
        }

        if days not in mapping:
            raise ValueError(
                f"Unsupported days value: {days}. " f"Supported: {list(mapping.keys())}"
            )

        return mapping[days]

    # Convenience class properties
    @classmethod
    def minute(cls) -> "Timeframe":
        """1-minute timeframe."""
        return cls.MIN_1

    @classmethod
    def hour(cls) -> "Timeframe":
        """1-hour timeframe."""
        return cls.HOUR_1

    @classmethod
    def day(cls) -> "Timeframe":
        """Daily timeframe."""
        return cls.DAY_1

    @classmethod
    def week(cls) -> "Timeframe":
        """Weekly timeframe."""
        return cls.WEEK_1

    @classmethod
    def month(cls) -> "Timeframe":
        """Monthly timeframe."""
        return cls.MONTH_1

    def to_pandas_rule(self) -> str | None:
        """Convert to pandas resample rule.

        Returns:
            Pandas resample rule string (e.g., "1h", "5T", "1D"), or None for tick data
        """
        mapping = {
            "tick": None,
            "1s": "1S",
            "5s": "5S",
            "15s": "15S",
            "30s": "30S",
            "1m": "1T",
            "2m": "2T",
            "3m": "3T",
            "5m": "5T",
            "15m": "15T",
            "30m": "30T",
            "1h": "1h",
            "2h": "2h",
            "4h": "4h",
            "6h": "6h",
            "8h": "8h",
            "12h": "12h",
            "1d": "1D",
            "3d": "3D",
            "1w": "1W",
            "1M": "1M",
        }
        rule = mapping.get(self.value)
        if rule is None and self.value != "tick":
            raise ValueError(f"Cannot convert {self.value} to pandas rule")
        return rule

    def to_seconds(self) -> int:
        """Convert timeframe to duration in seconds.

        Returns:
            Duration in seconds for this timeframe.
            Returns 0 for TICK (no fixed interval).
            Monthly (1M) returns approximate 30-day value (2592000 seconds).

        Raises:
            ValueError: If timeframe cannot be converted to seconds.

        Examples:
            >>> Timeframe.HOUR_1.to_seconds()
            3600
            >>> Timeframe.DAY_1.to_seconds()
            86400
        """
        mapping = {
            "tick": 0,  # No fixed interval for raw tick data
            "1s": 1,
            "5s": 5,
            "15s": 15,
            "30s": 30,
            "1m": 60,
            "2m": 120,
            "3m": 180,
            "5m": 300,
            "15m": 900,
            "30m": 1800,
            "1h": 3600,
            "2h": 7200,
            "4h": 14400,
            "6h": 21600,
            "8h": 28800,
            "12h": 43200,
            "1d": 86400,
            "3d": 259200,
            "1w": 604800,
            "1M": 2592000,  # Approximate (30 days)
        }
        seconds = mapping.get(self.value)
        if seconds is None:
            raise ValueError(f"Cannot convert {self.value} to seconds")
        return seconds

    def __str__(self) -> str:
        """String representation."""
        return self.value
