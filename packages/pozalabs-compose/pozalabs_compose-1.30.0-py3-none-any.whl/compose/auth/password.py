from typing import Self

from compose.types import Str

try:
    import bcrypt
except ImportError:
    raise ImportError("bcrypt is required for password hashing")


class HashedPassword(Str):
    @classmethod
    def hash(cls, password: str) -> Self:
        return cls(bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt()).decode())

    def verify(self, password: str) -> bool:
        return bcrypt.checkpw(password=password.encode(), hashed_password=self.encode())
