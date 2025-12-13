"""Core sensor types and enums."""

from __future__ import annotations

from enum import Enum
from typing import Literal, NotRequired, TypedDict

# ========== Sensor Types ==========


class SensorType(str, Enum):
    """Sensor Type Enum - identifies the type of sensor/control/trigger/info."""

    # Detection Sensors
    Motion = "motion"
    Object = "object"
    Audio = "audio"
    Face = "face"
    LicensePlate = "licensePlate"
    Contact = "contact"

    # Controls
    Light = "light"
    Siren = "siren"
    PTZ = "ptz"

    # Triggers
    Doorbell = "doorbell"

    # Info
    Battery = "battery"


class SensorCategory(str, Enum):
    """Sensor Category - categorizes sensors by their behavior."""

    Sensor = "sensor"  # Detection sensors (read-only, 1 provider)
    Control = "control"  # Bidirectional controls
    Trigger = "trigger"  # Event-based triggers
    Info = "info"  # Read-only hardware status


# ========== Input Properties for Detectors ==========


class VideoInputProperties(TypedDict):
    """Video input properties for frame-based detection."""

    width: int  # Target frame width in pixels
    height: int  # Target frame height in pixels
    format: Literal["rgb", "nv12", "gray"]  # Pixel format


class AudioInputProperties(TypedDict):
    """Audio input properties for audio-based detection."""

    sampleRate: int  # Sample rate in Hz (e.g., 16000, 44100)
    channels: int  # Number of channels (1 = mono, 2 = stereo)
    format: Literal["pcm16", "float32"]  # Audio format


# ========== Core Detection Types ==========


class BoundingBox(TypedDict):
    """Bounding box for object detection (normalized 0-1)."""

    x: float  # X coordinate (0-1, relative to image width)
    y: float  # Y coordinate (0-1, relative to image height)
    width: float  # Width (0-1, relative to image width)
    height: float  # Height (0-1, relative to image height)


# Object class labels for detection
ObjectClassLabel = (
    Literal[
        "person",
        "face",
        "car",
        "truck",
        "motorcycle",
        "bicycle",
        "bus",
        "train",
        "boat",
        "airplane",
        "dog",
        "cat",
        "bird",
        "horse",
        "sheep",
        "cow",
        "bear",
        "elephant",
        "zebra",
        "giraffe",
        "backpack",
        "umbrella",
        "handbag",
        "suitcase",
        "bottle",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "bed",
        "table",
        "toilet",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy_bear",
        "hair_dryer",
        "toothbrush",
        "package",
        "license_plate",
        "motion",
        "audio",
    ]
    | str
)


class Detection(TypedDict):
    """Detection result from object/motion/audio detection."""

    label: ObjectClassLabel  # Object class label
    confidence: float  # Detection confidence (0-1)
    box: BoundingBox  # Bounding box
    sourcePluginId: NotRequired[str]  # Source plugin ID
    zone: NotRequired[str]  # Zone name (if detection zone matched)


# ========== Specialized Detection Types ==========


class FaceLandmarks(TypedDict):
    """Face landmarks."""

    leftEye: tuple[float, float]
    rightEye: tuple[float, float]
    nose: tuple[float, float]
    leftMouth: tuple[float, float]
    rightMouth: tuple[float, float]


class FaceDetection(Detection):
    """Face detection with identity info."""

    identity: NotRequired[str]  # Face identity (if recognized)
    embedding: NotRequired[list[float]]  # Face embedding vector
    landmarks: NotRequired[FaceLandmarks]  # Landmarks (eyes, nose, mouth)


class LicensePlateDetection(Detection):
    """License plate detection."""

    plateText: str  # Plate text (OCR result)
    plateConfidence: float  # Plate confidence


# ========== PTZ Types ==========


class PTZPosition(TypedDict):
    """PTZ Position."""

    pan: float  # Pan angle (-180 to 180)
    tilt: float  # Tilt angle (-90 to 90)
    zoom: float  # Zoom level (0 to 1)


class PTZDirection(TypedDict):
    """PTZ Movement direction (for continuous movement)."""

    panSpeed: float  # Pan speed (-1 to 1, negative = left)
    tiltSpeed: float  # Tilt speed (-1 to 1, negative = down)
    zoomSpeed: float  # Zoom speed (-1 to 1, negative = out)


# ========== Battery Types ==========


class ChargingState(str, Enum):
    """Charging state for battery."""

    NotChargeable = "NOT_CHARGEABLE"
    NotCharging = "NOT_CHARGING"
    Charging = "CHARGING"
    Full = "FULL"


# ========== Event Types ==========


class PropertyChangedEvent(TypedDict):
    """Property changed event."""

    cameraId: str
    sensorId: str
    sensorType: SensorType
    property: str  # SensorPropertyType
    value: object
    previousValue: NotRequired[object]
    timestamp: int


class SensorOnlineEvent(TypedDict):
    """Sensor online/offline event."""

    cameraId: str
    sensorId: str
    sensorType: SensorType
    online: bool


class StoredSensorData(TypedDict):
    """Stored sensor data (for sensor:added event)."""

    id: str
    type: SensorType
    name: str  # Stable name (set by plugin, used for storage key)
    displayName: str  # Display name for UI/HomeKit
    pluginId: NotRequired[str]
    properties: dict[str, object]
    capabilities: NotRequired[list[str]]
    requiresFrames: NotRequired[bool]
    inputProperties: NotRequired[VideoInputProperties | AudioInputProperties]


class SensorRefreshedState(TypedDict):
    """Sensor refreshed state (for sensor:added event)."""

    online: bool
    properties: dict[str, object]
    capabilities: NotRequired[list[str]]
    displayName: NotRequired[str]


class SensorAddedEvent(TypedDict):
    """Sensor added event - emitted when a new sensor is registered."""

    cameraId: str
    sensor: StoredSensorData
    state: SensorRefreshedState


class SensorRemovedEvent(TypedDict):
    """Sensor removed event - emitted when a sensor is unregistered."""

    cameraId: str
    sensorId: str
    sensorType: SensorType


class SensorCapabilitiesChangedEvent(TypedDict):
    """Sensor capabilities changed event."""

    cameraId: str
    sensorId: str
    capabilities: list[str]
