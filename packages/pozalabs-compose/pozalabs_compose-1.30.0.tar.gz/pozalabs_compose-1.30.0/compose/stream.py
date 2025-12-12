from collections.abc import Generator
from typing import IO


def chunk_reader[T](f: IO[T], chunk_size: int = 1024 * 1024) -> Generator[T, None, None]:
    while chunk := f.read(chunk_size):
        yield chunk
