from typing import Any

from ..base import Evaluable, GeneralAggregationOperator, Operator
from ..types import DictExpression


class Concat(GeneralAggregationOperator):
    mongo_operator = "$concat"


class Split(Operator):
    def __init__(self, expr: Any, delimiter: str):
        self.expr = expr
        self.delimiter = delimiter

    def expression(self) -> DictExpression:
        return Evaluable({"$split": [self.expr, self.delimiter]}).expression()
