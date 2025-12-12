"""
Custom OpenTelemetry exporter for Trajectory API.

This exporter sends spans to the Trajectory API using the existing format.
The BatchSpanProcessor handles all batching, threading, and retry logic.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

from trajectory.common.api.api import TrajectoryApiClient
from trajectory.common.logger import trajectory_logger
from trajectory.common.tracer.span_transformer import SpanTransformer


class TrajectoryAPISpanExporter(SpanExporter):
    """
    Custom OpenTelemetry exporter that sends spans to Trajectory API.

    This exporter is used by BatchSpanProcessor which handles all the
    batching, threading, and retry logic for us.
    """

    def __init__(
        self,
        trajectory_api_key: str,
        organization_id: str,
    ):
        self.api_client = TrajectoryApiClient(trajectory_api_key, organization_id)

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        """
        Export spans to Trajectory API.

        This method is called by BatchSpanProcessor with a batch of spans.
        We send them synchronously since BatchSpanProcessor handles threading.
        """
        if not spans:
            return SpanExportResult.SUCCESS

        try:
            spans_data = []
            eval_runs_data = []

            for span in spans:
                span_data = self._convert_span_to_trajectory_format(span)

                if span.attributes and span.attributes.get("trajectory.evaluation_run"):
                    eval_runs_data.append(span_data)
                else:
                    spans_data.append(span_data)

            if spans_data:
                self._send_spans_batch(spans_data)

            if eval_runs_data:
                self._send_evaluation_runs_batch(eval_runs_data)

            return SpanExportResult.SUCCESS

        except Exception as e:
            trajectory_logger.error(f"Error in TrajectoryAPISpanExporter.export: {e}")
            return SpanExportResult.FAILURE

    def _convert_span_to_trajectory_format(self, span: ReadableSpan) -> dict[str, Any]:
        """Convert OpenTelemetry span to existing Trajectory API format."""
        if span.attributes and span.attributes.get("trajectory.evaluation_run"):
            return SpanTransformer.otel_span_to_evaluation_run_format(span)
        else:
            return SpanTransformer.otel_span_to_trajectory_format(span)

    def _send_spans_batch(self, spans: list[dict[str, Any]]):
        """Send a batch of spans to the spans endpoint."""
        spans_data = [span["data"] for span in spans]
        self.api_client.send_spans_batch(spans_data)

    def _send_evaluation_runs_batch(self, eval_runs: list[dict[str, Any]]):
        """Send a batch of evaluation runs to the evaluation runs endpoint."""
        evaluation_entries = []
        for eval_run in eval_runs:
            eval_data = eval_run["data"]
            entry = {
                "evaluation_run": {
                    key: value
                    for key, value in eval_data.items()
                    if key not in ["associated_span_id", "span_data", "queued_at"]
                },
                "associated_span": {
                    "span_id": eval_data.get("associated_span_id"),
                    "span_data": eval_data.get("span_data"),
                },
                "queued_at": eval_data.get("queued_at"),
            }
            evaluation_entries.append(entry)

        self.api_client.send_evaluation_runs_batch(evaluation_entries)

    def shutdown(self, timeout_millis: int = 30000) -> None:
        """Shutdown the exporter."""

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Force flush any pending requests."""
        return True
