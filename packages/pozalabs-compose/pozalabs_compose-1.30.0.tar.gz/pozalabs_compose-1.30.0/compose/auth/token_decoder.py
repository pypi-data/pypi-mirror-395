import pendulum
from authlib.jose import JWTClaims, errors, jwt

from .. import exceptions


class JWTDecoder:
    def __init__(self, secret_key: str, clock: type[pendulum.DateTime]):
        self.secret_key = secret_key
        self.clock = clock

    def decode(self, token: str) -> JWTClaims:
        try:
            decoded = jwt.decode(token.encode(), key=self.secret_key)
        except (errors.DecodeError, errors.BadSignatureError):
            raise exceptions.AuthorizationError("Invalid token")

        try:
            decoded.validate(now=int(self.clock.utcnow().timestamp()))
        except (errors.ExpiredTokenError, errors.InvalidClaimError):
            raise exceptions.AuthorizationError("Expired or incorrect format")

        return decoded
