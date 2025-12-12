"""Generic WebSocket client for streaming data."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

try:
    import websockets

    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False


logger = logging.getLogger(__name__)


class WebSocketClient:
    """Generic WebSocket client with reconnection and heartbeat.

    Example:
        >>> client = WebSocketClient("wss://example.com/stream")
        >>> client.on_message = lambda msg: print(msg)
        >>> asyncio.run(client.connect())
    """

    def __init__(
        self,
        url: str,
        reconnect_interval: int = 5,
        heartbeat_interval: int = 30,
    ) -> None:
        """Initialize WebSocket client.

        Args:
            url: WebSocket URL
            reconnect_interval: Seconds between reconnection attempts
            heartbeat_interval: Seconds between heartbeat pings
        """
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets package required for live streaming. "
                "Install with: pip install websockets"
            )

        self.url = url
        self.reconnect_interval = reconnect_interval
        self.heartbeat_interval = heartbeat_interval

        self._ws: Any = None
        self._running = False
        self._subscriptions: set[str] = set()

        # Callbacks
        self.on_message: Callable[[dict], None] | None = None
        self.on_connect: Callable[[], None] | None = None
        self.on_disconnect: Callable[[], None] | None = None
        self.on_error: Callable[[Exception], None] | None = None

    async def connect(self) -> None:
        """Connect to WebSocket and start message loop."""
        self._running = True

        while self._running:
            try:
                async with websockets.connect(self.url) as ws:
                    self._ws = ws
                    logger.info(f"Connected to {self.url}")

                    if self.on_connect:
                        self.on_connect()

                    # Start message handler
                    await self._handle_messages()

            except Exception as e:
                logger.error(f"WebSocket error: {e}")

                if self.on_error:
                    self.on_error(e)

                if self._running:
                    logger.info(f"Reconnecting in {self.reconnect_interval}s...")
                    await asyncio.sleep(self.reconnect_interval)

            finally:
                if self.on_disconnect:
                    self.on_disconnect()

    async def _handle_messages(self) -> None:
        """Handle incoming messages."""
        try:
            if self._ws is None:
                return

            async for message in self._ws:
                try:
                    data = json.loads(message)

                    if self.on_message:
                        self.on_message(data)

                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON: {message}")

        except websockets.exceptions.ConnectionClosed:
            logger.warning("Connection closed")

    async def send(self, message: dict | str) -> None:
        """Send message to WebSocket.

        Args:
            message: Message to send (dict or JSON string)
        """
        if self._ws is None:
            raise RuntimeError("Not connected")
        if getattr(self._ws, "closed", False):
            raise RuntimeError("Connection is closed")

        if isinstance(message, dict):
            message = json.dumps(message)

        await self._ws.send(message)

    def disconnect(self) -> None:
        """Disconnect from WebSocket."""
        self._running = False
