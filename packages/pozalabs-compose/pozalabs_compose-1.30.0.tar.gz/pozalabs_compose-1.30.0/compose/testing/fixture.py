from typing import Any

import pytest


def get_fixture_param(request: pytest.FixtureRequest, default: Any | None = None) -> Any:
    return getattr(request, "param", default)


def get_fixture_value_from_param(request: pytest.FixtureRequest) -> Any:
    return request.getfixturevalue(get_fixture_param(request))
