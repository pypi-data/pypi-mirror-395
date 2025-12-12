"""Vemmio Implant Device Class."""

import json
import logging

from .api import VemmioHttpRestApi, VemmioWebsocketApi
from .device import Device, DeviceModel, OpenCloseCapability, SwitchCapability
from .models import ImplantStatusModel

logger = logging.getLogger(__name__)


class ImplantDevice(Device):
    """Class representing a Vemmio Implant Device."""

    def __init__(
        self,
        model: DeviceModel,
        api: VemmioHttpRestApi,
        websocket_api: VemmioWebsocketApi,
    ) -> None:
        """Initialize the ImplantDevice object."""
        super().__init__(model, api, websocket_api)

        self._switch_capabilities: list[tuple[SwitchCapability, int]] = []
        self._open_close_capabilities: list[tuple[OpenCloseCapability, int]] = []
        self._status_model: list[tuple[ImplantStatusModel, int]] = []

        switchIdx = 0
        openCloseIdx = 0

        # Get switch capabilities and store them separately
        for capability in self.capabilities:
            if isinstance(capability, SwitchCapability):
                self._switch_capabilities.append((capability, switchIdx))
                switchIdx += 1
            elif isinstance(capability, OpenCloseCapability):
                self._open_close_capabilities.append((capability, openCloseIdx))
                openCloseIdx += 1

        logger.debug(
            "Implant device switch capabilities: %s", self._switch_capabilities
        )

    async def async_turn_on_switch_by_uuid_and_id(self, uuid: str, id: int) -> None:
        """Turn on the implant's device switch."""
        logger.debug("Turning on implant device switch with uuid %s id: %s", uuid, id)

        # Check if the switch capability exists and store index
        capability_index = next(
            (
                index
                for index, capability in enumerate(self._switch_capabilities)
                if capability[0].node_uuid == uuid and capability[0].id == id
            ),
            None,
        )
        if capability_index is None:
            logger.warning("No switch capability found for uuid %s id: %s", uuid, id)
            return

        await self.async_turn_on_switch(capability_index)

    async def async_turn_on_switch(self, switch_index: int) -> None:
        """Turn on the implant's device switch by index."""
        logger.debug("Turning on implant device switch with index %s", switch_index)

        await self.api.change_relay_state(switch_index, True)

    async def async_turn_off_switch_by_uuid_and_id(self, uuid: str, id: int) -> None:
        """Turn off the implant's device switch."""
        logger.debug("Turning off implant device switch with uuid %s id: %s", uuid, id)

        capability_index = next(
            (
                index
                for index, capability in enumerate(self._switch_capabilities)
                if capability[0].node_uuid == uuid and capability[0].id == id
            ),
            None,
        )
        if capability_index is None:
            logger.warning("No switch capability found for uuid %s id: %s", uuid, id)
            return
        logger.debug(
            "Turning off implant device switch with index %s", capability_index
        )

        await self.async_turn_off_switch(capability_index)

    async def async_turn_off_switch(self, switch_index: int) -> None:
        """Turn off the implant's device switch by index."""
        logger.debug("Turning off implant device switch with index %s", switch_index)

        await self.api.change_relay_state(switch_index, False)

    async def get_status(self) -> None:
        """Get the status of the implant device."""
        try:
            status_response = await self.api.get_status()
            if not self._status_model:
                self._status_model = ImplantStatusModel()
            self._status_model.update_from_dict(json.loads(status_response))

        except Exception as e:
            logger.error("Error getting status: %s", e)

    def _websocket_callback(self, data: dict) -> None:
        """Handle websocket updates for the implant device."""
        logger.debug("Received websocket update for implant device: %s", data)
        self._status_model.update_from_dict(data)
        super()._websocket_callback(data)

    def get_relay_state(self, uuid: str, id: int) -> bool:
        """Get the relay state of a switch capability.

        Args:
        ----
            uuid: UUID of the switch capability to query.
            id: ID of the switch capability to query.

        Returns:
        -------
            The current state of the relay (True for ON, False for OFF).

        """
        capability_index = next(
            (
                index
                for index, capability in enumerate(self._switch_capabilities)
                if capability[0].node_uuid == uuid and capability[0].id == id
            ),
            None,
        )

        if capability_index is None:
            logger.warning("No switch capability found for uuid %s id: %s", uuid, id)
            return False

        logger.debug(
            "Getting relay state for implant device switch uuid %s and id %s with index %s",
            uuid,
            id,
            capability_index,
        )
        return self._status_model.relays[capability_index].state == "on"

    def get_input_state(self, uuid: str, id: int) -> bool:
        """Get the input state of a switch capability.

        Args:
        ----
            uuid: UUID of the switch capability to query.
            id: ID of the switch capability to query.

        Returns:
        -------
            The current state of the input (True for ON, False for OFF).

        """
        capability_index = next(
            (
                index
                for index, capability in enumerate(self._open_close_capabilities)
                if capability[0].node_uuid == uuid and capability[0].id == id
            ),
            None,
        )

        if capability_index is None:
            logger.warning("No input capability found for uuid %s id: %s", uuid, id)
            return False

        return self._status_model.inputs[capability_index].state == "open"
