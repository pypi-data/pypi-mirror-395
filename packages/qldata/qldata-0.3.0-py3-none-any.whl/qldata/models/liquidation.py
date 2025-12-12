"""Liquidation and insurance fund data models.

These models represent exchange liquidation events and
insurance fund data for market microstructure analysis.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal


@dataclass
class LiquidationEvent:
    """A liquidation event on an exchange.

    Represents a forced liquidation of a position, which can
    indicate market stress and potential price impact.

    Attributes:
        symbol: Trading pair symbol
        timestamp: Time of liquidation
        side: Liquidator's side (BUY = short liquidated, SELL = long liquidated)
        price: Liquidation price
        quantity: Liquidated quantity
        value_usd: Value in USD (if available)
        order_type: Order type used for liquidation
        source: Data source (e.g., "binance", "bybit")
    """

    symbol: str
    timestamp: datetime
    side: Literal["BUY", "SELL"]
    price: Decimal
    quantity: Decimal
    value_usd: Decimal | None = None
    order_type: str | None = None
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate liquidation event."""
        if self.price <= 0:
            raise ValueError(f"Price must be positive, got {self.price}")
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {self.quantity}")
        if self.value_usd is not None and self.value_usd < 0:
            raise ValueError(f"Value USD must be non-negative, got {self.value_usd}")

    @property
    def notional(self) -> Decimal:
        """Calculate notional value (price * quantity)."""
        return self.price * self.quantity

    @property
    def is_long_liquidation(self) -> bool:
        """Check if this was a long position liquidation.

        When a long is liquidated, the liquidation engine sells.
        """
        return self.side == "SELL"

    @property
    def is_short_liquidation(self) -> bool:
        """Check if this was a short position liquidation.

        When a short is liquidated, the liquidation engine buys.
        """
        return self.side == "BUY"


@dataclass
class InsuranceFund:
    """Exchange insurance fund balance.

    The insurance fund covers losses when liquidations cannot
    be executed at the bankruptcy price. Monitoring it can
    indicate exchange health and systemic risk.

    Attributes:
        timestamp: Time of measurement
        balance: Fund balance in base asset
        balance_usd: Fund balance in USD (if available)
        asset: Asset denomination (e.g., "BTC", "USDT")
        source: Data source
    """

    timestamp: datetime
    balance: Decimal
    balance_usd: Decimal | None = None
    asset: str = "USDT"
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate insurance fund data."""
        if self.balance < 0:
            raise ValueError(f"Balance must be non-negative, got {self.balance}")
        if self.balance_usd is not None and self.balance_usd < 0:
            raise ValueError(f"Balance USD must be non-negative, got {self.balance_usd}")


@dataclass
class LiquidationStats:
    """Aggregated liquidation statistics over a period.

    Useful for analyzing market stress and liquidation cascades.

    Attributes:
        symbol: Trading pair symbol (or "ALL" for aggregate)
        start_time: Period start
        end_time: Period end
        long_liquidations: Number of long liquidations
        short_liquidations: Number of short liquidations
        long_volume: Total long liquidation volume
        short_volume: Total short liquidation volume
        long_value_usd: Total long liquidation value in USD
        short_value_usd: Total short liquidation value in USD
        source: Data source
    """

    symbol: str
    start_time: datetime
    end_time: datetime
    long_liquidations: int = 0
    short_liquidations: int = 0
    long_volume: Decimal = Decimal("0")
    short_volume: Decimal = Decimal("0")
    long_value_usd: Decimal | None = None
    short_value_usd: Decimal | None = None
    source: str | None = None

    @property
    def total_liquidations(self) -> int:
        """Total number of liquidations."""
        return self.long_liquidations + self.short_liquidations

    @property
    def total_volume(self) -> Decimal:
        """Total liquidation volume."""
        return self.long_volume + self.short_volume

    @property
    def total_value_usd(self) -> Decimal | None:
        """Total liquidation value in USD."""
        if self.long_value_usd is None or self.short_value_usd is None:
            return None
        return self.long_value_usd + self.short_value_usd

    @property
    def long_short_ratio(self) -> float | None:
        """Ratio of long to short liquidations by volume.

        Returns:
            Ratio (>1 = more long liqs), None if no short volume
        """
        if self.short_volume == 0:
            return None
        return float(self.long_volume / self.short_volume)

    def add_event(self, event: LiquidationEvent) -> None:
        """Add a liquidation event to stats.

        Args:
            event: Liquidation event to add
        """
        if event.is_long_liquidation:
            self.long_liquidations += 1
            self.long_volume += event.quantity
            if event.value_usd is not None:
                if self.long_value_usd is None:
                    self.long_value_usd = Decimal("0")
                self.long_value_usd += event.value_usd
        else:
            self.short_liquidations += 1
            self.short_volume += event.quantity
            if event.value_usd is not None:
                if self.short_value_usd is None:
                    self.short_value_usd = Decimal("0")
                self.short_value_usd += event.value_usd
