"""Base sensor classes and protocols."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Protocol, TypeVar, runtime_checkable
from uuid import uuid4

from .types import SensorCategory, SensorType

# Type variables for Sensor generics
TProperties = TypeVar("TProperties", bound=dict[str, Any])
TStorage = TypeVar("TStorage", bound=dict[str, Any])
TCapability = TypeVar("TCapability", bound=str)


@runtime_checkable
class SensorLike(Protocol):
    """
    SensorLike interface - common interface for Sensor and SensorProxy.

    This allows plugins to access sensors (both owned and from other plugins)
    through a unified interface.

    Use type guards (isMotionSensor, isLightControl, etc.) for runtime type checking.
    """

    # Properties (camelCase for RPC compatibility)
    @property
    def id(self) -> str:
        """Unique sensor ID."""
        ...

    @property
    def type(self) -> SensorType:
        """Sensor type."""
        ...

    @property
    def name(self) -> str:
        """Stable name (set by plugin, used for storage key)."""
        ...

    @property
    def displayName(self) -> str:
        """Display name for UI/HomeKit (initially = name, can be changed by user)."""
        ...

    @property
    def online(self) -> bool:
        """Whether the sensor is online."""
        ...

    @property
    def pluginId(self) -> str | None:
        """Plugin ID that provides this sensor."""
        ...

    @property
    def capabilities(self) -> list[str]:
        """Sensor capabilities (e.g., PTZCapability.Pan, LightCapability.Brightness)."""
        ...

    # Methods (camelCase for RPC compatibility)
    def getPropertyValue(self, property: str) -> Any | None:
        """
        Get a property value.

        Args:
            property: The property key (use enum values like MotionProperty.Detected)

        Returns:
            The property value or None
        """
        ...

    def getAllPropertyValues(self) -> dict[str, Any]:
        """
        Get all property values.

        Returns:
            All properties as a dictionary
        """
        ...

    async def setPropertyValue(self, property: str, value: Any) -> None:
        """
        Set a property value (for Control sensors).
        Note: Only works for Control sensors, others are read-only.

        Args:
            property: The property key (use enum values like LightProperty.On)
            value: The new value
        """
        ...

    def onPropertyChanged(self, callback: Callable[[str, Any], None]) -> Callable[[], None]:
        """
        Subscribe to property changes for this sensor.

        Args:
            callback: Callback with property key and new value

        Returns:
            Unsubscribe function
        """
        ...

    def onCapabilitiesChanged(self, callback: Callable[[list[str]], None]) -> Callable[[], None]:
        """
        Subscribe to capability changes for this sensor.

        Args:
            callback: Callback with new capabilities array

        Returns:
            Unsubscribe function
        """
        ...

    def hasCapability(self, capability: str) -> bool:
        """
        Check if sensor has a specific capability.

        Args:
            capability: The capability to check (use enum values like PTZCapability.Zoom)

        Returns:
            True if the sensor has the capability
        """
        ...


class Sensor(ABC, Generic[TProperties, TStorage, TCapability]):
    """
    Abstract Base Class for all sensors.

    Plugins extend this class to implement custom sensor functionality.
    The sensor communicates with the server via RPC.

    Type Parameters:
        TProperties: Type of the sensor properties dictionary
        TStorage: Type of the sensor storage dictionary
        TCapability: Type of the sensor capabilities (enum)
    """

    # Class-level flag for detector sensors
    _requires_frames: bool = False

    def __init__(self, camera_id: str, name: str) -> None:
        """
        Create a new sensor instance.

        Args:
            camera_id: ID of the camera this sensor is for
            name: Stable name for the sensor (used as storage key)
        """
        self._camera_id = camera_id
        self._name = name
        self._id = str(uuid4())
        self._display_name = name
        self._online = False
        self._plugin_id: str | None = None
        self._properties: dict[str, Any] = {}
        self._capabilities: list[TCapability] = []
        self._property_listeners: list[Callable[[str, Any], None]] = []
        self._capabilities_listeners: list[Callable[[list[str]], None]] = []
        self._update_fn: Callable[[str, Any], None] | None = None
        self._online_change_fn: Callable[[bool], None] | None = None
        self._capabilities_change_fn: Callable[[list[str]], None] | None = None

    @property
    @abstractmethod
    def type(self) -> SensorType:
        """Sensor type - must be implemented by subclasses."""
        ...

    @property
    @abstractmethod
    def category(self) -> SensorCategory:
        """Sensor category - must be implemented by subclasses."""
        ...

    @property
    def id(self) -> str:
        """Unique sensor ID."""
        return self._id

    @property
    def name(self) -> str:
        """Stable name (set by plugin, used for storage key)."""
        return self._name

    @property
    def displayName(self) -> str:
        """Display name for UI/HomeKit."""
        return self._display_name

    @displayName.setter
    def displayName(self, value: str) -> None:
        self._display_name = value

    @property
    def online(self) -> bool:
        """Whether the sensor is online."""
        return self._online

    @online.setter
    def online(self, value: bool) -> None:
        if self._online != value:
            self._online = value
            if self._online_change_fn:
                self._online_change_fn(value)

    @property
    def pluginId(self) -> str | None:
        """Plugin ID that provides this sensor."""
        return self._plugin_id

    @property
    def cameraId(self) -> str:
        """Camera ID this sensor is associated with."""
        return self._camera_id

    @property
    def capabilities(self) -> list[TCapability]:
        """Sensor capabilities."""
        return self._capabilities.copy()

    @property
    def requiresFrames(self) -> bool:
        """Whether this sensor requires video/audio frames for detection."""
        return self._requires_frames

    def _setProperty(self, key: str, value: Any) -> None:
        """
        Internal method to set property and notify.

        Args:
            key: Property key
            value: Property value
        """
        old_value = self._properties.get(key)
        self._properties[key] = value
        if self._update_fn and old_value != value:
            self._update_fn(key, value)
        for listener in self._property_listeners:
            listener(key, value)

    def _setPropertyInternal(self, key: str, value: Any) -> None:
        """
        Set property from external source (no RPC callback).

        Args:
            key: Property key
            value: Property value
        """
        self._properties[key] = value
        for listener in self._property_listeners:
            listener(key, value)

    # RPC-exposed methods (camelCase for compatibility)

    def getPropertyValue(self, property: str) -> Any | None:
        """Get a property value."""
        return self._properties.get(property)

    def getAllPropertyValues(self) -> dict[str, Any]:
        """Get all property values."""
        return self._properties.copy()

    async def setPropertyValue(self, property: str, value: Any) -> None:
        """Set a property value (for Control sensors)."""
        self._setProperty(property, value)

    def hasCapability(self, capability: TCapability | str) -> bool:
        """Check if sensor has a specific capability."""
        return capability in self._capabilities

    def addCapabilities(self, *capabilities: TCapability) -> None:
        """Add capabilities to the sensor."""
        changed = False
        for cap in capabilities:
            if cap not in self._capabilities:
                self._capabilities.append(cap)
                changed = True

        if changed:
            caps_list: list[str] = [str(c) for c in self._capabilities]
            if self._capabilities_change_fn:
                self._capabilities_change_fn(caps_list)
            for listener in self._capabilities_listeners:
                listener(caps_list)

    def removeCapabilities(self, *capabilities: TCapability) -> None:
        """Remove capabilities from the sensor."""
        changed = False
        for cap in capabilities:
            if cap in self._capabilities:
                self._capabilities.remove(cap)
                changed = True

        if changed:
            caps_list: list[str] = [str(c) for c in self._capabilities]
            if self._capabilities_change_fn:
                self._capabilities_change_fn(caps_list)
            for listener in self._capabilities_listeners:
                listener(caps_list)

    def onPropertyChanged(self, callback: Callable[[str, Any], None]) -> Callable[[], None]:
        """Subscribe to property changes."""
        self._property_listeners.append(callback)
        return lambda: self._property_listeners.remove(callback)

    def onCapabilitiesChanged(self, callback: Callable[[list[str]], None]) -> Callable[[], None]:
        """Subscribe to capability changes."""
        self._capabilities_listeners.append(callback)
        return lambda: self._capabilities_listeners.remove(callback)

    def _init(
        self,
        plugin_id: str,
        update_fn: Callable[[str, Any], None],
        online_change_fn: Callable[[bool], None],
        capabilities_change_fn: Callable[[list[str]], None],
    ) -> None:
        """
        Internal initialization - sets up the RPC callbacks.

        Called by the runtime when the sensor is registered.

        Args:
            plugin_id: Plugin ID that provides this sensor
            update_fn: Callback to notify server of property changes
            online_change_fn: Callback to notify server of online status changes
            capabilities_change_fn: Callback to notify server of capability changes
        """
        self._plugin_id = plugin_id
        self._update_fn = update_fn
        self._online_change_fn = online_change_fn
        self._capabilities_change_fn = capabilities_change_fn

    def _cleanup(self) -> None:
        """Internal cleanup - called when sensor is unregistered."""
        self._update_fn = None
        self._online_change_fn = None
        self._capabilities_change_fn = None
        self._online = False

    def _getProperties(self) -> dict[str, Any]:
        """Get all properties (internal use)."""
        return self._properties.copy()
