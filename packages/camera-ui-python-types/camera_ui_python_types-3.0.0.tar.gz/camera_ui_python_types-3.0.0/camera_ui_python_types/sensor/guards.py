"""Type guards for sensor type narrowing."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeGuard

from .types import SensorType

if TYPE_CHECKING:
    from .audio import AudioSensorLike
    from .base import SensorLike
    from .battery import BatteryInfoLike
    from .contact import ContactSensorLike
    from .doorbell import DoorbellTriggerLike
    from .face import FaceSensorLike
    from .license_plate import LicensePlateSensorLike
    from .light import LightControlLike
    from .motion import MotionSensorLike
    from .object import ObjectSensorLike
    from .ptz import PTZControlLike
    from .siren import SirenControlLike


def isMotionSensor(sensor: SensorLike) -> TypeGuard[MotionSensorLike]:
    """
    Type guard for Motion sensors.

    Narrows a SensorLike to MotionSensorLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a Motion sensor
    """
    return sensor.type == SensorType.Motion


def isObjectSensor(sensor: SensorLike) -> TypeGuard[ObjectSensorLike]:
    """
    Type guard for Object detection sensors.

    Narrows a SensorLike to ObjectSensorLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is an Object sensor
    """
    return sensor.type == SensorType.Object


def isAudioSensor(sensor: SensorLike) -> TypeGuard[AudioSensorLike]:
    """
    Type guard for Audio sensors.

    Narrows a SensorLike to AudioSensorLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is an Audio sensor
    """
    return sensor.type == SensorType.Audio


def isFaceSensor(sensor: SensorLike) -> TypeGuard[FaceSensorLike]:
    """
    Type guard for Face detection sensors.

    Narrows a SensorLike to FaceSensorLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a Face sensor
    """
    return sensor.type == SensorType.Face


def isLicensePlateSensor(sensor: SensorLike) -> TypeGuard[LicensePlateSensorLike]:
    """
    Type guard for License Plate detection sensors.

    Narrows a SensorLike to LicensePlateSensorLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a License Plate sensor
    """
    return sensor.type == SensorType.LicensePlate


def isContactSensor(sensor: SensorLike) -> TypeGuard[ContactSensorLike]:
    """
    Type guard for Contact sensors.

    Narrows a SensorLike to ContactSensorLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a Contact sensor
    """
    return sensor.type == SensorType.Contact


def isLightControl(sensor: SensorLike) -> TypeGuard[LightControlLike]:
    """
    Type guard for Light controls.

    Narrows a SensorLike to LightControlLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a Light control
    """
    return sensor.type == SensorType.Light


def isSirenControl(sensor: SensorLike) -> TypeGuard[SirenControlLike]:
    """
    Type guard for Siren controls.

    Narrows a SensorLike to SirenControlLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a Siren control
    """
    return sensor.type == SensorType.Siren


def isPTZControl(sensor: SensorLike) -> TypeGuard[PTZControlLike]:
    """
    Type guard for PTZ controls.

    Narrows a SensorLike to PTZControlLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a PTZ control
    """
    return sensor.type == SensorType.PTZ


def isDoorbellTrigger(sensor: SensorLike) -> TypeGuard[DoorbellTriggerLike]:
    """
    Type guard for Doorbell triggers.

    Narrows a SensorLike to DoorbellTriggerLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a Doorbell trigger
    """
    return sensor.type == SensorType.Doorbell


def isBatteryInfo(sensor: SensorLike) -> TypeGuard[BatteryInfoLike]:
    """
    Type guard for Battery info sensors.

    Narrows a SensorLike to BatteryInfoLike for type-safe property access.

    Args:
        sensor: The sensor to check

    Returns:
        True if the sensor is a Battery info sensor
    """
    return sensor.type == SensorType.Battery
