"""
Workday tool validation scorer.

Validates that expected Workday tools were called with correct parameters in a trace.
"""

from typing import Any

from trajectory.scorers.trajectory_scorer import TrajectoryScorer


class WorkdayToolScorer(TrajectoryScorer):
    """
    Scorer that validates Workday tool calls against expected tools.

    Checks that:
    1. Expected tools were called
    2. Tool parameters match expected parameters
    """

    score_type: str = "workday_tool_validation"
    threshold: float = 1.0  # All expected tools must be called correctly
    name: str = "WorkdayToolScorer"

    def score_trajectory(
        self,
        trace: Any,
        example: Any = None,
        expected_tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Score a trace by validating tool calls against expected tools.

        Args:
            trace: Trace object or dict with trace data
            example: Example object (optional, not used here)
            expected_tools: List of expected tool calls with format:
                [{"tool_name": "wd_get_worker", "parameters": {"worker_id": "123"}}]

        Returns:
            dict with score, passed, details, etc.
        """
        # Handle both Trace objects and dicts
        if isinstance(trace, dict):
            trace_spans = trace.get("trace_spans", [])
        else:
            trace_spans = getattr(trace, "trace_spans", []) or getattr(
                trace, "spans", []
            )

        # Extract actual tool calls from trace
        actual_tools = []
        for span in trace_spans:
            span_dict = (
                span
                if isinstance(span, dict)
                else span.__dict__
                if hasattr(span, "__dict__")
                else {}
            )
            span_type = span_dict.get("span_type") or getattr(span, "span_type", None)
            if span_type == "tool":
                function_name = span_dict.get("function") or getattr(
                    span, "function", None
                )
                inputs = span_dict.get("inputs") or getattr(span, "inputs", {}) or {}
                if function_name:
                    actual_tools.append(
                        {
                            "tool_name": function_name,
                            "parameters": inputs if isinstance(inputs, dict) else {},
                        }
                    )

        # Get expected tools from args or example
        if expected_tools is None:
            if example and hasattr(example, "expected_tools"):
                expected_tools = example.expected_tools
            elif isinstance(example, dict):
                expected_tools = example.get("expected_tools")
            else:
                expected_tools = []

        if not expected_tools:
            return self.result(
                1.0,
                passed=True,
                details="No expected tools specified",
                actual_tools=actual_tools,
                expected_tools=[],
            )

        # Validate each expected tool
        matches = []
        mismatches = []

        for expected in expected_tools:
            expected_tool_name = (
                expected.get("tool_name")
                if isinstance(expected, dict)
                else getattr(expected, "tool_name", None)
            )
            expected_params = (
                expected.get("parameters")
                if isinstance(expected, dict)
                else getattr(expected, "parameters", {})
            )

            # Find matching tool call
            found = False
            for actual in actual_tools:
                if actual["tool_name"] == expected_tool_name:
                    # Check if parameters match
                    actual_params = actual.get("parameters", {})
                    param_match = True
                    param_details = {}

                    for key, expected_value in expected_params.items():
                        actual_value = actual_params.get(key)
                        if actual_value != expected_value:
                            param_match = False
                            param_details[key] = {
                                "expected": expected_value,
                                "actual": actual_value,
                            }

                    if param_match:
                        matches.append(
                            {
                                "tool_name": expected_tool_name,
                                "parameters": actual_params,
                                "status": "matched",
                            }
                        )
                        found = True
                        break
                    else:
                        mismatches.append(
                            {
                                "tool_name": expected_tool_name,
                                "parameters": param_details,
                                "status": "parameter_mismatch",
                            }
                        )
                        found = True
                        break

            if not found:
                mismatches.append(
                    {
                        "tool_name": expected_tool_name,
                        "parameters": expected_params,
                        "status": "not_called",
                    }
                )

        # Calculate score: 1.0 if all expected tools matched, 0.0 otherwise
        score = 1.0 if len(mismatches) == 0 else 0.0

        details = {
            "matches": matches,
            "mismatches": mismatches,
            "total_expected": len(expected_tools),
            "total_matched": len(matches),
            "total_mismatched": len(mismatches),
        }

        return self.result(
            score,
            passed=score >= self.threshold,
            details=details,
            actual_tools=actual_tools,
            expected_tools=expected_tools,
        )


def validate_workday_tools(
    trace_data: dict[str, Any],
    args: dict[str, Any] | None = None,
    ctx: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Convenience function for backward compatibility with old scorer interface.

    This function wraps WorkdayToolScorer to match the old function-based scorer API.

    Args:
        trace_data: Trace data as dict
        args: Scorer arguments, should contain 'expected_tools' key
        ctx: Context dict (evaluation_id, project_name, etc.)

    Returns:
        dict with score, passed, details, etc.
    """
    scorer = WorkdayToolScorer()
    expected_tools = (args or {}).get("expected_tools", [])

    # Convert trace_data to a format the scorer can handle
    result = scorer.score_trajectory(
        trace=trace_data, example=None, expected_tools=expected_tools
    )

    # Ensure score is an integer for backward compatibility
    if "score" in result:
        score = result["score"]
        if isinstance(score, bool):
            result["score"] = int(score)
        elif isinstance(score, (int, float)):
            result["score"] = int(score)

    return result
