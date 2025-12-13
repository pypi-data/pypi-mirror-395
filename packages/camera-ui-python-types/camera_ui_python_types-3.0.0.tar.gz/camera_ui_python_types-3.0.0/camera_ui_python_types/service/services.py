"""Service interface protocols."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .base import CameraService
from .types import ServiceType


@runtime_checkable
class StreamingService(CameraService, Protocol):
    """
    Streaming Service Interface.

    Provides custom streaming URL generation for camera sources.
    Used by camera controller plugins (Ring, Eufy, etc.) to provide
    their own streaming URLs instead of go2rtc defaults.
    """

    @property
    def type(self) -> ServiceType:
        """Must be ServiceType.Streaming."""
        ...

    async def streamUrl(self, sourceName: str) -> str:
        """
        Generate a streaming URL for a source.

        Args:
            sourceName: Name of the source (e.g., 'high-resolution', 'mid-resolution')

        Returns:
            The streaming URL for the source
        """
        ...


@runtime_checkable
class SnapshotService(CameraService, Protocol):
    """
    Snapshot Service Interface.

    Provides custom snapshot capture for cameras.
    Used by camera controller plugins to provide their own
    snapshot mechanism instead of go2rtc defaults.
    """

    @property
    def type(self) -> ServiceType:
        """Must be ServiceType.Snapshot."""
        ...

    async def snapshot(self, sourceId: str, forceNew: bool | None = None) -> bytes | None:
        """
        Capture a snapshot from a source.

        Args:
            sourceId: ID of the source to capture from
            forceNew: If true, bypass cache and capture fresh snapshot

        Returns:
            The snapshot image data, or None if unavailable
        """
        ...


# Type alias for any service
AnyService = StreamingService | SnapshotService
