"""Factory class for creating Vemmio Device objects."""

from typing import Any

from .api.vemmioHttpRestApi import VemmioHttpRestApi
from .api.vemmioWebsocketApi import VemmioWebsocketApi
from .device import Device
from .implant import ImplantDevice
from .models import DeviceModel
from .motion import MotionDetectorDevice


class DeviceFactory:
    """Factory class for creating Vemmio Device objects."""

    @staticmethod
    async def create_device_from_dict(
        data: dict[str, Any], api: VemmioHttpRestApi, websocket_api: VemmioWebsocketApi
    ):
        """Create the Device object with the data received from a Vemmio device API.

        Args:
        ----
            data: Data received from a Vemmio device API.
            api: VemmioHttpRestApi instance for making API calls.
            websocket_api: VemmioWebsocketApi instance for websocket communication.

        Returns:
        -------
            The created Device object.

        """

        model = DeviceModel()
        model.create_from_dict(data)

        if (model.info.type is None) or (len(model.info.nodes) == 0):
            raise ValueError("Invalid device data received from Vemmio API")

        if model.info.type == "implant":
            device = ImplantDevice(model, api, websocket_api)
            await device.get_status()
            return device

        if model.info.type == "motion":
            device = MotionDetectorDevice(model, api, websocket_api)
            await device.get_status()
            return device

        return Device(model, api, websocket_api)
