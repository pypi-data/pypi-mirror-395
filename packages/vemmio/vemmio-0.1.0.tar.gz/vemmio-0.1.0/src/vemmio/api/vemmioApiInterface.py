"""Vemmio API interface definition."""

from abc import ABC, abstractmethod
from typing import Any


class VemmioApiInterface(ABC):
    """Abstract interface for Vemmio API implementations."""

    @abstractmethod
    async def get_status(self) -> dict[str, Any]:
        """Get device information."""
