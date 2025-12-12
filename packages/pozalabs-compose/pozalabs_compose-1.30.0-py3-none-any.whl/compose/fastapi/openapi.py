import enum
from collections.abc import Callable
from typing import Any

from fastapi import Depends, FastAPI, Response
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse

from compose import container, schema


def openapi_tags(tag: type[enum.StrEnum]) -> list[dict[str, Any]]:
    return [{"name": member.value} for member in tag.__members__.values()]


def additional_responses(
    *status_codes: int, schema_type: type[container.BaseModel] = schema.Error
) -> dict[int, dict[str, Any]]:
    return {int(status_code): {"model": schema_type} for status_code in sorted(status_codes)}


class OpenAPIDoc:
    def add_to_app(self, app: FastAPI) -> None:
        raise NotImplementedError

    def get_endpoint(self, app: FastAPI) -> Callable[[], Response]:
        raise NotImplementedError


class SwaggerUIHTML(OpenAPIDoc):
    def __init__(
        self,
        path: str = "/docs",
        dependencies: list[Depends] | None = None,
        openapi_url: str = "/openapi.json",
        **kwargs: Any,
    ):
        self.path = path
        self.dependencies = dependencies
        self.openapi_url = openapi_url
        self.kwargs = kwargs

    def add_to_app(self, app: FastAPI) -> None:
        app.get(
            self.path,
            response_class=HTMLResponse,
            dependencies=self.dependencies,
            include_in_schema=False,
        )(self.get_endpoint(app))

    def get_endpoint(self, app: FastAPI) -> Callable[[], HTMLResponse]:
        def endpoint():
            default_kwargs = {
                "openapi_url": app.root_path + self.openapi_url,
                "title": f"{app.title} - Swagger UI",
                "oauth2_redirect_url": (
                    app.swagger_ui_oauth2_redirect_url
                    and app.root_path + app.swagger_ui_oauth2_redirect_url
                ),
                "init_oauth": app.swagger_ui_init_oauth,
                "swagger_ui_parameters": app.swagger_ui_parameters,
            }
            return get_swagger_ui_html(**(default_kwargs | self.kwargs))

        return endpoint


class RedocHTML(OpenAPIDoc):
    def __init__(
        self,
        path: str = "/redoc",
        dependencies: list[Depends] | None = None,
        openapi_url: str = "/openapi.json",
        **kwargs: Any,
    ):
        self.path = path
        self.dependencies = dependencies
        self.openapi_url = openapi_url
        self.kwargs = kwargs

    def add_to_app(self, app: FastAPI) -> None:
        app.get(
            self.path,
            response_class=HTMLResponse,
            dependencies=self.dependencies,
            include_in_schema=False,
        )(self.get_endpoint(app))

    def get_endpoint(self, app: FastAPI) -> Callable[[], Response]:
        def endpoint():
            default_kwargs = {
                "openapi_url": app.root_path + self.openapi_url,
                "title": f"{app.title} - ReDoc",
            }
            return get_redoc_html(**(default_kwargs | self.kwargs))

        return endpoint


class OpenAPISchema(OpenAPIDoc):
    def __init__(self, path: str = "/openapi.json"):
        self.path = path

    def add_to_app(self, app: FastAPI) -> None:
        app.get(
            self.path,
            include_in_schema=False,
        )(self.get_endpoint(app))

    def get_endpoint(self, app: FastAPI, **kwargs: Any) -> Callable[[], dict[str, Any]]:
        def endpoint() -> dict[str, Any]:
            return app.openapi()

        return endpoint


def add_doc_routes(app: FastAPI, docs: list[OpenAPIDoc], cond: bool) -> None:
    if not cond:
        return

    for doc in docs:
        doc.add_to_app(app)
