"""Plugin detection interfaces."""

from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

from ..sensor.types import (
    AudioInputProperties,
    Detection,
    FaceDetection,
    LicensePlateDetection,
    VideoInputProperties,
)

__all__ = [
    "AudioFrameData",
    "AudioResult",
    "FaceResult",
    "LicensePlateResult",
    "MotionResult",
    "ObjectResult",
    "VideoFrameData",
    "VideoInputProperties",
    "AudioInputProperties",
]


class VideoFrameData(TypedDict):
    """Video frame data passed to detection plugins."""

    cameraId: NotRequired[str]  # Camera ID this frame belongs to (optional, set by coordinator)
    data: bytes  # Frame data (NV12, RGB, etc.) - ArrayBuffer in TS, bytes in Python
    width: int  # Frame width
    height: int  # Frame height
    format: Literal["nv12", "rgb", "rgba", "gray"]  # Pixel format
    timestamp: NotRequired[int]  # Frame timestamp (optional)


class AudioFrameData(TypedDict):
    """Audio data passed to audio detection plugins."""

    cameraId: NotRequired[str]  # Camera ID this audio belongs to (optional, set by coordinator)
    data: bytes  # Audio sample data (PCM16 or Float32)
    sampleRate: int  # Sample rate in Hz
    channels: int  # Number of channels (1 = mono, 2 = stereo)
    format: Literal["pcm16", "float32"]  # Audio format
    decibels: NotRequired[float]  # Current decibel level (optional)
    timestamp: NotRequired[int]  # Timestamp (optional)


class MotionResult(TypedDict):
    """Motion detection result."""

    detected: bool  # Whether motion was detected
    detections: list[Detection]  # Detection regions


class ObjectResult(TypedDict):
    """Object detection result."""

    detected: bool  # Whether objects were detected
    detections: list[Detection]  # Detection results


class FaceResult(TypedDict):
    """Face detection result."""

    detected: bool  # Whether faces were detected
    faces: list[FaceDetection]  # Face detections


class AudioResult(TypedDict):
    """Audio detection result."""

    detected: bool  # Whether audio event was detected
    detections: list[Detection]  # Audio detections
    decibels: NotRequired[float]  # Decibel level


class LicensePlateResult(TypedDict):
    """License plate detection result."""

    detected: bool  # Whether license plates were detected
    plates: list[LicensePlateDetection]  # License plate detections
