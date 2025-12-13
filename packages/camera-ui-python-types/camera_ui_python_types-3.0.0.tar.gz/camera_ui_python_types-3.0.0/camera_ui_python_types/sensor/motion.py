"""Motion sensor types and classes."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import Detection, SensorCategory, SensorType

if TYPE_CHECKING:
    from ..plugin.interfaces import MotionResult, VideoFrameData, VideoInputProperties


class MotionProperty(str, Enum):
    """Motion sensor properties."""

    Detected = "detected"
    Detections = "detections"


@runtime_checkable
class MotionSensorLike(SensorLike, Protocol):
    """Protocol for motion sensor type checking."""

    @property
    def detected(self) -> bool:
        """Whether motion is currently detected."""
        ...

    @property
    def detections(self) -> list[Detection]:
        """Current motion detections."""
        ...

    def setMotion(self, detected: bool, detections: list[Detection] | None = None) -> None:
        """Set motion state."""
        ...

    def clearMotion(self) -> None:
        """Clear motion state."""
        ...


@runtime_checkable
class MotionDetectorSensorLike(MotionSensorLike, Protocol):
    """Protocol for frame-based motion detector sensor."""

    @property
    def inputProperties(self) -> VideoInputProperties:
        """Required input frame properties."""
        ...

    async def detectMotion(self, frame: VideoFrameData) -> MotionResult:
        """Detect motion in a frame."""
        ...


class MotionSensor(Sensor[dict[str, object], dict[str, object], str]):
    """
    Base motion sensor for external triggers (Ring, ONVIF, SMTP).

    Use this class when motion detection is provided by an external source
    (e.g., camera firmware, cloud service, or SMTP notifications).
    """

    _requires_frames = False

    @property
    def type(self) -> SensorType:
        return SensorType.Motion

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Sensor

    @property
    def detected(self) -> bool:
        """Whether motion is currently detected."""
        return self.getPropertyValue(MotionProperty.Detected) or False

    @detected.setter
    def detected(self, value: bool) -> None:
        self._setProperty(MotionProperty.Detected, value)

    @property
    def detections(self) -> list[Detection]:
        """Current motion detections."""
        return self.getPropertyValue(MotionProperty.Detections) or []

    @detections.setter
    def detections(self, value: list[Detection]) -> None:
        self._setProperty(MotionProperty.Detections, value)

    # RPC methods (camelCase for compatibility)

    def setMotion(self, detected: bool, detections: list[Detection] | None = None) -> None:
        """
        Set motion state.

        Args:
            detected: Whether motion is detected
            detections: Optional list of detection regions
        """
        self.detected = detected
        if detections is not None:
            self.detections = detections

    def clearMotion(self) -> None:
        """Clear motion state."""
        self.detected = False
        self.detections = []


class MotionDetectorSensor(MotionSensor):
    """
    Frame-based motion detector (rust-motion, OpenCV, etc.).

    Use this class when implementing a motion detection plugin that
    processes video frames to detect motion.

    Subclasses must implement:
        - inputProperties: Define required frame format
        - detectMotion: Process frame and return detection result
    """

    _requires_frames = True

    @property
    @abstractmethod
    def inputProperties(self) -> VideoInputProperties:
        """
        Define required frame format.

        Returns:
            VideoInputProperties with width, height, and format
        """
        ...

    @abstractmethod
    async def detectMotion(self, frame: VideoFrameData) -> MotionResult:
        """
        Process frame and return detection result.

        Args:
            frame: Video frame data

        Returns:
            MotionResult with detected flag and detection regions
        """
        ...
