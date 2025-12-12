from __future__ import annotations

from typing import Any, Self, TypeVar

from pydantic.alias_generators import to_camel

DictExpression = dict[str, Any]
ListExpression = list[DictExpression]
Expression = TypeVar("Expression", DictExpression, ListExpression)

Id = "$_id"


class MongoKeyword(str):
    def __new__(cls, v: str):
        if v != _camelize(v):
            raise ValueError(f"Cannot interpret {v} as valid mongo keyword")

        return super().__new__(cls, v)

    @classmethod
    def from_py(cls, v: str) -> Self:
        return cls(_camelize(v))


def _camelize(v: str) -> str:
    return to_camel(v.strip("_"))


class _FieldPath(str):
    def __new__(cls, v: str):
        if not v.startswith("$"):
            raise ValueError("path must be prefixed with $")

        return super().__new__(cls, v)


class _String(str):
    def __new__(cls, v: str):
        if v.startswith("$"):
            raise ValueError("string must not be prefixed with $")

        return super().__new__(cls, v)
