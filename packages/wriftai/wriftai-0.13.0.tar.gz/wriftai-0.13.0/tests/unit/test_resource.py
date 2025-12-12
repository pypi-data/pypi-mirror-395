from unittest.mock import Mock

import pytest

from wriftai._resource import Resource


class MockAPIResource(Resource):
    """Concrete subclass for testing the abstract Resource."""

    pass


def test_api_resource() -> None:
    mock_api = Mock()
    resource = MockAPIResource(api=mock_api)
    assert resource._api == mock_api


@pytest.mark.parametrize(
    "invalid_model",
    [
        "invalidformat",
        "/modelname",
        "owner/",
    ],
)
def test_parse_model_raises_erro(invalid_model: str) -> None:
    mock_api = Mock()
    resource = MockAPIResource(api=mock_api)

    with pytest.raises(ValueError) as e:
        resource._parse_model(model=invalid_model)

    assert str(e.value) == resource._ERROR_MSG_INVALID_MODEL
