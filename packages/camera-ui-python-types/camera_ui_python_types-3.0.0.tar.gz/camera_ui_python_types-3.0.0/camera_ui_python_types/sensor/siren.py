"""Siren control sensor types and classes."""

from __future__ import annotations

import asyncio
from enum import Enum
from typing import Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import SensorCategory, SensorType


class SirenCapability(str, Enum):
    """Siren capabilities - describes what features this siren supports."""

    Volume = "volume"
    Modes = "modes"


class SirenProperty(str, Enum):
    """Siren control properties."""

    Active = "active"
    Volume = "volume"


@runtime_checkable
class SirenControlLike(SensorLike, Protocol):
    """Protocol for siren control type checking."""

    @property
    def active(self) -> bool:
        """Whether siren is active."""
        ...

    @property
    def volume(self) -> int:
        """Volume level (0-100)."""
        ...

    def activate(self) -> None:
        """Activate siren."""
        ...

    def deactivate(self) -> None:
        """Deactivate siren."""
        ...

    async def soundFor(self, durationMs: int) -> None:
        """Sound siren for a duration."""
        ...


class SirenControl(Sensor[dict[str, object], dict[str, object], SirenCapability]):
    """
    Siren Control.

    Bidirectional control for camera siren/alarm.
    Properties can be set directly: `siren.active = True`
    """

    _requires_frames = False

    def __init__(self, camera_id: str, name: str = "Siren") -> None:
        super().__init__(camera_id, name)
        # Initialize defaults
        self._setProperty(SirenProperty.Active, False)
        self._setProperty(SirenProperty.Volume, 100)

    @property
    def type(self) -> SensorType:
        return SensorType.Siren

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Control

    @property
    def active(self) -> bool:
        """Whether siren is active."""
        return self.getPropertyValue(SirenProperty.Active) or False

    @active.setter
    def active(self, value: bool) -> None:
        self._setProperty(SirenProperty.Active, value)

    @property
    def volume(self) -> int:
        """Volume level (0-100)."""
        return self.getPropertyValue(SirenProperty.Volume) or 100

    @volume.setter
    def volume(self, value: int) -> None:
        self._setProperty(SirenProperty.Volume, max(0, min(100, value)))

    # RPC methods (camelCase for compatibility)

    def activate(self) -> None:
        """Activate siren."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate siren."""
        self.active = False

    async def soundFor(self, durationMs: int) -> None:
        """
        Sound siren for a duration.

        Args:
            durationMs: Duration to sound siren in milliseconds
        """
        self.activate()
        await asyncio.sleep(durationMs / 1000)
        self.deactivate()
