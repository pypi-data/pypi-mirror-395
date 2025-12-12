from __future__ import annotations

import dataclasses
import enum
import logging
import sys
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Protocol, Self, Unpack

from typing_extensions import deprecated

try:
    from loguru import logger
except ImportError:
    raise ImportError(
        "The `loguru` extra must be installed to use the `compose.logging` module. "
        "Install `compose` with `loguru` extra (`compose[loguru]`)"
    )

if TYPE_CHECKING:
    from loguru import BasicHandlerConfig, Logger, Record


class InterceptHandler(logging.Handler):
    """https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    def filter(self, record: logging.LogRecord) -> bool:
        return "/health-check" not in record.getMessage()


def intercept_logging(intercept_handler: InterceptHandler, log_level: int) -> None:
    """Python 내장 logging 모듈을 loguru로 대체합니다. (해당 함수를 호출하려면 `loguru`를 설치해야 합니다.)"""
    logging.basicConfig(handlers=[intercept_handler], level=log_level, force=True)


def intercept(
    intercept_handler: InterceptHandler,
    log_names: Iterable[str] = (
        "gunicorn.error",
        "gunicorn.access",
        "uvicorn.error",
        "uvicorn.access",
    ),
) -> None:
    intercept_logging(intercept_handler=intercept_handler, log_level=logging.INFO)
    for name in log_names:
        logging.getLogger(name).handlers = [intercept_handler]


def get_default_logging_config(serialize_log: bool) -> dict[str, Any]:
    non_serialized_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{level: <8}</level> | <level>{message}</level>"
    )
    return {
        "sink": sys.stdout,
        "diagnose": False,
        "format": "{message}" if serialize_log else non_serialized_format,
        "serialize": serialize_log,
    }


@deprecated("'get_default_logger' is deprecated. Use 'create_logger' instead")
def get_default_logger(
    log_level: int,
    serialize_log: bool,
    **config: Unpack[BasicHandlerConfig],
) -> Logger:
    intercept_handler = InterceptHandler()
    logging.basicConfig(handlers=[intercept_handler], level=log_level, force=True)
    intercept(intercept_handler=intercept_handler)
    logger.configure(handlers=[get_default_logging_config(serialize_log) | config])
    return logger


class LogFilterOp(Protocol):
    def __call__(self, record: Record) -> bool: ...


class LogFilterNotContains:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def __call__(self, record: Record) -> bool:
        return self.pattern not in record["message"]


class LogFilter:
    def __init__(self, *ops: *tuple[LogFilterOp, ...]):
        self.ops = list(ops)

    def __call__(self, record: Record) -> bool:
        return all(op(record) for op in self.ops)


class LogFormat(enum.StrEnum):
    SERIALIZED = "{message}"
    NON_SERIALIZED = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{level: <8}</level> | <level>{message}</level>"
    )


@dataclasses.dataclass
class LogDisplayConfig:
    format: str
    colorize: bool
    serialize: bool

    @classmethod
    def serialized(cls) -> Self:
        return cls(
            format=LogFormat.SERIALIZED,
            colorize=False,
            serialize=True,
        )

    @classmethod
    def non_serialized(cls) -> Self:
        return cls(
            format=LogFormat.NON_SERIALIZED,
            colorize=True,
            serialize=False,
        )


def create_logger(level: int = logging.INFO, **config: Unpack[BasicHandlerConfig]) -> Logger:
    intercept_handler = InterceptHandler()
    logging.basicConfig(handlers=[intercept_handler], level=level, force=True)
    intercept(intercept_handler=intercept_handler)

    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "diagnose": False,
                "filter": LogFilter(
                    LogFilterNotContains("/health-check"),
                    LogFilterNotContains("/metrics"),
                ),
                **dataclasses.asdict(LogDisplayConfig.non_serialized()),
            }
            | config
        ]
    )

    return logger
