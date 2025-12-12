"""Bar (OHLCV) data model."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from qldata.validation.rules.ohlcv import OHLCVRules


@dataclass
class Bar:
    """OHLCV bar data model.

    Represents aggregated price/volume data over a time period.

    Attributes:
        timestamp: Bar start time
        symbol: Symbol ticker
        open: Opening price
        high: Highest price
        low: Lowest price
        close: Closing price
        volume: Total volume
    """

    timestamp: datetime
    symbol: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal

    def __post_init__(self) -> None:
        """Validate OHLC consistency."""
        rules = OHLCVRules()
        ok, errors = rules.validate_all(
            float(self.open), float(self.high), float(self.low), float(self.close)
        )
        if not ok:
            joined = "; ".join(errors)
            raise ValueError(joined)

        if self.volume < 0:
            raise ValueError(f"Volume must be non-negative, got {self.volume}")

    def range(self) -> Decimal:
        """Calculate price range (high - low).

        Returns:
            Price range
        """
        return self.high - self.low

    def body(self) -> Decimal:
        """Calculate body size (abs(close - open)).

        Returns:
            Absolute value of price change
        """
        return abs(self.close - self.open)

    def is_bullish(self) -> bool:
        """Check if bar is bullish (close > open).

        Returns:
            True if bullish, False otherwise
        """
        return self.close > self.open

    def is_bearish(self) -> bool:
        """Check if bar is bearish (close < open).

        Returns:
            True if bearish, False otherwise
        """
        return self.close < self.open
