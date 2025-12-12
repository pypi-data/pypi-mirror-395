"""Base data source interface."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import pandas as pd

from qldata.models.timeframe import Timeframe


class DataSource(ABC):
    """Abstract base class for data sources.

    A DataSource handles reading market data from various backends.
    """

    @abstractmethod
    def get_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe: Timeframe, **kwargs: Any
    ) -> pd.DataFrame:
        """Get bar data from source.

        Args:
            symbol: Symbol ticker
            start: Start datetime
            end: End datetime
            timeframe: Bar timeframe
            **kwargs: Additional source-specific parameters

        Returns:
            DataFrame with OHLCV data
        """
        pass
