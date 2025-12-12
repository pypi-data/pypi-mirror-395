"""Base adapter class for broker integrations."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from qldata.models.timeframe import Timeframe


class BaseBrokerAdapter(ABC):
    """Abstract base class for broker data adapters.

    Provides common functionality for broker integrations including:
    - Interval/time frame mapping validation
    - Error handling patterns
    - Automatic chunking for large date ranges
    - Common configuration

    Subclasses should define:
    - INTERVAL_MAP: Mapping of Timeframe to broker-specific interval strings
    - MAX_BARS_PER_REQUEST: Maximum bars returned per API request (default: 1000)
    - _fetch_data: Implementation-specific data fetching logic
    """

    # Subclasses must override this
    INTERVAL_MAP: dict[Timeframe, str] = {}

    # Subclasses can override this (most exchanges limit to ~1000-1500)
    MAX_BARS_PER_REQUEST: int = 1000

    def get_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe: Timeframe, **kwargs: Any
    ) -> pd.DataFrame:
        """Get bar data from the broker with automatic chunking.

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

        # Calculate required bars
        total_seconds = (end - start).total_seconds()
        bars_per_interval = timeframe.to_seconds()
        bars_needed = int(total_seconds / bars_per_interval)

        # If within limit, fetch directly
        if bars_needed <= self.MAX_BARS_PER_REQUEST:
            return self._fetch_data(symbol, start, end, interval, **kwargs)

        # Otherwise, chunk the request
        return self._fetch_chunked(symbol, start, end, timeframe, interval, **kwargs)

    def _fetch_chunked(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: Timeframe,
        interval: str,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Fetch data in chunks for large date ranges.

        Args:
            symbol: Trading symbol/ticker
            start: Start datetime
            end: End datetime
            timeframe: Timeframe enum
            interval: Broker-specific interval string
            **kwargs: Additional parameters

        Returns:
            Combined DataFrame from all chunks
        """
        chunks = self._calculate_chunks(start, end, timeframe)
        results: list[pd.DataFrame] = []

        for chunk_start, chunk_end in chunks:
            chunk_data = self._fetch_data(symbol, chunk_start, chunk_end, interval, **kwargs)
            if not chunk_data.empty:
                results.append(chunk_data)

        if not results:
            return pd.DataFrame()

        # Combine all chunks and remove duplicates
        combined = pd.concat(results, ignore_index=False)
        combined = combined[~combined.index.duplicated(keep="last")]
        combined = combined.sort_index()

        return combined

    def _calculate_chunks(
        self, start: datetime, end: datetime, timeframe: Timeframe
    ) -> list[tuple[datetime, datetime]]:
        """Calculate time chunks based on MAX_BARS_PER_REQUEST.

        Args:
            start: Start datetime
            end: End datetime
            timeframe: Timeframe for bars

        Returns:
            List of (chunk_start, chunk_end) tuples
        """
        seconds_per_bar = timeframe.to_seconds()
        seconds_per_chunk = seconds_per_bar * self.MAX_BARS_PER_REQUEST

        chunks: list[tuple[datetime, datetime]] = []
        current_start = start

        while current_start < end:
            current_end = min(current_start + timedelta(seconds=seconds_per_chunk), end)
            chunks.append((current_start, current_end))
            current_start = current_end

        return chunks

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

    def get_exchange_info(self) -> dict[str, Any]:
        """Return exchange metadata and symbol listings.

        Adapters should override this when reference data is available.
        """
        raise NotImplementedError("Exchange info not implemented for this adapter")
