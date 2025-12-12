import pytest

from compose import enums

from .. import hook


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    hook.check_env_is_allowed(enums.AppEnv.current())
    hook.register_test_type_markers(config)


@pytest.hookimpl()
def pytest_collection_modifyitems(items: list[pytest.Function]) -> None:
    hook.add_test_type_markers(items)
