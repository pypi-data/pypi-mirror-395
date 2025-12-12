# src/qldata/adapters/brokers/binance/rest_client.py
"""Binance REST API client with multi-category support, retry logic and rate limiting."""

import asyncio
from datetime import datetime
from typing import Any, cast

import pandas as pd

try:
    from binance.client import Client  # type: ignore[import-untyped]
    from binance.exceptions import BinanceAPIException  # type: ignore[import-untyped]

    BINANCE_AVAILABLE = True
except ImportError:
    BINANCE_AVAILABLE = False

try:
    from tenacity import (
        retry,
        retry_if_exception_type,
        stop_after_attempt,
        wait_exponential,
    )

    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False

from qldata.common.rate_limiter import AdaptiveRateLimiter


def _ensure_event_loop() -> None:
    """Create and set an event loop if the current thread does not have one."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


class BinanceRestClient:
    """Client for Binance REST API with multi-category support, retry and rate limiting.

    Supports multiple Binance market types:
    - spot: Spot trading
    - usdm: USD-M Futures (USDT perpetual contracts)
    - coinm: COIN-M Futures (coin-margined perpetuals)

    Example:
        >>> # Spot market
        >>> client = BinanceRestClient(category="spot")
        >>> klines = client.get_klines("BTCUSDT", "1h", start_time, end_time)

        >>> # USD-M Futures
        >>> futures_client = BinanceRestClient(category="usdm")
        >>> perp = futures_client.get_klines("BTCUSDT", "1h", start_time, end_time)
    """

    def __init__(
        self,
        category: str = "spot",
        api_key: str | None = None,
        api_secret: str | None = None,
        max_retries: int = 3,
    ) -> None:
        """Initialize Binance REST client.

        Args:
            category: Market type ("spot", "usdm", "coinm")
            api_key: Optional API key for authenticated requests
            api_secret: Optional API secret for authenticated requests
            max_retries: Maximum number of retry attempts (default: 3)
        """
        if not BINANCE_AVAILABLE:
            raise ImportError(
                "python-binance package required for Binance integration. "
                "Install with: pip install python-binance"
            )

        self.category = category
        _ensure_event_loop()
        self._client = Client(api_key, api_secret)
        self.max_retries = max_retries
        self._exchange_info_cache: dict[str, Any] | None = None

        # Rate limiter: 1200 requests per minute = 20 per second
        self._rate_limiter = AdaptiveRateLimiter(
            max_calls=20, period=1.0, backoff_factor=0.5
        )

    def _create_retry_decorator(self):
        """Create retry decorator if tenacity is available."""
        if not TENACITY_AVAILABLE:
            # Return identity decorator if tenacity not available
            def no_retry(func):
                return func

            return no_retry

        return retry(
            retry=retry_if_exception_type((BinanceAPIException, ConnectionError)),
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=10),
            reraise=True,
        )

    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: datetime | int | None = None,
        end_time: datetime | int | None = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Get historical kline/candlestick data with retry logic.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT" for spot/usdm, "BTCUSD_PERP" for coinm)
            interval: Kline interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
            start_time: Start time (datetime or timestamp in milliseconds)
            end_time: End time (datetime or timestamp in milliseconds)
            limit: Number of klines to return (max 1000)

        Returns:
            DataFrame with OHLCV data

        Raises:
            RuntimeError: If API request fails after all retries
        """
        # Apply rate limiting
        self._rate_limiter.wait_if_needed()

        # Convert datetime to milliseconds if needed
        if isinstance(start_time, datetime):
            start_time = int(start_time.timestamp() * 1000)
        if isinstance(end_time, datetime):
            end_time = int(end_time.timestamp() * 1000)

        # Create retry decorator
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def _fetch_with_retry():
            try:
                # Select appropriate API method based on category
                if self.category == "spot":
                    klines = self._client.get_klines(
                        symbol=symbol,
                        interval=interval,
                        startTime=start_time,
                        endTime=end_time,
                        limit=limit,
                    )
                elif self.category == "usdm":
                    klines = self._client.futures_klines(
                        symbol=symbol,
                        interval=interval,
                        startTime=start_time,
                        endTime=end_time,
                        limit=limit,
                    )
                elif self.category == "coinm":
                    klines = self._client.futures_coin_klines(
                        symbol=symbol,
                        interval=interval,
                        startTime=start_time,
                        endTime=end_time,
                        limit=limit,
                    )
                else:
                    raise ValueError(f"Unknown category: {self.category}")

                self._rate_limiter.on_success()
                return klines

            except BinanceAPIException as e:
                # Check if it's a rate limit error
                if e.code == -1003 or "rate limit" in str(e.message).lower():
                    self._rate_limiter.on_rate_limit_error()

                raise RuntimeError(f"Binance API error: {e.message}") from e

        klines = _fetch_with_retry()

        if not klines:
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(
            klines,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore",
            ],
        )

        # Convert timestamp to datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        # Convert price/volume to float
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)

        # Keep only OHLCV columns
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]

        # Set timestamp as index
        df = df.set_index("timestamp")

        return df

    def get_exchange_info(self) -> dict[str, Any]:
        """Get exchange trading rules and symbol information.

        Returns:
            Dictionary with exchange information

        Raises:
            RuntimeError: If API request fails
        """
        if self._exchange_info_cache is not None:
            return self._exchange_info_cache

        self._rate_limiter.wait_if_needed()

        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def _fetch_with_retry():
            try:
                if self.category == "spot":
                    info = self._client.get_exchange_info()
                elif self.category == "usdm":
                    info = self._client.futures_exchange_info()
                elif self.category == "coinm":
                    info = self._client.futures_coin_exchange_info()
                else:
                    raise ValueError(f"Unknown category: {self.category}")

                self._rate_limiter.on_success()
                return info
            except BinanceAPIException as e:
                if e.code == -1003 or "rate limit" in str(e.message).lower():
                    self._rate_limiter.on_rate_limit_error()
                raise RuntimeError(f"Binance API error: {e.message}") from e

        info = cast(dict[str, Any], _fetch_with_retry())
        self._exchange_info_cache = info
        return info

    def get_symbol_info(self, symbol: str) -> dict[str, Any] | None:
        """Get information for a specific symbol.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")

        Returns:
            Dictionary with symbol information or None if not found
        """
        info = self.get_exchange_info()
        for s in info["symbols"]:
            if s["symbol"] == symbol:
                return cast(dict[str, Any], s)
        return None

    def get_ticker(self, symbol: str) -> dict[str, Any]:
        """Get 24hr ticker price change statistics.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")

        Returns:
            Dictionary with ticker data

        Raises:
            RuntimeError: If API request fails
        """
        self._rate_limiter.wait_if_needed()

        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def _fetch_with_retry():
            try:
                if self.category == "spot":
                    ticker = self._client.get_ticker(symbol=symbol)
                elif self.category == "usdm":
                    ticker = self._client.futures_ticker(symbol=symbol)
                elif self.category == "coinm":
                    ticker = self._client.futures_coin_ticker(symbol=symbol)
                else:
                    raise ValueError(f"Unknown category: {self.category}")

                self._rate_limiter.on_success()
                return ticker
            except BinanceAPIException as e:
                if e.code == -1003 or "rate limit" in str(e.message).lower():
                    self._rate_limiter.on_rate_limit_error()
                raise RuntimeError(f"Binance API error: {e.message}") from e

        return cast(dict[str, Any], _fetch_with_retry())

    def get_rate_limit_stats(self) -> dict[str, Any]:
        """Get current rate limiter statistics.

        Returns:
            Dictionary with rate limit stats
        """
        return self._rate_limiter.get_stats()

    def reset_rate_limiter(self) -> None:
        """Reset the rate limiter."""
        self._rate_limiter.reset()
