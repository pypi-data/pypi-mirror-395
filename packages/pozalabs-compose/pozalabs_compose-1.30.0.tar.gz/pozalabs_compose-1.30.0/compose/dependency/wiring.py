import enum
import importlib
import inspect
from collections.abc import Callable, Iterable
from typing import Any, Protocol

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

type Container = type[containers.Container] | containers.Container

DEFAULT_RESOLVABLE_PROVIDER_TYPES = (providers.Factory, providers.Singleton)


class Wirer(Protocol):
    def __call__(
        self,
        container: containers.Container,
        modules: Iterable[str] | None = None,
        from_package: str | None = None,
    ) -> None: ...


def create_wirer(packages: Iterable[str]) -> Wirer:
    def wire_container(
        container: containers.Container,
        modules: Iterable[str] | None = None,
        from_package: str | None = None,
    ) -> None:
        container.check_dependencies()
        container.wire(modules=modules, packages=packages, from_package=from_package)

    return wire_container


def resolve_by_name_from_container_provider(
    name: str,
    container: providers.Container,
    provider_types: Iterable[type[providers.Provider]],
) -> providers.Factory:
    if not isinstance(name, str):
        raise ValueError("`name` must be string")

    for provider_name, provider in container.providers.items():
        if not isinstance(provider, (providers.Container, *provider_types)):
            continue

        if provider_name == name:
            return provider

        if isinstance(provider, providers.Container):
            return resolve_by_name_from_container_provider(
                name=name,
                container=provider,
                provider_types=provider_types,
            )


def resolve_by_name(
    name: str,
    container: Container,
    provider_types: Iterable[type[providers.Provider]],
) -> providers.Factory:
    if not isinstance(name, str):
        raise ValueError("`name` must be string")

    for provider_name, provider in container.providers.items():
        if not isinstance(provider, (providers.Container, *provider_types)):
            continue

        if provider_name == name:
            return provider

        if isinstance(provider, providers.Container):
            result = resolve_by_name_from_container_provider(
                name=name,
                container=provider,
                provider_types=provider_types,
            )
            if result is not None:
                return result

    raise ValueError(f"Cannot find {name} from given container")


def resolve_by_object_name(
    name: str,
    container: Container,
    provider_types: Iterable[type[providers.Provider]],
) -> Any:
    candidates: list[providers.Factory] = []
    for provider in container.traverse([*provider_types]):
        if not inspect.isclass(provider.cls):
            continue

        if provider.cls.__name__.split(".")[-1] == name:
            candidates.append(provider)

    if not candidates:
        raise ValueError(f"Cannot find {name} from given container")

    if len(candidates) > 1:
        raise ValueError(f"Cannot resolve {name} since there are multiple candidates")

    return candidates[0]()


class ConflictResolution(str, enum.Enum):
    FIRST = "first"
    ERROR = "error"


def resolve(
    type_: type[Any] | str,
    container: Container,
    provider_types: Iterable[type[providers.Provider]] = DEFAULT_RESOLVABLE_PROVIDER_TYPES,
    *,
    name: str | None = None,
    conflict_resolution: ConflictResolution = ConflictResolution.FIRST,
) -> providers.Factory:
    """
    의존성 전체 등록 경로를 참조하지 않고 의존성을 해결합니다. 다른 패키지의 의존성을 참조하는 경우
    의존 대상 선언 경로에 깊게 의존하는 것을 방지합니다. `container_cls`는 최상위 컨테이너일수도,
    의존성이 등록된 (하위) 컨테이너일수도 있습니다. 클래스 대상으로만 작동합니다.
    """
    if not (inspect.isclass(type_) or isinstance(type_, str)):
        raise ValueError("Only class or string can be resolved")

    if isinstance(type_, str):
        return resolve_by_name(name=type_, container=container, provider_types=provider_types)

    candidates = []
    for provider in container.traverse([*provider_types]):
        provider_cls = provider.cls
        if not (inspect.isclass(provider_cls) or inspect.ismethod(provider_cls)):
            continue

        cls = provider_cls.__self__ if inspect.ismethod(provider_cls) else provider_cls
        if cls.__name__ == type_.__name__:
            candidates.append(provider)

    if not candidates:
        raise ValueError(f"Cannot find {type_.__name__} from given container")

    if len(candidates) > 1 and name is None and conflict_resolution == ConflictResolution.ERROR:
        type_name = type_.__name__ if inspect.isclass(type_) else type_
        raise ValueError(
            f"Cannot resolve {type_name} since there are multiple candidates. "
            f"You must specify `name` argument to resolve dependency"
        )

    if len(candidates) == 1:
        return candidates[0]

    if name is None and conflict_resolution == ConflictResolution.FIRST:
        return candidates[0]

    return resolve_by_name(name=name, container=container, provider_types=provider_types)


def provide[T](
    type_: type[T],
    from_: type[containers.Container],
    /,
    *,
    provider_types: Iterable[type[providers.Provider]] = DEFAULT_RESOLVABLE_PROVIDER_TYPES,
    name: str | None = None,
    conflict_resolution: ConflictResolution = ConflictResolution.FIRST,
) -> Provide[T]:
    return Provide[
        resolve(
            type_=type_,
            container=from_,
            provider_types=provider_types,
            name=name,
            conflict_resolution=conflict_resolution,
        )
    ]


def create_resolver(container: Container) -> Callable[[str], Any]:
    def resolver(name: str) -> Any:
        return resolve(type_=name, container=container)

    return resolver


def create_lazy_resolver(container_path: str) -> Callable[[str], Any]:
    def resolver(object_name: str) -> Any:
        module_path, container_name = container_path.split(":")
        try:
            container = importlib.import_module(module_path)
        except ImportError:
            raise ImportError(f"Cannot not import module {module_path}")

        if (container_cls := getattr(container, container_name, None)) is None:
            raise ValueError(f"Cannot find container {container_name} in {module_path}")

        return resolve_by_object_name(
            name=object_name,
            container=container_cls,
            provider_types=DEFAULT_RESOLVABLE_PROVIDER_TYPES,
        )

    return resolver


class Provider[T](Protocol):
    def __call__(
        self,
        t: type[T],
        /,
        name: str | None = None,
        conflict_resolution: ConflictResolution = ConflictResolution.FIRST,
    ) -> Provide[T]: ...


def create_provider[T](
    container: type[containers.Container],
    provider_types: Iterable[type[providers.Provider]] = DEFAULT_RESOLVABLE_PROVIDER_TYPES,
) -> Provider[T]:
    def provider(
        type_: type[T],
        /,
        name: str | None = None,
        conflict_resolution: ConflictResolution = ConflictResolution.FIRST,
    ) -> Provide[T]:
        return provide(
            type_,
            container,
            provider_types=provider_types,
            name=name,
            conflict_resolution=conflict_resolution,
        )

    return provider


def get_wiring_packages(*container_types: *tuple[type[containers.Container], ...]) -> set[str]:
    return {get_container_package(c) for c in container_types}


def get_container_package(container_type: type[containers.Container]) -> str:
    parts = container_type.__module__.split(".")

    if len(parts) >= 2:
        root, package, *_ = parts
        return f"{root}.{package}"

    raise ValueError(
        f"Invalid module path for {container_type.__name__}: expected 'root.package.*', got '{container_type.__module__}'"
    )
