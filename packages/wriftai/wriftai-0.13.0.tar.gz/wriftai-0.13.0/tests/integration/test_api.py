import json
import re
from typing import Callable

import httpx
import pytest
from respx import Router

from tests.integration.conftest import Route
from wriftai import Client, ClientOptions


@pytest.mark.asyncio
@pytest.mark.parametrize("async_flag", [True, False])
async def test_request(mock_router: Callable[..., Router], async_flag: bool) -> None:
    expected_json = {"key": "value"}
    expected_method = "POST"
    expected_path = "/request"
    test_headers = {"headers-key": "headers-value"}
    test_body = {"body-key": "body-value"}
    test_user_agent = r"^wriftai-python/\d+\.\d+\.\d+(-[\w.-]+)?$"
    expected_access_token = "some-access-token"  # noqa: S105

    call_count = 0

    def request_assertions(request: httpx.Request) -> None:
        nonlocal call_count
        call_count += 1
        assert request.method == expected_method
        assert request.url.path == f"/v1{expected_path}"
        assert re.match(test_user_agent, request.headers.get("user-agent"))
        assert request.headers.get("content-type") == "application/json"
        assert request.headers.get("headers-key") == "headers-value"
        assert request.headers.get("Authorization") == f"Bearer {expected_access_token}"
        json_payload = json.loads(request.content.decode())
        assert json_payload == test_body

    router = mock_router(
        route=Route(
            method="POST",
            path=expected_path,
            status_code=200,
            json=expected_json,
        ),
        callback=request_assertions,
    )

    client = Client(
        access_token=expected_access_token,
        client_options=ClientOptions(
            headers={},
            timeout=httpx.Timeout(15),
            transport=httpx.MockTransport(router.handler),
        ),
    )

    if async_flag:
        response = await client.api.async_request(
            method=expected_method,
            path=expected_path,
            body=test_body,
            headers=test_headers,
        )
    else:
        response = client.api.request(
            method=expected_method,
            path=expected_path,
            body=test_body,
            headers=test_headers,
        )

    assert response == expected_json
    assert call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("async_flag", [True, False])
async def test_request_raises_404_error(
    mock_router: Callable[..., Router], async_flag: bool
) -> None:
    test_method = "POST"
    test_path = "/request"
    test_error_body = {"error": "Request not successful."}
    test_status = 404
    router = mock_router(
        route=Route(
            method=test_method,
            path=test_path,
            status_code=test_status,
            json=test_error_body,
        )
    )

    client = Client(
        client_options=ClientOptions(
            headers={},
            timeout=httpx.Timeout(15),
            transport=httpx.MockTransport(router.handler),
        )
    )

    with pytest.raises(httpx.HTTPStatusError) as e:
        if async_flag:
            await client.api.async_request(method=test_method, path=test_path)
        else:
            client.api.request(method=test_method, path=test_path)

    assert (
        str(e.value)
        == "Client error '404 Not Found' for url "
        + f"'https://api.wrift.ai/v1{test_path}'\n"
        + "For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
    )
    assert e.value.response.status_code == test_status
    assert e.value.response.json() == test_error_body
