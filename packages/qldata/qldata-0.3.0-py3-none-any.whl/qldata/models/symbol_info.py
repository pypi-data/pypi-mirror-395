"""Symbol metadata and reference data models."""

from dataclasses import dataclass, field
from datetime import time
from decimal import Decimal


@dataclass
class TradingHours:
    """Trading hours for a symbol.

    Attributes:
        open_time: Market open time (UTC)
        close_time: Market close time (UTC)
        timezone: Timezone identifier
        is_24_7: Whether trading is 24/7
    """

    open_time: time | None = None
    close_time: time | None = None
    timezone: str = "UTC"
    is_24_7: bool = True


@dataclass
class SymbolFilters:
    """Price and quantity filters for a trading symbol.

    Attributes:
        price_filter: Min/max price, tick size
        quantity_filter: Min/max quantity, step size
        notional_filter: Min/max notional value
        max_num_orders: Maximum number of open orders
        max_algo_orders: Maximum algorithmic orders
    """

    # Price constraints
    min_price: Decimal | None = None
    max_price: Decimal | None = None
    tick_size: Decimal | None = None

    # Quantity constraints
    min_quantity: Decimal | None = None
    max_quantity: Decimal | None = None
    step_size: Decimal | None = None

    # Notional constraints
    min_notional: Decimal | None = None
    max_notional: Decimal | None = None

    # Order limits
    max_num_orders: int | None = None
    max_algo_orders: int | None = None


@dataclass
class SymbolInfo:
    """Complete symbol metadata and trading specifications.

    Attributes:
        symbol: Trading pair symbol
        base_asset: Base currency (e.g., "BTC" in "BTCUSDT")
        quote_asset: Quote currency (e.g., "USDT" in "BTCUSDT")
        status: Trading status ("TRADING", "HALT", "BREAK", etc.)
        filters: Price/quantity filters
        trading_hours: Market hours
        contract_type: For futures ("PERPETUAL", "CURRENT_QUARTER", etc.)
        delivery_date: For futures contracts
        margin_asset: Asset used for margin
        fee_tier: Fee tier or maker/taker fees
        source: Data source
    """

    symbol: str
    base_asset: str
    quote_asset: str
    status: str = "TRADING"

    # Trading constraints
    filters: SymbolFilters = field(default_factory=SymbolFilters)
    trading_hours: TradingHours = field(default_factory=TradingHours)

    # Contract details (for futures/perpetuals)
    contract_type: str | None = None
    delivery_date: str | None = None
    margin_asset: str | None = None

    # Fee structure
    maker_fee: Decimal | None = None
    taker_fee: Decimal | None = None
    fee_tier: str | None = None

    # Metadata
    source: str | None = None
    last_updated: str | None = None

    @property
    def is_spot(self) -> bool:
        """Check if this is a spot market."""
        return self.contract_type is None

    @property
    def is_perpetual(self) -> bool:
        """Check if this is a perpetual contract."""
        return self.contract_type == "PERPETUAL"

    @property
    def is_futures(self) -> bool:
        """Check if this is a dated futures contract."""
        return self.contract_type is not None and not self.is_perpetual

    @property
    def is_active(self) -> bool:
        """Check if symbol is actively trading."""
        return self.status == "TRADING"

    def validate_price(self, price: Decimal) -> bool:
        """Check if price meets filter requirements.

        Args:
            price: Price to validate

        Returns:
            True if valid, False otherwise
        """
        if self.filters.min_price and price < self.filters.min_price:
            return False
        if self.filters.max_price and price > self.filters.max_price:
            return False
        if self.filters.tick_size:
            # Check if price is multiple of tick size
            remainder = price % self.filters.tick_size
            if remainder != 0:
                return False
        return True

    def validate_quantity(self, quantity: Decimal) -> bool:
        """Check if quantity meets filter requirements.

        Args:
            quantity: Quantity to validate

        Returns:
            True if valid, False otherwise
        """
        if self.filters.min_quantity and quantity < self.filters.min_quantity:
            return False
        if self.filters.max_quantity and quantity > self.filters.max_quantity:
            return False
        if self.filters.step_size:
            # Check if quantity is multiple of step size
            remainder = quantity % self.filters.step_size
            if remainder != 0:
                return False
        return True

    def validate_notional(self, price: Decimal, quantity: Decimal) -> bool:
        """Check if notional value (price * quantity) meets requirements.

        Args:
            price: Order price
            quantity: Order quantity

        Returns:
            True if valid, False otherwise
        """
        notional = price * quantity

        if self.filters.min_notional and notional < self.filters.min_notional:
            return False
        return not (self.filters.max_notional and notional > self.filters.max_notional)


@dataclass
class ExchangeInfo:
    """Exchange-wide information and status.

    Attributes:
        exchange: Exchange name
        timezone: Exchange timezone
        server_time: Current server time
        rate_limits: API rate limits
        symbols: List of available symbols
        status: Exchange status
    """

    exchange: str
    timezone: str = "UTC"
    server_time: str | None = None
    status: str = "OPERATIONAL"

    # Rate limiting info
    rate_limits: dict[str, int] = field(default_factory=dict)

    # Available symbols
    symbols: list[str] = field(default_factory=list)
    symbol_count: int = 0
