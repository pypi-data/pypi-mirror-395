"""Plugin module exports."""

from .interfaces import (
    AudioFrameData,
    AudioResult,
    FaceResult,
    LicensePlateResult,
    MotionResult,
    ObjectResult,
    VideoFrameData,
)
from .types import (
    AudioDetectionPluginResponse,
    AudioMetadata,
    CuiPlugin,
    ImageMetadata,
    MotionDetectionPluginResponse,
    ObjectDetectionPluginResponse,
    PluginAPI,
)

__all__ = [
    # Interfaces (detection results)
    "AudioFrameData",
    "AudioResult",
    "FaceResult",
    "LicensePlateResult",
    "MotionResult",
    "ObjectResult",
    "VideoFrameData",
    # Types
    "ImageMetadata",
    "AudioMetadata",
    "MotionDetectionPluginResponse",
    "ObjectDetectionPluginResponse",
    "AudioDetectionPluginResponse",
    "PluginAPI",
    "CuiPlugin",
]
