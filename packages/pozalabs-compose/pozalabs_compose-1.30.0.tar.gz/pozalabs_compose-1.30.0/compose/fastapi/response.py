import http
from collections.abc import Mapping
from typing import Any, Self

from fastapi import Response
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from starlette.responses import ContentStream

from compose.types import ContentDisposition


class NoContentResponse(Response):
    def __init__(
        self,
        content: Any = None,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(
            content=content,
            headers=headers,
            media_type=media_type,
            status_code=http.HTTPStatus.NO_CONTENT,
            background=background,
        )


class ZipStreamingResponse(StreamingResponse):
    default_media_type = "application/zip"

    @classmethod
    def with_filename(
        cls,
        content: ContentStream,
        filename: str,
        background: BackgroundTask | None = None,
    ) -> Self:
        return cls(
            content=content,
            media_type=cls.default_media_type,
            headers={"Content-Disposition": ContentDisposition.attachment(filename)},
            background=background,
        )
