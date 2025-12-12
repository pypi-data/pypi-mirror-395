import os
from typing import Any

from pydantic import Field

from compose.container import BaseModel


class GunicornSettings(BaseModel):
    wsgi_app: str
    bind: str = "0.0.0.0:80"
    workers: int = Field(default_factory=lambda: os.cpu_count() + 1)
    worker_class: str = "uvicorn.UvicornWorker"
    threads: int = 2
    timeout: int = 120
    max_requests: int | None = None
    max_requests_jitter: int | None = None


def export_settings(
    globals_: dict[str, Any],
    settings: GunicornSettings,
    **kwargs,
) -> None:
    globals_ |= settings.model_dump(exclude_none=True) | kwargs
