import datetime
from collections.abc import Callable, Generator
from dataclasses import dataclass
from typing import Any, Self

import pendulum
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema

from .helper import get_pydantic_core_schema


class DateTime(pendulum.DateTime):
    """https://stackoverflow.com/a/76719893"""

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], pendulum.DateTime], None, None]:
        yield cls._instance

    @classmethod
    def _instance(cls, v: datetime.datetime | pendulum.DateTime) -> pendulum.DateTime:
        return pendulum.instance(obj=v, tz=pendulum.UTC)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return get_pydantic_core_schema(cls, handler(datetime.datetime))


@dataclass
class DateRange:
    start: DateTime
    end: DateTime

    @classmethod
    def day_of(
        cls,
        dt: pendulum.DateTime,
        tz: pendulum.tz.Timezone | str = pendulum.UTC,
    ) -> Self:
        if dt.tzinfo is None:
            raise ValueError("input datetime must be aware")

        return cls(start=(start := dt.start_of("day").in_tz(tz)), end=start.add(days=1))
