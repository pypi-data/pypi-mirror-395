from .consumer import MessageConsumer
from .consumer_runner import ThreadMessageConsumerRunner
from .messagebus import MessageBus
from .model import EventMessage, SqsEventMessage
from .publisher import EventPublisher
from .queue.base import MessageQueue
from .queue.local import LocalMessageQueue, event_store
from .signal_handler import DefaultSignalHandler, SignalHandler, ThreadSignalHandler

__all__ = [
    "EventMessage",
    "SqsEventMessage",
    "MessageQueue",
    "LocalMessageQueue",
    "event_store",
    "MessageConsumer",
    "ThreadMessageConsumerRunner",
    "MessageBus",
    "EventPublisher",
    "SignalHandler",
    "DefaultSignalHandler",
    "ThreadSignalHandler",
]

try:
    from .queue.sqs import SqsMessageQueue  # noqa: F401

    __all__.append("SqsMessageQueue")
except ImportError:
    pass


try:
    from .consumer.fastapi import MessageConsumerASGIMiddleware  # noqa: F401

    __all__.append("MessageConsumerASGIMiddleware")
except ImportError:
    pass
