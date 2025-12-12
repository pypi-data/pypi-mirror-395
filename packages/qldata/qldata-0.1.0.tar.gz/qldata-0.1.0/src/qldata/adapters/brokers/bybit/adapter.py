"""Bybit data adapter."""

from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from qldata.adapters.brokers.base_adapter import BaseBrokerAdapter
from qldata.adapters.brokers.bybit.rest_client import BybitRestClient
from qldata.common.logger import get_logger
from qldata.models.timeframe import Timeframe

logger = get_logger(__name__)


class BybitAdapter(BaseBrokerAdapter):
    """Data source adapter for Bybit.

    Supports multiple product types:
    - spot: Spot trading
    - linear: USDT perpetual
    - inverse: Inverse perpetual
    - option: Options

    Example:
        >>> # Linear (USDT perpetual)
        >>> adapter = BybitAdapter(category="linear")
        >>> btc = adapter.get_bars("BTCUSDT", start, end, Timeframe.HOUR_1)

        >>> # Spot
        >>> adapter = BybitAdapter(category="spot")
        >>> eth = adapter.get_bars("ETHUSDT", start, end, Timeframe.MIN_15)
    """

    # Bybit interval mapping (in minutes for most, or D/W/M for day/week/month)
    INTERVAL_MAP = {
        Timeframe.MIN_1: "1",
        Timeframe.MIN_3: "3",
        Timeframe.MIN_5: "5",
        Timeframe.MIN_15: "15",
        Timeframe.MIN_30: "30",
        Timeframe.HOUR_1: "60",
        Timeframe.HOUR_2: "120",
        Timeframe.HOUR_4: "240",
        Timeframe.HOUR_6: "360",
        Timeframe.HOUR_12: "720",
        Timeframe.DAY_1: "D",
        Timeframe.WEEK_1: "W",
        Timeframe.MONTH_1: "M",
    }

    def __init__(
        self,
        category: str = "linear",
        api_key: str | None = None,
        api_secret: str | None = None,
        testnet: bool = False,
    ) -> None:
        """Initialize Bybit adapter.

        Args:
            category: Product type ("spot", "linear", "inverse", "option")
            api_key: Optional API key for authenticated requests
            api_secret: Optional API secret for authenticated requests
            testnet: Whether to use testnet
        """
        self.category = category
        self._client = BybitRestClient(category, api_key, api_secret, testnet)
        logger.debug(f"Initialized BybitAdapter with category={category}, testnet={testnet}")

    @staticmethod
    def _empty_bars() -> pd.DataFrame:
        """Return an empty frame with the expected schema and DatetimeIndex."""
        index = pd.DatetimeIndex([], name="timestamp")
        cols = ["open", "high", "low", "close", "volume"]
        return pd.DataFrame({col: pd.Series(dtype=float) for col in cols}, index=index)

    def _fetch_data(
        self, symbol: str, start: datetime, end: datetime, interval: str, **kwargs: Any
    ) -> pd.DataFrame:
        """Fetch data from Bybit API with automatic chunking.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            start: Start datetime
            end: End datetime
            interval: Bybit interval string
            **kwargs: Additional parameters

        Returns:
            DataFrame with OHLCV data

        Note:
            Bybit returns max 200 klines per request.
            For longer periods, multiple requests are made automatically.
        """
        logger.info(
            f"Fetching {symbol} from Bybit {self.category} "
            f"({start} to {end}, interval={interval})"
        )
        
        # Bybit limit is 200 klines per request
        all_data = []
        current_start = start
        limit = 200
        chunk_count = 0

        while current_start < end:
            chunk_count += 1
            logger.debug(f"Fetching chunk {chunk_count} from {current_start}")
            
            # Fetch chunk
            chunk = self._client.get_klines(
                symbol=symbol,
                interval=interval,
                start_time=current_start,
                end_time=end,
                limit=limit,
            )

            if chunk.empty:
                logger.debug("Received empty chunk, stopping")
                break

            all_data.append(chunk)
            logger.debug(f"Chunk {chunk_count}: {len(chunk)} bars")

            # Move to next chunk
            last_timestamp = chunk.index[-1]
            current_start = last_timestamp + timedelta(seconds=1)

            # Break if we got less than the limit (no more data)
            if len(chunk) < limit:
                logger.debug(f"Received {len(chunk)} < {limit} bars, assuming end of data")
                break

        if not all_data:
            logger.warning(f"No data retrieved for {symbol}")
            return self._empty_bars()

        # Combine all chunks
        data = pd.concat(all_data)

        # Remove duplicates
        duplicates = data.index.duplicated(keep="first").sum()
        if duplicates > 0:
            logger.debug(f"Removing {duplicates} duplicate rows")
            data = data[~data.index.duplicated(keep="first")]

        # Filter to exact range
        data = data[(data.index >= start) & (data.index <= end)]

        logger.info(f"Retrieved {len(data)} total bars for {symbol} in {chunk_count} chunks")
        return data
