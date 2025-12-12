---
title: pagination
description: Pagination module.
---

# pagination module

Pagination module.

<a id="wriftai.pagination.PaginatedResponse"></a>

### *class* PaginatedResponse(items, next_cursor, previous_cursor, next_url, previous_url)

Bases: `Generic`[`T`]

Represents a paginated response.

* **Parameters:**
  * **items** (*list* *[**T* *]*)
  * **next_cursor** (*str* *|* *None*)
  * **previous_cursor** (*str* *|* *None*)
  * **next_url** (*str* *|* *None*)
  * **previous_url** (*str* *|* *None*)

<a id="wriftai.pagination.PaginatedResponse.items"></a>

#### items *: list[T]*

List of items returned in the current page.

<a id="wriftai.pagination.PaginatedResponse.next_cursor"></a>

#### next_cursor *: str | None*

Cursor pointing to the next page.

<a id="wriftai.pagination.PaginatedResponse.previous_cursor"></a>

#### previous_cursor *: str | None*

Cursor pointing to the previous page.

<a id="wriftai.pagination.PaginatedResponse.next_url"></a>

#### next_url *: str | None*

URL to fetch the next page.

<a id="wriftai.pagination.PaginatedResponse.previous_url"></a>

#### previous_url *: str | None*

URL to fetch the previous page.