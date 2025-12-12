"""Live streaming source for Bybit public tickers."""

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


_CATEGORY_TO_URL = {
    "linear": "wss://stream.bybit.com/v5/public/linear",
    "inverse": "wss://stream.bybit.com/v5/public/inverse",
    "spot": "wss://stream.bybit.com/v5/public/spot",
}


class BybitLiveSource(StreamingSource):
    """Stream live tickers/klines from Bybit public websockets."""

    def __init__(self, category: str = "linear", kline_interval: str | None = None) -> None:
        if not WEBSOCKETS_AVAILABLE:  # pragma: no cover - runtime guard
            raise ImportError("websockets package required for live streaming. Install with: pip install websockets")

        self._category = category
        self._kline_interval = kline_interval
        self._symbols: list[str] = []
        self._callback: Callable[[pd.DataFrame], None] | None = None
        self._error_cb: Callable[[Exception], None] | None = None
        self._running = False
        self._thread: threading.Thread | None = None
        self._error_count = 0

    def subscribe(self, symbols: list[str], callback: Callable[[pd.DataFrame], None], **kwargs: Any) -> None:
        self._symbols = [s.upper() for s in symbols]
        self._callback = callback
        self._error_cb = kwargs.get("on_error")
        if self._running:
            self.stop()
            self.start()

    def unsubscribe(self, symbols: list[str] | None = None) -> None:
        if symbols is None:
            self._symbols = []
        else:
            remove = {s.upper() for s in symbols}
            self._symbols = [s for s in self._symbols if s not in remove]
        if self._running:
            self.stop()

    def start(self) -> None:
        if self._running or not self._symbols:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    @property
    def is_connected(self) -> bool:
        return self._running

    def _run(self) -> None:
        async def runner() -> None:
            backoff = 1.0
            while self._running:
                try:
                    url = _CATEGORY_TO_URL.get(self._category, _CATEGORY_TO_URL["linear"])
                    async with websockets.connect(url, ping_interval=None) as ws:  # type: ignore[attr-defined]
                        backoff = 1.0
                        topic_prefix = "tickers" if self._kline_interval is None else f"kline.{self._kline_interval}"
                        sub_msg = {
                            "op": "subscribe",
                            "args": [f"{topic_prefix}.{sym}" for sym in self._symbols],
                        }
                        await ws.send(json.dumps(sub_msg))

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
            data = payload.get("data")
            if not data:
                return
            if isinstance(data, dict):
                entries = [data]
            else:
                entries = data

            rows = []
            for item in entries:
                symbol = item.get("symbol")

                if self._kline_interval and "close" in item:
                    # Kline payload
                    timestamp = datetime.fromtimestamp(item.get("start", 0) / 1000, tz=timezone.utc)
                    rows.append(
                        {
                            "timestamp": timestamp,
                            "symbol": symbol,
                            "price": float(item.get("close", 0)),
                            "volume": float(item.get("turnover", 0)),
                            "bid": None,
                            "ask": None,
                            "open": float(item.get("open", 0)),
                            "high": float(item.get("high", 0)),
                            "low": float(item.get("low", 0)),
                            "close": float(item.get("close", 0)),
                        }
                    )
                    continue

                price = float(item.get("lastPrice", item.get("lastPrice", 0) or 0))
                bid = item.get("bid1Price")
                ask = item.get("ask1Price")
                volume = float(item.get("turnover24h", 0))
                timestamp = datetime.now(timezone.utc)

                rows.append(
                    {
                        "timestamp": timestamp,
                        "symbol": symbol,
                        "price": price,
                        "volume": volume,
                        "bid": float(bid) if bid else None,
                        "ask": float(ask) if ask else None,
                    }
                )

            if rows:
                df = pd.DataFrame(rows)
                self._callback(df)
        except Exception as exc:
            self._emit_error(exc, fatal=False)

    def _emit_error(self, exc: Exception, fatal: bool) -> None:
        """Report an error to the provided callback and log with context."""
        self._error_count += 1
        if fatal:
            logger.error("Bybit stream fatal error: %s", exc)
        else:
            logger.warning("Bybit stream error: %s", exc)

        if self._error_cb:
            try:
                self._error_cb(exc)
            except Exception:  # pragma: no cover - defensive
                logger.exception("Bybit error callback raised")
