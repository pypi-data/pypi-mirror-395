import functools
from collections.abc import Callable
from typing import Any

from pymongo.client_session import ClientSession, SessionOptions, TransactionOptions

from ..utils import unordered_partial


class MongoUnitOfWork[T]:
    def __init__(self, session_factory: Callable[..., ClientSession]):
        self.session_factory = session_factory

    def with_transaction(
        self,
        callback: Callable[[ClientSession], T] | Callable[..., T],
        *,
        session_options: SessionOptions | None = None,
        transaction_options: TransactionOptions | None = None,
        **kwargs: Any,
    ) -> T:
        session_options = session_options or SessionOptions()
        transaction_options = transaction_options or TransactionOptions()

        with self.session_factory(
            causal_consistency=session_options.causal_consistency,
            default_transaction_options=session_options.default_transaction_options,
            snapshot=session_options.snapshot,
        ) as session:
            result = session.with_transaction(
                callback=(
                    unordered_partial(p=functools.partial(callback), t=ClientSession)
                    if isinstance(callback, functools.partial)
                    else unordered_partial(p=functools.partial(callback, **kwargs), t=ClientSession)
                ),
                read_concern=transaction_options.read_concern,
                write_concern=transaction_options.write_concern,
                read_preference=transaction_options.read_preference,
                max_commit_time_ms=transaction_options.max_commit_time_ms,
            )

        return result


def mongo_transactional[T](func: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        instance = args[0]

        if not hasattr(instance, "__dict__"):
            raise ValueError(f"`{instance.__class__.__name__}` does not have `__dict__` attribute")

        uow: MongoUnitOfWork | None = next(
            (t for t in instance.__dict__.values() if isinstance(t, MongoUnitOfWork)),
            None,
        )
        if uow is None:
            raise ValueError(
                f"`{instance.__class__.__name__}` does not have `{MongoUnitOfWork.__name__}` attribute"
            )

        return uow.with_transaction(functools.partial(func, *args, **kwargs))

    return wrapper
