---
title: api
description: API client module.
---

# api module

API client module.

<a id="wriftai.api.API"></a>

### *class* API(sync_client, async_client)

Bases: `object`

Initializes the API with synchronous and asynchronous HTTP clients.

* **Parameters:**
  * **sync_client** (*httpx.Client*) – An instance of a synchronous HTTP client.
  * **async_client** (*httpx.AsyncClient*) – An instance of an asynchronous HTTP
    client.

<a id="wriftai.api.API.request"></a>

#### request(method, path, body=None, headers=None, params=None)

Sends a synchronous HTTP request using the configured sync client.

* **Parameters:**
  * **method** (*str*) – The HTTP method to use (e.g., ‘GET’, ‘POST’).
  * **path** (*str*) – The URL path to send the request to.
  * **body** (Optional[JsonValue]) – The JSON body to include in
    the request.
  * **headers** (Optional[dict[str, Any]]) – Optional HTTP headers to
    include in the request.
  * **params** (Optional[Mapping[str, Any]]) – Optional query parameters.
* **Returns:**
  The json response received from the server.
* **Return type:**
  JsonValue

<a id="wriftai.api.API.async_request"></a>

#### *async* async_request(method, path, body=None, headers=None, params=None)

Sends an asynchronous HTTP request using the configured async client.

* **Parameters:**
  * **method** (*str*) – The HTTP method to use (e.g., ‘GET’, ‘POST’).
  * **path** (*str*) – The URL path to send the request to.
  * **body** (Optional[JsonValue]) – The JSON body to include in
    the request.
  * **headers** (Optional[dict[str, Any]]) – Optional HTTP headers to
    include in the request.
  * **params** (Optional[Mapping[str, Any]]) – Optional query parameters.
* **Returns:**
  The json response received from the server.
* **Return type:**
  JsonValue