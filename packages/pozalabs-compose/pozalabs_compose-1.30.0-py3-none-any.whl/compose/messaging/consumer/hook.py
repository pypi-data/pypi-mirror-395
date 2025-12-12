import json
import logging
from collections.abc import Callable
from typing import Literal

from ..model import EventMessage

logger = logging.getLogger("compose")

HookEventType = Literal[
    "on_start",
    "on_receive",
    "on_receive_error",
    "on_consume",
    "on_consume_error",
    "on_shutdown",
]
type HookArgType = str | EventMessage | Exception
type Hook = Callable[[HookArgType], None]


def default_hook(_) -> None: ...


def log_event_message(log_message: str, message: EventMessage) -> None:
    logger.info(
        f"{log_message}: {json.dumps(message.encode())}",
        extra={"event_message": message.encode()},
    )


def log_exception(log_message: str, exc: Exception) -> None:
    logger.exception(log_message, exc_info=exc, stack_info=True)


DEFAULT_HOOKS = {
    "on_start": [logger.info],
    "on_receive": [lambda message: log_event_message("Received message", message)],
    "on_receive_error": [lambda exc: log_exception("Failed to receive message", exc)],
    "on_consume": [lambda message: log_event_message("Consumed message", message)],
    "on_consume_error": [lambda exc: log_exception(f"Failed to consume message due to {exc}", exc)],
    "on_shutdown": [logger.info],
}
