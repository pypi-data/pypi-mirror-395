import functools
import uuid
from collections.abc import Callable, Generator
from typing import Any, get_type_hints


def descendants_of[T](cls: type[T]) -> Generator[type[T], None, None]:
    stack = cls.__subclasses__()
    while stack:
        current_cls = stack.pop()
        yield current_cls
        stack.extend(current_cls.__subclasses__())


def unordered_partial[RT, T](p: functools.partial[RT], t: T) -> Callable[..., RT]:
    type_hints = get_type_hints(p.func)

    exclude_keys = {*p.keywords.keys(), "return"}
    candidates = [k for k, v in type_hints.items() if v == t and k not in exclude_keys]

    if not candidates or len(candidates) > 1:
        raise TypeError(
            f"Cannot inject argument of type {t} into {p}. "
            f"Expected exactly one argument of type {t}, "
            f"but found {len(candidates)}: {candidates}"
        )

    arg_name = candidates[0]

    def wrapper(arg: Any) -> T:
        return p(**{arg_name: arg})

    return functools.partial(wrapper)


def ident[T](x: T) -> T:
    return x


def uuid4_hex() -> str:
    return uuid.uuid4().hex
