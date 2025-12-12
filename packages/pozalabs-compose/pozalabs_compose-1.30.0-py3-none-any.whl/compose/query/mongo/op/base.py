from __future__ import annotations

import abc
import functools
import operator
from collections.abc import Callable
from typing import Any, ClassVar, Self

from .types import DictExpression, ListExpression


class Operator:
    @abc.abstractmethod
    def expression(self) -> Any:
        raise NotImplementedError

    def then(self, op: Callable[..., Operator]) -> Operator:
        return op(self.expression())


class ComparisonOperator(Operator):
    def __init__(self, field: str, value: Any | None = None):
        self.field = field
        self.value = value

    @abc.abstractmethod
    def expression(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_(cls, **kwargs: Any) -> Self:
        if (kv := next(iter(kwargs.items()), None)) is None:
            raise ValueError("key-value pair is required")

        return cls(**dict(zip(("field", "value"), kv)))


class EqualityOperator(ComparisonOperator):
    @abc.abstractmethod
    def expression(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def is_null(cls, field: str) -> Self:
        return cls(field=field, value=None)

    @classmethod
    def is_true(cls, field: str) -> Self:
        return cls(field=field, value=True)

    @classmethod
    def is_false(cls, field: str) -> Self:
        return cls(field=field, value=False)


class LogicalOperator(Operator):
    def __init__(self, *ops: Operator):
        self.ops = list(ops)

    @abc.abstractmethod
    def expression(self) -> dict[str, ListExpression]:
        raise NotImplementedError


class GeneralAggregationOperator(Operator):
    mongo_operator: ClassVar[str] = ""

    def __init__(self, *expressions: Any):
        self.expressions = list(expressions)

    def expression(self) -> DictExpression:
        return Evaluable({self.mongo_operator: self.expressions}).expression()


class Stage[T](Operator):
    @abc.abstractmethod
    def expression(self) -> T:
        raise NotImplementedError


class Merge[T](Operator):
    def __init__(self, *ops: Operator, initial: Any):
        self.ops = list(ops)
        self.initial = initial

    def expression(self) -> T:
        return functools.reduce(operator.or_, [op.expression() for op in self.ops], self.initial)

    @classmethod
    def dict(cls, *ops: *tuple[Operator, ...]) -> Merge[dict[str, Any]]:
        return cls(*ops, initial={})


class Evaluable(Operator):
    def __init__(self, op: Any):
        self.op = op

    def expression(self) -> Any:
        match self.op:
            case Operator():
                return self.op.expression()
            case dict():
                return {k: Evaluable(v).expression() for k, v in self.op.items()}
            case list():
                return [Evaluable(v).expression() for v in self.op]
            case _:
                return self.op
