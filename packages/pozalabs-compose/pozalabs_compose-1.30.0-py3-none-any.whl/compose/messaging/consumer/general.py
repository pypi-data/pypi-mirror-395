import asyncio
import logging

from .. import model
from ..messagebus import MessageBus
from ..queue.base import MessageQueue
from ..signal_handler import DefaultSignalHandler, SignalHandler
from .hook import DEFAULT_HOOKS, Hook, HookArgType, HookEventType, default_hook

logger = logging.getLogger("compose")


class MessageConsumer:
    def __init__(
        self,
        messagebus: MessageBus,
        message_queue: MessageQueue,
        hooks: dict[HookEventType, list[Hook]] | None = None,
        signal_handler: SignalHandler | None = None,
    ):
        self.messagebus = messagebus
        self.message_queue = message_queue
        self.hooks = DEFAULT_HOOKS | (hooks or {})
        self.signal_handler = signal_handler or DefaultSignalHandler()

        self._default_hook = default_hook

    async def run(self) -> None:
        self._execute_hook("on_start", "MessageConsumer started")

        while not self.signal_handler.received_signal:
            try:
                message = self.message_queue.peek()
            except Exception as exc:
                self._execute_hook("on_receive_error", exc)
                continue

            if message is None:
                continue
            self._execute_hook("on_receive", message)

            try:
                await asyncio.create_task(self.consume(message))
            except Exception as exc:
                self._execute_hook("on_consume_error", exc)
                continue
            self._execute_hook("on_consume", message)

    async def consume(self, message: model.EventMessage) -> None:
        await self.messagebus.handle_event(message.body)
        self.message_queue.delete(message)

    def _execute_hook(self, hook_event_type: HookEventType, arg: HookArgType, /) -> None:
        for hook in self.hooks.get(hook_event_type, [self._default_hook]):
            hook(arg)

    def shutdown(self) -> None:
        self._execute_hook("on_shutdown", "MessageConsumer shutting down")
        self.signal_handler.handle()
