"""Detection zone and settings types."""

from __future__ import annotations

from typing import TypedDict

from .types import Point, ZoneFilter, ZoneType


class DetectionZone(TypedDict):
    """Detection zone configuration."""

    name: str
    points: list[Point]
    type: ZoneType
    filter: ZoneFilter
    classes: list[str]  # ObjectClassLabel
    isPrivacyMask: bool
    color: str


class MotionDetectionSettings(TypedDict):
    """Motion detection settings."""

    timeout: int


class ObjectDetectionSettings(TypedDict):
    """Object detection settings."""

    confidence: float


class CameraDetectionSettings(TypedDict):
    """Camera detection settings."""

    motion: MotionDetectionSettings
    object: ObjectDetectionSettings
