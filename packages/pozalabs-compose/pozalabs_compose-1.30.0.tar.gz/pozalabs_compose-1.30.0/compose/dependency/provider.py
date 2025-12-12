from collections.abc import Callable

from dependency_injector import providers


def factory_of_factory[**P, T](
    t: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> providers.Factory[providers.Factory[T]]:
    return providers.Factory(
        providers.Factory,
        t,
        *args,
        **kwargs,
    )
