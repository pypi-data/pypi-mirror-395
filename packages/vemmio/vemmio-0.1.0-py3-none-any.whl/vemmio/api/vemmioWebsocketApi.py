"""Vemmio WebSocket API Client."""

from collections.abc import Callable
import logging
import socket
from typing import Any

import aiohttp
import orjson
from yarl import URL

from vemmio.exceptions import VemmioConnectionError, VemmioError

logger = logging.getLogger(__name__)


class VemmioWebsocketApi:
    """WebSocket API client for Vemmio devices.

    This class provides WebSocket connectivity to Vemmio devices, allowing
    real-time communication and message handling.

    Attributes:
    ----------
    host : str
        The hostname or IP address of the Vemmio device.
    session : aiohttp.ClientSession | None
        The aiohttp session to use for WebSocket connections.

    Methods:
    -------
    connect() -> None
        Establish WebSocket connection to the device.
    disconnect() -> None
        Close the WebSocket connection.
    listen(callback) -> None
        Listen for incoming WebSocket messages.
    is_connected() -> bool
        Check if WebSocket is currently connected.
    set_close_callback(callback) -> None
        Set callback function to be called when connection closes.
    """

    def __init__(
        self,
        host: str,
        session: aiohttp.ClientSession | None = None,
        on_close_callback: Callable[[], None] | None = None,
    ) -> None:
        """Initialize the Vemmio WebSocket API client."""
        self.host = host
        self.session = session
        self._is_connected = False
        self._on_close_callback = on_close_callback
        self._client: aiohttp.ClientWebSocketResponse | None = None

    def set_close_callback(self, callback: Callable[[], None] | None) -> None:
        """Set or update the callback to be called when the WebSocket connection is closed."""
        self._on_close_callback = callback

    async def connect(self) -> None:
        """Connect to the WebSocket of a Vemmio device."""
        if self._is_connected:
            return

        url = URL.build(scheme="ws", host=self.host, port=80, path="/ws")
        logger.debug("Connecting to WebSocket at %s", url)

        try:
            self._client = await self.session.ws_connect(url=url, heartbeat=30)
            self._is_connected = True
            logger.debug("WebSocket connection established")
        except (
            aiohttp.WSServerHandshakeError,
            aiohttp.ClientConnectionError,
            socket.gaierror,
        ) as exception:
            raise VemmioConnectionError from exception

    async def disconnect(self) -> None:
        """Disconnect from the WebSocket of a Vemmio device."""
        if not self._client or not self._is_connected:
            return

        self._is_connected = False
        await self._client.close()

        logger.debug("WebSocket connection disconnected")

        # Call the close callback if it's set
        if self._on_close_callback:
            self._on_close_callback()

    async def listen(self, callback: Callable[[Any], None]) -> None:
        """Listen for messages from the WebSocket."""
        if not self._client or not self._is_connected:
            raise VemmioError("WebSocket is not connected.")

        try:
            while not self._client.closed:
                msg = await self._client.receive()

                if msg.type == aiohttp.WSMsgType.TEXT:
                    if not callback:
                        logger.warning(
                            "No callback provided, skipping message processing."
                        )
                        continue

                    json_data = orjson.loads(msg.data)
                    callback(json_data)
                elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.ERROR):
                    break
        finally:
            # Mark as disconnected and call close callback if connection was lost
            if self._is_connected:
                self._is_connected = False
                await self._client.close()
                if self._on_close_callback:
                    self._on_close_callback()

    def is_connected(self) -> bool:
        """Check if the WebSocket is connected."""
        return self._is_connected
