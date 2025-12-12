from typing import Callable

import httpx
import pytest
from respx import Router

from tests.integration.conftest import Route
from wriftai import Client, ClientOptions
from wriftai.pagination import PaginatedResponse, PaginationOptions


@pytest.mark.asyncio
@pytest.mark.parametrize("async_flag", [True, False])
async def test_list(mock_router: Callable[..., Router], async_flag: bool) -> None:
    expected_cursor = "abc123"
    expected_page_size = "10"
    expected_json = {
        "items": [
            {
                "identifier": "hardware identifier",
                "name": "hardware name",
                "gpus": 8,
                "cpus": 64,
                "ram_per_gpu_gb": 40,
                "ram_gb": 320,
                "created_at": "2025-08-13T11:48:44.371093Z",
            }
        ],
        "next_cursor": "abc123",
        "previous_cursor": None,
        "next_url": "/hardware?cursor=abc123",
        "previous_url": None,
    }

    call_count = 0

    def request_assertions(request: httpx.Request) -> None:
        nonlocal call_count
        call_count += 1
        assert request.url.params.get("cursor") == expected_cursor
        assert request.url.params.get("page_size") == expected_page_size
        assert set(request.url.params.keys()).issubset({"cursor", "page_size"})

    router = mock_router(
        route=Route(
            method="GET",
            path="/hardware",
            status_code=200,
            json=expected_json,
        ),
        callback=request_assertions,
    )

    client = Client(
        client_options=ClientOptions(
            headers={"Authorization": "test-token"},
            timeout=httpx.Timeout(15),
            transport=httpx.MockTransport(router.handler),
        )
    )

    pagination_options = PaginationOptions({
        "cursor": expected_cursor,
        "page_size": int(expected_page_size),
    })

    if async_flag:
        response = await client.hardware.async_list(
            pagination_options=pagination_options
        )
    else:
        response = client.hardware.list(pagination_options=pagination_options)

    # expected_json is a dictionary.
    # Although the structure matches the expected fields, static type checkers like mypy
    # may not be able to verify this due to dynamic typing.
    assert response == PaginatedResponse(**expected_json)  # type:ignore[arg-type]
    assert call_count == 1
