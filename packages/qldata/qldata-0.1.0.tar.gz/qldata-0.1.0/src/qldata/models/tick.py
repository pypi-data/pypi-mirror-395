"""Tick data model."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Tick:
    """Tick (trade) data model.

    Represents a single market trade.

    Attributes:
        timestamp: Time of trade
        symbol: Symbol ticker
        price: Trade price
        volume: Trade volume
        bid: Best bid price (optional)
        ask: Best ask price (optional)
    """

    timestamp: datetime
    symbol: str
    price: Decimal
    volume: Decimal
    bid: Decimal | None = None
    ask: Decimal | None = None

    def __post_init__(self) -> None:
        """Validate tick data."""
        if self.price <= 0:
            raise ValueError(f"Price must be positive, got {self.price}")

        if self.volume < 0:
            raise ValueError(f"Volume must be non-negative, got {self.volume}")

        if self.bid is not None and self.bid <= 0:
            raise ValueError(f"Bid must be positive, got {self.bid}")

        if self.ask is not None and self.ask <= 0:
            raise ValueError(f"Ask must be positive, got {self.ask}")

        if self.bid is not None and self.ask is not None and self.bid > self.ask:
            raise ValueError(f"Bid ({self.bid}) cannot be greater than ask ({self.ask})")

    def spread(self) -> Decimal | None:
        """Calculate bid-ask spread.

        Returns:
            Spread if both bid and ask are available, None otherwise
        """
        if self.bid is not None and self.ask is not None:
            return self.ask - self.bid
        return None

    def mid_price(self) -> Decimal | None:
        """Calculate mid price (average of bid and ask).

        Returns:
            Mid price if both bid and ask are available, None otherwise
        """
        if self.bid is not None and self.ask is not None:
            return (self.bid + self.ask) / 2
        return None
