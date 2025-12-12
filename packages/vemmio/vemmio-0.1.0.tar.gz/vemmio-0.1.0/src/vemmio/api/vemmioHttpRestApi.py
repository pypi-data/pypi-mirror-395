"""Vemmio HTTP REST API Client."""

import asyncio
import logging
import socket
from typing import Any

import aiohttp
import backoff
import orjson
from yarl import URL

from vemmio.exceptions import (
    VemmioConnectionError,
    VemmioConnectionTimeoutError,
    VemmioError,
)

from .vemmioApiInterface import VemmioApiInterface

logger = logging.getLogger(__name__)


class VemmioHttpRestApi(VemmioApiInterface):
    """HTTP REST API client for Vemmio devices.

    This class provides an interface to communicate with Vemmio devices
    over HTTP using REST API endpoints.

    Attributes:
    ----------
    host : str
        Hostname or IP address of the Vemmio device.
    session : aiohttp.ClientSession | None
        Optional aiohttp ClientSession to use for requests.
    request_timeout : float
        Timeout for HTTP requests in seconds.
    """

    def __init__(
        self,
        host: str,
        session: aiohttp.ClientSession | None = None,
        request_timeout: float = 8.0,
    ) -> None:
        """Initialize the Vemmio HTTP API client.

        Args:
        ----
            host: Hostname or IP address of the Vemmio device.
            session: Optional aiohttp ClientSession to use for requests.
            request_timeout: Timeout for HTTP requests in seconds.
        """
        self.host = host
        self.session = session
        self.request_timeout = request_timeout
        self._close_session = False

    @backoff.on_exception(backoff.expo, VemmioConnectionError, max_tries=3, logger=None)
    async def request(
        self,
        uri: str = "",
        method: str = "GET",
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to a Vemmio device.

        A generic method for sending/handling HTTP requests done gainst
        the Vemmio device.

        Args:
        ----
            uri: Request URI, for example `/json/si`.
            method: HTTP method to use for the request.E.g., "GET" or "POST".
            data: Dictionary of data to send to the WLED device.

        Returns:
        -------
            A Python dictionary (JSON decoded) with the response from the
            Vemmio device.

        Raises:
        ------
            VemmioConnectionError: An error occurred while communication with
                the Vemmio device.
            VemmioConnectionTimeoutError: A timeout occurred while communicating
                with the Vemmio device.
            VemmioError: Received an unexpected response from the Vemmio device.

        """
        url = URL.build(scheme="http", host=self.host, port=80, path=uri)

        headers = {
            "Accept": "application/json, text/plain, */*",
        }

        if self.session is None:
            try:
                self.session = aiohttp.ClientSession()
                self._close_session = True
            except Exception as e:
                logger.error("Exception of session: %s", e)
                raise
        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    json=data,
                    headers=headers,
                )

            content_type = response.headers.get("Content-Type", "")

            if response.status // 100 in [4, 5]:
                contents = await response.read()
                response.close()

                if content_type == "application/json":
                    raise VemmioError(
                        response.status,
                        orjson.loads(contents),
                    )
                raise VemmioError(
                    response.status,
                    {"message": contents.decode("utf8")},
                )

            response_data = await response.text()
            if "application/json" in content_type:
                response_data = orjson.loads(response_data)

        except TimeoutError as exception:
            msg = f"Timeout occurred while connecting to Vemmio device at {self.host}"
            raise VemmioConnectionTimeoutError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = (
                f"Error occurred while communicating with Vemmio device at {self.host}"
            )
            raise VemmioConnectionError(msg) from exception

        return response_data

    async def close(self) -> None:
        """Close session."""
        logger.debug("API Close called")
        if self.session:
            await self.session.close()

    async def get_status(self) -> dict[str, Any]:
        """Get the status of the Vemmio device.

        Returns:
        -------
            A dictionary containing the status information of the device.

        """
        uri = "/api/v1/status"

        return await self.request(uri=uri, method="GET")

    async def change_relay_state(self, index: int, state: bool) -> None:
        """Change the relay state of a switch capability.

        Args:
        ----
            index: Index of the switch capability to change.
            state: Desired state of the relay (True for ON, False for OFF).

        """
        uri = f"/api/v1/relays/{index}/{'on' if state else 'off'}"

        await self.request(uri=uri, method="POST")

    async def get_relay_state(self, index: int) -> bool:
        """Get the relay state of a switch capability.

        Args:
        ----
            index: Index of the switch capability to query.

        Returns:
        -------
            The current state of the relay (True for ON, False for OFF).

        """

        response = await self.get_status()
        logger.debug("Response from get_status: %s", response)
        response = orjson.loads(response)

        relay_state = response.get("relays", [])[index].get("state", False)
        return relay_state == "on"

    async def enable_home_assistant_integration(self) -> None:
        """Enable Home Assistant integration on the Vemmio device."""
        uri = "/api/v1/settings/home_assistant"
        data = {"home_assistant_enabled": True}

        await self.request(uri=uri, method="POST", data=data)
