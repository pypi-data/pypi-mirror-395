"""Vemmio Motion Device Class."""

import json
import logging

from .api import VemmioHttpRestApi, VemmioWebsocketApi
from .capability import (
    CAPABILITY_TYPES,
    Capability,
    IlluminationCapability,
    MotionDetectorCapability,
    TemperatureCapability,
)
from .device import Device, DeviceModel
from .models import MotionDetectorStatusModel

logger = logging.getLogger(__name__)


class MotionDetectorDevice(Device):
    """Class representing a Vemmio Motion Detector Device."""

    def __init__(
        self,
        model: DeviceModel,
        api: VemmioHttpRestApi,
        websocket_api: VemmioWebsocketApi,
    ) -> None:
        """Initialize the MotionDetectorDevice object."""
        super().__init__(model, api, websocket_api)

        self._motion_detector_capability = None
        self._temperature_capability = None
        self._illumination_capability = None
        self._status_model: list[tuple[MotionDetectorStatusModel, int]] = []

        # Get switch capabilities and store them separately
        for capability in self.capabilities:
            if isinstance(capability, MotionDetectorCapability):
                self._motion_detector_capability = capability
            elif isinstance(capability, TemperatureCapability):
                self._temperature_capability = capability
            elif isinstance(capability, IlluminationCapability):
                self._illumination_capability = capability

    async def get_status(self) -> None:
        """Get the status of the motion detector device."""
        try:
            status_response = await self.api.get_status()
            if not self._status_model:
                self._status_model = MotionDetectorStatusModel()
            self._status_model.update_from_dict(json.loads(status_response))
            logger.debug("Motion detector status model updated: %s", self._status_model)

        except Exception as e:
            logger.error("Error getting status: %s", e)

    def get_motion_status_state(self) -> bool | None:
        """Get the last known motion status state."""
        if self._status_model is not None:
            return self._status_model.motion.state == "detected"
        return None

    def get_motion_status_timestamp(self) -> int | None:
        """Get the last known motion status timestamp."""
        if self._status_model is not None:
            return self._status_model.motion.timestamp
        return None

    def get_temperature_status_value(self) -> int | None:
        """Get the last known temperature status value."""
        if self._status_model is not None:
            return self._status_model.temperature.value
        return None

    def get_temperature_status_units(self) -> str | None:
        """Get the last known temperature status units."""
        if self._status_model is not None:
            return self._status_model.temperature.units
        return None

    def get_temperature_status_timestamp(self) -> int | None:
        """Get the last known temperature status timestamp."""
        if self._status_model is not None:
            return self._status_model.temperature.timestamp
        return None

    def get_illumination_status_value(self) -> int | None:
        """Get the last known illumination status value."""
        if self._status_model is not None:
            return self._status_model.illumination.value
        return None

    def get_illumination_status_units(self) -> str | None:
        """Get the last known illumination status units."""
        if self._status_model is not None:
            return self._status_model.illumination.units
        return None

    def get_illumination_status_timestamp(self) -> int | None:
        """Get the last known illumination status timestamp."""
        if self._status_model is not None:
            return self._status_model.illumination.timestamp
        return None

    def _websocket_callback(self, data: dict) -> None:
        """Handle websocket updates for the motion detector device."""
        logger.debug("Received websocket update for motion detector device: %s", data)
        self._status_model.update_from_dict(data)
        super()._websocket_callback(data)
