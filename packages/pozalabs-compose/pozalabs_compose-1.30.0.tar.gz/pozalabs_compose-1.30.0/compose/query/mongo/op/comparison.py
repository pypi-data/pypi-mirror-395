from __future__ import annotations

from collections.abc import Callable
from typing import Any, Self

import pendulum

from compose import types

from . import utils
from .base import ComparisonOperator, EqualityOperator, Operator
from .types import DictExpression


class EmptyOnNull(Operator):
    def __init__(self, op: ComparisonOperator):
        self.op = op

    def expression(self) -> dict[str, Any]:
        return self.op.expression() if self.op.value is not None else {}


def _expression_factory(mongo_operator: str) -> Callable[[ComparisonOperator], DictExpression]:
    def expression(self: ComparisonOperator) -> DictExpression:
        return {self.field: {mongo_operator: self.value}}

    return expression


def create_comparison_operator[T](
    name: str, mongo_operator: str, base: tuple[type[T], ...] = (ComparisonOperator,)
) -> type[T]:
    return utils.create_operator(
        name=name,
        base=base,
        expression_factory=_expression_factory(mongo_operator),
    )


Eq = create_comparison_operator(name="Eq", mongo_operator="$eq", base=(EqualityOperator,))
Ne = create_comparison_operator(name="Ne", mongo_operator="$ne", base=(EqualityOperator,))
Gt = create_comparison_operator(name="Gt", mongo_operator="$gt")
Gte = create_comparison_operator(name="Gte", mongo_operator="$gte")
Lt = create_comparison_operator(name="Lt", mongo_operator="$lt")
Lte = create_comparison_operator(name="Lte", mongo_operator="$lte")
In = create_comparison_operator(name="In", mongo_operator="$in")
Nin = create_comparison_operator(name="Nin", mongo_operator="$nin")


class Regex(ComparisonOperator):
    def __init__(
        self,
        field: str,
        value: Any | None = None,
        options: str = "ms",
    ):
        super().__init__(field=field, value=value)
        self.options = options

    def expression(self) -> dict[str, Any]:
        return {self.field: {"$regex": self.value, "$options": self.options}}


class Range(Operator):
    def __init__(self, g: Gt | Gte, l: Lt | Lte):  # noqa: E741
        self.g = g
        self.l = l

    def expression(self) -> dict[str, Any]:
        field = self.g.field
        return {field: self.g.expression()[field] | self.l.expression()[field]}

    @classmethod
    def date(cls, field: str, start: pendulum.DateTime, end: pendulum.DateTime) -> Self:
        return cls(g=Gte(field=field, value=start), l=Lt(field=field, value=end))

    @classmethod
    def day_of(cls, field: str, dt: pendulum.DateTime) -> Self:
        date_range = types.DateRange.day_of(dt)
        return cls.date(field=field, start=date_range.start, end=date_range.end)
