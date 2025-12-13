"""Manager types and interfaces."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Protocol, TypedDict, runtime_checkable

if TYPE_CHECKING:
    from ..camera.config import CameraConfig
    from ..camera.device import CameraDevice
    from ..camera.types import HwAccelMethod
    from ..plugin.types import CuiPlugin


class LoggerService(Protocol):
    """Logger service interface."""

    def log(self, *args: Any) -> None:
        """Log a message."""
        ...

    def error(self, *args: Any) -> None:
        """Log an error."""
        ...

    def warn(self, *args: Any) -> None:
        """Log a warning."""
        ...

    def success(self, *args: Any) -> None:
        """Log a success message."""
        ...

    def debug(self, *args: Any) -> None:
        """Log a debug message."""
        ...

    def trace(self, *args: Any) -> None:
        """Log a trace message."""
        ...

    def attention(self, *args: Any) -> None:
        """Log an attention message."""
        ...


@runtime_checkable
class DeviceManager(Protocol):
    """Device manager for camera operations."""

    async def createCamera(self, cameraConfig: CameraConfig) -> CameraDevice:
        """
        Create a new camera.

        Args:
            cameraConfig: Camera configuration

        Returns:
            The created camera device
        """
        ...

    async def updateCamera(self, cameraIdOrName: str, cameraConfig: dict[str, Any]) -> CameraDevice:
        """
        Update a camera configuration.

        Args:
            cameraIdOrName: Camera ID or name
            cameraConfig: Partial camera configuration to update

        Returns:
            The updated camera device
        """
        ...

    async def getCamera(self, cameraIdOrName: str) -> CameraDevice | None:
        """
        Get a camera by ID or name.

        Args:
            cameraIdOrName: Camera ID or name

        Returns:
            The camera device or None if not found
        """
        ...

    async def removeCamera(self, cameraIdOrName: str) -> None:
        """
        Remove a camera.

        Args:
            cameraIdOrName: Camera ID or name
        """
        ...

    def on(self, event: str, listener: Callable[..., None]) -> DeviceManager:
        """
        Subscribe to an event.

        Args:
            event: Event name ('cameraSelected' or 'cameraDeselected')
            listener: Event listener

        Returns:
            Self for chaining
        """
        ...

    def once(self, event: str, listener: Callable[..., None]) -> DeviceManager:
        """
        Subscribe to an event once.

        Args:
            event: Event name
            listener: Event listener

        Returns:
            Self for chaining
        """
        ...

    def off(self, event: str, listener: Callable[..., None]) -> DeviceManager:
        """
        Unsubscribe from an event.

        Args:
            event: Event name
            listener: Event listener

        Returns:
            Self for chaining
        """
        ...

    def removeListener(self, event: str, listener: Callable[..., None]) -> DeviceManager:
        """
        Remove a listener.

        Args:
            event: Event name
            listener: Event listener

        Returns:
            Self for chaining
        """
        ...

    def removeAllListeners(self, event: str | None = None) -> DeviceManager:
        """
        Remove all listeners.

        Args:
            event: Optional event name to remove listeners for

        Returns:
            Self for chaining
        """
        ...


class HWAccelOptions(TypedDict, total=False):
    """Hardware acceleration options."""

    targetCodec: str  # 'h264' | 'h265'
    keepOnHardware: bool
    pixelFormat: str
    scale: dict[str, int]  # {width: int, height: int}


class FfmpegArgs(TypedDict):
    """FFmpeg arguments for hardware acceleration."""

    codec: str
    hwaccel: HwAccelMethod
    hwaccelArgs: list[str]
    hwaccelFilters: list[str]
    hwDeviceArgs: list[str]
    supported: bool


@runtime_checkable
class CoreManager(Protocol):
    """Core manager for system operations."""

    async def connectToPlugin(self, pluginName: str) -> CuiPlugin | None:
        """
        Connect to another plugin.

        Args:
            pluginName: Name of the plugin to connect to

        Returns:
            The plugin instance or None if not found
        """
        ...

    async def getFFmpegPath(self) -> str:
        """
        Get the FFmpeg executable path.

        Returns:
            Path to FFmpeg
        """
        ...

    async def getHwaccelInfo(self, options: HWAccelOptions) -> list[FfmpegArgs]:
        """
        Get hardware acceleration information.

        Args:
            options: Hardware acceleration options

        Returns:
            List of FFmpeg argument configurations
        """
        ...

    async def getServerAddresses(self) -> list[str]:
        """
        Get server addresses.

        Returns:
            List of server addresses
        """
        ...
