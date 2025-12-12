from typing import Any

from ..base import Evaluable, Operator
from ..types import DictExpression


class SetIntersection(Operator):
    def __init__(self, *values: Any):
        self.values = list(values)

    def expression(self) -> DictExpression:
        return Evaluable({"$setIntersection": self.values}).expression()
