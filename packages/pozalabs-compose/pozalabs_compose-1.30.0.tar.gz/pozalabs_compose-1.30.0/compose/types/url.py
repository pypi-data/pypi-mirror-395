from __future__ import annotations

import urllib.parse
from typing import Any, ClassVar, Self, cast

from .primitive import Str


class S3ContentUrl(Str):
    base_url: ClassVar[str]

    def __new__(cls, v: Any):
        if getattr(cls, "base_url", None) is None:
            raise ValueError("`base_url` must be set")

        v = urllib.parse.unquote(str(v).strip("/"))
        if v.startswith(cls.base_url):
            v = v[len(cls.base_url) :].lstrip("/")

        quoted_parts = [urllib.parse.quote(part, safe="~()*!.'") for part in v.split("/")]
        url = f"{cls.base_url}/{'/'.join(quoted_parts)}"
        return super().__new__(cls, url)

    @classmethod
    def with_base_url(cls, base_url: str) -> type[S3ContentUrl]:
        return cast(
            type[Self],
            type(
                cls.__name__,
                (cls,),
                {"base_url": base_url},
            ),
        )
