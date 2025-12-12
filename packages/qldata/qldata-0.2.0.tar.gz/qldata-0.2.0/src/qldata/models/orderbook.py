"""Order book data models."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class OrderBookLevel:
    """Single price level in an order book.

    Attributes:
        price: Price level
        quantity: Total quantity at this price level
    """

    price: Decimal
    quantity: Decimal

    def __post_init__(self) -> None:
        """Validate order book level."""
        if self.price <= 0:
            raise ValueError(f"Price must be positive, got {self.price}")
        if self.quantity < 0:
            raise ValueError(f"Quantity must be non-negative, got {self.quantity}")


@dataclass
class OrderBook:
    """Order book snapshot with bids and asks.

    Represents a point-in-time view of the order book.

    Attributes:
        symbol: Trading pair symbol
        timestamp: Time of snapshot
        bids: List of bid levels (sorted descending by price)
        asks: List of ask levels (sorted ascending by price)
        sequence: Sequence number for ordering updates (optional)
        source: Data source (e.g., "binance", "bybit")
    """

    symbol: str
    timestamp: datetime
    bids: list[OrderBookLevel]
    asks: list[OrderBookLevel]
    sequence: int | None = None
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate order book."""
        if not self.bids and not self.asks:
            raise ValueError("Order book must have at least one bid or ask")

        # Validate bid ordering (descending)
        for i in range(len(self.bids) - 1):
            if self.bids[i].price < self.bids[i + 1].price:
                raise ValueError("Bids must be sorted in descending order by price")

        # Validate ask ordering (ascending)
        for i in range(len(self.asks) - 1):
            if self.asks[i].price > self.asks[i + 1].price:
                raise ValueError("Asks must be sorted in ascending order by price")

    @property
    def best_bid(self) -> OrderBookLevel | None:
        """Get best (highest) bid price level."""
        return self.bids[0] if self.bids else None

    @property
    def best_ask(self) -> OrderBookLevel | None:
        """Get best (lowest) ask price level."""
        return self.asks[0] if self.asks else None

    @property
    def spread(self) -> Decimal | None:
        """Calculate bid-ask spread.

        Returns:
            Spread (ask - bid) if both sides exist, None otherwise
        """
        if self.best_bid and self.best_ask:
            return self.best_ask.price - self.best_bid.price
        return None

    @property
    def mid_price(self) -> Decimal | None:
        """Calculate mid price (average of best bid and ask).

        Returns:
            Mid price if both sides exist, None otherwise
        """
        if self.best_bid and self.best_ask:
            return (self.best_bid.price + self.best_ask.price) / 2
        return None

    def get_depth(self, side: str, depth: int) -> list[OrderBookLevel]:
        """Get top N levels from one side of the book.

        Args:
            side: "bid" or "ask"
            depth: Number of levels to return

        Returns:
            List of order book levels
        """
        if side.lower() == "bid":
            return self.bids[:depth]
        elif side.lower() == "ask":
            return self.asks[:depth]
        else:
            raise ValueError(f"Side must be 'bid' or 'ask', got {side}")

    def total_volume(self, side: str, depth: int | None = None) -> Decimal:
        """Calculate total volume on one side of the book.

        Args:
            side: "bid" or "ask"
            depth: Optional depth limit (all levels if None)

        Returns:
            Total volume
        """
        levels = self.get_depth(side, depth or len(self.bids if side == "bid" else self.asks))
        return sum((level.quantity for level in levels), Decimal("0"))

    def imbalance(self, depth: int | None = None) -> float:
        """Calculate order book imbalance.

        Imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)

        Args:
            depth: Optional depth limit

        Returns:
            Imbalance ratio (-1 to 1, positive = more bids)
        """
        bid_vol = float(self.total_volume("bid", depth))
        ask_vol = float(self.total_volume("ask", depth))

        total = bid_vol + ask_vol
        if total == 0:
            return 0.0

        return (bid_vol - ask_vol) / total
