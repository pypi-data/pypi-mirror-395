"""Bybit REST API client."""

from datetime import datetime
from typing import Any, cast

import pandas as pd

try:
    from pybit.unified_trading import HTTP  # type: ignore[import-untyped]

    PYBIT_AVAILABLE = True
except ImportError:
    PYBIT_AVAILABLE = False


class BybitRestClient:
    """Client for Bybit REST API (V5).

    Provides access to Bybit market data.
    No API key required for public data.

    Example:
        >>> client = BybitRestClient(category="linear")
        >>> klines = client.get_klines("BTCUSDT", "60", start_time, end_time)
    """

    def __init__(
        self,
        category: str = "linear",
        api_key: str | None = None,
        api_secret: str | None = None,
        testnet: bool = False,
    ) -> None:
        """Initialize Bybit REST client.

        Args:
            category: Product type ("spot", "linear", "inverse", "option")
            api_key: Optional API key for authenticated requests
            api_secret: Optional API secret for authenticated requests
            testnet: Whether to use testnet
        """
        if not PYBIT_AVAILABLE:
            raise ImportError(
                "pybit package required for Bybit integration. " "Install with: pip install pybit"
            )

        self.category = category
        self._client = HTTP(testnet=testnet, api_key=api_key, api_secret=api_secret)
        self._instrument_cache: dict[str | None, dict[str, Any]] = {}

    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: datetime | int | None = None,
        end_time: datetime | int | None = None,
        limit: int = 200,
    ) -> pd.DataFrame:
        """Get historical kline/candlestick data.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            interval: Kline interval (1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, W, M)
            start_time: Start time (datetime or timestamp in milliseconds)
            end_time: End time (datetime or timestamp in milliseconds)
            limit: Number of klines to return (max 1000)

        Returns:
            DataFrame with OHLCV data
        """
        # Convert datetime to milliseconds if needed
        if isinstance(start_time, datetime):
            start_time = int(start_time.timestamp() * 1000)
        if isinstance(end_time, datetime):
            end_time = int(end_time.timestamp() * 1000)

        try:
            # Fetch klines
            response = self._client.get_kline(
                category=self.category,
                symbol=symbol,
                interval=interval,
                start=start_time,
                end=end_time,
                limit=limit,
            )

            if response["retCode"] != 0:
                raise RuntimeError(f"Bybit API error: {response['retMsg']}")

            klines = response["result"]["list"]

            if not klines:
                return pd.DataFrame()

            # Convert to DataFrame
            # Bybit format: [startTime, open, high, low, close, volume, turnover]
            df = pd.DataFrame(
                klines, columns=["timestamp", "open", "high", "low", "close", "volume", "turnover"]
            )

            # Convert timestamp to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms")

            # Convert price/volume to float
            for col in ["open", "high", "low", "close", "volume"]:
                df[col] = df[col].astype(float)

            # Keep only OHLCV columns
            df = df[["timestamp", "open", "high", "low", "close", "volume"]]

            # Set timestamp as index
            df = df.set_index("timestamp")

            # Sort by timestamp (Bybit returns descending)
            df = df.sort_index()

            return df

        except Exception as e:
            raise RuntimeError(f"Bybit API error: {e}") from e

    def get_tickers(self, symbol: str | None = None) -> dict[str, Any]:
        """Get latest ticker information.

        Args:
            symbol: Optional symbol to filter (None = all symbols)

        Returns:
            Dictionary with ticker data
        """
        try:
            response = self._client.get_tickers(category=self.category, symbol=symbol)

            if response["retCode"] != 0:
                raise RuntimeError(f"Bybit API error: {response['retMsg']}")

            return cast(dict[str, Any], response["result"])

        except Exception as e:
            raise RuntimeError(f"Bybit API error: {e}") from e

    def get_instruments_info(self, symbol: str | None = None) -> dict[str, Any]:
        """Get instrument specifications.

        Args:
            symbol: Optional symbol to filter

        Returns:
            Dictionary with instrument info
        """
        try:
            if symbol in self._instrument_cache:
                return self._instrument_cache[symbol]

            response = self._client.get_instruments_info(category=self.category, symbol=symbol)

            if response["retCode"] != 0:
                raise RuntimeError(f"Bybit API error: {response['retMsg']}")

            result = cast(dict[str, Any], response["result"])
            self._instrument_cache[symbol] = result
            return result

        except Exception as e:
            raise RuntimeError(f"Bybit API error: {e}") from e
