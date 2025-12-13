"""Face sensor types and classes."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import Detection, FaceDetection, SensorCategory, SensorType

if TYPE_CHECKING:
    from ..plugin.interfaces import FaceResult, VideoFrameData, VideoInputProperties


class FaceProperty(str, Enum):
    """Face sensor properties."""

    Detected = "detected"
    Faces = "faces"


@runtime_checkable
class FaceSensorLike(SensorLike, Protocol):
    """Protocol for face sensor type checking."""

    @property
    def detected(self) -> bool:
        """Whether faces are currently detected."""
        ...

    @property
    def faces(self) -> list[FaceDetection]:
        """Current face detections."""
        ...

    def getKnownFaces(self) -> list[FaceDetection]:
        """Get known faces (with identity)."""
        ...

    def getUnknownFaces(self) -> list[FaceDetection]:
        """Get unknown faces (without identity)."""
        ...

    def hasIdentity(self, identity: str) -> bool:
        """Check if a specific identity is detected."""
        ...


@runtime_checkable
class FaceDetectorSensorLike(FaceSensorLike, Protocol):
    """Protocol for frame-based face detector sensor."""

    @property
    def inputProperties(self) -> VideoInputProperties:
        """Required input frame properties."""
        ...

    async def detectFaces(
        self, frame: VideoFrameData, personRegions: list[Detection] | None = None
    ) -> FaceResult:
        """Detect faces in a frame."""
        ...


class FaceSensor(Sensor[dict[str, object], dict[str, object], str]):
    """
    Base face sensor for external triggers.

    Use this class when face detection is provided by an external source.
    """

    _requires_frames = False

    @property
    def type(self) -> SensorType:
        return SensorType.Face

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Sensor

    @property
    def detected(self) -> bool:
        """Whether faces are currently detected."""
        return self.getPropertyValue(FaceProperty.Detected) or False

    @detected.setter
    def detected(self, value: bool) -> None:
        self._setProperty(FaceProperty.Detected, value)

    @property
    def faces(self) -> list[FaceDetection]:
        """Current face detections."""
        return self.getPropertyValue(FaceProperty.Faces) or []

    @faces.setter
    def faces(self, value: list[FaceDetection]) -> None:
        self._setProperty(FaceProperty.Faces, value)

    # RPC methods (camelCase for compatibility)

    def getKnownFaces(self) -> list[FaceDetection]:
        """Get known faces (with identity)."""
        return [f for f in self.faces if f.get("identity")]

    def getUnknownFaces(self) -> list[FaceDetection]:
        """Get unknown faces (without identity)."""
        return [f for f in self.faces if not f.get("identity")]

    def hasIdentity(self, identity: str) -> bool:
        """Check if a specific identity is detected."""
        return any(f.get("identity") == identity for f in self.faces)


class FaceDetectorSensor(FaceSensor):
    """
    Frame-based face detector.

    Use this class when implementing a face detection plugin.
    """

    _requires_frames = True

    @property
    @abstractmethod
    def inputProperties(self) -> VideoInputProperties:
        """Define required frame format."""
        ...

    @abstractmethod
    async def detectFaces(
        self, frame: VideoFrameData, personRegions: list[Detection] | None = None
    ) -> FaceResult:
        """
        Process frame and return face detection result.

        Args:
            frame: Video frame data
            personRegions: Optional person regions from ObjectDetectorSensor

        Returns:
            FaceResult with detected flag and face detections
        """
        ...
