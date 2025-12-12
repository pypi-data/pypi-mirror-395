"""Market metadata models."""

from dataclasses import dataclass
from enum import Enum


class AssetType(Enum):
    """Asset type classification (crypto-focused)."""

    CRYPTO = "crypto"
    DERIVATIVE = "derivative"
    OPTION = "option"


class Exchange(Enum):
    """Exchange identifiers (crypto-focused)."""

    BINANCE = "BINANCE"
    BYBIT = "BYBIT"
    OTHER = "OTHER"

@dataclass
class Symbol:
    """Symbol metadata.

    Attributes:
        ticker: Symbol ticker (e.g., "BTCUSDT", "ETHUSDT")
        exchange: Exchange where symbol is traded
        asset_type: Type of asset
        name: Full name of the security (optional)
    """

    ticker: str
    exchange: Exchange = Exchange.OTHER
    asset_type: AssetType = AssetType.CRYPTO
    name: str | None = None

    def __post_init__(self) -> None:
        """Validate and normalize ticker."""
        self.ticker = self.ticker.strip().upper()

    def __str__(self) -> str:
        """String representation."""
        return f"{self.ticker} ({self.exchange.value})"

    def __hash__(self) -> int:
        """Hash for use in sets/dicts."""
        return hash((self.ticker, self.exchange))
