import asyncio
import collections
import contextlib

from ..messagebus import MessageBus
from ..model import EventMessage
from ..queue.local import LocalMessageQueue, event_store
from .hook import DEFAULT_HOOKS, Hook, HookArgType, HookEventType, default_hook

try:
    from starlette.types import ASGIApp, Receive, Scope, Send
except ImportError:
    raise ImportError("Please install `starlette` to use `MessageConsumerASGIMiddleware`")


class MessageConsumerASGIMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        messagebus: MessageBus,
        message_queue: LocalMessageQueue,
        hooks: dict[HookEventType, list[Hook]] | None = None,
    ) -> None:
        self.app = app
        self.messagebus = messagebus
        self.message_queue = message_queue
        self.hooks = DEFAULT_HOOKS | (hooks or {})

        self._default_hook = default_hook

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        self._execute_hook("on_start", "MessageConsumer started")
        with self.event_store_context():
            try:
                await self.app(scope, receive, send)
            finally:
                await self.consume_messages(event_store.get())
                self._execute_hook("on_shutdown", "MessageConsumer shutting down")

    @contextlib.contextmanager
    def event_store_context(self):
        token = event_store.set(collections.deque())

        try:
            yield
        finally:
            event_store.reset(token)

    async def consume_messages(self, messages: collections.deque[EventMessage]) -> None:
        await asyncio.gather(*(self.consume(message) for message in messages))

    async def consume(self, message: EventMessage) -> None:
        self._execute_hook("on_receive", message)
        try:
            await self.messagebus.handle_event(message.body)
            self.message_queue.delete(message)
        except Exception as exc:
            self._execute_hook("on_consume_error", exc)
            return

        self._execute_hook("on_consume", message)

    def _execute_hook(self, hook_event_type: HookEventType, arg: HookArgType, /) -> None:
        for hook in self.hooks.get(hook_event_type, [self._default_hook]):
            hook(arg)
