import enum
import functools
from collections.abc import Awaitable, Callable
from typing import Any, Self

from fastapi import Request, Response

from compose import container

from .exception_handler import ExceptionHandler

try:
    import sentry_sdk
    from sentry_sdk.integrations import Integration
except ImportError:
    raise ImportError("Install `sentry-sdk` to use sentry helpers")


class Level(enum.StrEnum):
    INFO = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()


class ErrorEvent(container.BaseModel):
    level: Level

    @classmethod
    def for_info(cls) -> Self:
        return cls(level=Level.INFO)

    @classmethod
    def for_warning(cls) -> Self:
        return cls(level=Level.WARNING)

    @classmethod
    def for_error(cls) -> Self:
        return cls(level=Level.ERROR)


type SentryHook = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]


def create_before_send_hook(
    error: dict[str, ErrorEvent], default_error_level: Level = Level.WARNING
) -> SentryHook:
    def before_send(event: dict[str, Any], hint: dict[str, Any]) -> dict[str, Any]:
        exc_name = ""
        if "exc_info" in hint:
            exc_type, *_ = hint["exc_info"]
            exc_name = exc_type.__name__

        error_event = error.get(exc_name)
        event["level"] = default_error_level if error_event is None else error_event.level
        return event

    return before_send


def init_sentry(
    integrations: list[Integration],
    environment: str,
    tags: dict[str, str],
    dsn: str | None = None,
    before_send: SentryHook | None = None,
    **kwargs,
) -> None:
    if dsn is None:
        return

    sentry_sdk.init(
        dsn=dsn,
        integrations=integrations,
        environment=environment,
        before_send=before_send,
        **kwargs,
    )
    scope = sentry_sdk.Scope.get_current_scope()
    for key, value in tags.items():
        scope.set_tag(key, value)


def capture_error(handler: ExceptionHandler) -> ExceptionHandler:
    @functools.wraps(handler)
    async def wrapper(request: Request, exc: Exception) -> Response | Awaitable[Response]:
        sentry_sdk.capture_exception(exc)
        result = handler(request, exc)
        if isinstance(result, Awaitable):
            return await result
        return result

    return wrapper
