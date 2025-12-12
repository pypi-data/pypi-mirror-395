"""Module holding ImplantStatusModel class."""

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin

from .base_model import BaseModel


@dataclass(kw_only=True)
class RelayState(BaseModel):
    """Enum holding relay states."""

    name: str = field(default="Unknown", metadata=field_options(alias="name"))

    state: str = field(default="off", metadata=field_options(alias="state"))

    timestamp: int = field(default=0, metadata=field_options(alias="timestamp"))


@dataclass(kw_only=True)
class InputState(BaseModel):
    """Object holding input states from Implant Vemmio device."""

    name: str = field(default="Unknown", metadata=field_options(alias="name"))

    state: str = field(default="closed", metadata=field_options(alias="state"))

    timestamp: int = field(default=0, metadata=field_options(alias="timestamp"))


@dataclass(kw_only=True)
class ImplantStatusModel(BaseModel):
    """Object holding status information from Implant Vemmio device."""

    relays: list[RelayState] = field(
        default_factory=list, metadata=field_options(alias="relays")
    )

    inputs: list[InputState] = field(
        default_factory=list, metadata=field_options(alias="inputs")
    )

    def update_from_dict(self, data: dict[str, Any]) -> "ImplantStatusModel":
        """Return ImplantStatusModel object from Vemmio API response.

        Args:
        ----
            data: Update the device object with the data received from a
                Vemmio device API.

        Returns:
        -------
            The updated DeviceModel object.

        """

        if _relays := data.get("relays"):
            self.relays = [RelayState.from_dict(relay) for relay in _relays]

        if _inputs := data.get("inputs"):
            self.inputs = [InputState.from_dict(inp) for inp in _inputs]

        return self
