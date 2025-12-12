"""
Custom OpenTelemetry span processor for Trajectory API.

This processor uses BatchSpanProcessor to handle batching and export
of TraceSpan objects converted to OpenTelemetry format.
"""

from __future__ import annotations

import threading
from typing import Any

from opentelemetry.context import Context
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanProcessor
from opentelemetry.trace import Span, SpanContext, Status, StatusCode, TraceFlags
from opentelemetry.trace.span import INVALID_SPAN_CONTEXT, TraceState
from opentelemetry.util.types import Attributes

from trajectory.common.logger import trajectory_logger
from trajectory.common.tracer.otel_exporter import TrajectoryAPISpanExporter
from trajectory.common.tracer.span_processor import SpanProcessorBase
from trajectory.common.tracer.span_transformer import SpanTransformer
from trajectory.data import TraceSpan
from trajectory.evaluation_run import EvaluationRun


class SimpleReadableSpan(ReadableSpan):
    """Simple ReadableSpan implementation that wraps TraceSpan data."""

    def __init__(self, trace_span: TraceSpan, span_state: str = "completed"):
        self._name = trace_span.function
        self._span_id = trace_span.span_id
        self._trace_id = trace_span.trace_id

        self._start_time = (
            int(trace_span.created_at * 1_000_000_000)
            if trace_span.created_at
            else None
        )
        self._end_time: int | None = None

        if (
            span_state == "completed"
            and trace_span.duration is not None
            and self._start_time is not None
        ):
            self._end_time = self._start_time + int(trace_span.duration * 1_000_000_000)

        self._status = (
            Status(StatusCode.ERROR) if trace_span.error else Status(StatusCode.OK)
        )

        self._attributes = SpanTransformer.trace_span_to_otel_attributes(
            trace_span, span_state
        )

        try:
            trace_id_int = (
                int(trace_span.trace_id.replace("-", ""), 16)
                if trace_span.trace_id
                else 0
            )
            span_id_int = (
                int(trace_span.span_id.replace("-", ""), 16)
                if trace_span.span_id
                else 0
            )

            self._context = SpanContext(
                trace_id=trace_id_int,
                span_id=span_id_int,
                is_remote=False,
                trace_flags=TraceFlags(0x01),
                trace_state=TraceState(),
            )
        except (ValueError, TypeError) as e:
            trajectory_logger.warning(f"Failed to create proper SpanContext: {e}")
            self._context = INVALID_SPAN_CONTEXT

        self._parent: SpanContext | None = None
        self._events: list[Any] = []
        self._links: list[Any] = []
        self._resource: Any | None = None
        self._instrumentation_info: Any | None = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def context(self) -> SpanContext:
        return self._context

    @property
    def parent(self) -> SpanContext | None:
        return self._parent

    @property
    def start_time(self) -> int | None:
        return self._start_time

    @property
    def end_time(self) -> int | None:
        return self._end_time

    @property
    def status(self) -> Status:
        return self._status

    @property
    def attributes(self) -> Attributes | None:
        return self._attributes

    @property
    def events(self):
        return self._events

    @property
    def links(self):
        return self._links

    @property
    def resource(self) -> Any | None:
        return self._resource

    @property
    def instrumentation_info(self) -> Any | None:
        return self._instrumentation_info


class TrajectorySpanProcessor(SpanProcessor, SpanProcessorBase):
    """
    Span processor that converts TraceSpan objects to OpenTelemetry format
    and uses BatchSpanProcessor for export.
    """

    def __init__(
        self,
        trajectory_api_key: str,
        organization_id: str,
        batch_size: int = 50,
        flush_interval: float = 1.0,
        max_queue_size: int = 2048,
        export_timeout: int = 30000,
    ):
        self.trajectory_api_key = trajectory_api_key
        self.organization_id = organization_id

        self._span_cache: dict[str, TraceSpan] = {}
        self._span_states: dict[str, str] = {}
        self._cache_lock = threading.RLock()

        self.batch_processor = BatchSpanProcessor(
            TrajectoryAPISpanExporter(
                trajectory_api_key=trajectory_api_key,
                organization_id=organization_id,
            ),
            max_queue_size=max_queue_size,
            schedule_delay_millis=int(flush_interval * 1000),
            max_export_batch_size=batch_size,
            export_timeout_millis=export_timeout,
        )

    def on_start(self, span: Span, parent_context: Context | None = None) -> None:
        self.batch_processor.on_start(span, parent_context)

    def on_end(self, span: ReadableSpan) -> None:
        self.batch_processor.on_end(span)

    def queue_span_update(self, span: TraceSpan, span_state: str = "input") -> None:
        if span_state == "completed":
            span.set_update_id_to_ending_number()
        else:
            span.increment_update_id()

        with self._cache_lock:
            span_id = span.span_id

            self._span_cache[span_id] = span
            self._span_states[span_id] = span_state

            self._send_span_update(span, span_state)

            if span_state == "completed" or span_state == "error":
                self._span_cache.pop(span_id, None)
                self._span_states.pop(span_id, None)

    def _send_span_update(self, span: TraceSpan, span_state: str) -> None:
        readable_span = SimpleReadableSpan(span, span_state)
        self.batch_processor.on_end(readable_span)

    def flush_pending_spans(self) -> None:
        with self._cache_lock:
            if not self._span_cache:
                return

            for span_id, span in self._span_cache.items():
                span_state = self._span_states.get(span_id, "input")
                self._send_span_update(span, span_state)

    def queue_evaluation_run(
        self, evaluation_run: EvaluationRun, span_id: str, span_data: TraceSpan
    ) -> None:
        attributes = SpanTransformer.evaluation_run_to_otel_attributes(
            evaluation_run, span_id, span_data
        )

        readable_span = SimpleReadableSpan(span_data, "evaluation_run")
        readable_span._attributes.update(attributes)

        self.batch_processor.on_end(readable_span)

    def shutdown(self) -> None:
        try:
            self.flush_pending_spans()
        except Exception as e:
            trajectory_logger.warning(
                f"Error flushing pending spans during shutdown: {e}"
            )

        self.batch_processor.shutdown()

        with self._cache_lock:
            self._span_cache.clear()
            self._span_states.clear()

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        try:
            self.flush_pending_spans()
        except Exception as e:
            trajectory_logger.warning(f"Error flushing pending spans: {e}")

        return self.batch_processor.force_flush(timeout_millis)
