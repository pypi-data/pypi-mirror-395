from collections.abc import Callable
from typing import Any

import pendulum
from pydantic import Field

from . import types


class _IdField:
    def __call__(self, **kwargs) -> Any:
        default_kwargs = {"alias": "_id"}
        return Field(**(default_kwargs | kwargs))  # type: ignore


class _DatetimeField:
    def __call__(self, **kwargs) -> types.DateTime:
        default_kwargs = {"default_factory": pendulum.DateTime.utcnow}
        return Field(**(default_kwargs | kwargs))  # type: ignore


IdField: Callable[..., Any] = _IdField()
DateTimeField: Callable[..., types.DateTime] = _DatetimeField()
