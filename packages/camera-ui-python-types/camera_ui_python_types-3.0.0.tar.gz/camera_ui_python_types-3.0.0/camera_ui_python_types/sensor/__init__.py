"""Sensor module exports."""

# Base
# Audio
from .audio import (
    AudioDetectorSensor,
    AudioDetectorSensorLike,
    AudioProperty,
    AudioSensor,
    AudioSensorLike,
)
from .base import Sensor, SensorLike

# Battery
from .battery import (
    BatteryCapability,
    BatteryInfo,
    BatteryInfoLike,
    BatteryProperty,
)

# Contact
from .contact import (
    ContactProperty,
    ContactSensor,
    ContactSensorLike,
)

# Doorbell
from .doorbell import (
    DoorbellProperty,
    DoorbellTrigger,
    DoorbellTriggerLike,
)

# Face
from .face import (
    FaceDetectorSensor,
    FaceDetectorSensorLike,
    FaceProperty,
    FaceSensor,
    FaceSensorLike,
)

# Guards
from .guards import (
    isAudioSensor,
    isBatteryInfo,
    isContactSensor,
    isDoorbellTrigger,
    isFaceSensor,
    isLicensePlateSensor,
    isLightControl,
    isMotionSensor,
    isObjectSensor,
    isPTZControl,
    isSirenControl,
)

# License Plate
from .license_plate import (
    LicensePlateDetectorSensor,
    LicensePlateDetectorSensorLike,
    LicensePlateProperty,
    LicensePlateSensor,
    LicensePlateSensorLike,
)

# Light
from .light import (
    LightCapability,
    LightControl,
    LightControlLike,
    LightProperty,
)

# Motion
from .motion import (
    MotionDetectorSensor,
    MotionDetectorSensorLike,
    MotionProperty,
    MotionSensor,
    MotionSensorLike,
)

# Object
from .object import (
    ObjectDetectorSensor,
    ObjectDetectorSensorLike,
    ObjectProperty,
    ObjectSensor,
    ObjectSensorLike,
)

# PTZ
from .ptz import (
    PTZCapability,
    PTZControl,
    PTZControlLike,
    PTZProperty,
)

# Siren
from .siren import (
    SirenCapability,
    SirenControl,
    SirenControlLike,
    SirenProperty,
)

# Types
from .types import (
    AudioInputProperties,
    BoundingBox,
    ChargingState,
    Detection,
    FaceDetection,
    FaceLandmarks,
    LicensePlateDetection,
    ObjectClassLabel,
    PropertyChangedEvent,
    PTZDirection,
    PTZPosition,
    SensorAddedEvent,
    SensorCapabilitiesChangedEvent,
    SensorCategory,
    SensorOnlineEvent,
    SensorRefreshedState,
    SensorRemovedEvent,
    SensorType,
    StoredSensorData,
    VideoInputProperties,
)

__all__ = [
    # Base
    "Sensor",
    "SensorLike",
    # Types
    "AudioInputProperties",
    "BoundingBox",
    "ChargingState",
    "Detection",
    "FaceDetection",
    "FaceLandmarks",
    "LicensePlateDetection",
    "ObjectClassLabel",
    "PropertyChangedEvent",
    "PTZDirection",
    "PTZPosition",
    "SensorAddedEvent",
    "SensorCapabilitiesChangedEvent",
    "SensorCategory",
    "SensorOnlineEvent",
    "SensorRefreshedState",
    "SensorRemovedEvent",
    "SensorType",
    "StoredSensorData",
    "VideoInputProperties",
    # Motion
    "MotionProperty",
    "MotionSensorLike",
    "MotionDetectorSensorLike",
    "MotionSensor",
    "MotionDetectorSensor",
    # Object
    "ObjectProperty",
    "ObjectSensorLike",
    "ObjectDetectorSensorLike",
    "ObjectSensor",
    "ObjectDetectorSensor",
    # Audio
    "AudioProperty",
    "AudioSensorLike",
    "AudioDetectorSensorLike",
    "AudioSensor",
    "AudioDetectorSensor",
    # Face
    "FaceProperty",
    "FaceSensorLike",
    "FaceDetectorSensorLike",
    "FaceSensor",
    "FaceDetectorSensor",
    # License Plate
    "LicensePlateProperty",
    "LicensePlateSensorLike",
    "LicensePlateDetectorSensorLike",
    "LicensePlateSensor",
    "LicensePlateDetectorSensor",
    # Contact
    "ContactProperty",
    "ContactSensorLike",
    "ContactSensor",
    # Light
    "LightCapability",
    "LightProperty",
    "LightControlLike",
    "LightControl",
    # Siren
    "SirenCapability",
    "SirenProperty",
    "SirenControlLike",
    "SirenControl",
    # PTZ
    "PTZCapability",
    "PTZProperty",
    "PTZControlLike",
    "PTZControl",
    # Doorbell
    "DoorbellProperty",
    "DoorbellTriggerLike",
    "DoorbellTrigger",
    # Battery
    "BatteryCapability",
    "BatteryProperty",
    "BatteryInfoLike",
    "BatteryInfo",
    # Guards
    "isMotionSensor",
    "isObjectSensor",
    "isAudioSensor",
    "isFaceSensor",
    "isLicensePlateSensor",
    "isContactSensor",
    "isLightControl",
    "isSirenControl",
    "isPTZControl",
    "isDoorbellTrigger",
    "isBatteryInfo",
]
