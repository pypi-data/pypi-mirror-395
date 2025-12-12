import base64
from typing import Any, Self

import pymongo

from compose.container import BaseModel

from .aggregation import Push
from .comparison import Eq, Gt, Lt
from .logical import And
from .pipeline import Pipeline
from .stage import EmptyStage, Group, Limit, Match, Project, Sort, Spec, Stage
from .types import DictExpression, ListExpression


class Cursor(BaseModel):
    def to_str(self) -> str:
        return base64.b64encode(self.model_dump_json(by_alias=True).encode()).decode()

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)

    @classmethod
    def from_str(cls, cursor: str) -> Self:
        return cls.model_validate_json(json_data=base64.b64decode(cursor).decode())


class CursorPaginationClause(And):
    direction_to_op = {pymongo.ASCENDING: Gt, pymongo.DESCENDING: Lt}
    default_direction = pymongo.ASCENDING

    @classmethod
    def from_cursor_params(
        cls,
        sort_field: str,
        cursor_params: list[tuple[str, Any]],
        sort: Sort,
    ) -> Self:
        sort_params = {criterion.field: criterion.direction for criterion in sort.criteria}
        return cls(
            *(
                cls.direction_to_op[sort_params.get(field, cls.default_direction)](
                    field=field,
                    value=value,
                )
                if field == sort_field
                else Eq(field=field, value=value)
                for field, value in cursor_params
            )
        )


class CursorQuery(Stage[DictExpression]):
    def __init__(self, sort: Sort, cursor: Cursor | None = None):
        self.sort = sort
        self.cursor = cursor

    def expression(self) -> DictExpression:
        if (cursor := self.cursor) is None:
            return EmptyStage().expression()

        clauses = []
        cursor_params = cursor.to_dict().items()
        for idx, (field, _) in enumerate(cursor_params):
            current_cursor_params = list(cursor_params)[: idx + 1]
            clauses.append(
                CursorPaginationClause.from_cursor_params(
                    sort_field=field,
                    cursor_params=current_cursor_params,
                    sort=self.sort,
                )
            )

        return Match.or_(*clauses).expression()


class CursorPagination(Stage[ListExpression]):
    def __init__(
        self,
        sort: Sort,
        cursor: Cursor | None = None,
        per_page: int | None = None,
    ):
        self.sort = sort
        self.cursor = cursor
        self.per_page = per_page

    def expression(self) -> ListExpression:
        return Pipeline(
            CursorQuery(sort=self.sort, cursor=self.cursor),
            self.sort,
            Limit(self.per_page),
            Group.by_null(Spec(field="items", spec=Push("$$ROOT"))),
            Project(
                Spec.exclude("_id"),
                Spec.include("items"),
            ),
        ).expression()
