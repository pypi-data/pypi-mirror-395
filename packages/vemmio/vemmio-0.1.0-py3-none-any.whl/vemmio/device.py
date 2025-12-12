"""Class representing a Vemmio device."""

import asyncio
from collections.abc import Callable
import logging
from typing import Any

import aiohttp

from .api import VemmioHttpRestApi, VemmioWebsocketApi
from .capability import (
    CAPABILITY_TYPES,
    Capability,
    IlluminationCapability,
    MotionDetectorCapability,
    OpenCloseCapability,
    SwitchCapability,
    TemperatureCapability,
)
from .models import DeviceModel

logger = logging.getLogger(__name__)


class Device:
    """Class representing a Vemmio device."""

    def __init__(
        self,
        model: DeviceModel,
        api: VemmioHttpRestApi,
        websocket_api: VemmioWebsocketApi,
    ) -> None:
        """Initialize the Device object."""
        self.model = model
        self.capabilities = []
        self.api = api
        self.websocket_api = websocket_api
        self.websocket_api.set_close_callback(self._websocket_close_callback)
        self._build_capabilities()
        self._websocket_enabled = False
        self._websocket_handler = None
        self._status_update_callbacks = {}

    def update_from_dict(self, data: dict[str, Any]) -> "Device":
        """Update the Device object with the data received from a Vemmio device API.

        Args:
        ----
            data: Data received from a Vemmio device API.

        Returns:
        -------
            The updated Device object.

        """
        self.model.update_from_dict(data)

        return self

    def __repr__(self) -> str:
        """Return a string representation of the Device object."""
        return f"Device(capabilities={self.capabilities})"

    def _build_capabilities(self) -> None:
        """Build capability objects for each node in the device."""
        cap_id = 0

        self.capabilities = []

        for node in self.model.info.nodes:
            if len(node.capabilities) == 0:
                continue

            cap_id = 0
            for cap in node.capabilities:
                logger.debug("Try adding capability: %s", cap)

                if cap in CAPABILITY_TYPES:
                    cap_id += 1
                    capability_obj: Capability | None = None

                    if cap == "switch":
                        capability_obj = SwitchCapability(
                            name=cap, node_uuid=node.uuid, id=cap_id
                        )
                        logger.debug("Built capability: %s", capability_obj)

                    if cap == "openClose":
                        capability_obj = OpenCloseCapability(
                            name=cap, node_uuid=node.uuid, id=cap_id
                        )
                        logger.debug("Built capability: %s", capability_obj)

                    if cap == "motionDetector":
                        capability_obj = MotionDetectorCapability(
                            name=cap, node_uuid=node.uuid, id=cap_id
                        )
                        logger.debug("Built capability: %s", capability_obj)

                    if cap == "temperature":
                        capability_obj = TemperatureCapability(
                            name=cap, node_uuid=node.uuid, id=cap_id
                        )
                        logger.debug("Built capability: %s", capability_obj)

                    if cap == "illumination":
                        capability_obj = IlluminationCapability(
                            name=cap, node_uuid=node.uuid, id=cap_id
                        )
                        logger.debug("Built capability: %s", capability_obj)

                    if capability_obj:
                        self.capabilities.append(capability_obj)

    def get_capabilities(self, type: str) -> list[Capability]:
        """Get capabilities of a specific type.

        Args:
        ----
            type: The type of capability to filter by.

        Returns:
        -------
            A list of capabilities of the specified type.

        """
        return [cap for cap in self.capabilities if cap.name == type]

    def enable_websocket(self) -> None:
        """Enable websocket communication."""
        self._websocket_enabled = True
        if not self._websocket_handler:
            self._websocket_handler = asyncio.create_task(self.websocket_handler_task())

    async def websocket_handler_task(self):
        """Websocket handler task to maintain connection and listen for updates."""
        while self._websocket_enabled:
            if not self.is_websocket_connected():
                logger.debug("Enabling WebSocket communication...")
                try:
                    await self.api.enable_home_assistant_integration()
                    await self.websocket_api.connect()
                except Exception as e:
                    logger.error("Error connecting to WebSocket: %s", e)
            try:
                await self.websocket_api.listen(callback=self._websocket_callback)
            except Exception as e:
                logger.error("Error during WebSocket listen: %s", e)
            logger.debug("WebSocket listen ended.")
            await asyncio.sleep(60)  # Check every 60 seconds

        await self.websocket_api.disconnect()

    def disable_websocket(self):
        """Disable websocket communication."""
        self._websocket_enabled = False

        if self._websocket_handler:
            self._websocket_handler.cancel()
            self._websocket_handler = None

    def is_websocket_connected(self) -> bool:
        """Check if the websocket is connected."""
        return self.websocket_api.is_connected()

    def register_status_update_callback(
        self, uuid_with_id: str, callback: Callable[[], None]
    ) -> None:
        """Register a callback for websocket updates."""
        self._status_update_callbacks[uuid_with_id] = callback

    def _websocket_callback(self, data: dict) -> None:
        # Call the registered callbacks on websocket update
        logger.debug("Device::_websocket_callback called with json: %s", data)
        logger.debug(
            "Invoking %d registered status update callbacks.",
            len(self._status_update_callbacks),
        )
        for callback in self._status_update_callbacks.values():
            callback()

    def _websocket_close_callback(self) -> None:
        logger.debug("WebSocket connection closed.")
