import collections
import contextvars

from .. import model
from .base import MessageQueue

type EventMessageQueue = collections.deque[model.EventMessage]

event_store: contextvars.ContextVar[EventMessageQueue] = contextvars.ContextVar("event_store")


class LocalMessageQueue(MessageQueue):
    def push(self, message: model.EventMessage) -> None:
        events = event_store.get()
        events.append(message)

    def peek(self) -> model.EventMessage | None:
        events = event_store.get()
        return events[0] if events else None

    def delete(self, message: model.EventMessage) -> None:
        events = event_store.get()

        if message in events:
            events.remove(message)
