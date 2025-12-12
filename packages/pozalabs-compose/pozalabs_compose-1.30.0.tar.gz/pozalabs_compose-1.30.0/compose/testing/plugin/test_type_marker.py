import pytest

from .. import hook


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[pytest.Function]) -> None:
    hook.add_test_type_markers(items)
