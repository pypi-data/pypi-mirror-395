from __future__ import annotations

import functools
import warnings
from collections.abc import Iterable
from typing import Any, ClassVar, Self, Unpack, get_args, get_origin, overload

import pendulum
import pymongo
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import UpdateResult

from .. import types
from ..entity import Entity
from ..pagination import Pagination
from ..query.mongo import MongoFilterQuery, MongoQuery
from .base import BaseRepository

registry: dict[str, list[pymongo.IndexModel]] = {}


class MongoDocument(dict[str, Any]):
    @classmethod
    def from_entity(cls, entity: Entity, **kwargs: Any) -> Self:
        return entity.model_dump(
            by_alias=True,
            **{key: value for key, value in kwargs.items() if key not in {"by_alias"}},
        )


class MongoRepository[T: Entity](BaseRepository):
    """
    `MongoRepository` 추상 클래스

    상속 인자:
        `session_requirement`: `MongoRepository` 상속 시 `session_requirement` 인자를 통해
        `session` 인자 선언 여부를 검사할 수 있습니다. 프로덕션에서는 `session_requirement`를
        `SessionRequirement.REQUIRED`로 설정하는 것을 권장합니다.

        ```python
        class UserRepository(
            MongoRepository[User],
            session_requirement=SessionRequirement.REQUIRED,
        ):
            ...
        ```

    """

    __collection_name__: ClassVar[str] = ""
    __indexes__: ClassVar[list[pymongo.IndexModel] | None] = None

    def __init__(self, collection: Collection):
        self.collection = collection

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        indexes = cls.__indexes__ or []
        if cls.__collection_name__ not in registry:
            registry[cls.__collection_name__] = indexes
            return

        index_documents = [idx.document for idx in registry[cls.__collection_name__]]
        registry[cls.__collection_name__].extend(
            [idx for idx in indexes if idx.document not in index_documents]
        )

    @classmethod
    def create(cls, database: Database, **kwargs) -> MongoRepository:
        collection = database.get_collection(cls.__collection_name__, **kwargs)
        if (
            cls.__collection_name__ not in database.list_collection_names()
            and cls.__indexes__ is not None
        ):
            collection.create_indexes(cls.__indexes__)

        return cls(collection=collection)

    def find_by_id(
        self,
        entity_id: types.PyObjectId,
        session: ClientSession | None = None,
        **kwargs,
    ) -> T | None:
        return self.find_by({"_id": entity_id}, session=session, **kwargs)

    @overload
    def find_by(
        self,
        filter_: dict[str, Any],
        *,
        projection: None = None,
        session: ClientSession | None = None,
        **kwargs,
    ) -> T | None: ...

    @overload
    def find_by(
        self,
        filter_: dict[str, Any],
        *,
        projection: dict[str, Any],
        session: ClientSession | None = None,
        **kwargs,
    ) -> dict[str, Any] | None: ...

    def find_by(
        self,
        filter_: dict[str, Any],
        *,
        projection: dict[str, Any] | None = None,
        session: ClientSession | None = None,
        **kwargs,
    ) -> T | dict[str, Any] | None:
        validate_to_entity = projection is None
        query_result = self.collection.find_one(
            filter=filter_,
            session=session,
            **kwargs,
        )
        if query_result is None:
            return None

        return (
            self._entity_type.model_validate(query_result) if validate_to_entity else query_result
        )

    def find_by_query(
        self, qry: MongoQuery, session: ClientSession | None = None, **kwargs
    ) -> dict[str, Any] | None:
        query_result = self.collection.aggregate(qry.to_query(), session=session, **kwargs)
        return next(query_result, None)

    @overload
    def list_by(
        self,
        filter_: dict[str, Any],
        *,
        projection: None = None,
        sort: list[tuple[str, int]] | None = None,
        session: ClientSession | None = None,
        **kwargs,
    ) -> list[T]: ...

    @overload
    def list_by(
        self,
        filter_: dict[str, Any],
        *,
        projection: dict[str, Any],
        sort: list[tuple[str, int]] | None = None,
        session: ClientSession | None = None,
        **kwargs,
    ) -> list[dict[str, Any]]: ...

    def list_by(
        self,
        filter_: dict[str, Any],
        *,
        projection: dict[str, Any] | None = None,
        sort: list[tuple[str, int]] | None = None,
        session: ClientSession | None = None,
        **kwargs,
    ) -> list[T] | list[dict[str, Any]]:
        validate_to_entity = projection is None
        query_result = self.collection.find(
            filter=filter_,
            projection=projection,
            sort=sort,
            session=session,
            **kwargs,
        )
        return (
            [self._entity_type.model_validate(item) for item in query_result]
            if validate_to_entity
            else list(query_result)
        )

    def list_by_query(
        self, qry: MongoQuery, session: ClientSession | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        query_result = self.collection.aggregate(qry.to_query(), session=session, **kwargs)
        return list(query_result)

    def add(self, entity: T, session: ClientSession | None = None, **kwargs) -> None:
        self.collection.insert_one(MongoDocument.from_entity(entity), session=session, **kwargs)

    def add_many(self, entities: list[T], session: ClientSession | None = None, **kwargs) -> None:
        self.collection.insert_many(
            [MongoDocument.from_entity(entity) for entity in entities], session=session, **kwargs
        )

    def update(self, entity: T, session: ClientSession | None = None, **kwargs) -> None:
        document = MongoDocument.from_entity(entity)
        update_result = self.collection.update_one(
            {"_id": entity.id},
            {"$set": document},
            session=session,
            **kwargs,
        )

        self.on_update(
            update_result=update_result,
            entity=entity,
            session=session,
            **kwargs,
        )

    def on_update(
        self,
        update_result: UpdateResult,
        entity: T,
        session: ClientSession | None = None,
        **kwargs,
    ) -> None:
        if not update_result.modified_count:
            return

        if getattr(entity, "updated_at") is None:
            return

        self.collection.update_one(
            {"_id": entity.id},
            {"$set": {"updated_at": pendulum.DateTime.utcnow()}},
            session=session,
            **kwargs,
        )

    def update_many(
        self, entities: list[T], session: ClientSession | None = None, **kwargs
    ) -> None:
        for entity in entities:
            self.update(entity=entity, session=session, **kwargs)

    def delete(
        self, entity_id: types.PyObjectId, session: ClientSession | None = None, **kwargs
    ) -> None:
        self.collection.delete_one({"_id": entity_id}, session=session, **kwargs)

    def execute_raw(
        self,
        operation: str,
        session: ClientSession | None = None,
        **operation_kwargs,
    ) -> Any:
        op = getattr(self.collection, operation, None)
        if op is None:
            raise ValueError(f"Unknown operation on collection: {operation}")
        return op(session=session, **operation_kwargs)

    def filter(
        self, qry: MongoFilterQuery, session: ClientSession | None = None, **kwargs
    ) -> Pagination:
        query_result = self.collection.aggregate(qry.to_query(), session=session, **kwargs)
        if (unwrapped := next(query_result, None)) is None:
            raise ValueError(f"{qry.__class__.__name__} returned nothing")

        return Pagination(
            total=(unwrapped["metadata"][0]["total"] if unwrapped["metadata"] else 0),
            items=unwrapped["items"],
            page=qry.page,
            per_page=qry.per_page,
        )

    @functools.cached_property
    def _entity_type(self) -> T:
        orig_base = next(
            (base for base in self.__class__.__orig_bases__ if get_origin(base) is MongoRepository),
            None,
        )
        if orig_base is None:
            raise ValueError("No origin base found")

        return get_args(orig_base)[0]


def setup_indexes(
    db_names: Iterable[str],
    mongo_client: pymongo.MongoClient | None = None,
    mongo_uri: str | None = None,
) -> None:
    # NOTE: 동일한 이름의 컬렉션이 여러 DB에 존재할 경우, 컬렉션별로 인덱스를 생성할 수 없음

    if mongo_client is None and mongo_uri is None:
        raise ValueError("Either `mongo_client` or `mongo_uri` must be provided")

    if mongo_uri is not None:
        warnings.warn(
            (
                "`mongo_uri` is deprecated and will be removed in the future. "
                "Use `mongo_client` instead."
            ),
            DeprecationWarning,
        )

        with pymongo.MongoClient(mongo_uri) as mongo_client:
            setup_database_indexes(*(mongo_client.get_database(db_name) for db_name in db_names))

        return

    setup_database_indexes(*(mongo_client.get_database(db_name) for db_name in db_names))


def setup_database_indexes(*databases: Unpack[tuple[Database, ...]]) -> None:
    for database in databases:
        collection_names = database.list_collection_names()
        for collection_name, indexes in registry.items():
            if not collection_name or collection_name not in collection_names:
                continue
            collection = database.get_collection(collection_name)

            previous_index_names = {index["name"] for index in collection.list_indexes()}
            current_index_names = {
                *(index.document["name"] for index in indexes),
                "_id_",
            }

            for index_name in previous_index_names - current_index_names:
                collection.drop_index(index_name)

            if indexes:
                collection.create_indexes(indexes)
