"""Decimal operations for financial calculations."""

from decimal import ROUND_HALF_UP, Decimal


def safe_decimal(value: float | int | str | Decimal) -> Decimal:
    """Convert value to Decimal safely.

    Args:
        value: Value to convert

    Returns:
        Decimal representation
    """
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def round_price(price: Decimal, decimals: int = 2) -> Decimal:
    """Round price to specified decimal places.

    Args:
        price: Price to round
        decimals: Number of decimal places (default: 2)

    Returns:
        Rounded price
    """
    quantizer = Decimal(10) ** -decimals
    return price.quantize(quantizer, rounding=ROUND_HALF_UP)
