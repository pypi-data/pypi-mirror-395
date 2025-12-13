"""Camera configuration types."""

from __future__ import annotations

from typing import TypedDict

from .streaming import StreamUrls
from .types import (
    CameraAspectRatio,
    CameraFrameWorkerResolution,
    CameraRole,
    StreamingRole,
    VideoStreamingMode,
)


class CameraInformation(TypedDict, total=False):
    """Camera information metadata."""

    model: str
    manufacturer: str
    hardware: str
    serialNumber: str
    firmwareVersion: str
    supportUrl: str


class CameraFrameWorkerSettings(TypedDict):
    """Frame worker settings for a camera."""

    fps: int
    resolution: CameraFrameWorkerResolution


class CameraInput(TypedDict):
    """Camera input source configuration."""

    _id: str
    name: str
    role: CameraRole
    useForSnapshot: bool
    hotMode: bool
    preload: bool
    prebuffer: bool
    urls: StreamUrls


class CameraInputSettings(TypedDict):
    """Camera input settings."""

    _id: str
    name: str
    role: CameraRole
    useForSnapshot: bool
    hotMode: bool
    preload: bool
    prebuffer: bool
    urls: list[str]


class CameraConfigInputSettings(TypedDict):
    """Camera config input settings (without _id and urls)."""

    name: str
    role: CameraRole
    useForSnapshot: bool
    hotMode: bool
    preload: bool
    prebuffer: bool


class BaseCameraConfig(TypedDict, total=False):
    """Base camera configuration."""

    name: str
    nativeId: str
    isCloud: bool
    disabled: bool
    info: CameraInformation


class CameraConfig(BaseCameraConfig):
    """Full camera configuration with sources."""

    sources: list[CameraConfigInputSettings]


class CameraUiSettings(TypedDict):
    """Camera UI display settings."""

    streamingMode: VideoStreamingMode
    streamingSource: StreamingRole | str  # 'auto' or a StreamingRole
    aspectRatio: CameraAspectRatio


class CameraRecordingSettings(TypedDict):
    """Camera recording settings."""

    enabled: bool


class CameraSource(CameraInput):
    """Camera source with snapshot capability."""

    pass  # Methods defined via Protocol


class SnapshotInterface(TypedDict):
    """Snapshot interface (deprecated - use SnapshotService instead)."""

    pass


class StreamingInterface(TypedDict):
    """Streaming interface (deprecated - use StreamingService instead)."""

    pass
