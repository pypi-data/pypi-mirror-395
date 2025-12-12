from typing import Any, Self

from .. import constants
from . import primitive


class Byte(primitive.Int):
    def __new__(cls, v: Any, /) -> Self:
        v = super().__new__(cls, v)
        if v < 0:
            raise ValueError(f"`{cls.__name__}` must be a non-negative integer")
        return v

    @classmethod
    def from_mib(cls, v: int | float, /) -> Self:
        return cls(v * constants.Unit.MIB)

    @classmethod
    def from_gib(cls, v: int | float, /) -> Self:
        return cls(v * constants.Unit.GIB)
