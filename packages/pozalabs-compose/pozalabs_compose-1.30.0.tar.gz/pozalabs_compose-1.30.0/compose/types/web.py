import mimetypes
import os
import urllib.parse
from typing import ClassVar, Self, TypedDict

from .primitive import Str


class ContentDisposition(str):
    @classmethod
    def attachment(cls, filename: str) -> Self:
        return cls(f"attachment; filename*=UTF-8''{urllib.parse.quote(filename)}")


class MimeTypeInfo(TypedDict):
    type: str
    ext: str


class MimeType(Str):
    """MIME Type을 표현하는 타입

    mimetypes 패키지에서 제공하지 않는 타입을 사용하려면
    어플리케이션 진입점에서 `MimeType.register([MimeTypeInfo(type="...", ext="..."), ...])`를 호출한 뒤
    `MimeType.guess(...)` 호출
    """

    default_type: ClassVar[str] = "binary/octet-stream"
    _known_types: ClassVar[list[MimeTypeInfo]] = [
        MimeTypeInfo(type="audio/midi", ext=".mid"),
        MimeTypeInfo(type="audio/midi", ext=".midi"),
    ]
    _is_known_mime_types_registered: ClassVar[bool] = False

    @classmethod
    def register_known_types(cls) -> None:
        if cls._is_known_mime_types_registered:
            return

        for t in cls._known_types:
            mimetypes.add_type(**t)

        cls._is_known_mime_types_registered = True

    @classmethod
    def register(cls, *types: *tuple[MimeTypeInfo, ...]) -> None:
        for t in [*types]:
            mimetypes.add_type(**t)

    @classmethod
    def guess(cls, url: str | os.PathLike[str]) -> Self:
        mime_type, _ = mimetypes.guess_type(url)
        return cls(mime_type or cls.default_type)

    @classmethod
    def default(cls) -> Self:
        return cls(cls.default_type)


MimeType.register_known_types()
