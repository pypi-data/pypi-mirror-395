"""Funding rate and open interest models for perpetual contracts."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class FundingRate:
    """Funding rate for a perpetual contract.

    Attributes:
        symbol: Trading pair symbol
        timestamp: Time of funding rate
        rate: Funding rate (as decimal, e.g., 0.0001 = 0.01%)
        next_funding_time: When next funding will occur
        mark_price: Mark price at funding time
        source: Data source
    """

    symbol: str
    timestamp: datetime
    rate: Decimal
    next_funding_time: datetime | None = None
    mark_price: Decimal | None = None
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate funding rate."""
        # Funding rates typically range from -0.75% to +0.75%
        if abs(self.rate) > Decimal("0.0075"):
            # Warning but don't fail - extreme rates can happen
            pass

    @property
    def rate_bps(self) -> Decimal:
        """Get funding rate in basis points (1 bps = 0.01%)."""
        return self.rate * Decimal("10000")

    @property
    def rate_percent(self) -> Decimal:
        """Get funding rate as percentage."""
        return self.rate * Decimal("100")


@dataclass
class OpenInterest:
    """Open interest for a perpetual or futures contract.

    Attributes:
        symbol: Trading pair symbol
        timestamp: Time of measurement
        value: Open interest value
        value_usd: Open interest in USD (if available)
        unit: Unit of measurement ("contracts", "USD", "base_currency")
        source: Data source
    """

    symbol: str
    timestamp: datetime
    value: Decimal
    value_usd: Decimal | None = None
    unit: str = "contracts"
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate open interest."""
        if self.value < 0:
            raise ValueError(f"Open interest must be non-negative, got {self.value}")

        if self.value_usd is not None and self.value_usd < 0:
            raise ValueError(f"OI in USD must be non-negative, got {self.value_usd}")
