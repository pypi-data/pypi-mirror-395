from typing import TypeVar

from compose import container
from compose.event import Event

MessageBody = TypeVar("MessageBody", bound=Event)


class EventMessage(container.BaseModel):
    body: MessageBody


class SqsEventMessage(EventMessage):
    receipt_handle: str
