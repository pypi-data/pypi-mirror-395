from dataclasses import dataclass
import json
import logging
from typing import Self

import aiohttp
import backoff

from .api import VemmioHttpRestApi, VemmioWebsocketApi
from .device import Device
from .device_factory import DeviceFactory
from .exceptions import VemmioEmptyResponseError

logger = logging.getLogger(__name__)

# Set logger to debug level for detailed output
logger.setLevel(logging.DEBUG)


class Vemmio:
    """Main class for handling connections with Vemmio device."""

    def __init__(
        self,
        host: str,
        session: aiohttp.ClientSession | None = None,
        request_timeout: float = 8.0,
    ) -> None:
        """Initialize the Vemmio client.

        Args:
        ----
            host: Hostname or IP address of the Vemmio device.
            session: Optional aiohttp ClientSession to use for requests.
            request_timeout: Timeout for requests to the Vemmio device.

        """
        self.host = host
        self.request_timeout = request_timeout
        self.session = session
        self._device = None
        self._api = VemmioHttpRestApi(host=self.host, session=self.session)
        self._websocket_api = VemmioWebsocketApi(host=self.host, session=self.session)

    @backoff.on_exception(
        backoff.expo,
        VemmioEmptyResponseError,
        max_tries=3,
        logger=None,
    )
    async def update(self) -> Device:
        """Get all information about the device in a single call.

        This method updates all Vemmio information available with a single API
        call.

        Returns:
        -------
            Vemmio Device data.

        Raises:
        ------
            VemmioEmptyResponseError: The Vemmio device returned an empty response.

        """
        if not (data := await self._api.request("/api/v1/vemmio")):
            msg = (
                f"Vemmio device at {self.host} returned an empty API"
                " response on full update",
            )
            raise VemmioEmptyResponseError(msg)

        data = json.loads(data)

        if not self._device:
            self._device = await DeviceFactory.create_device_from_dict(
                {"info": data}, self._api, self._websocket_api
            )
        else:
            self._device.update_from_dict({"info": data})

        return self._device

    async def close(self) -> None:
        """Close session."""
        logger.debug("Close called")
        await self._api.close()
        if self.session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns:
        -------
            The WLED object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
