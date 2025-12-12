import abc

from .. import model


class MessageQueue(abc.ABC):
    @abc.abstractmethod
    def push(self, message: model.EventMessage) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def peek(self) -> model.EventMessage | None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, message: model.EventMessage) -> None:
        raise NotImplementedError
