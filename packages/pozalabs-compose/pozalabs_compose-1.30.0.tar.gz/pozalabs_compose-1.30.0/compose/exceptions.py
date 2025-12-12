import enum
from typing import Any, ClassVar, Self, cast


class BaseError(Exception):
    default_message: ClassVar[str | None] = None

    def __init__(
        self,
        message: str | enum.Enum | None = None,
        detail: Any | None = None,
        invalid_params: list[dict[str, Any]] | None = None,
    ):
        if isinstance(message, enum.Enum):
            message = message.value
        super().__init__(message)

        if message is None and self.default_message is None:
            raise ValueError("`message` or `default_message` must not be None")

        self.message = str(message) if message is not None else self.default_message
        self.detail = detail
        self.invalid_params = invalid_params

    def __str__(self):
        return self.message

    @classmethod
    def with_default_message(cls, name: str, message: str) -> type[Self]:
        return cast(
            type[Self],
            type(name, (cls,), {"default_message": message}),
        )


AuthorizationError = BaseError.with_default_message("AuthorizationError", "Authorization failed")
NotAllowedError = BaseError.with_default_message("NotAllowedError", "Not allowed")
DoesNotExistError = BaseError.with_default_message("DoesNotExistError", "Resource not found")
DomainValidationError = BaseError.with_default_message("DomainValidationError", "Validation failed")
