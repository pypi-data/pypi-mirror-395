import http
import secrets
from collections.abc import Callable
from typing import Literal, Self

from fastapi import HTTPException, Request
from fastapi.security import APIKeyHeader as FastAPIAPIKeyHeader
from fastapi.security import HTTPBasic as FastAPIHTTPBasic
from fastapi.security import HTTPBearer as FastAPIHTTPBearer
from fastapi.security.base import SecurityBase
from starlette.exceptions import HTTPException as StarletteHTTPException


def unauthorized_error(detail: str, headers: dict[str, str] | None = None) -> HTTPException:
    return HTTPException(
        status_code=http.HTTPStatus.UNAUTHORIZED,
        detail=detail,
        headers=headers,
    )


class HTTPBasic[T](FastAPIHTTPBasic):
    def __init__(
        self,
        *,
        authenticator: Callable[[str, str], T],
        scheme_name: str | None = None,
        realm: str | None = None,
        description: str | None = None,
        auto_error: bool = True,
    ):
        super().__init__(
            scheme_name=scheme_name,
            realm=realm,
            description=description,
            auto_error=auto_error,
        )
        self.authenticator = authenticator

    async def __call__(self, request: Request) -> T:
        credentials = await super().__call__(request)
        return self.authenticator(credentials.username, credentials.password)

    @classmethod
    def static(cls, username: str, password: str) -> Self:
        def compare_digest(a: str, b: str) -> bool:
            return secrets.compare_digest(a.encode(), b.encode())

        def authenticate(_username: str, _password: str) -> None:
            is_correct_username = compare_digest(_username, username)
            is_correct_password = compare_digest(_password, password)

            if not (is_correct_username and is_correct_password):
                raise unauthorized_error(
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Basic"},
                )

        return cls(authenticator=authenticate)


class APIKeyHeader(FastAPIAPIKeyHeader):
    def __init__(
        self,
        *,
        api_key: str,
        name: str = "X-API-Key",
        auto_error: bool = True,
        scheme_name: str | None = None,
        description: str | None = None,
    ):
        super().__init__(
            name=name,
            auto_error=auto_error,
            scheme_name=scheme_name,
            description=description,
        )
        self.api_key = api_key

    async def __call__(self, request: Request) -> str:
        exc = unauthorized_error(detail="Not authenticated. Invalid API key")

        try:
            input_api_key = await super().__call__(request)
        except (StarletteHTTPException, HTTPException):
            raise exc

        if input_api_key is None or input_api_key != self.api_key:
            raise exc

        return input_api_key


class HTTPBearer(FastAPIHTTPBearer):
    def __init__(
        self,
        *,
        auto_error: bool = True,
        error_handlers: dict[Literal["on_credentials_missing"], Callable[[], HTTPException]]
        | None = None,
    ):
        super().__init__(auto_error=auto_error)
        self.error_handlers = error_handlers or {}
        self._default_error_handler = lambda: unauthorized_error(detail="Not authenticated")

    async def __call__(self, request: Request) -> str:
        try:
            credentials = await super().__call__(request)
        except HTTPException:
            raise self.error_handlers.get("on_credentials_missing", self._default_error_handler)()

        return credentials.credentials


class CookieAuth(SecurityBase):
    def __init__(
        self,
        *,
        name: str,
        error_handlers: dict[Literal["on_cookie_missing"], Callable[[], HTTPException]]
        | None = None,
    ):
        self.name = name
        self.error_handlers = error_handlers or {}
        self._default_error_handler = lambda: unauthorized_error(detail="Not authenticated")

    async def __call__(self, request: Request) -> str:
        if (credentials := request.cookies.get(self.name)) is None:
            raise self.error_handlers.get("on_cookie_missing", self._default_error_handler)()

        return credentials
