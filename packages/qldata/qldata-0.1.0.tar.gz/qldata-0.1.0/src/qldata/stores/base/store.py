"""Base data store interface."""

from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

from qldata.models.timeframe import Timeframe


class DataStore(ABC):
    """Abstract base class for data stores.

    A DataStore handles reading and writing market data to a storage backend.
    """

    @abstractmethod
    def write_bars(
        self,
        symbol: str,
        data: pd.DataFrame,
        timeframe: Timeframe,
    ) -> None:
        """Write bar data to store.

        Args:
            symbol: Symbol ticker
            data: DataFrame with OHLCV data
            timeframe: Bar timeframe
        """
        pass

    @abstractmethod
    def read_bars(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Timeframe,
    ) -> pd.DataFrame:
        """Read bar data from store.

        Args:
            symbol: Symbol ticker
            start: Start datetime
            end: End datetime
            timeframe: Bar timeframe

        Returns:
            DataFrame with OHLCV data
        """
        pass

    @abstractmethod
    def has_data(
        self,
        symbol: str,
        timeframe: Timeframe,
    ) -> bool:
        """Check if store has data for symbol/timeframe.

        Args:
            symbol: Symbol ticker
            timeframe: Bar timeframe

        Returns:
            True if data exists
        """
        pass

    @abstractmethod
    def delete_data(
        self,
        symbol: str,
        timeframe: Timeframe,
    ) -> None:
        """Delete all data for symbol/timeframe.

        Args:
            symbol: Symbol ticker
            timeframe: Bar timeframe
        """
        pass
