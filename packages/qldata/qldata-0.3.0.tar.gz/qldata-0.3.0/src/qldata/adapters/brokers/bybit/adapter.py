"""Bybit data adapter."""

from datetime import datetime
from typing import Any

import pandas as pd

try:
    from pybit.unified_trading import HTTP

    PYBIT_AVAILABLE = True
except ImportError:
    PYBIT_AVAILABLE = False

from qldata.adapters.brokers.base import BaseBrokerAdapter
from qldata.common.logger import get_logger
from qldata.errors import NetworkError, RateLimitError, ServerError
from qldata.models.timeframe import Timeframe

logger = get_logger(__name__)


class BybitAdapter(BaseBrokerAdapter):
    """Unified Bybit data adapter with REST API client.

    Supports multiple product types:
    - spot: Spot trading
    - linear: USDT perpetual
    - inverse: Inverse perpetual
    - option: Options

    Features:
    - Automatic chunking for large date ranges
    - Specific exception handling
    - Retry logic for transient errors

    Example:
        >>> # Linear (USDT perpetual)
        >>> adapter = BybitAdapter(category="linear")
        >>> btc = adapter.get_bars("BTCUSDT", start, end, Timeframe.HOUR_1)

        >>> # Spot
        >>> spot = BybitAdapter(category="spot")
        >>> eth = spot.get_bars("ETHUSDT", start, end, Timeframe.MIN_15)
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

    # Bybit returns max 200 klines per request
    MAX_BARS_PER_REQUEST = 200

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
        if not PYBIT_AVAILABLE:
            raise ImportError(
                "pybit package required for Bybit integration. " "Install with: pip install pybit"
            )

        self.category = category
        self._testnet = testnet
        self._client = HTTP(testnet=testnet, api_key=api_key, api_secret=api_secret)

        # WebSocket manager (lazy initialization)
        self._ws = None

        logger.debug(f"Initialized BybitAdapter with category={category}, testnet={testnet}")

    def _fetch_data(
        self, symbol: str, start: datetime, end: datetime, interval: str, **kwargs: Any
    ) -> pd.DataFrame:
        """Fetch data from Bybit API.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            start: Start datetime
            end: End datetime
            interval: Bybit interval string (from INTERVAL_MAP)
            **kwargs: Additional parameters

        Returns:
            DataFrame with OHLCV data
        """
        logger.info(
            f"Fetching {symbol} from Bybit {self.category} " f"({start} to {end}, interval={interval})"
        )

        # Convert datetime to milliseconds
        start_time = int(start.timestamp() * 1000)
        end_time = int(end.timestamp() * 1000)

        try:
            # Fetch klines
            response = self._client.get_kline(
                category=self.category,
                symbol=symbol,
                interval=interval,
                start=start_time,
                end=end_time,
                limit=self.MAX_BARS_PER_REQUEST,
            )

            if response["retCode"] != 0:
                # Check for rate limiting
                if response["retCode"] == 10006:  # Bybit rate limit code
                    raise RateLimitError(f"Bybit rate limit exceeded: {response['retMsg']}")
                # Server errors
                elif response["retCode"] >= 10000:
                    raise ServerError(f"Bybit server error: {response['retMsg']}")
                else:
                    raise NetworkError(f"Bybit API error: {response['retMsg']}")

            # Validate response structure before accessing nested fields
            if "result" not in response:
                raise NetworkError("Unexpected API response format: missing 'result' field")
            if "list" not in response["result"]:
                raise NetworkError("Unexpected API response format: missing 'list' field in result")

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

            logger.info(f"Retrieved {len(df)} bars for {symbol}")
            return df

        except Exception as e:
            if not isinstance(e, RateLimitError | ServerError | NetworkError):
                raise NetworkError(f"Bybit API error: {e}") from e
            raise

    def get_exchange_info(self) -> dict[str, Any]:
        """Fetch instrument info and normalize to a symbol list."""
        try:
            response = self._client.get_instruments_info(category=self.category)
            if response.get("retCode") != 0:
                raise ServerError(f"Bybit API error: {response.get('retMsg')}")
            result = response.get("result", {})
            instruments = result.get("list", [])

            symbols = []
            for inst in instruments:
                symbols.append(
                    {
                        "symbol": inst.get("symbol"),
                        "baseAsset": inst.get("baseCoin", ""),
                        "quoteAsset": inst.get("quoteCoin", ""),
                        "status": inst.get("status", "TRADING"),
                    }
                )

            return {"symbols": symbols}
        except Exception as exc:
            if isinstance(exc, RateLimitError | ServerError | NetworkError):
                raise
            raise NetworkError(f"Bybit exchange info error: {exc}") from exc

    # WebSocket streaming methods

    def stream_klines(self, symbol: str, interval: int, callback: callable) -> None:
        """Stream live klines/candlesticks for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            interval: Kline interval in minutes (1, 3, 5, 15, 30, 60, 120, 240, 360, 720, "D", "W", "M")
            callback: Function to call with each kline message

        Example:
            >>> def on_kline(msg):
            ...     print(msg)
            >>> adapter = BybitAdapter(category="linear")
            >>> adapter.stream_klines("BTCUSDT", 1, on_kline)
            >>> # Later: adapter.stop_all_streams()
        """
        self._ensure_websocket()
        self._ws.kline_stream(
            interval=interval,
            symbol=symbol,
            callback=callback
        )
        logger.info(f"Started kline stream for {symbol} @ {interval}min")

    def stream_ticker(self, symbol: str, callback: callable) -> None:
        """Stream ticker updates for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            callback: Function to call with each ticker update
        """
        self._ensure_websocket()
        self._ws.ticker_stream(
            symbol=symbol,
            callback=callback
        )
        logger.info(f"Started ticker stream for {symbol}")

    def stream_trades(self, symbol: str, callback: callable) -> None:
        """Stream live trades for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            callback: Function to call with each trade
        """
        self._ensure_websocket()
        self._ws.trade_stream(
            symbol=symbol,
            callback=callback
        )
        logger.info(f"Started trade stream for {symbol}")

    def stream_orderbook(self, symbol: str, depth: int, callback: callable) -> None:
        """Stream order book updates for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            depth: Depth level (1, 50, 200, 500)
            callback: Function to call with each orderbook update
        """
        self._ensure_websocket()
        self._ws.orderbook_stream(
            depth=depth,
            symbol=symbol,
            callback=callback
        )
        logger.info(f"Started orderbook stream for {symbol} (depth={depth})")

    def stop_all_streams(self) -> None:
        """Stop all active WebSocket streams."""
        if self._ws:
            # pybit WebSocket cleanup is automatic
            self._ws = None
            logger.info("Stopped all streams")

    def _ensure_websocket(self) -> None:
        """Ensure WebSocket connection is initialized."""
        if not self._ws:
            try:
                from pybit.unified_trading import WebSocket
            except ImportError as exc:
                raise ImportError(
                    "pybit WebSocket not available. "
                    "Install/upgrade pybit: pip install --upgrade pybit"
                ) from exc

            self._ws = WebSocket(
                channel_type=self.category,
                testnet=self._testnet if hasattr(self, '_testnet') else False
            )
            logger.debug(f"Started WebSocket for {self.category}")

