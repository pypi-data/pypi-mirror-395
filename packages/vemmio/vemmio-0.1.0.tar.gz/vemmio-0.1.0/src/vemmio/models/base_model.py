"""Module holding Vemmio data models."""

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin


class BaseModel(DataClassORJSONMixin):
    """Base model class for Vemmio data models."""

    class Config(BaseConfig):
        """Configuration for Mashumaro serialization."""

        debug = False