from typing import Any

from ..base import Evaluable, Operator
from ..types import DictExpression


class ToString(Operator):
    def __init__(self, expr: Any):
        self.expr = expr

    def expression(self) -> DictExpression:
        return Evaluable({"$toString": self.expr}).expression()


class ToBool(Operator):
    def __init__(self, expression: Any):
        self._expression = expression

    def expression(self) -> DictExpression:
        return Evaluable({"$toBool": self._expression}).expression()


class ToInt(Operator):
    def __init__(self, expression: Any):
        self._expression = expression

    def expression(self) -> DictExpression:
        return Evaluable({"$toInt": self._expression}).expression()
