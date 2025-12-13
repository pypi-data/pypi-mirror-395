"""Object sensor types and classes."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import Detection, ObjectClassLabel, SensorCategory, SensorType

if TYPE_CHECKING:
    from ..plugin.interfaces import ObjectResult, VideoFrameData, VideoInputProperties


class ObjectProperty(str, Enum):
    """Object sensor properties."""

    Detected = "detected"
    Detections = "detections"
    Labels = "labels"


@runtime_checkable
class ObjectSensorLike(SensorLike, Protocol):
    """Protocol for object sensor type checking."""

    @property
    def detected(self) -> bool:
        """Whether objects are currently detected."""
        ...

    @property
    def detections(self) -> list[Detection]:
        """Current object detections."""
        ...

    @property
    def labels(self) -> list[ObjectClassLabel]:
        """Detected object labels."""
        ...

    def setObjects(self, detected: bool, detections: list[Detection] | None = None) -> None:
        """Set object detection state."""
        ...

    def getDetectionsByLabel(self, label: ObjectClassLabel) -> list[Detection]:
        """Get detections by label."""
        ...

    def hasLabel(self, label: ObjectClassLabel) -> bool:
        """Check if a label is detected."""
        ...


@runtime_checkable
class ObjectDetectorSensorLike(ObjectSensorLike, Protocol):
    """Protocol for frame-based object detector sensor."""

    @property
    def inputProperties(self) -> VideoInputProperties:
        """Required input frame properties."""
        ...

    async def detectObjects(self, frame: VideoFrameData) -> ObjectResult:
        """Detect objects in a frame."""
        ...


class ObjectSensor(Sensor[dict[str, object], dict[str, object], str]):
    """
    Base object sensor for external triggers (Ring, ONVIF, cloud APIs).

    Use this class when object detection is provided by an external source.
    """

    _requires_frames = False

    @property
    def type(self) -> SensorType:
        return SensorType.Object

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Sensor

    @property
    def detected(self) -> bool:
        """Whether objects are currently detected."""
        return self.getPropertyValue(ObjectProperty.Detected) or False

    @detected.setter
    def detected(self, value: bool) -> None:
        self._setProperty(ObjectProperty.Detected, value)

    @property
    def detections(self) -> list[Detection]:
        """Current object detections."""
        return self.getPropertyValue(ObjectProperty.Detections) or []

    @detections.setter
    def detections(self, value: list[Detection]) -> None:
        self._setProperty(ObjectProperty.Detections, value)
        # Update labels automatically
        labels = list({d["label"] for d in value})
        self._setProperty(ObjectProperty.Labels, labels)

    @property
    def labels(self) -> list[ObjectClassLabel]:
        """Detected object labels."""
        return self.getPropertyValue(ObjectProperty.Labels) or []

    # RPC methods (camelCase for compatibility)

    def setObjects(self, detected: bool, detections: list[Detection] | None = None) -> None:
        """
        Set object detection state.

        Args:
            detected: Whether objects are detected
            detections: Optional list of detections
        """
        self.detected = detected
        if detections is not None:
            self.detections = detections

    def getDetectionsByLabel(self, label: ObjectClassLabel) -> list[Detection]:
        """Get detections by label."""
        return [d for d in self.detections if d["label"] == label]

    def hasLabel(self, label: ObjectClassLabel) -> bool:
        """Check if a label is detected."""
        return label in self.labels


class ObjectDetectorSensor(ObjectSensor):
    """
    Frame-based object detector (TensorFlow, YOLO, etc.).

    Use this class when implementing an object detection plugin that
    processes video frames to detect objects.
    """

    _requires_frames = True

    @property
    @abstractmethod
    def inputProperties(self) -> VideoInputProperties:
        """Define required frame format."""
        ...

    @abstractmethod
    async def detectObjects(self, frame: VideoFrameData) -> ObjectResult:
        """Process frame and return detection result."""
        ...
