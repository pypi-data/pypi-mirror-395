from enum import Enum
from typing import TYPE_CHECKING, Any

from pydantic import Field

from trajectory.scorers.trajectory_scorer import TrajectoryScorer

if TYPE_CHECKING:
    from trajectory.data import Example, Trace


class ToolCallMode(str, Enum):
    ORDERING_MATCH = "ordering_match"
    EXACT_MATCH = "exact_match"


class ToolCallOrderScorer(TrajectoryScorer):
    mode: ToolCallMode = Field(
        default=ToolCallMode.ORDERING_MATCH,
        description="Scoring mode for tool call order",
    )

    def __init__(self, mode: str = "ordering_match", **kwargs):
        super().__init__(
            score_type="tool_call_order_trajectory",
            threshold=0.8,
            name="ToolCallOrderScorer",
            **kwargs,
        )
        self.mode = ToolCallMode(mode)

    def score_trajectory(self, trace: "Trace", example: "Example") -> dict[str, Any]:
        """Score tool call ordering against expected tools"""

        # Extract actual tool calls from trace
        actual_tool_calls = self._extract_tool_calls_from_trace(trace)

        # Get expected tools from example
        expected_tools = example.expected_tools or []

        # Score based on mode
        if self.mode == ToolCallMode.ORDERING_MATCH:
            score, details = self._score_ordering_match(
                actual_tool_calls, expected_tools
            )
        else:  # EXACT_MATCH
            score, details = self._score_exact_match(actual_tool_calls, expected_tools)

        return {
            "score": score,
            "passed": score >= self.threshold,
            "mode": self.mode.value,
            "actual_tool_calls": actual_tool_calls,
            "expected_tools": [
                {"tool_name": tool.tool_name, "parameters": tool.parameters}
                for tool in expected_tools
            ],
            "details": details,
        }

    def _extract_tool_calls_from_trace(self, trace: "Trace") -> list[dict[str, Any]]:
        """Extract tool calls from trace spans"""
        tool_calls = []

        # Use trace_spans instead of spans
        for span in trace.trace_spans:
            if span.span_type == "tool" and span.function:
                tool_calls.append(
                    {
                        "tool_name": span.function,
                        "parameters": span.inputs if span.inputs else {},
                    }
                )

        return tool_calls

    def _score_ordering_match(
        self, actual_tool_calls: list[dict], expected_tools: list
    ) -> tuple[float, str]:
        """Check if tool call ordering matches expected ordering"""
        if not expected_tools:
            return 1.0, "No expected tools specified"

        if len(actual_tool_calls) != len(expected_tools):
            return (
                0.0,
                f"Tool count mismatch: expected {len(expected_tools)}, got {len(actual_tool_calls)}",
            )

        # Check if tool names match in order
        for i, (actual, expected) in enumerate(zip(actual_tool_calls, expected_tools)):
            expected_tool_name = (
                expected.tool_name
                if hasattr(expected, "tool_name")
                else expected.get("tool_name")
            )
            if actual["tool_name"] != expected_tool_name:
                return (
                    0.0,
                    f"Tool order mismatch at position {i}: expected {expected_tool_name}, got {actual['tool_name']}",
                )

        return 1.0, "Tool call ordering matches expected order"

    def _score_exact_match(
        self, actual_tool_calls: list[dict], expected_tools: list
    ) -> tuple[float, str]:
        """Check if tool calls exactly match expected tools (including parameters)"""
        if not expected_tools:
            return 1.0, "No expected tools specified"

        if len(actual_tool_calls) != len(expected_tools):
            return (
                0.0,
                f"Tool count mismatch: expected {len(expected_tools)}, got {len(actual_tool_calls)}",
            )

        # Check exact match including parameters
        for i, (actual, expected) in enumerate(zip(actual_tool_calls, expected_tools)):
            # Handle both ToolTrajectoryType objects and dictionaries
            if hasattr(expected, "tool_name"):
                expected_tool_name = expected.tool_name
                expected_params = expected.parameters or {}
            else:
                expected_tool_name = expected.get("tool_name")
                expected_params = expected.get("parameters", {})

            if actual["tool_name"] != expected_tool_name:
                return (
                    0.0,
                    f"Tool name mismatch at position {i}: expected {expected_tool_name}, got {actual['tool_name']}",
                )

            # Check parameters match
            actual_params = actual.get("parameters", {})

            if expected_params != actual_params:
                return (
                    0.0,
                    f"Parameter mismatch at position {i}: expected {expected_params}, got {actual_params}",
                )

        return 1.0, "Tool calls exactly match expected tools and parameters"
