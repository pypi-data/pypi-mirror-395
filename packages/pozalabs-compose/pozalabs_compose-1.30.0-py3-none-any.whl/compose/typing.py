from __future__ import annotations

import io
from collections.abc import Callable, Generator
from typing import IO, TYPE_CHECKING, Annotated, Any, Self

from pydantic import GetPydanticSchema
from pydantic_core import core_schema

if TYPE_CHECKING:
    from .types import PyObjectId

type Validator = Callable[[Any], Self]
type ValidatorGenerator = Generator[Validator, None, None]

type Factory[T] = Callable[..., T]
type PyObjectIdFactory = Factory[PyObjectId]

type NoArgsFactory[T] = Callable[[], T]
type NoArgsPyObjectIdFactory = NoArgsFactory[PyObjectId]


type BinaryIO = Annotated[
    io.BytesIO | IO[bytes],
    GetPydanticSchema(
        lambda tp, handler: core_schema.no_info_after_validator_function(
            validate_binary_io, core_schema.any_schema()
        )
    ),
]


def validate_binary_io[T](value: T) -> T:
    if not (isinstance(value, io.BytesIO) or isinstance(value, io.BufferedReader)):
        raise ValueError(
            f"Expected an instance of io.BytesIO or io.BufferedReader, got {value.__class__.__name__}"
        )
    return value
