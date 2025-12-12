from collections.abc import Callable
from typing import Any, cast

from .base import GeneralAggregationOperator, Operator


def create_operator[T: Operator](
    name: str,
    expression_factory: Callable[[T], Any],
    base: tuple[type[T], ...],
) -> type[T]:
    return cast(
        type[T],
        type(name, base, {"expression": expression_factory}),
    )


def create_general_aggregation_operator(
    name: str, mongo_operator: str
) -> type[GeneralAggregationOperator]:
    return cast(
        type[GeneralAggregationOperator],
        type(name, (GeneralAggregationOperator,), {"mongo_operator": mongo_operator}),
    )
