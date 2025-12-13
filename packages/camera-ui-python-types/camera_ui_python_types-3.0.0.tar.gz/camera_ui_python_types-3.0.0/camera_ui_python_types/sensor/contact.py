"""Contact sensor types and classes."""

from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import SensorCategory, SensorType


class ContactProperty(str, Enum):
    """Contact sensor properties."""

    Detected = "detected"


@runtime_checkable
class ContactSensorLike(SensorLike, Protocol):
    """Protocol for contact sensor type checking."""

    @property
    def detected(self) -> bool:
        """Whether contact is detected (door/window open)."""
        ...


class ContactSensor(Sensor[dict[str, object], dict[str, object], str]):
    """
    Contact sensor for door/window open/closed detection.

    Use this class for door/window sensors.
    """

    _requires_frames = False

    @property
    def type(self) -> SensorType:
        return SensorType.Contact

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Sensor

    @property
    def detected(self) -> bool:
        """Whether contact is detected (door/window open)."""
        return self.getPropertyValue(ContactProperty.Detected) or False

    @detected.setter
    def detected(self, value: bool) -> None:
        self._setProperty(ContactProperty.Detected, value)
