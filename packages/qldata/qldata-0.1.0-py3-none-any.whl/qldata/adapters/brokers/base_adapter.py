"""Base adapter class for broker integrations."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import pandas as pd

from qldata.models.timeframe import Timeframe
from qldata.sources.base.source import DataSource


class BaseBrokerAdapter(DataSource, ABC):
    """Abstract base class for broker data adapters.

    Provides common functionality for broker integrations including:
    - Interval/timeframe mapping validation
    - Error handling patterns
    - Common configuration

    Subclasses should define:
    - INTERVAL_MAP: Mapping of Timeframe to broker-specific interval strings
    - _fetch_data: Implementation-specific data fetching logic
    """

    # Subclasses must override this
    INTERVAL_MAP: dict[Timeframe, str] = {}

    def get_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe: Timeframe, **kwargs: Any
    ) -> pd.DataFrame:
        """Get bar data from the broker.

        Args:
            symbol: Trading symbol/ticker
            start: Start datetime
            end: End datetime
            timeframe: Bar timeframe
            **kwargs: Additional broker-specific parameters

        Returns:
            DataFrame with OHLCV data

        Raises:
            ValueError: If timeframe is not supported by this broker
        """
        # Validate timeframe is supported
        if timeframe not in self.INTERVAL_MAP:
            supported = ", ".join(str(tf) for tf in self.INTERVAL_MAP)
            raise ValueError(
                f"Timeframe {timeframe} not supported by {self.__class__.__name__}. "
                f"Supported timeframes: {supported}"
            )

        interval = self.INTERVAL_MAP[timeframe]

        # Delegate to subclass implementation
        return self._fetch_data(symbol, start, end, interval, **kwargs)

    @abstractmethod
    def _fetch_data(
        self, symbol: str, start: datetime, end: datetime, interval: str, **kwargs: Any
    ) -> pd.DataFrame:
        """Fetch data from the broker API.

        This method must be implemented by subclasses to handle
        broker-specific API calls and response formatting.

        Args:
            symbol: Trading symbol/ticker
            start: Start datetime
            end: End datetime
            interval: Broker-specific interval string (from INTERVAL_MAP)
            **kwargs: Additional broker-specific parameters

        Returns:
            DataFrame with OHLCV data
        """
        pass
