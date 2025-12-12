"""Async I/O support for concurrent operations."""

import asyncio
from datetime import datetime
from typing import Any

import pandas as pd

from qldata.config import get_config
from qldata.models.timeframe import Timeframe


async def async_get_bars(
    symbol: str, start: datetime, end: datetime, timeframe: Timeframe, **kwargs: Any
) -> pd.DataFrame:
    """Async version of get_bars.

    Args:
        symbol: Symbol ticker
        start: Start datetime
        end: End datetime
        timeframe: Bar timeframe
        **kwargs: Additional parameters

    Returns:
        DataFrame with OHLCV data
    """
    config = get_config()
    source = config.get_default_source()

    # Run sync code in executor
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(
        None,
        source.get_bars,
        symbol,
        start,
        end,
        timeframe,
    )

    return data


async def async_read_multiple(
    symbols: list[str], start: datetime, end: datetime, timeframe: Timeframe, **kwargs: Any
) -> dict[str, pd.DataFrame]:
    """Read data for multiple symbols using async I/O.

    Args:
        symbols: List of symbol tickers
        start: Start datetime
        end: End datetime
        timeframe: Bar timeframe
        **kwargs: Additional parameters

    Returns:
        Dictionary mapping symbols to DataFrames

    Example:
        >>> import asyncio
        >>> from datetime import datetime
        >>> symbols = ["BTCUSDT", "ETHUSDT"]
        >>> data = asyncio.run(async_read_multiple(symbols, datetime(2024,1,1), datetime(2024,12,1), Timeframe.DAY_1))
    """
    tasks = [async_get_bars(symbol, start, end, timeframe, **kwargs) for symbol in symbols]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Build result dictionary
    output = {}
    for symbol, result in zip(symbols, results, strict=False):
        if isinstance(result, Exception):
            output[symbol] = pd.DataFrame()  # Empty on error
        else:
            output[symbol] = result

    return output
