"""Mark price and index price models for derivatives.

These models represent the fair value prices used by exchanges
for margin calculations and liquidations.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class MarkPrice:
    """Mark price for a perpetual or futures contract.

    Mark price is the fair value price used by exchanges for:
    - Margin calculations
    - Liquidation triggers
    - Unrealized PnL

    It's typically derived from the index price plus a decaying
    funding basis to prevent manipulation.

    Attributes:
        symbol: Trading pair symbol
        timestamp: Time of price update
        mark_price: Current mark price
        index_price: Underlying index price (spot average)
        estimated_settle_price: Estimated settlement price (futures)
        funding_rate: Current funding rate (perpetuals)
        next_funding_time: Next funding timestamp
        source: Data source (e.g., "binance", "bybit")
    """

    symbol: str
    timestamp: datetime
    mark_price: Decimal
    index_price: Decimal | None = None
    estimated_settle_price: Decimal | None = None
    funding_rate: Decimal | None = None
    next_funding_time: datetime | None = None
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate mark price data."""
        if self.mark_price <= 0:
            raise ValueError(f"Mark price must be positive, got {self.mark_price}")
        if self.index_price is not None and self.index_price <= 0:
            raise ValueError(f"Index price must be positive, got {self.index_price}")

    @property
    def premium(self) -> Decimal | None:
        """Calculate premium (mark - index).

        Returns:
            Premium in quote currency, or None if no index price
        """
        if self.index_price is None:
            return None
        return self.mark_price - self.index_price

    @property
    def premium_percent(self) -> Decimal | None:
        """Calculate premium as percentage of index.

        Returns:
            Premium percentage, or None if no index price
        """
        if self.index_price is None or self.index_price == 0:
            return None
        return (self.mark_price - self.index_price) / self.index_price * Decimal("100")

    @property
    def basis_bps(self) -> Decimal | None:
        """Calculate basis in basis points.

        Returns:
            Basis in bps (1 bps = 0.01%), or None if no index price
        """
        if self.index_price is None or self.index_price == 0:
            return None
        return (self.mark_price - self.index_price) / self.index_price * Decimal("10000")


@dataclass
class PremiumIndex:
    """Premium index for basis trading analysis.

    Tracks the premium between perpetual/futures and spot,
    useful for basis trading and funding rate prediction.

    Attributes:
        symbol: Trading pair symbol
        timestamp: Time of measurement
        premium: Mark price - Index price
        premium_percent: Premium as percentage
        basis_rate: Annualized basis rate
        funding_rate: Current funding rate
        source: Data source
    """

    symbol: str
    timestamp: datetime
    premium: Decimal
    premium_percent: Decimal
    basis_rate: Decimal | None = None
    funding_rate: Decimal | None = None
    source: str | None = None

    @property
    def annualized_basis_percent(self) -> Decimal | None:
        """Get annualized basis as percentage.

        Returns:
            Annualized basis percentage
        """
        if self.basis_rate is None:
            return None
        return self.basis_rate * Decimal("100")

    @classmethod
    def from_mark_price(
        cls,
        mark: MarkPrice,
        annualize_days: int = 365,
        funding_interval_hours: int = 8,
    ) -> "PremiumIndex | None":
        """Create PremiumIndex from MarkPrice.

        Args:
            mark: MarkPrice instance
            annualize_days: Days to annualize funding
            funding_interval_hours: Hours between funding

        Returns:
            PremiumIndex or None if insufficient data
        """
        if mark.index_price is None:
            return None

        premium = mark.mark_price - mark.index_price
        premium_pct = premium / mark.index_price * Decimal("100")

        # Annualize funding rate if available
        basis_rate = None
        if mark.funding_rate is not None:
            # funding per interval -> annual
            intervals_per_year = Decimal(str(annualize_days * 24 / funding_interval_hours))
            basis_rate = mark.funding_rate * intervals_per_year

        return cls(
            symbol=mark.symbol,
            timestamp=mark.timestamp,
            premium=premium,
            premium_percent=premium_pct,
            basis_rate=basis_rate,
            funding_rate=mark.funding_rate,
            source=mark.source,
        )


@dataclass
class IndexPrice:
    """Spot index price aggregated from multiple exchanges.

    Represents the fair spot price calculated from a weighted
    average of prices across multiple exchanges.

    Attributes:
        symbol: Base asset symbol (e.g., "BTC")
        timestamp: Time of measurement
        price: Aggregated index price
        components: Individual exchange prices (optional)
        source: Data source
    """

    symbol: str
    timestamp: datetime
    price: Decimal
    components: dict[str, Decimal] | None = None
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate index price."""
        if self.price <= 0:
            raise ValueError(f"Index price must be positive, got {self.price}")

    def get_deviation(self, exchange: str) -> Decimal | None:
        """Get deviation of an exchange price from the index.

        Args:
            exchange: Exchange name

        Returns:
            Deviation as ratio, or None if exchange not in components
        """
        if self.components is None or exchange not in self.components:
            return None
        return (self.components[exchange] - self.price) / self.price
