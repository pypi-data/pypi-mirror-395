from typing import Any, Self, Unpack

from ..base import Evaluable, Merge, Operator
from ..sort import SortBy
from ..types import DictExpression, MongoKeyword, _String


class Map(Operator):
    def __init__(self, input_: Any, as_: str, in_: Any):
        self.input = input_
        self.as_ = _String(as_)
        self.in_ = in_

    def expression(self) -> DictExpression:
        return {
            "$map": {
                MongoKeyword.from_py(field): Evaluable(value).expression()
                for field, value in self.__dict__.items()
            }
        }


class Size(Operator):
    def __init__(self, expression: Any):
        self._expression = expression

    def expression(self) -> DictExpression:
        return {"$size": Evaluable(self._expression).expression()}


class Filter(Operator):
    def __init__(self, input_: Any, as_: str, cond: Any, limit: Any | None = None):
        self.input = input_
        self.as_ = _String(as_)
        self.cond = cond
        self.limit = limit

    def expression(self) -> DictExpression:
        return {
            "$filter": {
                MongoKeyword.from_py(field): Evaluable(value).expression()
                for field, value in self.__dict__.items()
                if value is not None
            },
        }


class Reduce(Operator):
    def __init__(self, input_: Any, initial_value: Any, in_: Any):
        self.input = input_
        self.initial_value = initial_value
        self.in_ = in_

    def expression(self) -> DictExpression:
        return {
            "$reduce": {
                MongoKeyword.from_py(field): Evaluable(value).expression()
                for field, value in self.__dict__.items()
            }
        }

    @classmethod
    def list(cls, input_: Any, in_: Any) -> Self:
        return cls(input_=input_, initial_value=[], in_=in_)

    @classmethod
    def int(cls, input_: Any, in_: Any) -> Self:
        return cls(input_=input_, initial_value=0, in_=in_)


class SortArray(Operator):
    def __init__(self, input_: Any, *sort_by: Unpack[tuple[SortBy, ...]]):
        self.input = input_
        self.sort_by = sort_by

    def expression(self) -> DictExpression:
        return {
            "$sortArray": {
                "input": Evaluable(self.input).expression(),
                "sortBy": Merge.dict(*self.sort_by).expression(),
            }
        }


class IndexOfArray(Operator):
    def __init__(
        self,
        array: Any,
        search: Any,
        /,
        *,
        start: Any | None = None,
        end: Any | None = None,
    ):
        self.array = array
        self.search = search
        self.start = start
        self.end = end

        if self.end is not None and self.start is None:
            raise ValueError("`end` must be used with `start`")

    def expression(self) -> DictExpression:
        args = [self.array, self.search]
        for v in (self.start, self.end):
            if v is not None:
                args.append(v)

        return Evaluable({"$indexOfArray": args}).expression()
