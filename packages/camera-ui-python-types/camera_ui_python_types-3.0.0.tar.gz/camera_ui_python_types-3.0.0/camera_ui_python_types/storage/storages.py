"""Storage interfaces for plugins."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from .schema import FormSubmitResponse, JsonSchema, SchemaConfig


@runtime_checkable
class DeviceStorage(Protocol):
    """Device storage for plugin configuration."""

    @property
    def schemas(self) -> list[JsonSchema]:
        """Get all schemas."""
        ...

    @property
    def values(self) -> dict[str, Any]:
        """Get all values."""
        ...

    async def getValue(self, key: str, defaultValue: Any | None = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            defaultValue: Default value if key doesn't exist

        Returns:
            The configuration value or default
        """
        ...

    async def setValue(self, key: str, newValue: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key
            newValue: New value to set
        """
        ...

    async def submitValue(self, key: str, newValue: Any) -> FormSubmitResponse | None:
        """
        Submit a value (for button/submit schemas).

        Args:
            key: Schema key
            newValue: Value to submit

        Returns:
            Optional response with toast message or new schema
        """
        ...

    def hasValue(self, key: str) -> bool:
        """
        Check if a value exists.

        Args:
            key: Configuration key

        Returns:
            True if the value exists
        """
        ...

    async def getConfig(self) -> SchemaConfig:
        """
        Get the full configuration.

        Returns:
            Schema configuration with schemas and values
        """
        ...

    async def setConfig(self, newConfig: dict[str, Any]) -> None:
        """
        Set the full configuration.

        Args:
            newConfig: New configuration values
        """
        ...

    async def addSchema(self, schema: JsonSchema) -> None:
        """
        Add a new schema.

        Args:
            schema: Schema to add
        """
        ...

    async def removeSchema(self, key: str) -> None:
        """
        Remove a schema.

        Args:
            key: Schema key to remove
        """
        ...

    async def changeSchema(self, key: str, newSchema: dict[str, Any]) -> None:
        """
        Update a schema.

        Args:
            key: Schema key to update
            newSchema: Partial schema with updates
        """
        ...

    def getSchema(self, key: str) -> JsonSchema | None:
        """
        Get a schema by key.

        Args:
            key: Schema key

        Returns:
            The schema or None if not found
        """
        ...

    def hasSchema(self, key: str) -> bool:
        """
        Check if a schema exists.

        Args:
            key: Schema key

        Returns:
            True if the schema exists
        """
        ...

    async def save(self) -> None:
        """Save configuration to persistent storage."""
        ...


@runtime_checkable
class StorageController(Protocol):
    """Storage controller for creating device/plugin storage."""

    def createCameraStorage(
        self, instance: Any, cameraId: str, schemas: list[JsonSchema] | None = None
    ) -> DeviceStorage:
        """
        Create storage for a camera.

        Args:
            instance: Plugin instance
            cameraId: Camera ID
            schemas: Optional initial schemas

        Returns:
            Device storage instance
        """
        ...

    def createPluginStorage(self, instance: Any, schemas: list[JsonSchema] | None = None) -> DeviceStorage:
        """
        Create storage for a plugin.

        Args:
            instance: Plugin instance
            schemas: Optional initial schemas

        Returns:
            Device storage instance
        """
        ...

    def getCameraStorage(self, cameraId: str) -> DeviceStorage | None:
        """
        Get storage for a camera.

        Args:
            cameraId: Camera ID

        Returns:
            Device storage or None if not found
        """
        ...

    def getPluginStorage(self) -> DeviceStorage | None:
        """
        Get storage for the plugin.

        Returns:
            Device storage or None if not found
        """
        ...
