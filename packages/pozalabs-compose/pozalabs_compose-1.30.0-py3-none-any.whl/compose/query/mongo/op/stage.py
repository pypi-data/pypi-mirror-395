from collections.abc import Iterable
from typing import Any, Self

from .base import Evaluable, Merge, Operator, Stage
from .evaulation import Expr
from .logical import And, Nor, Or
from .pipeline import Pipeline
from .sort import SortBy
from .types import DictExpression, ListExpression, MongoKeyword, _FieldPath


class EmptyStage(Stage[DictExpression]):
    def expression(self) -> DictExpression:
        return {}


class Match(Stage[DictExpression]):
    def __init__(self, op: Operator):
        self.op = op

    def expression(self) -> DictExpression:
        if not (expression := self.op.expression()):
            return EmptyStage().expression()
        return {"$match": expression}

    @classmethod
    def and_(cls, *ops: Operator) -> Self:
        return cls(And(*ops))

    @classmethod
    def or_(cls, *ops: Operator) -> Self:
        return cls(Or(*ops))

    @classmethod
    def nor(cls, *ops: Operator) -> Self:
        return cls(Nor(*ops))

    @classmethod
    def expr(cls, op: Any) -> Self:
        return cls(Expr(op))


class Sort(Stage[DictExpression]):
    def __init__(self, *criteria: SortBy):
        self.criteria = list(criteria)

    def expression(self) -> DictExpression:
        if not (merged := Merge.dict(*self.criteria).expression()):
            raise ValueError("Expression cannot be empty")
        return {"$sort": merged}


class Spec(Operator):
    def __init__(self, field: str, spec: Any):
        self.field = field
        self.spec = spec

    def expression(self) -> DictExpression:
        return {self.field: Evaluable(self.spec).expression()}

    @classmethod
    def include(cls, field: str) -> Self:
        return cls(field=field, spec=1)

    @classmethod
    def exclude(cls, field: str) -> Self:
        return cls(field=field, spec=0)

    @classmethod
    def ref(cls, field: str, spec: str) -> Self:
        return cls(field=field, spec=_FieldPath(spec))


class Project(Stage[DictExpression]):
    def __init__(self, *specs: Spec):
        self.specs = list(specs)

    def expression(self) -> DictExpression:
        return {"$project": Merge.dict(*self.specs).expression()}

    @classmethod
    def from_attrs(cls, **attrs: Any) -> Self:
        return cls(*(Spec(field, spec) for field, spec in attrs.items()))

    @classmethod
    def from_(
        cls,
        include: Iterable[str] | None = None,
        exclude: Iterable[str] | None = None,
        ref: dict[str, Any] | None = None,
    ) -> Self:
        if include is None and exclude is None and ref is None:
            raise ValueError("At least one of `include`, `exclude`, or `ref` must be provided")

        return cls(
            *(Spec.include(field) for field in (include or {})),
            *(Spec.exclude(field) for field in (exclude or {})),
            *(Spec(field, spec) for field, spec in (ref or {}).items()),
        )


class Lookup(Stage[DictExpression]):
    def __init__(self, from_: str, as_: str | None = None):
        self.from_ = from_
        self.as_ = as_ or self.from_

    def expression(self) -> DictExpression:
        return {
            "$lookup": {
                MongoKeyword.from_py(field): Evaluable(value).expression()
                for field, value in self.__dict__.items()
            }
        }


class MatchLookup(Lookup):
    def __init__(self, from_: str, local_field: str, foreign_field: str, as_: str | None = None):
        super().__init__(from_=from_, as_=as_)
        self.local_field = local_field
        self.foreign_field = foreign_field

    @classmethod
    def on_id(cls, from_: str, local_field: str, as_: str | None = None) -> Self:
        return cls(
            from_=from_,
            local_field=local_field,
            foreign_field="_id",
            as_=as_,
        )


class SubqueryLookup(Lookup):
    def __init__(
        self,
        from_: str,
        pipeline: Pipeline,
        let: Operator | None = None,
        as_: str | None = None,
    ):
        super().__init__(from_=from_, as_=as_)
        self.let = let
        self.pipeline = pipeline


