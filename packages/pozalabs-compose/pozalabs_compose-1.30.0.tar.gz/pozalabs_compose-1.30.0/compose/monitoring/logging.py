from __future__ import annotations

import functools
import inspect
import time
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Logger


def create_elapsed_logger[T, **P](logger: Logger) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator[T, **P](func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            func_name = get_function_name(func, *args)
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_time = f"{time.perf_counter() - start:.3f}"
            logger.info(
                f"{func_name} took {elapsed_time}", func_name=func_name, elasped_time=elapsed_time
            )
            return result

        @functools.wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            func_name = get_function_name(func, *args)
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed_time = f"{time.perf_counter() - start:.3f}"
            logger.info(
                f"{func_name} took {elapsed_time}", func_name=func_name, elasped_time=elapsed_time
            )
            return result

        return async_wrapper if inspect.iscoroutinefunction(func) else wrapper

    return decorator


def log_elapsed[T](
    func_name: str,
    logger: Logger,
    func: Callable[[], T],
) -> T:
    start = time.perf_counter()
    result = func()
    elapsed_time = f"{time.perf_counter() - start:.3f}"
    logger.info(f"{func_name} took {elapsed_time}", func_name=func_name, elasped_time=elapsed_time)
    return result


def get_function_name[T, **P](func: Callable[P, T], *args) -> str:
    func_name = func.__name__
    return (
        f"{args[0].__class__.__name__}.{func_name}"
        if args and hasattr(args[0], "__class__") and hasattr(args[0], func_name)
        else func_name
    )
