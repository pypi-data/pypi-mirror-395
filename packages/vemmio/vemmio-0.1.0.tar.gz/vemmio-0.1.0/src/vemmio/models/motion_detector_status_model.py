"""Module holding MotionStatusModel dataclass."""

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options

from .base_model import BaseModel


@dataclass(kw_only=True)
class MotionState(BaseModel):
    """Enum holding relay states."""

    state: str = field(default="detected", metadata=field_options(alias="state"))

    timestamp: int = field(default=0, metadata=field_options(alias="timestamp"))


@dataclass(kw_only=True)
class Temperature(BaseModel):
    """Object holding temperature information."""

    value: int = field(default=0, metadata=field_options(alias="value"))

    units: str = field(default="C", metadata=field_options(alias="units"))

    timestamp: int = field(default=0, metadata=field_options(alias="timestamp"))


@dataclass(kw_only=True)
class Illumination(BaseModel):
    """Object holding illumination information."""

    value: int = field(default=0, metadata=field_options(alias="value"))

    units: str = field(default="lux", metadata=field_options(alias="units"))

    timestamp: int = field(default=0, metadata=field_options(alias="timestamp"))


@dataclass(kw_only=True)
class MotionDetectorStatusModel(BaseModel):
    """Object holding status information from Motion Detector Vemmio device."""

    motion: MotionState = field(
        default_factory=MotionState, metadata=field_options(alias="motion")
    )

    temperature: Temperature = field(
        default_factory=Temperature, metadata=field_options(alias="temperature")
    )

    illumination: Illumination = field(
        default_factory=Illumination, metadata=field_options(alias="illumination")
    )

    def update_from_dict(self, data: dict[str, Any]) -> "MotionStatusModel":
        """Return MotionStatusModel object from Vemmio API response.

        Args:
        ----
            data: Update the device object with the data received from a
                Vemmio device API.

        Returns:
        -------
            The updated MotionStatusModel object.

        """

        if _motion := data.get("motion"):
            self.motion = MotionState.from_dict(_motion)

        if _temperature := data.get("temperature"):
            self.temperature = Temperature.from_dict(_temperature)

        if _illumination := data.get("illumination"):
            self.illumination = Illumination.from_dict(_illumination)

        return self
