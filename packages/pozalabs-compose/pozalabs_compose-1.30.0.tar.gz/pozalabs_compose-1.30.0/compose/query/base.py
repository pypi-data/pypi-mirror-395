from typing import Any

from pydantic import Field

from .. import container


class Query(container.BaseModel):
    def to_query(self) -> Any:
        ...


class OffsetPaginationQuery(Query):
    page: int | None = Field(None, ge=1)
    per_page: int | None = Field(None, ge=1)

    @property
    def can_paginate(self) -> bool:
        return self.page is not None and self.per_page is not None
