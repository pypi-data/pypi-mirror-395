import enum
import os
from collections.abc import Callable
from typing import Any, Self


def enum_values(e: type[enum.Enum], /) -> list[Any]:
    return [member.value for _, member in e.__members__.items()]


def create_env_getter(key: str, /) -> Callable[[], str | None]:
    def getter() -> str | None:
        return os.getenv(key)

    return getter


default_env_getter = create_env_getter("APP_ENV")


class AppEnv(enum.StrEnum):
    TEST = enum.auto()
    LOCAL = enum.auto()
    DEV = enum.auto()
    STG = enum.auto()
    PRD = enum.auto()

    @classmethod
    def current(cls, env_getter: Callable[[], str | None] = default_env_getter) -> Self:
        if (env := env_getter()) is None or env not in set(enum_values(cls)):
            raise ValueError(f"Invalid value for {cls.__name__}: {env}")

        return cls(env)
