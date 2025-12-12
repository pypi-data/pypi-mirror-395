from .._internal import is_package_installed

if not is_package_installed("fastapi"):
    raise ImportError("Install `fastapi` to use `compose.fastapi` package")

from .depends import CommandUpdater, UserInjector, create_with_user
from .endpoint import health_check
from .exception_handler import (
    ExceptionHandler,
    ExceptionHandlerInfo,
    create_exception_handler,
)
from .openapi import (
    OpenAPIDoc,
    OpenAPISchema,
    RedocHTML,
    SwaggerUIHTML,
    add_doc_routes,
    additional_responses,
    openapi_tags,
)
from .param import OffsetPaginationParams, WithPath, as_query, to_query, with_depends
from .response import NoContentResponse, ZipStreamingResponse
from .routing import APIRouter, create_auto_wired_route
from .security import APIKeyHeader, CookieAuth, HTTPBasic, HTTPBearer, unauthorized_error
from .wiring import AutoWired, auto_wired

__all__ = [
    "APIKeyHeader",
    "APIRouter",
    "AutoWired",
    "CommandUpdater",
    "CookieAuth",
    "ExceptionHandler",
    "ExceptionHandlerInfo",
    "HTTPBasic",
    "HTTPBearer",
    "NoContentResponse",
    "OffsetPaginationParams",
    "OpenAPIDoc",
    "OpenAPISchema",
    "RedocHTML",
    "SwaggerUIHTML",
    "UserInjector",
    "WithPath",
    "ZipStreamingResponse",
    "add_doc_routes",
    "additional_responses",
    "as_query",
    "auto_wired",
    "create_auto_wired_route",
    "create_exception_handler",
    "create_with_user",
    "health_check",
    "openapi_tags",
    "to_query",
    "unauthorized_error",
    "with_depends",
]


try:
    from .utils import (  # noqa: F401
        ErrorEvent,
        Level,
        capture_error,
        create_before_send_hook,
        init_sentry,
    )

    __all__.extend(
        [
            "ErrorEvent",
            "Level",
            "capture_error",
            "create_before_send_hook",
            "init_sentry",
        ]
    )
except ImportError:
    pass
