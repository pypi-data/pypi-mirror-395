"""Binance data adapter with multi-category support."""

from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from qldata.adapters.brokers.base_adapter import BaseBrokerAdapter
from qldata.adapters.brokers.binance.rest_client import BinanceRestClient
from qldata.common.logger import get_logger
from qldata.models.timeframe import Timeframe

logger = get_logger(__name__)


class BinanceAdapter(BaseBrokerAdapter):
    """Data source adapter for Binance.

    Supports multiple market types:
    - spot: Spot trading
    - usdm: USD-M Futures (USDT perpetual contracts)
    - coinm: COIN-M Futures (coin-margined perpetuals)
    - option: European Options

    Example:
        >>> # Spot market (default)
        >>> spot = BinanceAdapter(category="spot")
        >>> btc_spot = spot.get_bars("BTCUSDT", start, end, Timeframe.HOUR_1)

        >>> # USD-M Futures
        >>> futures = BinanceAdapter(category="usdm")
        >>> btc_perp = futures.get_bars("BTCUSDT", start, end, Timeframe.HOUR_1)

        >>> # COIN-M Futures
        >>> coinm = BinanceAdapter(category="coinm")
        >>> btc_coinm = coinm.get_bars("BTCUSD_PERP", start, end, Timeframe.HOUR_1)

        >>> # Options
        >>> options = BinanceAdapter(category="option")
        >>> btc_opt = options.get_bars("BTC-230728-30000-C", start, end, Timeframe.HOUR_1)
    """

    # Binance interval mapping
    INTERVAL_MAP = {
        Timeframe.MIN_1: "1m",
        Timeframe.MIN_3: "3m",
        Timeframe.MIN_5: "5m",
        Timeframe.MIN_15: "15m",
        Timeframe.MIN_30: "30m",
        Timeframe.HOUR_1: "1h",
        Timeframe.HOUR_2: "2h",
        Timeframe.HOUR_4: "4h",
        Timeframe.HOUR_6: "6h",
        Timeframe.HOUR_8: "8h",
        Timeframe.HOUR_12: "12h",
        Timeframe.DAY_1: "1d",
        Timeframe.DAY_3: "3d",
        Timeframe.WEEK_1: "1w",
        Timeframe.MONTH_1: "1M",
    }

    def __init__(
        self,
        category: str = "spot",
        api_key: str | None = None,
        api_secret: str | None = None
    ) -> None:
        """Initialize Binance adapter.

        Args:
            category: Market type ("spot", "usdm", "coinm", "option")
            api_key: Optional API key for authenticated requests
            api_secret: Optional API secret for authenticated requests

        Note:
            API key not required for public market data
        """
        if category not in ("spot", "usdm", "coinm", "option"):
            raise ValueError(
                f"Invalid category: {category}. "
                "Supported categories: spot, usdm, coinm, option"
            )

        self.category = category
        self._client = BinanceRestClient(category, api_key, api_secret)
        logger.debug(f"Initialized BinanceAdapter with category={category}")

    @staticmethod
    def _empty_bars() -> pd.DataFrame:
        """Return an empty frame with the expected schema and DatetimeIndex."""
        index = pd.DatetimeIndex([], name="timestamp")
        cols = ["open", "high", "low", "close", "volume"]
        return pd.DataFrame({col: pd.Series(dtype=float) for col in cols}, index=index)

    def _fetch_data(
        self, symbol: str, start: datetime, end: datetime, interval: str, **kwargs: Any
    ) -> pd.DataFrame:
        """Fetch data from Binance API with automatic chunking.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT" for spot/usdm, "BTCUSD_PERP" for coinm)
            start: Start datetime
            end: End datetime
            interval: Binance interval string
            **kwargs: Additional parameters

        Returns:
            DataFrame with OHLCV data

        Note:
            Binance returns max 1000 klines per request.
            For longer periods, multiple requests are made automatically.
        """
        logger.info(
            f"Fetching {symbol} from Binance {self.category} "
            f"({start} to {end}, interval={interval})"
        )
        
        # Binance limit is 1000 klines per request
        all_data = []
        current_start = start
        limit = 1000
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
