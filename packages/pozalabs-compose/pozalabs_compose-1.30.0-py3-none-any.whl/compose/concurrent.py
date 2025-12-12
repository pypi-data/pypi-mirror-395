import collections
import concurrent.futures
import functools
from collections.abc import Callable, Hashable
from typing import Literal, Self, overload

from pydantic.dataclasses import dataclass


def execute_in_pool[K, T](
    pool_factory: Callable[[], concurrent.futures.Executor],
    funcs: dict[K, functools.partial[T]],
    timeout: int | None = None,
) -> dict[K, T]:
    result = {}
    with pool_factory() as executor:
        future_to_key = dict()
        for key, func in funcs.items():
            future = executor.submit(func)
            future_to_key[future] = key

        for future in concurrent.futures.as_completed(future_to_key, timeout=timeout):
            result[future_to_key[future]] = future.result()

    return result


class ThreadPoolJob[K: Hashable, **P, T]:
    def __init__(
        self,
        key: K,
        func: Callable[P, T],
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


class ThreadPoolExecutor:
    def __init__(self, max_workers: int, timeout: int | None = None):
        self.max_workers = max_workers
        self.timeout = timeout

    @overload
    def execute[K, **P, T](
        self,
        jobs: list[ThreadPoolJob[K, P, T]],
        group: Literal[True] = True,
        max_workers: int | None = None,
        timeout: int | None = None,
    ) -> dict[K, Result[K, T]]: ...

    @overload
    def execute[K, **P, T](
        self,
        jobs: list[ThreadPoolJob[K, P, T]],
        group: Literal[False] = False,
        max_workers: int | None = None,
        timeout: int | None = None,
    ) -> list[Result[K, T]]: ...

    def execute[K, **P, T](
        self,
        jobs: list[ThreadPoolJob[K, P, T]],
        group: bool = False,
        max_workers: int | None = None,
        timeout: int | None = None,
    ) -> list[Result[K, T]] | dict[K, Result[K, T]]:
        result = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers or self.max_workers
        ) as executor:
            future_to_key = {}

            for job in jobs:
                future = executor.submit(job.func, *job.args, **job.kwargs)
                future_to_key[future] = job.key

            for future in concurrent.futures.as_completed(
                future_to_key, timeout=timeout or self.timeout
            ):
                result.append(Result(key=future_to_key[future], value=future.result()))

        return {result.key: result for result in result} if group else result


class DependencyJob[K: Hashable, **P, T]:
    def __init__(
        self,
        key: K,
        dependencies: set[K],
        func: Callable[P, T],
        **kwargs: P.kwargs,
    ):
        self.key = key
        self.dependencies = dependencies
        self.func = func
        self.kwargs = kwargs

    @classmethod
    def no_dependencies(
        cls,
        key: K,
        func: Callable[P, T],
        **kwargs: P.kwargs,
    ) -> Self:
        return cls(
            key=key,
            dependencies=set(),
            func=func,
            **kwargs,
        )


class DependencyExecutor:
    def __init__(self, max_workers: int, timeout: int | None = None):
        self.max_workers = max_workers
        self.timeout = timeout

    def execute[K, **P, T](
        self,
        jobs: list[DependencyJob[K, P, T]],
        max_workers: int | None = None,
        timeout: int | None = None,
    ) -> dict[K, T]:
        if not jobs:
            return {}

        max_workers = max_workers or self.max_workers

        job_map = {job.key: job for job in jobs}
        dependencies = {job.key: job.dependencies for job in jobs}
        dependents = self._build_dependents(dependencies)

        completed = {}
        ready_queue = self._get_ready_queue(jobs)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            active_futures = {}

            while len(completed) < len(jobs):
                while ready_queue and len(active_futures) < max_workers:
                    job_key = ready_queue.popleft()
                    job = job_map[job_key]
                    future = executor.submit(job.func, **job.kwargs)
                    active_futures[future] = job_key

                if not active_futures:
                    continue

                done, _ = concurrent.futures.wait(
                    active_futures,
                    return_when=concurrent.futures.FIRST_COMPLETED,
                    timeout=timeout or self.timeout,
                )

                for future in done:
                    job_id = active_futures.pop(future)
                    completed[job_id] = future.result()

                    # 완료된 작업에 의존하는 작업 중 모든 의존성이 충족된 작업만 확인
                    # dependencies = {"A": set(), "B": set(), "C": {"A"}, "D": {"A", "B"}, "E": {"C", "D"}}
                    # dependents = {"A": {"C", "D"}, "B": {"D"}, "C": {"E"}, "D": {"E"}}
                    # 1. completed = {}, ready_queue = [A, B]
                    # 2. A 완료 -> completed = {"A": "result_A"}, dependents.get("A") = {"C", "D"}
                    #    dependencies["C"] = {"A"} ⊆ completed.keys() -> ready_queue.append("C")
                    #    dependencies["D"] = {"A", "B"} ⊈ completed.keys() -> X
                    # 3. B 완료 -> completed = {"A": "result_A", "B": "result_B"}, dependents.get("B") = {"D"}
                    #    dependencies["D"] = {"A", "B"} ⊆ completed.keys() -> ready_queue.append("D")
                    # C, D, E도 같은 방식으로 처리
                    for dependent_id in dependents.get(job_id, set()):
                        if dependent_id not in completed and dependencies[dependent_id].issubset(
                            completed.keys()
                        ):
                            ready_queue.append(dependent_id)

        return completed

    @staticmethod
    def _get_ready_queue[K, **P, T](jobs: list[DependencyJob[K, P, T]]) -> collections.deque[K]:
        ready_queue = collections.deque()
        for job in jobs:
            if not job.dependencies:
                ready_queue.append(job.key)
        return ready_queue

    @staticmethod
    def _build_dependents[K](dependencies: dict[str, set[K]]) -> dict[str, set[K]]:
        dependents = collections.defaultdict(set)
        for key, deps in dependencies.items():
            for dep in deps:
                dependents[dep].add(key)
        return dict(dependents)