class Unwind(Stage[DictExpression]):
    def __init__(
        self,
        path: str,
        include_array_index: str | None = None,
        preserve_null_and_empty_arrays: bool | None = None,
    ):
        self.path = _FieldPath(path)
        self.include_array_index = include_array_index
        self.preserve_null_and_empty_arrays = preserve_null_and_empty_arrays

    def expression(self) -> DictExpression:
        return {
            "$unwind": {
                MongoKeyword.from_py(field): value
                for field, value in self.__dict__.items()
                if value is not None
            }
        }

    @classmethod
    def preserve_missing(cls, path: str, include_array_index: str | None = None) -> Self:
        return cls(
            path=path,
            include_array_index=include_array_index,
            preserve_null_and_empty_arrays=True,
        )


class Set(Stage[DictExpression]):
    def __init__(self, *specs: Spec):
        self.specs = list(specs)

    def expression(self) -> DictExpression:
        return {"$set": Merge.dict(*self.specs).expression()}


class FacetSubPipeline(Operator):
    def __init__(self, output_field: str, pipeline: Pipeline):
        self.output_field = output_field
        self.pipeline = pipeline

    def expression(self) -> DictExpression:
        return {self.output_field: self.pipeline.expression()}


class Facet(Stage[DictExpression]):
    def __init__(self, *pipelines: FacetSubPipeline):
        self.pipelines = list(pipelines)

    def expression(self) -> DictExpression:
        return {"$facet": Merge.dict(*self.pipelines).expression()}


class Skip(Stage[DictExpression]):
    def __init__(self, skip: int):
        self.skip = skip

    def expression(self) -> DictExpression:
        return {"$skip": self.skip}


class Limit(Stage[DictExpression]):
    def __init__(self, limit: int):
        self.limit = limit

    def expression(self) -> DictExpression:
        return {"$limit": self.limit}


class TextSearchOperator(Operator):
    def __init__(self, query: str, path: str | list[str]):
        self.query = query
        self.path = path

    def expression(self) -> DictExpression:
        return {"text": {"query": self.query, "path": self.path}}


class Search(Stage[DictExpression]):
    def __init__(self, index: str, op: Operator):
        self.index = index
        self.op = op

    def expression(self) -> DictExpression:
        return {"$search": {"index": self.index} | self.op.expression()}


class Pagination(Stage[DictExpression]):
    def __init__(
        self,
        page: int | None = None,
        per_page: int | None = None,
        metadata_ops: list[Operator] | None = None,
    ):
        if not ((page is not None and per_page is not None) or (page is None and per_page is None)):
            raise ValueError("`page` and `per_page` are mutual inclusive")

        self.page = page
        self.per_page = per_page
        self.metadata_ops = metadata_ops or []

        self.can_paginate = self.page is not None and self.per_page is not None

    def expression(self) -> DictExpression:
        return {
            "$facet": {
                "metadata": [{"$count": "total"}, *[op.expression() for op in self.metadata_ops]],
                "items": self._pagination_expression(),
            }
        }

    def _pagination_expression(self) -> ListExpression:
        if not self.can_paginate:
            return []

        return [
            Skip((self.page - 1) * self.per_page).expression(),  # type: ignore
            Limit(self.per_page).expression(),  # type: ignore
        ]


class ReplaceRoot(Stage[DictExpression]):
    def __init__(self, new_root: Any):
        self.new_root = new_root

    def expression(self) -> DictExpression:
        return {"$replaceRoot": {"newRoot": Evaluable(self.new_root).expression()}}


class Group(Stage[DictExpression]):
    def __init__(self, *ops: Operator, key: Any | None = None):
        self.ops = list(ops)
        self.key = key

    def expression(self) -> DictExpression:
        return {
            "$group": {
                "_id": Evaluable(self.key).expression(),
                **Merge.dict(*self.ops).expression(),
            }
        }

    @classmethod
    def by_null(cls, *ops: Operator) -> Self:
        return cls(*ops, key=None)


class Sample(Stage[DictExpression]):
    def __init__(self, size: int):
        self.size = size

    def expression(self) -> DictExpression:
        return Evaluable({"$sample": {"size": self.size}}).expression()
