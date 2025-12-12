"""Public adapter API for exchange connectivity.

This module provides clean access to exchange adapters.

Example:
    >>> from qldata.adapters import BinanceAdapter, BybitAdapter
    >>> binance = BinanceAdapter(category="spot")
    >>> bybit = BybitAdapter(category="linear")
"""

from qldata.adapters.brokers.binance.adapter import BinanceAdapter
from qldata.adapters.brokers.bybit.adapter import BybitAdapter

__all__ = [
    "BinanceAdapter",
    "BybitAdapter",
]
