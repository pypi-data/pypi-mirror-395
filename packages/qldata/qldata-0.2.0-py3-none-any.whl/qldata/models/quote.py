"""Quote (bid/ask) data model."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Quote:
    """Quote data model.

    Represents best bid/ask at a point in time.

    Attributes:
        timestamp: Time of quote
        symbol: Symbol ticker
        bid: Best bid price
        ask: Best ask price
        bid_size: Volume at bid (optional)
        ask_size: Volume at ask (optional)
    """

    timestamp: datetime
    symbol: str
    bid: Decimal
    ask: Decimal
    bid_size: Decimal | None = None
    ask_size: Decimal | None = None

    def __post_init__(self) -> None:
        """Validate quote data."""
        if self.bid <= 0:
            raise ValueError(f"Bid must be positive, got {self.bid}")

        if self.ask <= 0:
            raise ValueError(f"Ask must be positive, got {self.ask}")

        if self.bid > self.ask:
            raise ValueError(f"Bid ({self.bid}) cannot be greater than ask ({self.ask})")

        if self.bid_size is not None and self.bid_size < 0:
            raise ValueError(f"Bid size must be non-negative, got {self.bid_size}")

        if self.ask_size is not None and self.ask_size < 0:
            raise ValueError(f"Ask size must be non-negative, got {self.ask_size}")

    def spread(self) -> Decimal:
        """Calculate bid-ask spread.

        Returns:
            Spread (ask - bid)
        """
        return self.ask - self.bid

    def mid_price(self) -> Decimal:
        """Calculate mid price.

        Returns:
            Mid price ((bid + ask) / 2)
        """
        return (self.bid + self.ask) / 2

    def spread_bps(self) -> Decimal:
        """Calculate spread in basis points.

        Returns:
            Spread as basis points relative to mid price
        """
        mid = self.mid_price()
        if mid == 0:
            return Decimal(0)
        return (self.spread() / mid) * 10000
