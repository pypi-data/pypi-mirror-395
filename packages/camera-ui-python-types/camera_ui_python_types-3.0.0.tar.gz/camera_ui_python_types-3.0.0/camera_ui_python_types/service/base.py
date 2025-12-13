"""Service base class and protocol."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Protocol, runtime_checkable

from .types import ServiceType


@runtime_checkable
class CameraService(Protocol):
    """Base service interface - all services must implement this."""

    @property
    def type(self) -> ServiceType:
        """Service type identifier."""
        ...

    @property
    def cameraId(self) -> str:
        """Camera this service is associated with."""
        ...

    @property
    def pluginId(self) -> str:
        """Plugin that provides this service."""
        ...

    @property
    def online(self) -> bool:
        """Whether the service is currently online/available."""
        ...


class Service(ABC):
    """
    Abstract base class for all camera services.

    Plugins extend this class to implement custom service functionality.
    The service communicates with the server via RPC, with the base class
    handling online/offline status management.

    Example:
        ```python
        class MyStreamingService(Service):
            @property
            def type(self) -> ServiceType:
                return ServiceType.Streaming

            async def streamUrl(self, sourceName: str) -> str:
                return f"rtsp://my-camera/{sourceName}"

        # In plugin:
        service = MyStreamingService(camera.id, self.plugin_id)
        await camera.registerService(service)
        ```
    """

    _online: bool = False
    _online_change_fn: Callable[[bool], None] | None = None

    def __init__(self, camera_id: str, plugin_id: str) -> None:
        """
        Create a new service instance.

        Args:
            camera_id: ID of the camera this service is for
            plugin_id: ID of the plugin providing this service
        """
        self._camera_id = camera_id
        self._plugin_id = plugin_id

    @property
    @abstractmethod
    def type(self) -> ServiceType:
        """Service type - must be implemented by subclasses."""
        ...

    @property
    def cameraId(self) -> str:
        """Camera ID this service is associated with."""
        return self._camera_id

    @property
    def pluginId(self) -> str:
        """Plugin ID that provides this service."""
        return self._plugin_id

    @property
    def online(self) -> bool:
        """
        Whether the service is currently online/available.

        Setting this property notifies the server of the status change.
        """
        return self._online

    @online.setter
    def online(self, value: bool) -> None:
        if self._online != value:
            self._online = value
            if self._online_change_fn:
                self._online_change_fn(value)

    def _init(self, online_change_fn: Callable[[bool], None]) -> None:
        """
        Internal initialization - sets up the online status callback.

        Called by the runtime when the service is registered.

        Args:
            online_change_fn: Callback to notify server of online status changes
        """
        self._online_change_fn = online_change_fn

    def _cleanup(self) -> None:
        """Internal cleanup - called when service is unregistered."""
        self._online_change_fn = None
        self._online = False
