from ..base import GeneralAggregationOperator


class SetUnion(GeneralAggregationOperator):
    mongo_operator = "$setUnion"
