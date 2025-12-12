import asyncio
import collections
import functools
import re
from collections.abc import Callable
from typing import Protocol, Self

from compose.dependency.wiring import create_lazy_resolver
from compose.event import Event


class EventHandler(Protocol):
    def handle(self, evt: Event) -> None:
        ...


class MessageBus:
    def __init__(self, dependency_resolver: Callable[[str], EventHandler]):
        self.dependency_resolver = dependency_resolver

        self._event_handlers: dict[str, set[str]] = collections.defaultdict(set)

    @classmethod
    def with_container(cls, container_path: str) -> Self:
        container_path_pattern = re.compile("^(?P<module_path>.+):(?P<container_name>.+)$")
        if container_path_pattern.match(container_path) is None:
            raise ValueError(
                f"Invalid container path: {container_path}. "
                "Must be in the format `module.path:ContainerName`"
            )

        return cls(dependency_resolver=create_lazy_resolver(container_path))

    async def handle_event(self, evt: Event) -> None:
        handler_names = self._event_handlers.get(evt.__class__.__name__, set())
        event_loop = asyncio.get_running_loop()
        for handler_name in handler_names:
            handler = self.dependency_resolver(handler_name)
            await event_loop.run_in_executor(None, functools.partial(handler.handle, evt))

    def register(self, event_cls: type[Event]) -> Callable[[EventHandler], EventHandler]:
        def wrapper(handler_cls: EventHandler) -> EventHandler:
            event_name = event_cls.__name__
            handler_name = handler_cls.__name__

            registered_handler_names = self._event_handlers.get(event_cls.__name__, set())
            if handler_cls.__name__ in registered_handler_names:
                raise ValueError(
                    f"Handler {handler_name} already registered for event {event_name}"
                )

            self._event_handlers[event_name].add(handler_name)
            return handler_cls

        return wrapper
