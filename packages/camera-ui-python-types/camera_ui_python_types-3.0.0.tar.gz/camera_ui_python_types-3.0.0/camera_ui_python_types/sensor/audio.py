"""Audio sensor types and classes."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import Detection, SensorCategory, SensorType

if TYPE_CHECKING:
    from ..plugin.interfaces import AudioFrameData, AudioInputProperties, AudioResult


class AudioProperty(str, Enum):
    """Audio sensor properties."""

    Detected = "detected"
    Detections = "detections"
    Decibels = "decibels"


@runtime_checkable
class AudioSensorLike(SensorLike, Protocol):
    """Protocol for audio sensor type checking."""

    @property
    def detected(self) -> bool:
        """Whether audio is currently detected."""
        ...

    @property
    def detections(self) -> list[Detection]:
        """Current audio detections."""
        ...

    @property
    def decibels(self) -> float:
        """Current decibel level."""
        ...

    def setAudio(
        self, detected: bool, detections: list[Detection] | None = None, decibels: float | None = None
    ) -> None:
        """Set audio detection state."""
        ...

    def clearAudio(self) -> None:
        """Clear audio state."""
        ...


@runtime_checkable
class AudioDetectorSensorLike(AudioSensorLike, Protocol):
    """Protocol for frame-based audio detector sensor."""

    @property
    def inputProperties(self) -> AudioInputProperties:
        """Required input audio properties."""
        ...

    async def detectAudio(self, audio: AudioFrameData) -> AudioResult:
        """Detect audio events."""
        ...


class AudioSensor(Sensor[dict[str, object], dict[str, object], str]):
    """
    Base audio sensor for external triggers (Ring, ONVIF).

    Use this class when audio detection is provided by an external source.
    """

    _requires_frames = False

    @property
    def type(self) -> SensorType:
        return SensorType.Audio

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Sensor

    @property
    def detected(self) -> bool:
        """Whether audio is currently detected."""
        return self.getPropertyValue(AudioProperty.Detected) or False

    @detected.setter
    def detected(self, value: bool) -> None:
        self._setProperty(AudioProperty.Detected, value)

    @property
    def detections(self) -> list[Detection]:
        """Current audio detections."""
        return self.getPropertyValue(AudioProperty.Detections) or []

    @detections.setter
    def detections(self, value: list[Detection]) -> None:
        self._setProperty(AudioProperty.Detections, value)

    @property
    def decibels(self) -> float:
        """Current decibel level."""
        return self.getPropertyValue(AudioProperty.Decibels) or 0.0

    @decibels.setter
    def decibels(self, value: float) -> None:
        self._setProperty(AudioProperty.Decibels, value)

    # RPC methods (camelCase for compatibility)

    def setAudio(
        self, detected: bool, detections: list[Detection] | None = None, decibels: float | None = None
    ) -> None:
        """
        Set audio detection state.

        Args:
            detected: Whether audio is detected
            detections: Optional list of detections
            decibels: Optional decibel level
        """
        self.detected = detected
        if detections is not None:
            self.detections = detections
        if decibels is not None:
            self.decibels = decibels

    def clearAudio(self) -> None:
        """Clear audio state."""
        self.detected = False
        self.detections = []


class AudioDetectorSensor(AudioSensor):
    """
    Frame-based audio detector (glass break detection, etc.).

    Use this class when implementing an audio detection plugin that
    processes audio frames.
    """

    _requires_frames = True

    @property
    @abstractmethod
    def inputProperties(self) -> AudioInputProperties:
        """Define required audio format."""
        ...

    @abstractmethod
    async def detectAudio(self, audio: AudioFrameData) -> AudioResult:
        """Process audio and return detection result."""
        ...
