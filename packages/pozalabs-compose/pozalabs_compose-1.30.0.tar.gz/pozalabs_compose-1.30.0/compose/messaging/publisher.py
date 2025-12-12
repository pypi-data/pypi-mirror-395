import logging

from ..event import Event
from .model import EventMessage
from .queue.base import MessageQueue

logger = logging.getLogger("compose")


class EventPublisher:
    def __init__(self, message_queue: MessageQueue):
        self.message_queue = message_queue

    def publish(self, evt: Event) -> None:
        self.message_queue.push(EventMessage(body=evt))

        logger.info(f"Published event: {evt.__class__.__name__}")
        logger.debug(f"Event: {evt.encode()}")
