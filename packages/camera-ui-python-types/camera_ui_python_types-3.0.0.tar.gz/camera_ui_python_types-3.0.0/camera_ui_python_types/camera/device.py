"""Camera device protocol and types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Protocol, TypedDict, runtime_checkable

from .config import (
    CameraFrameWorkerSettings,
    CameraInformation,
    CameraRecordingSettings,
    CameraSource,
    CameraUiSettings,
)
from .detection import CameraDetectionSettings, DetectionZone
from .types import CameraType

if TYPE_CHECKING:
    from ..manager.types import LoggerService
    from ..sensor.base import Sensor, SensorLike
    from ..sensor.types import Detection, SensorOnlineEvent, SensorType
    from ..service.base import Service, ServiceType


class AssignedPlugin(TypedDict):
    """Assigned plugin information."""

    id: str
    name: str


class PluginAssignments(TypedDict, total=False):
    """Plugin assignments for a camera - maps sensor types to assigned plugins."""

    # Single provider - Detection (only 1 plugin can process frames)
    motion: AssignedPlugin
    object: AssignedPlugin
    audio: AssignedPlugin
    face: AssignedPlugin
    licensePlate: AssignedPlugin

    # Single provider - Special
    ptz: AssignedPlugin
    battery: AssignedPlugin
    cameraController: AssignedPlugin

    # Multiple provider - Controls (external hardware)
    light: list[AssignedPlugin]
    siren: list[AssignedPlugin]

    # Multiple provider - Triggers/Sensors (external hardware)
    contact: list[AssignedPlugin]
    doorbell: list[AssignedPlugin]

    # Multiple provider - Integration
    hub: list[AssignedPlugin]


class CameraPluginInfo(TypedDict):
    """Camera plugin info."""

    id: str
    name: str


class BaseCamera(TypedDict):
    """Base camera properties."""

    _id: str
    nativeId: str | None
    pluginInfo: CameraPluginInfo | None
    name: str
    disabled: bool
    isCloud: bool
    info: CameraInformation
    type: CameraType
    snapshotTTL: int
    detectionZones: list[DetectionZone]
    detectionSettings: CameraDetectionSettings
    frameWorkerSettings: CameraFrameWorkerSettings
    interface: CameraUiSettings
    recording: CameraRecordingSettings
    plugins: list[AssignedPlugin]
    assignments: PluginAssignments


@runtime_checkable
class CameraDevice(Protocol):
    """
    Camera Device - Main interface for plugin developers.

    This protocol defines the interface that plugins use to interact with cameras.
    """

    @property
    def id(self) -> str:
        """Camera ID."""
        ...

    @property
    def nativeId(self) -> str | None:
        """Native ID from the camera/plugin."""
        ...

    @property
    def pluginInfo(self) -> CameraPluginInfo | None:
        """Plugin info if camera was created by a plugin."""
        ...

    @property
    def disabled(self) -> bool:
        """Whether the camera is disabled."""
        ...

    @property
    def name(self) -> str:
        """Camera name."""
        ...

    @property
    def type(self) -> CameraType:
        """Camera type (camera or doorbell)."""
        ...

    @property
    def snapshotTTL(self) -> int:
        """Snapshot time-to-live in seconds."""
        ...

    @property
    def info(self) -> CameraInformation:
        """Camera information metadata."""
        ...

    @property
    def isCloud(self) -> bool:
        """Whether this is a cloud camera."""
        ...

    @property
    def detectionZones(self) -> list[DetectionZone]:
        """Detection zones configured for this camera."""
        ...

    @property
    def detectionSettings(self) -> CameraDetectionSettings:
        """Detection settings for this camera."""
        ...

    @property
    def frameWorkerSettings(self) -> CameraFrameWorkerSettings:
        """Frame worker settings."""
        ...

    @property
    def sources(self) -> list[CameraSource]:
        """All camera sources."""
        ...

    @property
    def connected(self) -> bool:
        """Whether the camera is connected."""
        ...

    @property
    def frameWorkerConnected(self) -> bool:
        """Whether the frame worker is connected."""
        ...

    @property
    def logger(self) -> LoggerService:
        """Logger service for this camera."""
        ...

    async def connect(self) -> None:
        """Connect to the camera."""
        ...

    async def disconnect(self) -> None:
        """Disconnect from the camera."""
        ...

    # Sensor-based Architecture

    def getSensors(self) -> list[SensorLike]:
        """Get all sensors for this camera."""
        ...

    def getSensor(self, sensorId: str) -> SensorLike | None:
        """Get a sensor by ID."""
        ...

    def getSensorsByType(self, sensorType: SensorType) -> list[SensorLike]:
        """Get all sensors of a specific type."""
        ...

    async def addSensor(self, sensor: SensorLike) -> None:
        """Add a sensor to this camera."""
        ...

    async def removeSensor(self, sensorId: str) -> None:
        """Remove a sensor from this camera."""
        ...

    def onSensorOnlineChanged(self, callback: Callable[[SensorOnlineEvent], None]) -> Callable[[], None]:
        """Subscribe to sensor online status changes."""
        ...

    def onSensorAdded(self, callback: Callable[[SensorLike], None]) -> Callable[[], None]:
        """Subscribe to sensor added events."""
        ...

    def onSensorRemoved(self, callback: Callable[[str, SensorType], None]) -> Callable[[], None]:
        """Subscribe to sensor removed events."""
        ...

    # Detection Methods

    async def reportDetection(self, sensorType: SensorType, detections: list[Detection]) -> None:
        """Report detection results for a sensor type."""
        ...

    # Service Methods

    async def registerService(self, service: Service) -> None:
        """Register a service for this camera."""
        ...

    async def unregisterService(self, serviceType: ServiceType) -> None:
        """Unregister a service from this camera."""
        ...
