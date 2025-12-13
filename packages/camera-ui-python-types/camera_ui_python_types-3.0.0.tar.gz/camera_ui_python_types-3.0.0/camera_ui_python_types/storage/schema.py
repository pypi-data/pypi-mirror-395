"""JSON Schema types for plugin configuration."""

from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable, Literal, NotRequired, TypedDict

# JSON types
JSONValue = dict[str, Any] | list[Any] | str | int | float | bool | None
JSONObject = dict[str, JSONValue]
JSONArray = list[JSONValue]
Path = list[int | str] | int | str

# Plugin config type
PluginConfig = dict[str, Any]

# Schema types
JsonSchemaType = Literal["string", "number", "boolean", "array", "button", "submit"]


class JsonFactorySchema(TypedDict):
    """Base schema factory type."""

    type: JsonSchemaType
    key: str
    title: str
    description: str
    group: NotRequired[str]


class JsonBaseSchemaWithoutCallbacks(JsonFactorySchema, total=False):
    """Base schema without callbacks."""

    hidden: bool
    required: bool
    readonly: bool
    placeholder: str
    defaultValue: Any


class JsonBaseSchema(JsonBaseSchemaWithoutCallbacks, total=False):
    """Base schema with optional callbacks."""

    store: bool
    onSet: Callable[[Any, Any], Awaitable[None]]
    onGet: Callable[[], Awaitable[Any]]


class JsonStringSchema(TypedDict, total=False):
    """String schema properties."""

    type: Literal["string"]
    format: Literal[
        "date-time", "date", "time", "email", "uuid", "ipv4", "ipv6", "password", "qrCode", "image"
    ]
    minLength: int
    maxLength: int


class JsonNumberSchema(TypedDict, total=False):
    """Number schema properties."""

    type: Literal["number"]
    minimum: int | float
    maximum: int | float
    step: int | float


class JsonBooleanSchema(TypedDict):
    """Boolean schema properties."""

    type: Literal["boolean"]


class JsonEnumSchema(TypedDict, total=False):
    """Enum schema properties."""

    type: Literal["string"]
    enum: list[str]
    multiple: bool


class JsonArraySchema(TypedDict, total=False):
    """Array schema properties."""

    type: Literal["array"]
    opened: bool
    items: dict[str, Any]  # JsonSchemaWithoutCallbacks without key


# Union types for all schema variants
JsonSchema = dict[str, Any]  # Union of all schema types
JsonSchemaWithoutKey = dict[str, Any]
JsonSchemaWithoutCallbacks = dict[str, Any]


class ToastMessage(TypedDict):
    """Toast notification message."""

    type: Literal["info", "success", "warning", "error"]
    message: str


class FormSubmitSchema(TypedDict):
    """Form submit schema."""

    config: dict[str, Any]


class FormSubmitResponse(TypedDict, total=False):
    """Form submit response."""

    toast: ToastMessage
    schema: list[JsonSchemaWithoutCallbacks]


class SchemaConfig(TypedDict):
    """Schema configuration."""

    schema: list[JsonSchema]
    config: dict[str, Any]
