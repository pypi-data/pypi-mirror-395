"""Common types used across the WriftAI package."""

import sys
from collections.abc import Mapping
from enum import Enum
from typing import Any, TypeAlias, TypedDict, Union

__all__ = [
    "JsonValue",
    "NotRequired",
    "SchemaIO",
    "Schemas",
    "SortDirection",
    "StrEnum",
    "User",
    "Version",
]

JsonValue: TypeAlias = Union[
    list["JsonValue"],
    Mapping[str, "JsonValue"],
    str,
    bool,
    int,
    float,
    None,
]
"""A JSON-compatible value."""


class _FallbackStrEnum(str, Enum):
    """Fallback StrEnum for python 3.10 version."""

    def __str__(self) -> str:
        """Return the enum value as string."""
        return str(self.value)


if sys.version_info >= (3, 11):
    from enum import StrEnum
    from typing import NotRequired
else:
    from enum import Enum

    from typing_extensions import NotRequired

    StrEnum = _FallbackStrEnum


class User(TypedDict):
    """Represents a user."""

    id: str
    """Unique identifier of the user."""
    username: str
    """The username of the user."""
    avatar_url: str
    """URL of the user's avatar."""
    name: str | None
    """The name of the user."""
    bio: str | None
    """The biography of the user."""
    urls: list[str] | None
    """Personal or professional website URLs."""
    location: str | None
    """Location of the user."""
    company: str | None
    """Company the user is associated with."""
    created_at: str
    """Timestamp when the user joined WriftAI."""
    updated_at: str | None
    """Timestamp when the user was last updated."""


class SchemaIO(TypedDict):
    """Represents input and output schemas."""

    input: dict[str, Any]
    """Schema for input, following JSON Schema Draft 2020-12 standards."""
    output: dict[str, Any]
    """Schema for output, following JSON Schema Draft 2020-12 standards."""


class Schemas(TypedDict):
    """Represents schemas of a version."""

    prediction: SchemaIO
    """The input and output schemas for a prediction."""


class Version(TypedDict):
    """Represents a version."""

    id: str
    """The unique identifier of the version."""
    release_notes: str
    """Information about changes such as new features,bug fixes,
        or optimizations in this version."""
    created_at: str
    """The time when the version was created."""
    schemas: Schemas
    """The schemas of the model version."""
    container_image_digest: str
    """A sha256 hash digest of the version's container image."""


class Hardware(TypedDict):
    """Represents a hardware item."""

    name: str
    """The name of the hardware."""

    identifier: str
    """The identifier of the hardware."""


class SortDirection(StrEnum):
    """Enumeration of possible sorting directions."""

    ASC = "asc"
    DESC = "desc"
