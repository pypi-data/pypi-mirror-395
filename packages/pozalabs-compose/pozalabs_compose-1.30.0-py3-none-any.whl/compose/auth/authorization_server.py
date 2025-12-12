from collections.abc import Callable
from typing import ClassVar

from authlib.integrations.httpx_client import AsyncOAuth2Client

from . import vo


class AuthorizationServer:
    headers: ClassVar[dict[str, str]] = {"Content-Type": "application/x-www-form-urlencoded"}
    token_path: ClassVar[str] = ""

    def __init__(self, base_url: str, auth_client_factory: Callable[..., AsyncOAuth2Client]):
        self.base_url = base_url
        self.auth_client_factory = auth_client_factory

    async def grant_authorization(self, redirect_uri: str, code: str) -> vo.AuthorizationGrant:
        async with self.auth_client_factory() as client:
            response = await client.fetch_token(
                url=f"{self.base_url}{self.token_path}",
                headers=self.headers,
                grant_type="authorization_code",
                client_id=client.client_id,
                client_secret=client.client_secret,
                redirect_uri=redirect_uri,
                code=code,
            )
        return vo.AuthorizationGrant.model_validate(response)

    async def renew_token(self, token: str) -> vo.AuthorizationGrant:
        async with self.auth_client_factory() as client:
            response = await client.fetch_token(
                url=self.token_path,
                headers=self.headers,
                grant_type="refresh_token",
                client_id=client.client_id,
                client_secret=client.client_secret,
                refresh_token=token,
            )
        return vo.AuthorizationGrant.model_validate(response)

    async def create_authorization_url(self, redirect_uri: str) -> str:
        raise NotImplementedError

    async def revoke_token(self, token: str) -> None:
        raise NotImplementedError
