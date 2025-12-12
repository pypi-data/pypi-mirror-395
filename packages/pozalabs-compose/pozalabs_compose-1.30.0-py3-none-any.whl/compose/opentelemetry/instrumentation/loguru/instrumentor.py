from __future__ import annotations

from collections.abc import Callable, Collection
from typing import TYPE_CHECKING, Any

import wrapt
from loguru import logger
from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap

ORIGINAL_PATCHER_ATTR = "_otel_original_patcher"
_instruments = tuple()

if TYPE_CHECKING:
    from loguru import Logger


def trace_injector(
    tracer_provider: trace.TracerProvider,
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def inject_trace(record: dict[str, Any]) -> dict[str, Any]:
        span = trace.get_current_span()
        ctx = span.get_span_context()
        is_valid_span = span != trace.INVALID_SPAN

        resource = getattr(tracer_provider, "resource", None)
        trace_record = {
            "otel_service_name": (
                resource.attributes.get("service.name", "") if resource is not None else ""
            ),
            "otel_trace_id": (
                trace.format_trace_id(ctx.trace_id)
                if is_valid_span
                else str(trace.INVALID_TRACE_ID)
            ),
            "otel_span_id": (
                trace.format_span_id(ctx.span_id) if is_valid_span else str(trace.INVALID_SPAN_ID)
            ),
            "otel_trace_sampled": ctx.trace_flags.sampled if is_valid_span else False,
        }

        extra = record.get("extra", {})
        return {"extra": extra | trace_record}

    return inject_trace


def create_record_patcher(
    inject_trace: Callable[[dict[str, Any]], dict[str, Any]],
) -> Callable[[dict[str, Any]], None]:
    def patcher(record: dict[str, Any]) -> None:
        record |= inject_trace(record)

    return patcher


def create_configure_wrapper(
    inject_trace: Callable[[dict[str, Any]], dict[str, Any]],
) -> Callable[..., list[int]]:
    def wrapped_configure(
        func: Callable[..., list[int]],
        instance: Logger,
        *args,
        **kwargs,
    ) -> list[int]:
        """https://github.com/DataDog/dd-trace-py/blob/main/ddtrace/contrib/loguru/patch.py"""

        original_patcher = kwargs.get("patcher")
        setattr(instance, ORIGINAL_PATCHER_ATTR, original_patcher)

        if original_patcher is None:
            return func(*args, **kwargs)

        def wrapped_patcher(record: dict[str, Any]) -> None:
            original_patcher(record)
            record |= inject_trace(record)

        kwargs["patcher"] = wrapped_patcher
        return func(*args, **kwargs)

    return wrapped_configure


def default_record_patcher(_: dict[str, Any]) -> None:
    return None


class LoguruInstrumentor(BaseInstrumentor):
    """

    Reference:
        https://github.com/DataDog/dd-trace-py/tree/main/ddtrace/contrib/loguru
        https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-logging
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs) -> None:
        tracer_provider = kwargs.get("tracer_provider", trace.get_tracer_provider())

        inject_trace = trace_injector(tracer_provider)
        logger.configure(patcher=create_record_patcher(inject_trace))
        wrapt.wrap_function_wrapper(
            logger,
            "configure",
            create_configure_wrapper(inject_trace),
        )

    def _uninstrument(self, **kwargs) -> None:
        original_patcher = getattr(logger, ORIGINAL_PATCHER_ATTR, None)
        has_original_patcher = original_patcher is not None
        if has_original_patcher:
            logger.configure(patcher=original_patcher)

        unwrap(logger, "configure")
        if not has_original_patcher:
            logger.configure(patcher=default_record_patcher)
