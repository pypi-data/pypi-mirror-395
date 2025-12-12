"""Reference data API for symbol metadata and exchange information."""

from decimal import Decimal
from typing import Any

from qldata.api.queries.helpers import _get_adapter
from qldata.models.symbol_info import ExchangeInfo, SymbolFilters, SymbolInfo, TradingHours


def get_symbol_info(symbol: str, source: str, category: str | None = None) -> SymbolInfo:
    """Get complete symbol metadata and trading specifications.

    Args:
        symbol: Trading pair symbol (e.g., "BTCUSDT")
        source: Exchange ("binance", "bybit")
        category: Market category (spot, usdm, linear, etc.)

    Returns:
        SymbolInfo with complete trading specifications

    Examples:
        >>> info = get_symbol_info("BTCUSDT", source="binance", category="spot")
        >>> print(info.filters.tick_size, info.filters.min_notional)
        >>> if info.validate_price(Decimal("50000.5")):
        ...     print("Price is valid")
    """
    adapter = _get_adapter(source, category)

    # Get symbol info from adapter
    exchange_info = adapter.get_exchange_info()

    # Find the specific symbol
    symbols_data = exchange_info.get("symbols", [])
    symbol_data = None

    for s in symbols_data:
        if s.get("symbol") == symbol:
            symbol_data = s
            break

    if not symbol_data:
        raise ValueError(f"Symbol {symbol} not found on {source} {category}")

    # Parse symbol data into SymbolInfo
    return _parse_symbol_info(symbol_data, source)


def get_exchange_info(source: str, category: str | None = None) -> ExchangeInfo:
    """Get exchange-wide information and available symbols.

    Args:
        source: Exchange ("binance", "bybit")
        category: Market category (optional)

    Returns:
        ExchangeInfo with exchange metadata

    Examples:
        >>> info = get_exchange_info(source="binance")
        >>> print(f"Exchange: {info.exchange}, Symbols: {info.symbol_count}")
    """
    adapter = _get_adapter(source, category)
    exchange_data = adapter.get_exchange_info()

    symbols = [s.get("symbol") for s in exchange_data.get("symbols", [])]

    return ExchangeInfo(
        exchange=source,
        timezone=exchange_data.get("timezone", "UTC"),
        server_time=exchange_data.get("serverTime"),
        status="OPERATIONAL",  # Could parse from exchange response
        symbols=symbols,
        symbol_count=len(symbols),
    )


def list_symbols(
    source: str,
    category: str | None = None,
    active_only: bool = True,
    base_asset: str | None = None,
    quote_asset: str | None = None,
) -> list[str]:
    """List all available trading symbols on an exchange.

    Args:
        source: Exchange ("binance", "bybit")
        category: Market category (optional)
        active_only: Only return actively trading symbols
        base_asset: Filter by base asset (e.g., "BTC")
        quote_asset: Filter by quote asset (e.g., "USDT")

    Returns:
        List of symbol names

    Examples:
        >>> # Get all USDT pairs
        >>> symbols = list_symbols(source="binance", category="spot", quote_asset="USDT")
        >>> print(len(symbols), "USDT pairs")

        >>> # Get all BTC pairs that are actively trading
        >>> btc_pairs = list_symbols(source="binance", category="spot",  base_asset="BTC", active_only=True)
    """
    adapter = _get_adapter(source, category)
    exchange_data = adapter.get_exchange_info()

    symbols = []
    for s in exchange_data.get("symbols", []):
        symbol_name = s.get("symbol")
        status = s.get("status", "TRADING")

        # Filter by status
        if active_only and status != "TRADING":
            continue

        # Filter by base asset
        if base_asset and s.get("baseAsset") != base_asset:
            continue

        # Filter by quote asset
        if quote_asset and s.get("quoteAsset") != quote_asset:
            continue

        symbols.append(symbol_name)

    return symbols


def _parse_symbol_info(symbol_data: dict[str, Any], source: str) -> SymbolInfo:
    """Parse exchange-specific symbol data into SymbolInfo model.

    Args:
        symbol_data: Raw symbol data from exchange
        source: Exchange name

    Returns:
        Parsed SymbolInfo
    """
    # Extract basic info
    symbol = symbol_data.get("symbol", "")
    base_asset = symbol_data.get("baseAsset", "")
    quote_asset = symbol_data.get("quoteAsset", "")
    status = symbol_data.get("status", "TRADING")

    # Parse filters
    filters = SymbolFilters()
    for f in symbol_data.get("filters", []):
        filter_type = f.get("filterType")

        if filter_type == "PRICE_FILTER":
            filters.min_price = Decimal(f.get("minPrice", "0")) if f.get("minPrice") else None
            filters.max_price = Decimal(f.get("maxPrice", "0")) if f.get("maxPrice") else None
            filters.tick_size = Decimal(f.get("tickSize", "0")) if f.get("tickSize") else None

        elif filter_type == "LOT_SIZE":
            filters.min_quantity = Decimal(f.get("minQty", "0")) if f.get("minQty") else None
            filters.max_quantity = Decimal(f.get("maxQty", "0")) if f.get("maxQty") else None
            filters.step_size = Decimal(f.get("stepSize", "0")) if f.get("stepSize") else None

        elif filter_type in ("MIN_NOTIONAL", "NOTIONAL"):
            filters.min_notional = (
                Decimal(f.get("minNotional", "0")) if f.get("minNotional") else None
            )
            filters.max_notional = (
                Decimal(f.get("maxNotional", "0")) if f.get("maxNotional") else None
            )

        elif filter_type == "MAX_NUM_ORDERS":
            filters.max_num_orders = int(f.get("maxNumOrders", 0))

        elif filter_type == "MAX_NUM_ALGO_ORDERS":
            filters.max_algo_orders = int(f.get("maxNumAlgoOrders", 0))

    # Contract details (for futures/perpetuals)
    contract_type = symbol_data.get("contractType")
    delivery_date = symbol_data.get("deliveryDate")
    margin_asset = symbol_data.get("marginAsset")

    # Trading hours (assume 24/7 for crypto)
    trading_hours = TradingHours(is_24_7=True)

    return SymbolInfo(
        symbol=symbol,
        base_asset=base_asset,
        quote_asset=quote_asset,
        status=status,
        filters=filters,
        trading_hours=trading_hours,
        contract_type=contract_type,
        delivery_date=delivery_date,
        margin_asset=margin_asset,
        source=source,
    )


__all__ = [
    "get_symbol_info",
    "get_exchange_info",
    "list_symbols",
]
