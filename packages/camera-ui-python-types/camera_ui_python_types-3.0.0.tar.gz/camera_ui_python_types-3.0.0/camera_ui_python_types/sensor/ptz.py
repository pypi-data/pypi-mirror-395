"""PTZ control sensor types and classes."""

from __future__ import annotations

from enum import Enum
from typing import Protocol, cast, runtime_checkable

from .base import Sensor, SensorLike
from .types import PTZDirection, PTZPosition, SensorCategory, SensorType


class PTZCapability(str, Enum):
    """PTZ capabilities - describes what features this PTZ control supports."""

    Pan = "pan"
    Tilt = "tilt"
    Zoom = "zoom"
    Presets = "presets"
    Home = "home"


class PTZProperty(str, Enum):
    """PTZ control properties."""

    Position = "position"
    Moving = "moving"
    Presets = "presets"
    Velocity = "velocity"
    TargetPreset = "targetPreset"


@runtime_checkable
class PTZControlLike(SensorLike, Protocol):
    """Protocol for PTZ control type checking."""

    @property
    def position(self) -> PTZPosition:
        """Current PTZ position."""
        ...

    @property
    def moving(self) -> bool:
        """Whether PTZ is currently moving."""
        ...

    @property
    def presets(self) -> list[str]:
        """Available presets."""
        ...

    @property
    def velocity(self) -> PTZDirection | None:
        """Current velocity (for continuous move)."""
        ...

    @property
    def targetPreset(self) -> str | None:
        """Target preset to go to."""
        ...

    def goHome(self) -> None:
        """Go to home position."""
        ...

    def pan(self, angle: float) -> None:
        """Pan to specific angle."""
        ...

    def tilt(self, angle: float) -> None:
        """Tilt to specific angle."""
        ...

    def zoom(self, level: float) -> None:
        """Zoom to specific level."""
        ...

    def continuousMove(self, velocity: PTZDirection) -> None:
        """Start continuous movement."""
        ...

    def stop(self) -> None:
        """Stop all movement."""
        ...

    def goToPreset(self, preset: str) -> None:
        """Go to a saved preset."""
        ...


class PTZControl(Sensor[dict[str, object], dict[str, object], PTZCapability]):
    """
    PTZ Control.

    Bidirectional control for camera pan/tilt/zoom.

    Example:
        ```python
        # Move to absolute position
        ptz.position = {"pan": 45, "tilt": -10, "zoom": 0.5}

        # Continuous move
        ptz.continuousMove({"panSpeed": 1, "tiltSpeed": 0, "zoomSpeed": 0})

        # Stop all movement
        ptz.stop()

        # Go to preset
        ptz.goToPreset("Entrance")

        # Go to home position
        ptz.goHome()
        ```
    """

    _requires_frames = False

    def __init__(self, camera_id: str, name: str = "PTZ") -> None:
        super().__init__(camera_id, name)
        # Initialize defaults
        self._setProperty(PTZProperty.Position, {"pan": 0, "tilt": 0, "zoom": 0})
        self._setProperty(PTZProperty.Moving, False)
        self._setProperty(PTZProperty.Presets, [])

    @property
    def type(self) -> SensorType:
        return SensorType.PTZ

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Control

    @property
    def position(self) -> PTZPosition:
        """Current PTZ position."""
        pos = self.getPropertyValue(PTZProperty.Position)
        if isinstance(pos, dict) and "pan" in pos and "tilt" in pos and "zoom" in pos:
            return cast(PTZPosition, pos)
        return {"pan": 0.0, "tilt": 0.0, "zoom": 0.0}

    @position.setter
    def position(self, value: PTZPosition) -> None:
        self._setProperty(PTZProperty.Position, value)

    @property
    def moving(self) -> bool:
        """Whether PTZ is currently moving."""
        return self.getPropertyValue(PTZProperty.Moving) or False

    @moving.setter
    def moving(self, value: bool) -> None:
        self._setProperty(PTZProperty.Moving, value)

    @property
    def presets(self) -> list[str]:
        """Available presets."""
        return self.getPropertyValue(PTZProperty.Presets) or []

    @presets.setter
    def presets(self, value: list[str]) -> None:
        self._setProperty(PTZProperty.Presets, value)

    @property
    def velocity(self) -> PTZDirection | None:
        """Current velocity (for continuous move)."""
        return self.getPropertyValue(PTZProperty.Velocity)

    @velocity.setter
    def velocity(self, value: PTZDirection | None) -> None:
        self._setProperty(PTZProperty.Velocity, value)

    @property
    def targetPreset(self) -> str | None:
        """Target preset to go to."""
        return self.getPropertyValue(PTZProperty.TargetPreset)

    @targetPreset.setter
    def targetPreset(self, value: str | None) -> None:
        self._setProperty(PTZProperty.TargetPreset, value)

    # RPC methods (camelCase for compatibility)

    def goHome(self) -> None:
        """Go to home position (pan: 0, tilt: 0, zoom: 0)."""
        self.position = {"pan": 0, "tilt": 0, "zoom": 0}

    def pan(self, angle: float) -> None:
        """
        Pan to specific angle.

        Args:
            angle: Pan angle in degrees
        """
        current = self.position
        self.position = {**current, "pan": angle}

    def tilt(self, angle: float) -> None:
        """
        Tilt to specific angle.

        Args:
            angle: Tilt angle in degrees
        """
        current = self.position
        self.position = {**current, "tilt": angle}

    def zoom(self, level: float) -> None:
        """
        Zoom to specific level (0-1).

        Args:
            level: Zoom level between 0 and 1
        """
        current = self.position
        self.position = {**current, "zoom": max(0, min(1, level))}

    def continuousMove(self, velocity: PTZDirection) -> None:
        """
        Start continuous movement.

        Args:
            velocity: Movement speed for each axis (-1 to 1)
        """
        self.velocity = velocity

    def stop(self) -> None:
        """Stop all movement."""
        self.velocity = {"panSpeed": 0, "tiltSpeed": 0, "zoomSpeed": 0}

    def goToPreset(self, preset: str) -> None:
        """
        Go to a saved preset.

        Args:
            preset: Preset name
        """
        self.targetPreset = preset
