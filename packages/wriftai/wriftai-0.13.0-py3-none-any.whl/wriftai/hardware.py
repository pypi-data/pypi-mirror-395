"""Hardware module."""

from typing import Optional

from wriftai._resource import Resource
from wriftai.common_types import Hardware
from wriftai.pagination import PaginatedResponse, PaginationOptions


class HardwareWithDetails(Hardware):
    """Represents a hardware item with more details."""

    gpus: int
    """Number of GPUs available on the hardware."""
    cpus: int
    """Number of CPUs available on the hardware."""
    ram_per_gpu_gb: int
    """Amount of Ram (in GB) allocated per GPU."""
    ram_gb: int
    """Total RAM (in GB) available on the hardware."""
    created_at: str
    """Timestamp when the hardware was created."""


class HardwareResource(Resource):
    """Resource for operations related to hardware."""

    _API_PREFIX = "/hardware"

    def list(
        self, pagination_options: Optional[PaginationOptions] = None
    ) -> PaginatedResponse[Hardware]:
        """List hardware.

        Args:
            pagination_options (Optional[PaginationOptions]): Optional settings
                to control pagination behavior.

        Returns:
            PaginatedResponse[Hardware]: Paginated response containing
                hardware items and navigation metadata.
        """
        response = self._api.request(
            method="GET", params=pagination_options, path=self._API_PREFIX
        )

        # The response will always match the PaginatedResponse structure,
        # but static type checkers may not infer this correctly.
        # Hence, we ignore the argument type warning.
        return PaginatedResponse(**response)  # type:ignore[arg-type]

    async def async_list(
        self, pagination_options: Optional[PaginationOptions] = None
    ) -> PaginatedResponse[Hardware]:
        """List hardware.

        Args:
            pagination_options (Optional[PaginationOptions]): Optional settings
                to control pagination behavior.

        Returns:
            PaginatedResponse[Hardware]: Paginated response containing
                hardware items and navigation metadata.
        """
        response = await self._api.async_request(
            method="GET", params=pagination_options, path=self._API_PREFIX
        )
        # The response will always match the PaginatedResponse structure,
        # but static type checkers may not infer this correctly.
        # Hence, we ignore the argument type warning.
        return PaginatedResponse(**response)  # type:ignore[arg-type]
