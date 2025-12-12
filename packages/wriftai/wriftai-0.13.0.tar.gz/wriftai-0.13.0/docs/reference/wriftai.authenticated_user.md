---
title: authenticated_user
description: Authenticated user module.
---

# authenticated_user module

Authenticated user module.

<a id="wriftai.authenticated_user.UpdateUserParams"></a>

### *class* UpdateUserParams

Bases: `TypedDict`

Parameters for updating a user.

<a id="wriftai.authenticated_user.UpdateUserParams.username"></a>

#### username *: NotRequired[str]*

The new username of the user.

<a id="wriftai.authenticated_user.UpdateUserParams.name"></a>

#### name *: NotRequired[str | None]*

The new name of the user.

<a id="wriftai.authenticated_user.UpdateUserParams.bio"></a>

#### bio *: NotRequired[str | None]*

The new biography of the user.

<a id="wriftai.authenticated_user.UpdateUserParams.urls"></a>

#### urls *: NotRequired[list[str] | None]*

The new URLs associated with the user.

<a id="wriftai.authenticated_user.UpdateUserParams.company"></a>

#### company *: NotRequired[str | None]*

The new company of the user.

<a id="wriftai.authenticated_user.UpdateUserParams.location"></a>

#### location *: NotRequired[str | None]*

The new location of the user.

<a id="wriftai.authenticated_user.AuthenticatedUser"></a>

### *class* AuthenticatedUser(api)

Bases: `Resource`

Initializes the Resource with an API instance.

* **Parameters:**
  **api** ([*API*](wriftai.api.md#wriftai.api.API)) – An instance of the API class.

<a id="wriftai.authenticated_user.AuthenticatedUser.get"></a>

#### get()

Get the authenticated user.

* **Returns:**
  The user object.
* **Return type:**
  [User](wriftai.common_types.md#wriftai.common_types.User)

<a id="wriftai.authenticated_user.AuthenticatedUser.async_get"></a>

#### *async* async_get()

Get authenticated user.

* **Returns:**
  The user object.
* **Return type:**
  [User](wriftai.common_types.md#wriftai.common_types.User)

<a id="wriftai.authenticated_user.AuthenticatedUser.models"></a>

#### models(pagination_options=None)

List models of the authenticated user.

* **Parameters:**
  **pagination_options** (*Optional* *[*[*PaginationOptions*](wriftai.md#wriftai.PaginationOptions) *]*) – Optional settings
  to control pagination behavior.
* **Returns:**
  Paginated response containing models
  : and navigation metadata.
* **Return type:**
  [PaginatedResponse](wriftai.pagination.md#wriftai.pagination.PaginatedResponse)[[Model](wriftai.models.md#wriftai.models.Model)]

<a id="wriftai.authenticated_user.AuthenticatedUser.async_models"></a>

#### *async* async_models(pagination_options=None)

List models of the authenticated user.

* **Parameters:**
  **pagination_options** (*Optional* *[*[*PaginationOptions*](wriftai.md#wriftai.PaginationOptions) *]*) – Optional settings
  to control pagination behavior.
* **Returns:**
  Paginated response containing models
  : and navigation metadata.
* **Return type:**
  [PaginatedResponse](wriftai.pagination.md#wriftai.pagination.PaginatedResponse)[[Model](wriftai.models.md#wriftai.models.Model)]

<a id="wriftai.authenticated_user.AuthenticatedUser.update"></a>

#### update(params)

Update the authenticated user.

* **Parameters:**
  **params** ([*UpdateUserParams*](#wriftai.authenticated_user.UpdateUserParams)) – The fields to update.
* **Returns:**
  The updated user object.
* **Return type:**
  [User](wriftai.common_types.md#wriftai.common_types.User)

<a id="wriftai.authenticated_user.AuthenticatedUser.async_update"></a>

#### *async* async_update(params)

Update the authenticated user.

* **Parameters:**
  **params** ([*UpdateUserParams*](#wriftai.authenticated_user.UpdateUserParams)) – The fields to update.
* **Returns:**
  The updated user object.
* **Return type:**
  [User](wriftai.common_types.md#wriftai.common_types.User)