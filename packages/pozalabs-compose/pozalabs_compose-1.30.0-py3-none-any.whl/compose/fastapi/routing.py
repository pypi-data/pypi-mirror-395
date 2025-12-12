import functools
from collections.abc import Callable
from typing import Any

from fastapi import APIRouter as _FastAPIRouter
from fastapi.routing import APIRoute

from ..dependency.wiring import Provider
from .wiring import auto_wired

_OVERRIDE_DEFAULTS = {"response_model_by_alias": False}
_OVERRIDE_METHODS = {
    "get",
    "post",
    "put",
    "delete",
    "options",
    "head",
    "patch",
    "trace",
    "api_route",
    "add_api_route",
}

APIRouter = _FastAPIRouter

for method_name in _OVERRIDE_METHODS:
    func = getattr(APIRouter, method_name)
    func.__kwdefaults__ = func.__kwdefaults__ | _OVERRIDE_DEFAULTS


@functools.lru_cache(1)
def create_auto_wired_route(provider: Provider) -> type[APIRoute]:
    """
    Provider를 사용하는 AutoWiredAPIRoute를 생성하는 팩토리 함수.
    클래스 변수 대신 클로저를 사용하여 해시 문제를 회피
    """

    class AutoWiredAPIRoute(APIRoute):
        def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any):
            super().__init__(
                path=path,
                endpoint=auto_wired(provider, with_injection=True)(endpoint),
                **kwargs,
            )

    return AutoWiredAPIRoute
