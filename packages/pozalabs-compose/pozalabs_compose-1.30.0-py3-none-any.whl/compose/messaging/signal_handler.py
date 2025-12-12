import abc
import logging
import threading

logger = logging.getLogger("compose")


class SignalHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self) -> None:
        raise NotImplementedError

    @property
    def received_signal(self) -> bool:
        raise NotImplementedError


class DefaultSignalHandler(SignalHandler):
    def __init__(self):
        self._received_signal = False

    def handle(self) -> None:
        self._received_signal = True

    @property
    def received_signal(self) -> bool:
        return self._received_signal


class ThreadSignalHandler(SignalHandler):
    def __init__(self):
        self._exit_event = threading.Event()

    def handle(self) -> None:
        self._exit_event.set()

    @property
    def received_signal(self) -> bool:
        return self._exit_event.is_set()
