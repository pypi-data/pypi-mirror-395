import asyncio
from collections.abc import Awaitable, Callable, Hashable
from typing import Literal, overload

from pydantic.dataclasses import dataclass


class AsyncJob[K: Hashable, **P, T]:
    def __init__(
        self,
        key: K,
        func: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ):
        self.key = key
        self.func = func
        self.args = args
        self.kwargs = kwargs


@dataclass
class Result[K: Hashable, T]:
    key: K
    value: T


class AsyncTaskExecutor:
    def __init__(self, concurrency: int, timeout: float | None = None):
        self.concurrency = concurrency
        self.timeout = timeout

    @overload
    async def execute[K, **P, T](
        self,
        jobs: list[AsyncJob[K, P, T]],
        group: Literal[True] = True,
        concurrency: int | None = None,
        timeout: float | None = None,
    ) -> dict[K, Result[K, T]]: ...

    @overload
    async def execute[K, **P, T](
        self,
        jobs: list[AsyncJob[K, P, T]],
        group: Literal[False] = False,
        concurrency: int | None = None,
        timeout: float | None = None,
    ) -> list[Result[K, T]]: ...

    async def execute[K, **P, T](
        self,
        jobs: list[AsyncJob[K, P, T]],
        group: bool = False,
        concurrency: int | None = None,
        timeout: float | None = None,
    ) -> list[Result[K, T]] | dict[K, Result[K, T]]:
        result = await self._execute(
            jobs=jobs,
            concurrency=concurrency,
            timeout=timeout,
        )

        return {item.key: item for item in result} if group else result

    async def _execute[K, **P, T](
        self,
        jobs: list[AsyncJob[K, P, T]],
        concurrency: int | None = None,
        timeout: float | None = None,
    ) -> list[Result[K, T]]:
        concurrency = concurrency if concurrency is not None else self.concurrency
        timeout = timeout if timeout is not None else self.timeout

        coro = execute_jobs(jobs=jobs, semaphore=asyncio.Semaphore(concurrency))

        if timeout is None:
            return await coro

        async with asyncio.timeout(timeout):
            return await coro


async def execute_jobs[K, **P, T](
    jobs: list[AsyncJob[K, P, T]],
    semaphore: asyncio.Semaphore,
) -> list[Result[K, T]]:
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(execute_job(job=job, semaphore=semaphore)) for job in jobs]
    except* Exception as eg:
        raise eg.exceptions[0]

    return [task.result() for task in tasks]


async def execute_job[K, **P, T](
    job: AsyncJob[K, P, T], semaphore: asyncio.Semaphore
) -> Result[K, T]:
    async with semaphore:
        result = await job.func(*job.args, **job.kwargs)

    return Result(key=job.key, value=result)
