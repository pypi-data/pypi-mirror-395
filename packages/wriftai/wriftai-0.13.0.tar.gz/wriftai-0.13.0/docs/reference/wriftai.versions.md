---
title: versions
description: Versions module.
---

# versions module

Versions module.

<a id="wriftai.versions.CreateVersionParams"></a>

### *class* CreateVersionParams

Bases: `TypedDict`

Parameters for creating a version of a model.

* **Variables:**
  * **release_notes** (*str*) – Information about changes such as new features,
    bug fixes, or optimizations in this version.
  * **schemas** ([*Schemas*](wriftai.common_types.md#wriftai.common_types.Schemas)) – Schemas for the model version.
  * **container_image_digest** (*str*) – SHA256 hash digest of the version’s
    container image.

<a id="wriftai.versions.CreateVersionParams.release_notes"></a>

#### release_notes *: str*

<a id="wriftai.versions.CreateVersionParams.schemas"></a>

#### schemas *: [Schemas](wriftai.common_types.md#wriftai.common_types.Schemas)*

<a id="wriftai.versions.CreateVersionParams.container_image_digest"></a>

#### container_image_digest *: str*

<a id="wriftai.versions.Versions"></a>

### *class* Versions(api)

Bases: `Resource`

Initializes the Resource with an API instance.

* **Parameters:**
  **api** ([*API*](wriftai.api.md#wriftai.api.API)) – An instance of the API class.

<a id="wriftai.versions.Versions.get"></a>

#### get(version_id)

Fetch a model version by its id.

* **Parameters:**
  **version_id** (*str*) – The unique identifier of the version.
* **Returns:**
  The model version.
* **Return type:**
  [Version](wriftai.common_types.md#wriftai.common_types.Version)

<a id="wriftai.versions.Versions.async_get"></a>

#### *async* async_get(version_id)

Fetch a model version by its id.

* **Parameters:**
  **version_id** (*str*) – The unique identifier of the version.
* **Returns:**
  The model version.
* **Return type:**
  [Version](wriftai.common_types.md#wriftai.common_types.Version)

<a id="wriftai.versions.Versions.list"></a>

#### list(model_owner, model_name, pagination_options=None)

List versions.

* **Parameters:**
  * **model_owner** (*str*) – Username of the model’s owner.
  * **model_name** (*str*) – Name of the model.
  * **pagination_options** (*Optional* *[*[*PaginationOptions*](wriftai.md#wriftai.PaginationOptions) *]*) – Optional settings
    to control pagination behavior.
* **Returns:**
  Paginated response containing versions
  : and navigation metadata.
* **Return type:**
  [PaginatedResponse](wriftai.pagination.md#wriftai.pagination.PaginatedResponse)[[Version](wriftai.common_types.md#wriftai.common_types.Version)]

<a id="wriftai.versions.Versions.async_list"></a>

#### *async* async_list(model_owner, model_name, pagination_options=None)

List versions.

* **Parameters:**
  * **model_owner** (*str*) – Username of the model’s owner.
  * **model_name** (*str*) – Name of the model.
  * **pagination_options** (*Optional* *[*[*PaginationOptions*](wriftai.md#wriftai.PaginationOptions) *]*) – Optional settings
    to control pagination behavior.
* **Returns:**
  Paginated response containing versions
  : and navigation metadata.
* **Return type:**
  [PaginatedResponse](wriftai.pagination.md#wriftai.pagination.PaginatedResponse)[[Version](wriftai.common_types.md#wriftai.common_types.Version)]

<a id="wriftai.versions.Versions.delete"></a>

#### delete(version_id)

Delete a model version by its id.

* **Parameters:**
  **version_id** (*str*) – The unique identifier of the version.
* **Return type:**
  None

<a id="wriftai.versions.Versions.async_delete"></a>

#### *async* async_delete(version_id)

Delete a model version by its id.

* **Parameters:**
  **version_id** (*str*) – The unique identifier of the version.
* **Return type:**
  None

<a id="wriftai.versions.Versions.create"></a>

#### create(model_owner, model_name, options)

Create a version of a model.

* **Parameters:**
  * **model_owner** (*str*) – Username of the model’s owner.
  * **model_name** (*str*) – Name of the model.
  * **options** (*VersionCreateParams*) – Model’s version creation parameters.
* **Returns:**
  The new version.
* **Return type:**
  [Version](wriftai.common_types.md#wriftai.common_types.Version)

<a id="wriftai.versions.Versions.async_create"></a>

#### *async* async_create(model_owner, model_name, options)

Create a version of a model.

* **Parameters:**
  * **model_owner** (*str*) – Username of the model’s owner.
  * **model_name** (*str*) – Name of the model.
  * **options** (*VersionCreateParams*) – Model’s version creation parameters.
* **Returns:**
  The new version.
* **Return type:**
  [Version](wriftai.common_types.md#wriftai.common_types.Version)