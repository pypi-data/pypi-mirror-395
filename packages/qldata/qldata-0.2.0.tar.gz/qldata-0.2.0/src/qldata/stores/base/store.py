"""Base data store interface."""

from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

from qldata.models.dataset_metadata import DatasetMetadata
from qldata.models.timeframe import Timeframe


class DataStore(ABC):
    """Abstract base class for data stores.

    A DataStore handles reading and writing market data to a storage backend.
    Stores should also track metadata about datasets for smart caching and
    data quality monitoring.
    """

    @abstractmethod
    def write_bars(
        self,
        symbol: str,
        data: pd.DataFrame,
        timeframe: Timeframe,
        source: str = "unknown",
    ) -> None:
        """Write bar data to store.

        Args:
            symbol: Symbol ticker
            data: DataFrame with OHLCV data
            timeframe: Bar timeframe
            source: Data source name (for metadata tracking)
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

    # Metadata methods

    @abstractmethod
    def write_metadata(self, metadata: DatasetMetadata) -> None:
        """Write metadata for a dataset.

        Args:
            metadata: Dataset metadata to store
        """
        pass

    @abstractmethod
    def read_metadata(
        self, symbol: str, timeframe: Timeframe
    ) -> DatasetMetadata | None:
        """Read metadata for a dataset.

        Args:
            symbol: Symbol ticker
            timeframe: Bar timeframe

        Returns:
            Dataset metadata if exists, None otherwise
        """
        pass

    @abstractmethod
    def list_metadata(self) -> list[DatasetMetadata]:
        """List all dataset metadata.

        Returns:
            List of all dataset metadata entries
        """
        pass

    def get_metadata_or_none(
        self, symbol: str, timeframe: Timeframe
    ) -> DatasetMetadata | None:
        """Helper to safely get metadata.

        Args:
            symbol: Symbol ticker
            timeframe: Bar timeframe

        Returns:
            Metadata if exists, None otherwise
        """
        try:
            return self.read_metadata(symbol, timeframe)
        except Exception:
            return None
