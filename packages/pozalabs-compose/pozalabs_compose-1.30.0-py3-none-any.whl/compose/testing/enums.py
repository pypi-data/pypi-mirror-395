import enum
from collections.abc import Callable

import pytest

from . import param


class TestTypeMarker(enum.Enum):
    UNIT = ("unit", "단위 테스트")
    INTEGRATION = ("integration", "통합 테스트")
    E2E = ("e2e", "E2E 테스트")

    @classmethod
    def names(cls) -> list[str]:
        return [member.value[0] for member in cls]


def create_enum_flag_property_test(
    e: type[enum.Enum],
    f: Callable[[enum.Enum], bool],
    /,
    truthy: list[enum.Enum] | tuple[enum.Enum] | set[enum.Enum],
) -> Callable[[enum.Enum, bool], None]:
    """

    Examples:
        ```python
        import enum

        class Status(enum.StrEnum):
            SUCCEEDED = enum.auto()
            FAILED = enum.auto()

            @property
            def is_succeeded(self) -> bool:
                return self == Status.SUCCEEDED

        test_status_is_succeeded = compose.testing.create_enum_flag_property_test(
            Status,
            Status.is_succeeded.fget,
            truthy={Status.SUCCEEDED},
        )
        ```

    """

    def _test(value: enum.Enum, expected: bool) -> None:
        assert f(value) is expected

    return pytest.mark.parametrize(
        "value, expected", param.parametrize_enum_flag_property_test(e=e, truthy=truthy)
    )(_test)
