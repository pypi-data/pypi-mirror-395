from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Depends

from compose.container import BaseModel


class CommandUpdater[T: BaseModel, U]:
    def __init__(self, from_field: str, to_field: str):
        self.from_field = from_field
        self.to_field = to_field

    def __call__(self, cmd: T, user: U) -> T:
        return cmd.copy(update={self.to_field: getattr(user, self.from_field)}, deep=True)


class UserInjector[T: BaseModel, U]:
    def __init__(
        self,
        user_getter: Callable[[], U],
        command_updater: Callable[[T, U], T],
    ):
        self.user_getter = user_getter
        self.command_updater = command_updater

    def injector(self) -> Callable[..., Any]:
        return self._injector

    def _injector(self, t: T, /) -> Callable[..., Any]:
        def inject_user(cmd: t, user: U = Depends(self.user_getter)) -> T:
            return self.command_updater(cmd, user)

        return inject_user


def create_with_user[T: BaseModel](
    user_injector: Callable[..., Any],
) -> Callable[[type[T]], type[T]]:
    def with_user(cmd: type[T]) -> type[T]:
        return Annotated[cmd, Depends(user_injector(cmd))]

    return with_user
