from typing import Any

from ..base import DictExpression, Evaluable, Operator


class First(Operator):
    def __init__(self, expression: Any, /):
        self._expression = expression

    def expression(self) -> DictExpression:
        return Evaluable({"$first": self._expression}).expression()


class MergeObjects(Operator):
    def __init__(self, *expressions: Any):
        self._expressions = list(expressions)

    def expression(self) -> DictExpression:
        expressions = [Evaluable(e).expression() for e in self._expressions]
        return {"$mergeObjects": expressions if len(expressions) > 1 else expressions[0]}


class AddToSet(Operator):
    def __init__(self, expression: Any, /):
        self._expression = expression

    def expression(self) -> DictExpression:
        return Evaluable({"$addToSet": self._expression}).expression()


class Push(Operator):
    def __init__(self, expression: Any, /):
        self._expression = expression

    def expression(self) -> DictExpression:
        return Evaluable({"$push": self._expression}).expression()
