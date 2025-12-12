---
title: common_types
description: Common types used across the WriftAI package.
---

# common_types module

Common types used across the WriftAI package.

<a id="wriftai.common_types.JsonValue"></a>

### JsonValue

A JSON-compatible value.

alias of `list`[JsonValue] | `Mapping`[`str`, JsonValue] | `str` | `bool` | `int` | `float` | `None`

<a id="wriftai.common_types.SchemaIO"></a>

### *class* SchemaIO

Bases: `TypedDict`

Represents input and output schemas.

<a id="wriftai.common_types.SchemaIO.input"></a>

#### input *: dict[str, Any]*

Schema for input, following JSON Schema Draft 2020-12 standards.

<a id="wriftai.common_types.SchemaIO.output"></a>

#### output *: dict[str, Any]*

Schema for output, following JSON Schema Draft 2020-12 standards.

<a id="wriftai.common_types.Schemas"></a>

### *class* Schemas

Bases: `TypedDict`

Represents schemas of a version.

<a id="wriftai.common_types.Schemas.prediction"></a>

#### prediction *: [SchemaIO](#wriftai.common_types.SchemaIO)*

The input and output schemas for a prediction.

<a id="wriftai.common_types.SortDirection"></a>

### *class* SortDirection(StrEnum)

Bases: [`StrEnum`](#wriftai.common_types.StrEnum)

Enumeration of possible sorting directions.

<a id="wriftai.common_types.SortDirection.ASC"></a>

#### ASC *= 'asc'*

<a id="wriftai.common_types.SortDirection.DESC"></a>

#### DESC *= 'desc'*

<a id="wriftai.common_types.StrEnum"></a>

### *class* StrEnum(str, Enum)

Bases: `str`, `ReprEnum`

Enum where members are also (and must be) strings

<a id="wriftai.common_types.User"></a>

### *class* User

Bases: `TypedDict`

Represents a user.

<a id="wriftai.common_types.User.id"></a>

#### id *: str*

Unique identifier of the user.

<a id="wriftai.common_types.User.username"></a>

#### username *: str*

The username of the user.

<a id="wriftai.common_types.User.avatar_url"></a>

#### avatar_url *: str*

URL of the user’s avatar.

<a id="wriftai.common_types.User.name"></a>

#### name *: str | None*

The name of the user.

<a id="wriftai.common_types.User.bio"></a>

#### bio *: str | None*

The biography of the user.

<a id="wriftai.common_types.User.urls"></a>

#### urls *: list[str] | None*

Personal or professional website URLs.

<a id="wriftai.common_types.User.location"></a>

#### location *: str | None*

Location of the user.

<a id="wriftai.common_types.User.company"></a>

#### company *: str | None*

Company the user is associated with.

<a id="wriftai.common_types.User.created_at"></a>

#### created_at *: str*

Timestamp when the user joined WriftAI.

<a id="wriftai.common_types.User.updated_at"></a>

#### updated_at *: str | None*

Timestamp when the user was last updated.

<a id="wriftai.common_types.Version"></a>

### *class* Version

Bases: `TypedDict`

Represents a version.

<a id="wriftai.common_types.Version.id"></a>

#### id *: str*

The unique identifier of the version.

<a id="wriftai.common_types.Version.release_notes"></a>

#### release_notes *: str*

Information about changes such as new features,bug fixes,
or optimizations in this version.

<a id="wriftai.common_types.Version.created_at"></a>

#### created_at *: str*

The time when the version was created.

<a id="wriftai.common_types.Version.schemas"></a>

#### schemas *: [Schemas](#wriftai.common_types.Schemas)*

The schemas of the model version.

<a id="wriftai.common_types.Version.container_image_digest"></a>

#### container_image_digest *: str*

A sha256 hash digest of the version’s container image.