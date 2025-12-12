from .. import container


class AuthorizationGrant(container.BaseModel):
    access_token: str
    refresh_token: str | None = None


class UserResource(container.BaseModel):
    email: str
    name: str
