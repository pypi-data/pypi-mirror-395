from typing import Any

from .. import utils
from ..base import ComparisonOperator
from ..types import DictExpression


class AEqual(ComparisonOperator):
    def __init__(self, field: str, value: Any | None = None):
        super().__init__(field=field, value=value)

    def expression(self) -> DictExpression:
        return {"$eq": [self.field, self.value]}


AEq = utils.create_general_aggregation_operator(name="AEq", mongo_operator="$eq")
ANe = utils.create_general_aggregation_operator(name="ANe", mongo_operator="$ne")
AGt = utils.create_general_aggregation_operator(name="AGt", mongo_operator="$gt")
AGte = utils.create_general_aggregation_operator(name="AGte", mongo_operator="$gte")
ALt = utils.create_general_aggregation_operator(name="ALt", mongo_operator="$lt")
ALte = utils.create_general_aggregation_operator(name="ALte", mongo_operator="$lte")
