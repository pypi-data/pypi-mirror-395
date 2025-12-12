from collections.abc import Callable, Iterable
from typing import TypeAlias

from .base import Merge, Operator
from .pipeline import Pipeline as _Pipeline
from .raw import Raw
from .types import DictExpression, ListExpression

Expressionable: TypeAlias = Operator | DictExpression | ListExpression


class _Map[T]:
    def __init__(self, collection: Iterable[T], callback: Callable[[T], Operator]):
        self.collection = collection
        self.callback = callback

    def eval(self) -> list[Operator]:
        return [self.callback(item) for item in self.collection]


def Map[T](collection: Iterable[T], callback: Callable[[T], Operator]) -> list[Operator]:
    return _Map(collection, callback).eval()


class _Filter:
    def __init__(self, collection: list[Operator], predicate: Callable[[Operator], bool]):
        self.collection = collection
        self.predicate = predicate

    def eval(self) -> list[Operator]:
        return [item for item in self.collection if self.predicate(item)]


def Filter(collection: list[Operator], predicate: Callable[[Operator], bool]) -> list[Operator]:
    return _Filter(collection, predicate=predicate).eval()


class NonEmpty:
    def __call__(self, op: Operator) -> bool:
        return bool(op.expression())


class _Flatten:
    def __init__(self, ops: Iterable[Expressionable]):
        self.ops = list(ops)

    def eval(self) -> list[Operator]:
        result = []
        for op in self.ops:
            exp = op.expression() if isinstance(op, Operator) else op

            match exp:
                case dict():
                    result.append(Raw(exp))
                case list():
                    for e in exp:
                        result.extend([Raw(e)] if isinstance(e, dict) else self.__class__(e).eval())
                case _:
                    raise ValueError(f"Expression must be dict or list, not {type(exp)} ({exp})")

        return result


def Flatten(ops: Iterable[Expressionable]) -> list[Operator]:
    return _Flatten(ops).eval()


def Q(*ops: *tuple[Operator, ...]) -> DictExpression:
    return Merge.dict(*ops).expression()


def Pipeline(*ops: Operator) -> ListExpression:
    return _Pipeline(*ops).expression()
