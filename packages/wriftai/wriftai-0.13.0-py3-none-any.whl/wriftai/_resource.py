"""Resource module."""

from abc import ABC
from collections.abc import Mapping
from typing import Any, Optional

from wriftai.api import API
from wriftai.pagination import PaginationOptions


class Resource(ABC):
    """Abstract base class for API resources."""

    _api: API
    _MODELS_API_PREFIX = "/models"
    _VERSIONS_API_PREFIX = "/versions"
    _SEARCH_API_PREFIX = "/search"
    _ERROR_MSG_INVALID_MODEL = "Model must be in owner/name format."

    def __init__(self, api: API) -> None:
        """Initializes the Resource with an API instance.

        Args:
            api (API): An instance of the API class.
        """
        self._api = api

    def _build_search_params(
        self, q: str, pagination_options: Optional[PaginationOptions] = None
    ) -> Mapping[str, Any]:
        """Build search parameters.

        Args:
            q (str): The search query.
            pagination_options (Optional[PaginationOptions]): Optional settings to
                control pagination behavior.

        Returns:
            Mapping[str, Any]: Parameters for searching.
        """
        params = {**pagination_options} if pagination_options else {}
        params["q"] = q

        return params

    def _parse_model(self, model: str) -> tuple[str, str]:
        """Parses model string into owner and name.

        Args:
            model (str): The model reference in owner/name format
                (for example: deepseek-ai/deepseek-r1).

        Returns:
            tuple[str, str]: A tuple containing owner and name of the model.

        Raises:
            ValueError: When the provided model reference is not in owner/name format.
        """
        owner, sep, name = model.partition("/")
        if not owner or not name or not sep:
            raise ValueError(self._ERROR_MSG_INVALID_MODEL)
        return owner, name
