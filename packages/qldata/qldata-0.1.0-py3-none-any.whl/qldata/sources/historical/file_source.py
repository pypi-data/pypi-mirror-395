"""Historical data source implementation."""

from datetime import datetime
from typing import Any

import pandas as pd

from qldata.models.timeframe import Timeframe
from qldata.sources.base.source import DataSource
from qldata.stores.base.store import DataStore


class HistoricalDataSource(DataSource):
    """Read historical data from a DataStore."""

    def __init__(self, store: DataStore) -> None:
        """Initialize historical source.

        Args:
            store: DataStore instance to read from
        """
        self._store = store

    def get_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe: Timeframe, **kwargs: Any
    ) -> pd.DataFrame:
        """Get bar data from store.

        Args:
            symbol: Symbol ticker
            start: Start datetime
            end: End datetime
            timeframe: Bar timeframe
            **kwargs: Additional parameters (unused)

        Returns:
            DataFrame with OHLCV data
        """
        return self._store.read_bars(symbol, start, end, timeframe)
