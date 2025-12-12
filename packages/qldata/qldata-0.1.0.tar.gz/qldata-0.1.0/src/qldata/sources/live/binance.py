"""Live streaming source for Binance public trades."""

from __future__ import annotations

import asyncio
import json
import threading
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

import pandas as pd

try:
    import websockets  # type: ignore

    WEBSOCKETS_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    WEBSOCKETS_AVAILABLE = False

from qldata.sources.live.base import StreamingSource
from qldata.common.logger import get_logger

if WEBSOCKETS_AVAILABLE:  # type: ignore[truthy-bool]
    try:
        from websockets.exceptions import (
            ConnectionClosedError,
            ConnectionClosedOK,
            InvalidStatus,
            InvalidURI,
        )
    except ImportError:  # pragma: no cover - backwards compat
        from websockets.exceptions import (  # type: ignore[no-redef]
            ConnectionClosedError,
            ConnectionClosedOK,
            InvalidStatusCode as InvalidStatus,
            InvalidURI,
        )

logger = get_logger(__name__)


_WS_BASE = {
    "spot": "wss://stream.binance.com:9443",
    "usdm": "wss://fstream.binance.com",
    "coinm": "wss://dstream.binance.com",
}


class BinanceLiveSource(StreamingSource):
    """Stream live trades from Binance (public, no auth).

    Emits DataFrame batches with columns: timestamp, symbol, price, volume, bid, ask.
    """

    def __init__(
        self,
        interval: float = 1.0,
        category: str = "spot",
        kline_interval: str | None = None,
    ) -> None:
        if not WEBSOCKETS_AVAILABLE:  # pragma: no cover - runtime guard
            raise ImportError("websockets package required for live streaming. Install with: pip install websockets")

        self.interval = interval
        self._category = category
        self._kline_interval = kline_interval
        self._symbols: list[str] = []
        self._callback: Callable[[pd.DataFrame], None] | None = None
        self._error_cb: Callable[[Exception], None] | None = None
        self._running = False
        self._thread: threading.Thread | None = None
        self._error_count = 0

    def subscribe(self, symbols: list[str], callback: Callable[[pd.DataFrame], None], **kwargs: Any) -> None:
        """Subscribe to symbols; restarts stream if already running."""
        self._symbols = [s.upper() for s in symbols]
        self._callback = callback
        self._error_cb = kwargs.get("on_error")
        if self._running:
            self.stop()
            self.start()

    def unsubscribe(self, symbols: list[str] | None = None) -> None:
        """Unsubscribe (clears all if None)."""
        if symbols is None:
            self._symbols = []
        else:
            remove = {s.upper() for s in symbols}
            self._symbols = [s for s in self._symbols if s not in remove]
        if self._running:
            self.stop()

    def start(self) -> None:
        """Start streaming in a background thread."""
        if self._running or not self._symbols:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop streaming."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    @property
    def is_connected(self) -> bool:
        return self._running

    def _build_url(self) -> str:
        if self._kline_interval:
            streams = "/".join(f"{sym.lower()}@kline_{self._kline_interval}" for sym in self._symbols)
        else:
            streams = "/".join(f"{sym.lower()}@trade" for sym in self._symbols)
        base = _WS_BASE.get(self._category, _WS_BASE["spot"])
        return f"{base}/stream?streams={streams}"

    def _run(self) -> None:
        async def runner() -> None:
            backoff = self.interval
            while self._running:
                try:
                    url = self._build_url()
                    async with websockets.connect(url, ping_interval=None) as ws:  # type: ignore[attr-defined]
                        backoff = self.interval
                        while self._running:
                            msg = await ws.recv()
                            self._handle_message(msg)
                except (InvalidStatus, InvalidURI, ValueError) as exc:  # type: ignore[misc]
                    self._emit_error(exc, fatal=True)
                    self._running = False
                    break
                except (ConnectionClosedError, ConnectionClosedOK) as exc:  # type: ignore[misc]
                    if not self._running:
                        break
                    self._emit_error(exc, fatal=False)
                except Exception as exc:
                    if not self._running:
                        break
                    self._emit_error(exc, fatal=False)

                if self._running:
                    await asyncio.sleep(min(backoff, 30.0))
                    backoff = min(backoff * 2, 30.0)

        asyncio.run(runner())

    def _handle_message(self, message: str) -> None:
        if self._callback is None:
            return
        try:
            payload = json.loads(message)
            data = payload.get("data", {})
            if not data:
                return
            if self._kline_interval and "k" in data:
                k = data["k"]
                symbol = k.get("s")
                open_time = datetime.fromtimestamp(k.get("t", 0) / 1000, tz=timezone.utc)
                close_time = datetime.fromtimestamp(k.get("T", 0) / 1000, tz=timezone.utc)
                df = pd.DataFrame(
                    [
                        {
                            "timestamp": close_time,
                            "symbol": symbol,
                            "price": float(k.get("c", 0)),
                            "volume": float(k.get("v", 0)),
                            "bid": None,
                            "ask": None,
                            "open": float(k.get("o", 0)),
                            "high": float(k.get("h", 0)),
                            "low": float(k.get("l", 0)),
                            "close": float(k.get("c", 0)),
                            "open_time": open_time,
                        }
                    ]
                )
                self._callback(df)
                return

            symbol = data.get("s")
            price = float(data.get("p", 0))
            volume = float(data.get("q", 0))
            ts_ms = data.get("E")
            timestamp = (
                datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
                if ts_ms
                else datetime.now(timezone.utc)
            )
            df = pd.DataFrame(
                [
                    {
                        "timestamp": timestamp,
                        "symbol": symbol,
                        "price": price,
                        "volume": volume,
                        "bid": None,
                        "ask": None,
                    }
                ]
            )
            self._callback(df)
        except Exception as exc:
            self._emit_error(exc, fatal=False)

    def _emit_error(self, exc: Exception, fatal: bool) -> None:
        """Report an error to the provided callback and log with context."""
        self._error_count += 1
        if fatal:
            logger.error("Binance stream fatal error: %s", exc)
        else:
            logger.warning("Binance stream error: %s", exc)

        if self._error_cb:
            try:
                self._error_cb(exc)
            except Exception:  # pragma: no cover - defensive
                logger.exception("Binance error callback raised")
