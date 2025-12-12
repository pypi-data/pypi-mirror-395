import functools
import warnings
from collections.abc import Callable
from pathlib import Path

import pytest

from compose.enums import AppEnv

from .enums import TestTypeMarker


@functools.lru_cache(1)
def get_marker_name_to_marker() -> dict[str, pytest.MarkDecorator]:
    return {
        marker_name: getattr(pytest.mark, marker_name) for marker_name in TestTypeMarker.names()
    }


def check_env_is_allowed(env: AppEnv) -> None:
    if env is None or env != AppEnv.TEST:
        raise RuntimeError(f"`APP_ENV` must be set to `{AppEnv.TEST}` to run tests")


def register_test_type_markers(config: pytest.Config) -> None:
    for member in TestTypeMarker:
        name, description = member.value
        config.addinivalue_line("markers", f"{name}: {description}")


def default_marker_getter(item: pytest.Function) -> pytest.MarkDecorator:
    with warnings.catch_warnings(
        action="ignore",
        category=pytest.PytestUnknownMarkWarning,
    ):
        marker_name_to_marker = get_marker_name_to_marker()
        test_types = set(marker_name_to_marker.keys())
        default_test_type = pytest.mark.unit.name

        node_path = item.nodeid.split("::")[0]
        parts = Path(node_path).parts

        mark_name = next((part for part in parts if part in test_types), default_test_type)
        result = getattr(pytest.mark, mark_name)

    return result


def add_test_type_markers(
    items: list[pytest.Function],
    marker_getter: Callable[[pytest.Function], pytest.MarkDecorator] = default_marker_getter,
) -> None:
    """

    Examples:
        >>> from compose import testing
        >>> import pytest
        >>> def pytest_collection_modifyitems(items: list[pytest.Function]) -> None:
        >>>     testing.add_test_type_markers(items)

    """

    for item in items:
        item.add_marker(marker_getter(item))
