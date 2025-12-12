"""Parallel data reading using threading."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any

import pandas as pd

from qldata.config import get_config
from qldata.logging import get_logger
from qldata.models.timeframe import Timeframe

logger = get_logger(__name__)


def parallel_read(
    symbols: list[str],
    start: datetime,
    end: datetime,
    timeframe: Timeframe,
    workers: int = 4,
    **kwargs: Any,
) -> dict[str, pd.DataFrame]:
    """Read data for multiple symbols in parallel using threads.

    Args:
        symbols: List of symbol tickers
        start: Start datetime
        end: End datetime
        timeframe: Bar timeframe
        workers: Number of worker threads (default: 4)
        **kwargs: Additional source parameters

    Returns:
        Dictionary mapping symbols to DataFrames

    Example:
        >>> from datetime import datetime
        >>> symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
        >>> data = parallel_read(symbols, datetime(2024,1,1), datetime(2024,12,1), Timeframe.DAY_1)
        >>> len(data)
        3
    """
    config = get_config()
    source = config.get_default_source()

    results = {}

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all tasks
        future_to_symbol = {
            executor.submit(source.get_bars, symbol, start, end, timeframe, **kwargs): symbol
            for symbol in symbols
        }

        # Gather results as they complete
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                data = future.result()
                results[symbol] = data
                logger.debug(f"Loaded {len(data)} bars for {symbol}")
            except Exception as e:
                logger.error(f"Error loading {symbol}: {e}")
                results[symbol] = pd.DataFrame()  # Empty DataFrame on error

    return results


def parallel_write(
    data: dict[str, pd.DataFrame],
    timeframe: Timeframe,
    workers: int = 4,
) -> None:
    """Write data for multiple symbols in parallel.

    Args:
        data: Dictionary mapping symbols to DataFrames
        timeframe: Bar timeframe
        workers: Number of worker threads (default: 4)
    """
    config = get_config()
    store = config.get_default_store()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []

        for symbol, df in data.items():
            future = executor.submit(store.write_bars, symbol, df, timeframe)
            futures.append((future, symbol))

        # Wait for all writes to complete
        for future, symbol in futures:
            try:
                future.result()
                logger.debug(f"Wrote {symbol}")
            except Exception as e:
                logger.error(f"Error writing {symbol}: {e}")
