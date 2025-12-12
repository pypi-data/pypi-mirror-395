import functools
import time
import types
from typing import ClassVar, NewType, Protocol, Self

import pendulum
import pymongo
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

from .exceptions import LockAcquisitionFailedError

Seconds = NewType("Seconds", float)


class MongoLockAcquirer(Protocol):
    def __call__(
        self,
        key: str,
        auto_release_after: Seconds = Seconds(60),
        timeout: Seconds = Seconds(60),
        lock_acquisition_interval: Seconds = Seconds(0.1),
    ) -> Self: ...


class MongoLock:
    default_collection_name: ClassVar[str] = "compose.lock"
    index_name: ClassVar[str] = "expires_at_ttl"

    def __init__(
        self,
        key: str,
        collection: Collection,
        auto_release_after: Seconds = Seconds(60),
        timeout: Seconds = Seconds(60),
        lock_acquisition_interval: Seconds = Seconds(0.1),
    ):
        self.key = key
        self.collection = collection
        self.auto_release_after = auto_release_after
        self.timeout = timeout
        self.lock_acquisition_interval = lock_acquisition_interval

    def _ensure_ttl_index(self) -> None:
        current_index = self.collection.index_information()
        if self.index_name not in current_index:
            self.collection.create_index(
                [(self.index_name, pymongo.ASCENDING)],
                name=self.index_name,
                expireAfterSeconds=0,
            )

    @classmethod
    def acquirer(cls, db: Database, collection_name: str | None = None) -> MongoLockAcquirer:
        collection_name = collection_name or cls.default_collection_name
        return functools.partial(cls, collection=db[collection_name])

    def __enter__(self) -> Self:
        if self.acquire():
            return self

        raise LockAcquisitionFailedError(f"Failed to acquire lock for key: {self.key}")

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: types.TracebackType,
    ) -> None:
        self.release()

    def acquire(self) -> bool:
        start_time = pendulum.DateTime.utcnow()
        try_until = start_time.add(seconds=self.timeout)
        expires_at = pendulum.DateTime.utcnow().add(seconds=self.auto_release_after)

        while True:
            try:
                lock = self.collection.find_one_and_update(
                    {
                        "_id": self.key,
                        "expires_at": {"$lt": pendulum.DateTime.utcnow()},
                    },
                    {"$set": {"expires_at": expires_at}},
                    upsert=True,
                    return_document=pymongo.ReturnDocument.AFTER,
                )
                if lock is None:
                    continue

                # MongoDB는 Date 타입에서 나노초를 버리기 때문에 <=로 비교
                if pendulum.instance(lock["expires_at"], tz=pendulum.UTC) <= expires_at:
                    return True

            except PyMongoError:
                pass

            if pendulum.DateTime.utcnow() > try_until:
                return False

            time.sleep(self.lock_acquisition_interval)

    def release(self) -> None:
        self.collection.delete_one({"_id": self.key})
