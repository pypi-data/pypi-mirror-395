from . import func
from .base import Evaluable, ListExpression, Operator


class Pipeline(Operator):
    def __init__(self, *ops: Operator):
        self.ops = list(ops)

    def expression(self) -> ListExpression:
        return Evaluable(func.Flatten(func.Filter(self.ops, func.NonEmpty()))).expression()
