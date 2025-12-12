from collections.abc import Callable
from typing import Self

import pendulum
from authlib.jose import jwt

from .. import utils


class JWTIssuer:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        issuer: str,
        token_id_generator: Callable[[], str],
        clock: type[pendulum.DateTime],
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.issuer = issuer
        self.token_id_generator = token_id_generator
        self.clock = clock

    @classmethod
    def default(cls, secret_key: str, issuer: str) -> Self:
        return cls(
            secret_key=secret_key,
            algorithm="HS256",
            issuer=issuer,
            token_id_generator=utils.uuid4_hex,
            clock=pendulum.DateTime,
        )

    def issue(self, sub: str, expires_in: int, **kwargs) -> str:
        iat = self.clock.utcnow()
        return jwt.encode(
            header={"typ": "JWT", "alg": self.algorithm},
            payload={
                "sub": sub,
                "iss": self.issuer,
                "jti": self.token_id_generator(),
                "iat": int(iat.timestamp()),
                "exp": int(iat.add(seconds=expires_in).timestamp()),
                **kwargs,
            },
            key=self.secret_key,
        ).decode()
