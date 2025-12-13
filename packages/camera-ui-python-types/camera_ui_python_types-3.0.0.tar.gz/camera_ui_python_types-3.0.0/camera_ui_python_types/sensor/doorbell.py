"""Doorbell trigger sensor types and classes."""

from __future__ import annotations

import asyncio
from enum import Enum
from typing import Protocol, runtime_checkable

from .base import Sensor, SensorLike
from .types import SensorCategory, SensorType


class DoorbellProperty(str, Enum):
    """Doorbell trigger properties."""

    Ring = "ring"


@runtime_checkable
class DoorbellTriggerLike(SensorLike, Protocol):
    """Protocol for doorbell trigger type checking."""

    @property
    def ring(self) -> bool:
        """Whether doorbell is currently ringing."""
        ...

    def triggerRing(self, resetAfterMs: int = 1000) -> None:
        """Trigger doorbell ring."""
        ...

    def resetRing(self) -> None:
        """Reset ring state immediately."""
        ...


class DoorbellTrigger(Sensor[dict[str, object], dict[str, object], str]):
    """
    Doorbell Trigger.

    Event-based trigger for doorbell rings.
    Ring property auto-resets after a short delay.
    """

    _requires_frames = False
    _reset_task: asyncio.Task[None] | None = None

    def __init__(self, camera_id: str, name: str = "Doorbell") -> None:
        super().__init__(camera_id, name)
        # Initialize defaults
        self._setProperty(DoorbellProperty.Ring, False)

    @property
    def type(self) -> SensorType:
        return SensorType.Doorbell

    @property
    def category(self) -> SensorCategory:
        return SensorCategory.Trigger

    @property
    def ring(self) -> bool:
        """Whether doorbell is currently ringing."""
        return self.getPropertyValue(DoorbellProperty.Ring) or False

    @ring.setter
    def ring(self, value: bool) -> None:
        self._setProperty(DoorbellProperty.Ring, value)

    # RPC methods (camelCase for compatibility)

    def triggerRing(self, resetAfterMs: int = 1000) -> None:
        """
        Trigger doorbell ring.
        Auto-resets after duration (default: 1000ms).

        Args:
            resetAfterMs: Duration in milliseconds to auto-reset ring state
        """
        # Cancel any existing reset task
        if self._reset_task and not self._reset_task.done():
            self._reset_task.cancel()

        self.ring = True

        # Auto-reset after duration
        async def reset_after_delay() -> None:
            await asyncio.sleep(resetAfterMs / 1000)
            self.ring = False

        try:
            loop = asyncio.get_running_loop()
            self._reset_task = loop.create_task(reset_after_delay())
        except RuntimeError:
            # No event loop running, just set the ring state
            pass

    def resetRing(self) -> None:
        """Reset ring state immediately."""
        if self._reset_task and not self._reset_task.done():
            self._reset_task.cancel()
            self._reset_task = None
        self.ring = False
