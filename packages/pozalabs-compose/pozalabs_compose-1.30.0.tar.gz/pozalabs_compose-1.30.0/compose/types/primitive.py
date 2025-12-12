import types
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Self, cast

from compose import typing

from .helper import CoreSchemaGettable

MARKER_IS_COMPOSE_VALIDATOR = "_is_compose_validator"
MARKER_COMPOSE_VALIDATORS = "_compose_validators"


def caster[T](factory: Callable[[Any], T], /) -> Callable[[Any], T]:
    def _cast(v: Any) -> T:
        return factory(v)

    return _cast


def validator[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    setattr(func, MARKER_IS_COMPOSE_VALIDATOR, True)
    return func


class ValidatablePrimitive[T]:
    if TYPE_CHECKING:

        def __init__(self, *args, **kwargs) -> None: ...

    @classmethod
    def __get_validators__(cls) -> typing.ValidatorGenerator:
        yield from getattr(cls, MARKER_COMPOSE_VALIDATORS, [])

    @classmethod
    @validator
    def cast(cls, v: T) -> Self:
        return cls(v)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._compose_validators = [
            getattr(cls, name)
            for base_cls in cls.__mro__
            for name, member in base_cls.__dict__.items()
            if (
                isinstance(member, classmethod)
                and hasattr(member.__wrapped__, MARKER_IS_COMPOSE_VALIDATOR)
            )
        ]


class Str(str, ValidatablePrimitive[str], CoreSchemaGettable[str]): ...


class Int(int, ValidatablePrimitive[int], CoreSchemaGettable[int]): ...


class Float(float, ValidatablePrimitive[float], CoreSchemaGettable[float]): ...


def _create_list_type[T](t: type[T], /) -> type[list[T]]:
    def __get_validators__(c) -> typing.ValidatorGenerator:
        yield caster(c)

    return cast(
        type[list[T]],
        types.new_class(
            f"{t.__name__.title()}List",
            (list[t], ValidatablePrimitive[t], CoreSchemaGettable[list[t]]),
            exec_body=lambda ns: ns.update(
                {
                    "__get_validators__": classmethod(__get_validators__),
                }
            ),
        ),
    )


def create_list_type[T]() -> Callable[[type[T]], type[list[T]]]:
    cache = {}

    def factory(t: type[T]) -> type[list[T]]:
        type_name = t.__name__

        if (cached := cache.get(type_name)) is not None:
            return cached

        _result = _create_list_type(t)
        cache[type_name] = _result
        return _result

    return factory


TypedList = create_list_type()
StrList = TypedList(str)
IntList = TypedList(int)


class ListMeta(type):
    _cache = {}

    def __getitem__(self, item):
        type_name = item.__name__

        if (cached := self._cache.get(type_name)) is not None:
            return cached

        result = _create_list_type(item)
        self._cache[type_name] = result
        return result


class List[T](list[T], metaclass=ListMeta): ...
