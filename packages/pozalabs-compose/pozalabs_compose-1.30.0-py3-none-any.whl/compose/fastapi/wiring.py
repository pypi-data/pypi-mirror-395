import inspect
from collections.abc import Callable
from typing import Annotated, Any

from dependency_injector.wiring import inject
from fastapi import Depends

from compose.dependency.wiring import Provider


def auto_wired[F: Callable[..., Any]](
    provider: Provider,
    *,
    with_injection: bool = False,
) -> Callable[[F], F]:
    """
    FastAPI 엔드포인트에 의존성을 자동으로 주입하는 데코레이터. 해당 데코레이터는 `@inject` 데코레이터보다
    먼저 적용되어야 합니다.

    주의: `__signature__` 속성은 일반 함수에만 존재하므로 해당 데코레이터는 메서드에 사용할 수 없습니다.
    """

    def wrapper(f: F) -> F:
        signature = inspect.signature(f)

        updated_params = []
        for name, param in signature.parameters.items():
            updated_param = param
            try:
                provided = provider(param.annotation)
                updated_param = updated_param.replace(
                    annotation=Annotated[param.annotation, Depends(provided)]
                )
            except ValueError:
                pass

            updated_params.append(updated_param)

        f.__signature__ = signature.replace(parameters=updated_params)

        if with_injection:
            f = inject(f)

        return f

    return wrapper


class AutoWired:
    def __init__(self, provider: Provider, injectors: dict[str, Callable[..., Any]] | None = None):
        self.provider = provider
        self.injectors = injectors or {}

    def __call__[F: Callable[..., Any]](self) -> Callable[[F], F]:
        def wrapper(f: F) -> F:
            signature = inspect.signature(f)

            updated_params = []
            for name, param in signature.parameters.items():
                updated_param = param

                if (injector := self.injectors.get(name)) is not None:
                    updated_param = updated_param.replace(default=Depends(injector))
                else:
                    try:
                        provided = self.provider(param.annotation)
                        updated_param = updated_param.replace(default=Depends(provided))
                    except ValueError:
                        pass

                updated_params.append(updated_param)

            f.__signature__ = signature.replace(parameters=updated_params)
            f = inject(f)

            return f

        return wrapper
