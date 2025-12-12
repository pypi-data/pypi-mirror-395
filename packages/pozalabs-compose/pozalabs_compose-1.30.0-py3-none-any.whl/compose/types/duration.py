from typing import Any, Self

from .. import constants
from . import primitive


class Seconds(primitive.Float):
    def __new__(cls, v: Any, /) -> Self:
        v = super().__new__(cls, v)
        if v < 0:
            raise ValueError(f"`{cls.__name__}` must be a non-negative float")
        return v

    @classmethod
    def from_hours(cls, hours: float) -> Self:
        return cls(hours * constants.SECONDS_PER_HOUR)

    @classmethod
    def from_minutes(cls, minutes: float) -> Self:
        return cls(minutes * constants.SECONDS_PER_MINUTE)


class MilliSeconds(primitive.Int):
    def __new__(cls, v: Any, /) -> Self:
        v = super().__new__(cls, v)
        if v < 0:
            raise ValueError(f"`{cls.__name__}` must be a non-negative integer")
        return v

    @classmethod
    def from_seconds(cls, seconds: float) -> Self:
        return cls(seconds * constants.MILLISECONDS_PER_SECOND)
