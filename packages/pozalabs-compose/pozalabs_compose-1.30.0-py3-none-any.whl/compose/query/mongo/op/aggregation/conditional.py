from typing import Any

from ..base import Evaluable, GeneralAggregationOperator, Operator
from ..types import DictExpression


class IfNull(GeneralAggregationOperator):
    mongo_operator = "$ifNull"


class Cond(Operator):
    def __init__(self, if_: Any, then: Any, else_: Any):
        """
        Aggregation operator `$cond`

        Reference:
            https://www.mongodb.com/docs/manual/reference/operator/aggregation/cond/#mongodb-expression-exp.-cond
        """

        self.if_ = if_
        self.then = then
        self.else_ = else_

    def expression(self) -> DictExpression:
        return {
            "$cond": {
                "if": Evaluable(self.if_).expression(),
                "then": Evaluable(self.then).expression(),
                "else": Evaluable(self.else_).expression(),
            }
        }
