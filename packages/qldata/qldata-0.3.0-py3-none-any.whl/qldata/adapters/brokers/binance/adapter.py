"""Binance data adapter with multi-category support."""

import asyncio
from collections.abc import Callable
from datetime import datetime
from typing import Any, TypeVar, cast

import pandas as pd

try:
    from binance.client import Client
    from binance.exceptions import BinanceAPIException

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

from qldata.adapters.brokers.base import BaseBrokerAdapter
from qldata.common.logger import get_logger
from qldata.common.rate_limiter import AdaptiveRateLimiter
from qldata.errors import NetworkError, RateLimitError, ServerError
from qldata.models.timeframe import Timeframe
from qldata.resilience.rate_limit import RateLimitConfig, RateLimitManager

logger = get_logger(__name__)
F = TypeVar("F", bound=Callable[..., Any])


def _ensure_event_loop() -> None:
    """Create and set an event loop if the current thread does not have one."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


class BinanceAdapter(BaseBrokerAdapter):
    """Unified Binance data adapter with REST API client.

    Supports multiple market types:
    - spot: Spot trading
    - usdm: USD-M Futures (USDT perpetual contracts)
    - coinm: COIN-M Futures (coin-margined perpetuals)

    Features:
    - Automatic chunking for large date ranges
    - Rate limiting with adaptive backoff
    - Retry logic for transient errors
    - Specific exception handling

    Example:
        >>> # Spot market (default)
        >>> spot = BinanceAdapter(category="spot")
        >>> btc = spot.get_bars("BTCUSDT", start, end, Timeframe.HOUR_1)

        >>> # USD-M Futures
        >>> futures = BinanceAdapter(category="usdm")
        >>> btc_perp = futures.get_bars("BTCUSDT", start, end, Timeframe.HOUR_1)
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

    # Binance returns max 1000 klines per request
    MAX_BARS_PER_REQUEST = 1000

    def __init__(
        self,
        category: str = "spot",
        api_key: str | None = None,
        api_secret: str | None = None,
        max_retries: int = 3,
    ) -> None:
        """Initialize Binance adapter.

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

        if category not in ("spot", "usdm", "coinm"):
            raise ValueError(
                f"Invalid category: {category}. Supported categories: spot, usdm, coinm"
            )

        self.category = category
        _ensure_event_loop()
        self._client = Client(api_key, api_secret)
        self.max_retries = max_retries

        # Legacy rate limiter for backward compatibility
        self._rate_limiter = AdaptiveRateLimiter(max_calls=20, period=1.0, backoff_factor=0.5)

        # New RateLimitManager with per-endpoint tracking
        self._limit_manager = RateLimitManager(
            limits={
                "klines": RateLimitConfig(limit=1200, window_seconds=60, weight=1),
                "exchange_info": RateLimitConfig(limit=1200, window_seconds=60, weight=10),
                "orders": RateLimitConfig(limit=100, window_seconds=10, weight=1),
            },
            default_limit=1200,
        )

        # WebSocket manager (lazy initialization)
        self._ws_manager = None
        self._stream_keys: list[str] = []

        logger.debug(f"Initialized BinanceAdapter with category={category}")

    def get_exchange_info(self) -> dict[str, Any]:
        """Fetch exchange info for the configured category."""
        if self.category == "spot":
            return self._client.get_exchange_info()
        if self.category == "usdm":
            return self._client.futures_exchange_info()
        if self.category == "coinm":
            return self._client.futures_coin_exchange_info()
        raise ValueError(f"Unknown category: {self.category}")

    def _create_retry_decorator(self) -> Callable[[F], F]:
        """Create retry decorator if tenacity is available."""
        if not TENACITY_AVAILABLE:

            def no_retry(func: F) -> F:
                return func

            return no_retry

        # Retry on rate limits and network errors
        return cast(
            Callable[[F], F],
            retry(
                retry=retry_if_exception_type((RateLimitError, NetworkError, ConnectionError)),
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential(multiplier=1, min=4, max=10),
                reraise=True,
            ),
        )

    def _fetch_data(
        self, symbol: str, start: datetime, end: datetime, interval: str, **kwargs: Any
    ) -> pd.DataFrame:
        """Fetch data from Binance API.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            start: Start datetime
            end: End datetime
            interval: Binance interval string (from INTERVAL_MAP)
            **kwargs: Additional parameters

        Returns:
            DataFrame with OHLCV data
        """
        logger.info(
            f"Fetching {symbol} from Binance {self.category} "
            f"({start} to {end}, interval={interval})"
        )

        # Apply rate limiting (use new manager for klines endpoint)
        self._limit_manager.acquire("klines")
        self._rate_limiter.wait_if_needed()

        # Convert datetime to milliseconds
        start_time = int(start.timestamp() * 1000)
        end_time = int(end.timestamp() * 1000)

        # Create retry decorator
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def _fetch_with_retry() -> list[list[Any]]:
            try:
                # Select appropriate API method based on category
                if self.category == "spot":
                    klines = self._client.get_klines(
                        symbol=symbol,
                        interval=interval,
                        startTime=start_time,
                        endTime=end_time,
                        limit=self.MAX_BARS_PER_REQUEST,
                    )
                elif self.category == "usdm":
                    klines = self._client.futures_klines(
                        symbol=symbol,
                        interval=interval,
                        startTime=start_time,
                        endTime=end_time,
                        limit=self.MAX_BARS_PER_REQUEST,
                    )
                elif self.category == "coinm":
                    klines = self._client.futures_coin_klines(
                        symbol=symbol,
                        interval=interval,
                        startTime=start_time,
                        endTime=end_time,
                        limit=self.MAX_BARS_PER_REQUEST,
                    )
                else:
                    raise ValueError(f"Unknown category: {self.category}")

                self._rate_limiter.on_success()
                return klines

            except BinanceAPIException as e:
                # Check if it's a rate limit error
                if e.code == -1003 or "rate limit" in str(e.message).lower():
                    self._rate_limiter.on_rate_limit_error()
                    raise RateLimitError(f"Binance rate limit exceeded: {e.message}") from e
                # Server errors (5xx equivalent)
                elif e.code in (-1001, -1021):
                    raise ServerError(f"Binance server error: {e.message}") from e
                # Network/connectivity issues
                else:
                    raise NetworkError(f"Binance API error: {e.message}") from e
            except ConnectionError as e:
                raise NetworkError(f"Network connection failed: {e}") from e

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

        logger.info(f"Retrieved {len(df)} bars for {symbol}")
        return df

    # WebSocket streaming methods

    def stream_trades(self, symbol: str, callback: callable) -> str:
        """Stream live trades for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            callback: Function to call with each trade message

        Returns:
            Stream key for managing the connection

        Example:
            >>> def on_trade(msg):
            ...     print(f"Trade: {msg}")
            >>> adapter = BinanceAdapter(category="spot")
            >>> key = adapter.stream_trades("BTCUSDT", on_trade)
            >>> # Later: adapter.stop_stream(key) or adapter.stop_all_streams()
        """
        self._ensure_ws_manager()

        if self.category == "spot":
            key = self._ws_manager.start_trade_socket(callback=callback, symbol=symbol)
        elif self.category == "usdm":
            key = self._ws_manager.start_futures_socket(callback=callback, symbol=symbol)
        elif self.category == "coinm":
            key = self._ws_manager.start_coin_socket(callback=callback, symbol=symbol)
        else:
            raise ValueError(f"Unsupported category for trades: {self.category}")

        self._stream_keys.append(key)
        logger.info(f"Started trade stream for {symbol} (key: {key})")
        return key

    def stream_klines(self, symbol: str, interval: str, callback: callable) -> str:
        """Stream live klines/candlesticks for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            interval: Kline interval (e.g., "1m", "1h", "1d")
            callback: Function to call with each kline message

        Returns:
            Stream key for managing the connection

        Example:
            >>> def on_kline(msg):
            ...     k = msg['k']
            ...     print(f"Close: {k['c']}")
            >>> adapter = BinanceAdapter(category="spot")
            >>> key = adapter.stream_klines("BTCUSDT", "1m", on_kline)
        """
        self._ensure_ws_manager()

        if self.category == "spot":
            key = self._ws_manager.start_kline_socket(
                callback=callback, symbol=symbol, interval=interval
            )
        elif self.category == "usdm":
            key = self._ws_manager.start_kline_futures_socket(
                callback=callback, symbol=symbol, interval=interval
            )
        elif self.category == "coinm":
            key = self._ws_manager.start_kline_coin_socket(
                callback=callback, symbol=symbol, interval=interval
            )
        else:
            raise ValueError(f"Unsupported category for klines: {self.category}")

        self._stream_keys.append(key)
        logger.info(f"Started kline stream for {symbol} @ {interval} (key: {key})")
        return key

    def stream_ticker(self, symbol: str, callback: callable) -> str:
        """Stream 24hr ticker statistics for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            callback: Function to call with each ticker update

        Returns:
            Stream key for managing the connection
        """
        self._ensure_ws_manager()

        if self.category == "spot":
            key = self._ws_manager.start_symbol_ticker_socket(callback=callback, symbol=symbol)
        elif self.category == "usdm":
            key = self._ws_manager.start_symbol_ticker_futures_socket(
                callback=callback, symbol=symbol
            )
        else:
            raise ValueError(f"Unsupported category for ticker: {self.category}")

        self._stream_keys.append(key)
        logger.info(f"Started ticker stream for {symbol} (key: {key})")
        return key

    def stream_depth(self, symbol: str, callback: callable, depth: int = 10) -> str:
        """Stream order book depth updates for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            callback: Function to call with each depth update
            depth: Depth level (5, 10, or 20)

        Returns:
            Stream key for managing the connection
        """
        self._ensure_ws_manager()

        if self.category == "spot":
            key = self._ws_manager.start_depth_socket(
                callback=callback, symbol=symbol, depth=depth
            )
        else:
            raise ValueError("Depth streams only supported for spot")

        self._stream_keys.append(key)
        logger.info(f"Started depth stream for {symbol} (key: {key})")
        return key

    def stop_stream(self, key: str) -> None:
        """Stop a specific WebSocket stream.

        Args:
            key: Stream key returned from stream_* methods
        """
        if self._ws_manager and key in self._stream_keys:
            self._ws_manager.stop_socket(key)
            self._stream_keys.remove(key)
            logger.info(f"Stopped stream {key}")

    def stop_all_streams(self) -> None:
        """Stop all active WebSocket streams."""
        if self._ws_manager:
            for key in self._stream_keys:
                self._ws_manager.stop_socket(key)
            self._ws_manager.stop()
            self._ws_manager = None
            self._stream_keys = []
            logger.info("Stopped all streams")

    def _ensure_ws_manager(self) -> None:
        """Ensure WebSocket manager is initialized."""
        if not self._ws_manager:
            try:
                from binance import ThreadedWebsocketManager
            except ImportError as exc:
                raise ImportError(
                    "ThreadedWebsocketManager not available. "
                    "Upgrade python-binance: pip install --upgrade python-binance"
                ) from exc

            self._ws_manager = ThreadedWebsocketManager(
                api_key=self._client.API_KEY, api_secret=self._client.API_SECRET
            )
            self._ws_manager.start()
            self._stream_keys = []
            logger.debug("Started WebSocket manager")
