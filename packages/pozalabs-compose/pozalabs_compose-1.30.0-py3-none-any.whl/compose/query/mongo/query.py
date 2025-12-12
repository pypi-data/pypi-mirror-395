import abc
from typing import Any

from ..base import OffsetPaginationQuery, Query


class MongoQuery(Query, abc.ABC):
    @abc.abstractmethod
    def to_query(self) -> list[dict[str, Any]]:
        raise NotImplementedError


class MongoFilterQuery(OffsetPaginationQuery, MongoQuery):
    @abc.abstractmethod
    def to_query(self) -> list[dict[str, Any]]:
        raise NotImplementedError


MongoOffsetFilterQuery = MongoFilterQuery
