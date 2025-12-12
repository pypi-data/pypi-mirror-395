from collections.abc import Iterator


def find[T](iterator: Iterator[T], /) -> T | None:
    return next(iterator, None)


def unwrap[T](v: T | None, exc: Exception, /) -> T:
    if v is None:
        raise exc
    return v
