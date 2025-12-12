from collections.abc import Generator
from typing import Self

import httpx


class HeaderAuth(httpx.Auth):
    def __init__(self, secrets: dict[str, str]) -> None:
        self.secrets = secrets

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        for key, value in self.secrets.items():
            request.headers[key] = value
        yield request

    @classmethod
    def single(cls, key: str, header_name: str = "x-api-key") -> Self:
        return cls({header_name: key})
