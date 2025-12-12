from typing import Any

from ..base import Evaluable, Operator
from ..types import DictExpression


class RegexMatch(Operator):
    def __init__(self, field: Any, value: Any):
        self.field = field
        self.value = value

    def expression(self) -> DictExpression:
        return Evaluable({"$regexMatch": {"input": self.field, "regex": self.value}}).expression()
