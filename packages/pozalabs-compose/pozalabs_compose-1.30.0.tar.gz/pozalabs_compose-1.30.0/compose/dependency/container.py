from collections.abc import Iterable
from typing import Self

from dependency_injector import containers

from .wiring import Wirer


class DeclarativeContainer(containers.DeclarativeContainer):
    @classmethod
    def wired(
        cls,
        wirer: Wirer,
        modules: Iterable[str] | None = None,
        from_package: str | None = None,
    ) -> Self:
        container = cls()
        wirer(container, modules=modules, from_package=from_package)
        return container
