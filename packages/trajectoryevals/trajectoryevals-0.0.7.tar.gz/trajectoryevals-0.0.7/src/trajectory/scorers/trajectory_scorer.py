from abc import abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from trajectory.scorers.base_scorer import BaseScorer

if TYPE_CHECKING:
    from trajectory.data import Example, Trace


class TrajectoryScorer(BaseScorer):
    """Base class for trajectory-level scorers"""

    @abstractmethod
    def score_trajectory(self, trace: "Trace", example: "Example") -> dict[str, Any]:
        """Score a complete trajectory/trace against an example"""

    # Helper methods for common scorer needs

    def iter_spans(self, trace: "Trace") -> Iterable[Any]:
        """
        Yield spans from a Trace object in chronological order.
        Works whether spans are on trace.trace_spans or trace.spans.
        """
        spans = []
        if hasattr(trace, "trace_spans") and isinstance(trace.trace_spans, list):
            spans = trace.trace_spans
        elif hasattr(trace, "spans") and isinstance(trace.spans, list):
            spans = trace.spans
        return sorted(spans, key=lambda s: getattr(s, "created_at", "") or "")

    def find_spans_by_type(self, trace: "Trace", span_type: str) -> list[Any]:
        """Return spans matching a given span_type (case-insensitive)."""
        out = []
        for s in self.iter_spans(trace):
            st = getattr(s, "span_type", None)
            if isinstance(st, str) and st.lower() == span_type.lower():
                out.append(s)
        return out

    def extract_final_output(self, trace: "Trace") -> str | None:
        """
        Return the last available span output as string, if any.
        """
        for s in reversed(list(self.iter_spans(trace))):
            out = getattr(s, "output", None)
            if out:
                try:
                    return str(out)
                except Exception:
                    return None
        return None

    def extract_tool_calls(self, trace: "Trace") -> list[dict[str, Any]]:
        """
        Return a normalized list of tool calls from tool spans:
        [{tool_name, parameters, span_id}]
        """
        tools = []
        for s in self.find_spans_by_type(trace, "tool"):
            tools.append(
                {
                    "tool_name": getattr(s, "function", None)
                    or getattr(s, "tool_name", None),
                    "parameters": getattr(s, "inputs", None) or {},
                    "span_id": getattr(s, "span_id", None),
                }
            )
        return tools

    def result(
        self, score: float, passed: bool | None = None, **extras
    ) -> dict[str, Any]:
        """
        Convenience to format scorer output.
        """
        if passed is None:
            passed = score >= (self.threshold or 0.0)
        base = {"score": float(score), "passed": bool(passed)}
        base.update(extras or {})
        return base
