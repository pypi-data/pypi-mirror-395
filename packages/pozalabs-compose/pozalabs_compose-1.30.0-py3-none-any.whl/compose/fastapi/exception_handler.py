import http
from collections.abc import Awaitable, Callable
from typing import ClassVar, Self

from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException

from compose import schema

type ExceptionHandler[E: Exception] = Callable[[Request, E], Response | Awaitable[Response]]


class ExceptionHandlerInfo:
    default_response_cls: ClassVar[type[Response]] = JSONResponse

    def __init__(
        self, exc_class_or_status_code: int | type[Exception], handler: ExceptionHandler
    ) -> None:
        self.exc_class_or_status_code = exc_class_or_status_code
        self.handler = handler

    @classmethod
    def for_status_code(
        cls,
        status_code: http.HTTPStatus,
        error_type: str | None = None,
        response_cls: type[Response] | None = None,
    ) -> Self:
        return cls(
            exc_class_or_status_code=status_code,
            handler=create_exception_handler(
                status_code=status_code,
                error_type=error_type or status_code.name.lower(),
                response_cls=response_cls or cls.default_response_cls,
            ),
        )

    @classmethod
    def for_unauthorized_error(cls, response_cls: type[Response] | None = None) -> Self:
        return cls(
            exc_class_or_status_code=http.HTTPStatus.UNAUTHORIZED,
            handler=create_unauthorized_error_handler(response_cls or cls.default_response_cls),
        )

    @classmethod
    def for_exc(
        cls,
        exc_cls: type[Exception],
        status_code: int,
        error_type: str | None = None,
        response_cls: type[Response] | None = None,
    ) -> Self:
        return cls(
            exc_class_or_status_code=exc_cls,
            handler=create_exception_handler(
                status_code=status_code,
                error_type=error_type or http.HTTPStatus(status_code).name.lower(),
                response_cls=response_cls or cls.default_response_cls,
            ),
        )

    @classmethod
    def default(cls) -> Self:
        return cls(
            exc_class_or_status_code=Exception,
            handler=create_exception_handler(
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                error_type=http.HTTPStatus.INTERNAL_SERVER_ERROR.name.lower(),
                response_cls=cls.default_response_cls,
            ),
        )

    @classmethod
    def for_http_exception(cls, response_cls: type[Response] | None = None) -> Self:
        return cls(
            exc_class_or_status_code=HTTPException,
            handler=create_http_exception_handler(response_cls or cls.default_response_cls),
        )

    @classmethod
    def for_request_validation_error(
        cls,
        exception_handler: ExceptionHandler | None = None,
        response_cls: type[Response] | None = None,
    ) -> Self:
        return cls(
            exc_class_or_status_code=RequestValidationError,
            handler=(
                exception_handler
                or create_default_validation_error_handler(response_cls or cls.default_response_cls)
            ),
        )

    @classmethod
    def for_pydantic_validation_error(
        cls,
        exception_handler: ExceptionHandler | None = None,
        response_cls: type[Response] | None = None,
    ) -> Self:
        return cls(
            exc_class_or_status_code=ValidationError,
            handler=(
                exception_handler
                or create_default_validation_error_handler(response_cls or cls.default_response_cls)
            ),
        )


def create_exception_handler(
    status_code: int,
    error_type: str,
    response_cls: type[Response],
) -> ExceptionHandler:
    def exception_handler(request: Request, exc: Exception) -> Response:
        response = exc_to_error_schema(exc=exc, error_type=error_type)
        return response_cls(content=jsonable_encoder(response), status_code=status_code)

    return exception_handler


def create_unauthorized_error_handler(response_cls: type[Response]) -> ExceptionHandler:
    def exception_handler(request: Request, exc: Exception) -> Response:
        if isinstance(exc, HTTPException) and exc.headers.get(
            "WWW-Authenticate", ""
        ).lower().startswith("basic"):
            return PlainTextResponse(
                content=exc.detail,
                status_code=exc.status_code,
                headers=exc.headers,
            )

        response = exc_to_error_schema(
            exc=exc,
            error_type=(status_code := http.HTTPStatus.UNAUTHORIZED).name.lower(),
        )
        return response_cls(content=jsonable_encoder(response), status_code=status_code)

    return exception_handler


def exc_to_error_schema(exc: Exception, error_type: str) -> schema.Error:
    return schema.Error(
        title=str(exc),
        type=error_type,
        detail=getattr(exc, "detail", None),
        invalid_params=(
            (invalid_params := getattr(exc, "invalid_params", None))
            and [
                schema.InvalidParam.model_validate(obj=invalid_param)
                for invalid_param in invalid_params
            ]
        ),
    )


def create_http_exception_handler(response_cls: type[Response]) -> ExceptionHandler:
    def http_exception_handler(request: Request, exc: HTTPException) -> Response:
        status_code = http.HTTPStatus(exc.status_code)
        return response_cls(
            content=jsonable_encoder(
                schema.Error(
                    title=exc.detail,
                    type=status_code.name.lower(),
                )
            ),
            status_code=status_code,
            headers=exc.headers,
        )

    return http_exception_handler


def create_default_validation_error_handler(response_cls: type[Response]) -> ExceptionHandler:
    def validation_error_handler(
        request: Request, exc: RequestValidationError | ValidationError
    ) -> Response:
        return response_cls(
            content=jsonable_encoder(
                schema.Error.from_validation_error(exc=exc, title="Validation failed"),
            ),
            status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    return validation_error_handler
