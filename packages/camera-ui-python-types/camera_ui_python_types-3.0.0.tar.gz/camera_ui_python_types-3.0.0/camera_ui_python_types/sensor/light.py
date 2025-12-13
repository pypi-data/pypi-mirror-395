"""Light control sensor types and classes."""

from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import SensorCategory, SensorType


class LightCapability(str, Enum):
    """Light capabilities - describes what features this light supports."""

    Brightness = "brightness"


class LightProperty(str, Enum):
    """Light control properties."""

    On = "on"
    Brightness = "brightness"


@runtime_checkable
class LightControlLike(SensorLike, Protocol):
    """Protocol for light control type checking."""

    @property
    def on(self) -> bool:
        """Whether light is on."""
        ...

    @property
    def brightness(self) -> int:
        """Brightness level (0-100)."""
        ...

    def turnOn(self) -> None:
        """Turn light on."""
        ...

    def turnOff(self) -> None:
        """Turn light off."""
        ...

    def toggle(self) -> None:
        """Toggle light state."""
        ...


class LightControl(Sensor[dict[str, object], dict[str, object], LightCapability]):
    """
    Light Control.

    Bidirectional control for camera spotlight/floodlight.
    Properties can be set directly: `light.on = True`
    """

    _requires_frames = False

    def __init__(self, camera_id: str, name: str = "Light") -> None:
        super().__init__(camera_id, name)
        # Initialize defaults
        self._setProperty(LightProperty.On, False)
        self._setProperty(LightProperty.Brightness, 100)

    @property
    def type(self) -> SensorType:
        return SensorType.Light

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Control

    @property
    def on(self) -> bool:
        """Whether light is on."""
        return self.getPropertyValue(LightProperty.On) or False

    @on.setter
    def on(self, value: bool) -> None:
        self._setProperty(LightProperty.On, value)

    @property
    def brightness(self) -> int:
        """Brightness level (0-100)."""
        return self.getPropertyValue(LightProperty.Brightness) or 100

    @brightness.setter
    def brightness(self, value: int) -> None:
        self._setProperty(LightProperty.Brightness, max(0, min(100, value)))

    # RPC methods (camelCase for compatibility)

    def turnOn(self) -> None:
        """Turn light on."""
        self.on = True

    def turnOff(self) -> None:
        """Turn light off."""
        self.on = False

    def toggle(self) -> None:
        """Toggle light state."""
        self.on = not self.on
