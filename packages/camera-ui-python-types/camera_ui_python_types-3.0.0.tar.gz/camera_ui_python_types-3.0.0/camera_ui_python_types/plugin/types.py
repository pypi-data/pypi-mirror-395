"""Plugin types and interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Protocol, TypedDict, runtime_checkable

from ..sensor.types import Detection
from ..storage.schema import JsonSchema

if TYPE_CHECKING:
    from ..camera.device import CameraDevice
    from ..manager.types import CoreManager, DeviceManager, LoggerService
    from ..storage.storages import StorageController


class ImageMetadata(TypedDict):
    """Image metadata for test functions."""

    width: int
    height: int


class AudioMetadata(TypedDict):
    """Audio metadata for test functions."""

    mimeType: str  # 'audio/mpeg' | 'audio/wav' | 'audio/ogg'


class MotionDetectionPluginResponse(TypedDict, total=False):
    """Motion detection test response."""

    detected: bool
    detections: list[Detection]
    videoData: bytes


class ObjectDetectionPluginResponse(TypedDict):
    """Object detection test response."""

    detected: bool
    detections: list[Detection]


class AudioDetectionPluginResponse(TypedDict, total=False):
    """Audio detection test response."""

    detected: bool
    detections: list[Detection]
    decibels: float


@runtime_checkable
class PluginAPI(Protocol):
    """Plugin API - injected into plugins at runtime."""

    @property
    def coreManager(self) -> CoreManager:
        """Core manager for system operations."""
        ...

    @property
    def deviceManager(self) -> DeviceManager:
        """Device manager for camera operations."""
        ...

    @property
    def storageController(self) -> StorageController:
        """Storage controller for persistent storage."""
        ...

    @property
    def storagePath(self) -> str:
        """Path to plugin storage directory."""
        ...

    def on(self, event: str, listener: Callable[[], None]) -> PluginAPI:
        """
        Subscribe to an event.

        Args:
            event: Event name ('finishLaunching' or 'shutdown')
            listener: Event listener

        Returns:
            Self for chaining
        """
        ...

    def once(self, event: str, listener: Callable[[], None]) -> PluginAPI:
        """
        Subscribe to an event once.

        Args:
            event: Event name
            listener: Event listener

        Returns:
            Self for chaining
        """
        ...

    def off(self, event: str, listener: Callable[[], None]) -> PluginAPI:
        """
        Unsubscribe from an event.

        Args:
            event: Event name
            listener: Event listener

        Returns:
            Self for chaining
        """
        ...

    def removeListener(self, event: str, listener: Callable[[], None]) -> PluginAPI:
        """
        Remove a listener.

        Args:
            event: Event name
            listener: Event listener

        Returns:
            Self for chaining
        """
        ...

    def removeAllListeners(self, event: str | None = None) -> PluginAPI:
        """
        Remove all listeners.

        Args:
            event: Optional event name to remove listeners for

        Returns:
            Self for chaining
        """
        ...


class CuiPlugin(ABC):
    """
    Base plugin class - all plugins must extend this.

    Example:
        ```python
        class MyPlugin(CuiPlugin):
            def __init__(self, logger: LoggerService, api: PluginAPI) -> None:
                super().__init__(logger, api)

            async def configureCameras(self, cameras: list[CameraDevice]) -> None:
                for camera in cameras:
                    # Setup sensors for each camera
                    pass
        ```
    """

    def __init__(self, logger: LoggerService, api: PluginAPI) -> None:
        """
        Initialize the plugin.

        Args:
            logger: Logger service for this plugin
            api: Plugin API for accessing system services
        """
        self.logger = logger
        self.api = api

    @abstractmethod
    async def configureCameras(self, cameras: list[CameraDevice]) -> None:
        """
        Configure cameras for this plugin.

        Called when cameras are available for the plugin to configure.
        Add sensors, services, and set up event handlers here.

        Args:
            cameras: List of camera devices assigned to this plugin
        """
        ...

    async def interfaceSchema(self) -> list[JsonSchema] | None:
        """
        Return interface schema for plugin configuration UI.

        Override this method to provide a configuration UI schema.

        Returns:
            List of JSON schemas for configuration or None
        """
        return None

    async def testMotion(
        self, videoData: bytes, config: dict[str, Any]
    ) -> MotionDetectionPluginResponse | None:
        """
        Test motion detection with video data.

        Override this method to support motion detection testing.

        Args:
            videoData: Video data to test
            config: Plugin configuration

        Returns:
            Motion detection response or None
        """
        return None

    async def testObjects(
        self, imageData: bytes, metadata: ImageMetadata, config: dict[str, Any]
    ) -> ObjectDetectionPluginResponse | None:
        """
        Test object detection with image data.

        Override this method to support object detection testing.

        Args:
            imageData: Image data to test
            metadata: Image metadata
            config: Plugin configuration

        Returns:
            Object detection response or None
        """
        return None

    async def testAudio(
        self, audioData: bytes, metadata: AudioMetadata, config: dict[str, Any]
    ) -> AudioDetectionPluginResponse | None:
        """
        Test audio detection with audio data.

        Override this method to support audio detection testing.

        Args:
            audioData: Audio data to test
            metadata: Audio metadata
            config: Plugin configuration

        Returns:
            Audio detection response or None
        """
        return None
