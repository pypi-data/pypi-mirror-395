from collections.abc import Callable

from . import utils
from .base import LogicalOperator
from .types import ListExpression


def _expression_factory(
    mongo_operator: str,
) -> Callable[[LogicalOperator], dict[str, ListExpression]]:
    def expression(self: LogicalOperator) -> dict[str, ListExpression]:
        expressions = [expr for op in self.ops if (expr := op.expression())]
        return {mongo_operator: expressions} if expressions else {}

    return expression


def create_logical_operator(name: str, mongo_operator: str) -> type[LogicalOperator]:
    return utils.create_operator(
        name=name, base=(LogicalOperator,), expression_factory=_expression_factory(mongo_operator)
    )


And = create_logical_operator(name="And", mongo_operator="$and")
Or = create_logical_operator(name="Or", mongo_operator="$or")
Nor = create_logical_operator(name="Nor", mongo_operator="$nor")
