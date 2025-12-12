from typing import Any, Callable, Optional, TypedDict

import pytest
import respx
from httpx import Request, Response

from wriftai._client import API_BASE_URL


class Route(TypedDict):
    method: str
    path: str
    status_code: int
    json: dict[str, Any]


@pytest.fixture(scope="function")
def mock_router() -> Callable[..., respx.Router]:
    def _create_mock(
        *,
        route: Route,
        base_url: str = API_BASE_URL,
        callback: Optional[Callable[[Request], None]] = None,
    ) -> respx.Router:
        router = respx.Router(base_url=base_url)

        def handler(request: Request) -> Response:
            if callback:
                callback(request)
            return Response(route.get("status_code", 200), json=route["json"])

        router.route(
            method=route.get("method", "GET"),
            path=route["path"],
        ).mock(side_effect=handler)

        return router

    return _create_mock
