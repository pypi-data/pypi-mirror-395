---
title: hardware
description: Hardware module.
---

# hardware module

Hardware module.

<a id="wriftai.hardware.HardwareWithDetails"></a>

### *class* HardwareWithDetails

Bases: `Hardware`

Represents a hardware item with more details.

<a id="wriftai.hardware.HardwareWithDetails.gpus"></a>

#### gpus *: int*

Number of GPUs available on the hardware.

<a id="wriftai.hardware.HardwareWithDetails.cpus"></a>

#### cpus *: int*

Number of CPUs available on the hardware.

<a id="wriftai.hardware.HardwareWithDetails.ram_per_gpu_gb"></a>

#### ram_per_gpu_gb *: int*

Amount of Ram (in GB) allocated per GPU.

<a id="wriftai.hardware.HardwareWithDetails.ram_gb"></a>

#### ram_gb *: int*

Total RAM (in GB) available on the hardware.

<a id="wriftai.hardware.HardwareWithDetails.name"></a>

#### name *: str*

<a id="wriftai.hardware.HardwareWithDetails.identifier"></a>

#### identifier *: str*

<a id="wriftai.hardware.HardwareWithDetails.created_at"></a>

#### created_at *: str*

Timestamp when the hardware was created.

<a id="wriftai.hardware.HardwareResource"></a>

### *class* HardwareResource(api)

Bases: `Resource`

Initializes the Resource with an API instance.

* **Parameters:**
  **api** ([*API*](wriftai.api.md#wriftai.api.API)) – An instance of the API class.

<a id="wriftai.hardware.HardwareResource.list"></a>

#### list(pagination_options=None)

List hardware.

* **Parameters:**
  **pagination_options** (*Optional* *[*[*PaginationOptions*](wriftai.md#wriftai.PaginationOptions) *]*) – Optional settings
  to control pagination behavior.
* **Returns:**
  Paginated response containing
  : hardware items and navigation metadata.
* **Return type:**
  [PaginatedResponse](wriftai.pagination.md#wriftai.pagination.PaginatedResponse)[Hardware]

<a id="wriftai.hardware.HardwareResource.async_list"></a>

#### *async* async_list(pagination_options=None)

List hardware.

* **Parameters:**
  **pagination_options** (*Optional* *[*[*PaginationOptions*](wriftai.md#wriftai.PaginationOptions) *]*) – Optional settings
  to control pagination behavior.
* **Returns:**
  Paginated response containing
  : hardware items and navigation metadata.
* **Return type:**
  [PaginatedResponse](wriftai.pagination.md#wriftai.pagination.PaginatedResponse)[Hardware]