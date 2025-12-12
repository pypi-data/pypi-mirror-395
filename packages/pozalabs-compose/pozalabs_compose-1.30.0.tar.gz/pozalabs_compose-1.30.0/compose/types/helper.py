from __future__ import annotations

import copy
import inspect
from collections.abc import Callable, Generator
from typing import Any, Protocol, get_args

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class SupportsGetValidators(Protocol):
    """Naming Convention: https://github.com/python/typeshed/issues/4174"""

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], Any], None, None]: ...


def chain(*validators: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def apply_chain(v: Any) -> Any:
        result = copy.deepcopy(v)
        for _validator in validators:
            result = _validator(result)
        return result

    return apply_chain


def get_pydantic_core_schema(
    t: type[SupportsGetValidators], schema: core_schema.CoreSchema, /
) -> core_schema.CoreSchema:
    """Pydantic v1 커스텀 타입에 구현한 검증 제너레이터를 v2 커스텀 타입 검증 함수로 변환합니다.

    class CustomType(str):
        @classmethod
        def __get_validators__(cls):
            yield str_validator

        @classmethod
        def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
        ) -> core_schema.CoreSchema:
            return compose.types.get_pydantic_core_schema(cls, handler(str))
    """

    if not hasattr(t, "__get_validators__"):
        type_name = t.__name__ if inspect.isclass(t) else t.__class__.__name__
        raise AttributeError(f"`{type_name}` does not have `__get_validators__` method")

    return core_schema.no_info_after_validator_function(chain(*t.__get_validators__()), schema)


class CoreSchemaGettable[T]:
    """Pydantic v1 커스텀 타입을 v2 커스텁 타입으로 변환하는 믹스인

    ```python
    class CustomType(str, compose.types.CoreSchemaGettable[str]):
        @classmethod
        def __get_validators__(cls):
            yield str_validator
    ```

    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        core_schema_gettable_cls = next(
            (base for base in source_type.__orig_bases__ if base.__name__ == "CoreSchemaGettable"),
            None,
        )
        if core_schema_gettable_cls is None:
            raise AttributeError(f"`{source_type.__name__}` does not inherit `CoreSchemaGettable`")

        validatable_type = get_args(core_schema_gettable_cls)[0]
        return get_pydantic_core_schema(cls, handler(validatable_type))
