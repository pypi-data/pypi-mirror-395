"""Service types and event types."""

from __future__ import annotations

from enum import Enum
from typing import TypedDict


class ServiceType(str, Enum):
    """Service types that can be registered by plugins."""

    Streaming = "streaming"
    Snapshot = "snapshot"


class ServiceRegistration(TypedDict):
    """Service registration info."""

    type: ServiceType
    pluginId: str
    online: bool


class ServiceOnlineEvent(TypedDict):
    """Service online status change event."""

    cameraId: str
    serviceType: ServiceType
    pluginId: str
    online: bool
