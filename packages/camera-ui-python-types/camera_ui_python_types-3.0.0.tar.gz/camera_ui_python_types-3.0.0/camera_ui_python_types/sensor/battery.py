"""Battery info sensor types and classes."""

from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import ChargingState, SensorCategory, SensorType


class BatteryCapability(str, Enum):
    """Battery capabilities - describes what features this battery sensor supports."""

    LowBattery = "lowBattery"
    Charging = "charging"


class BatteryProperty(str, Enum):
    """Battery info properties."""

    Level = "level"
    Charging = "charging"
    Low = "low"


@runtime_checkable
class BatteryInfoLike(SensorLike, Protocol):
    """Protocol for battery info type checking."""

    @property
    def level(self) -> int:
        """Battery level (0-100)."""
        ...

    @property
    def charging(self) -> ChargingState:
        """Charging state."""
        ...

    @property
    def low(self) -> bool:
        """Whether battery is low."""
        ...

    def setBattery(self, level: int, charging: ChargingState | None = None) -> None:
        """Update battery state."""
        ...

    def isCharging(self) -> bool:
        """Check if battery is charging."""
        ...

    def isFullyCharged(self) -> bool:
        """Check if battery is fully charged."""
        ...


class BatteryInfo(Sensor[dict[str, object], dict[str, object], BatteryCapability]):
    """
    Battery Info.

    Read-only hardware status for battery-powered cameras.
    """

    _requires_frames = False
    lowBatteryThreshold: int = 20  # Threshold for low battery warning (default: 20%)

    def __init__(self, camera_id: str, name: str = "Battery") -> None:
        super().__init__(camera_id, name)
        # Initialize defaults
        self._setProperty(BatteryProperty.Level, 100)
        self._setProperty(BatteryProperty.Charging, ChargingState.NotCharging)
        self._setProperty(BatteryProperty.Low, False)

    @property
    def type(self) -> SensorType:
        return SensorType.Battery

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Info

    @property
    def level(self) -> int:
        """Battery level (0-100)."""
        return self.getPropertyValue(BatteryProperty.Level) or 100

    @level.setter
    def level(self, value: int) -> None:
        clamped_value = max(0, min(100, value))
        self._setProperty(BatteryProperty.Level, clamped_value)
        # Auto-update low battery state
        self._setProperty(BatteryProperty.Low, clamped_value <= self.lowBatteryThreshold)

    @property
    def charging(self) -> ChargingState:
        """Charging state."""
        return self.getPropertyValue(BatteryProperty.Charging) or ChargingState.NotCharging

    @charging.setter
    def charging(self, value: ChargingState) -> None:
        self._setProperty(BatteryProperty.Charging, value)

    @property
    def low(self) -> bool:
        """Whether battery is low."""
        return self.getPropertyValue(BatteryProperty.Low) or False

    @low.setter
    def low(self, value: bool) -> None:
        self._setProperty(BatteryProperty.Low, value)

    # RPC methods (camelCase for compatibility)

    def setBattery(self, level: int, charging: ChargingState | None = None) -> None:
        """
        Update battery state.

        Args:
            level: Battery level (0-100)
            charging: Charging state
        """
        self.level = level
        if charging is not None:
            self.charging = charging

    def isCharging(self) -> bool:
        """Check if battery is charging."""
        return self.charging == ChargingState.Charging

    def isFullyCharged(self) -> bool:
        """Check if battery is fully charged."""
        return self.charging == ChargingState.Full or self.level == 100
