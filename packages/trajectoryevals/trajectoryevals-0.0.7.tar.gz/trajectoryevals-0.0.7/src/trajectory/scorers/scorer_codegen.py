import os
import re
import types

from openai import OpenAI

SYSTEM_PROMPT = """You are an expert code generator for trajectory scorers in the JudgEval framework.
You MUST output a single valid Python class that extends judgeval.scorers.trajectory_scorer.TrajectoryScorer.

BASE CLASS (TrajectoryScorer)
- Inherits from pydantic.BaseModel via BaseScorer. Therefore, field overrides MUST be typed in subclasses:
  - score_type: str
  - threshold: float
  - name: Optional[str] (or str)
- Helper methods available to simplify implementations:
  - iter_spans(trace)                -> yields spans chronologically
  - find_spans_by_type(trace, str)   -> list of spans of a given type (e.g., 'tool')
  - extract_final_output(trace)      -> last non-empty span output as string or None
  - extract_tool_calls(trace)        -> normalized tool calls: [{tool_name, parameters, span_id}]
  - result(score, passed=None, **k)  -> formatted dict with {score, passed, ...}

CONSTRAINTS
- Import the base class like:
  from trajectory.scorers.trajectory_scorer import TrajectoryScorer
- Define a single top-level class that extends TrajectoryScorer.
- Override fields with types:
  score_type: str = "..."
  threshold: float = 0.8
  name: str = "MyScorer"
- Implement:
  def score_trajectory(self, trace: Trace, example: Example) -> Dict[str, Any]
- Return dict including:
  - "score": float
  - "passed": bool
  - Optionally "breakdown", "details", "reasoning", etc.
- No network calls or external deps; deterministic scoring from trace/example only.
- Be robust to missing fields (None-safe).

REFERENCE EXAMPLE A (tool-ordering, resilient to param shape)
from trajectory.scorers.trajectory_scorer import TrajectoryScorer
from trajectory.data import Trace, Example
from typing import Dict, Any

class ToolCallOrderScorerExample(TrajectoryScorer):
    score_type: str = "tool_call_order"
    threshold: float = 0.8
    name: str = "ToolCallOrderScorerExample"

    def score_trajectory(self, trace: Trace, example: Example) -> Dict[str, Any]:
        actual = [t.get("tool_name") for t in self.extract_tool_calls(trace)]
        expected = [
            (et.tool_name if hasattr(et, "tool_name") else (et or {}).get("tool_name"))
            for et in (example.expected_tools or [])
        ]
        matches = sum(1 for a, e in zip(actual, expected) if a == e)
        denom = max(len(expected), 1)
        score = matches / denom
        return self.result(score, breakdown={"actual": actual, "expected": expected, "matches": matches, "denom": denom})

REFERENCE EXAMPLE B (deterministic rubric, simple weights)
from trajectory.scorers.trajectory_scorer import TrajectoryScorer
from trajectory.data import Trace, Example
from typing import Dict, Any, List

class SimpleRubricScorerExample(TrajectoryScorer):
    score_type: str = "simple_rubric"
    threshold: float = 0.7
    name: str = "SimpleRubricScorerExample"

    def score_trajectory(self, trace: Trace, example: Example) -> Dict[str, Any]:
        # Example rubric: reward if any tool was called; reward if final output exists
        tools = self.extract_tool_calls(trace)
        final = self.extract_final_output(trace)
        checks = [
            (1.0, len(tools) > 0),
            (1.0, bool(final)),
        ]
        total = sum(w for w, _ in checks)
        score = sum(w for w, ok in checks if ok) / (total or 1.0)
        return self.result(score, breakdown={"has_tools": len(tools) > 0, "has_output": bool(final)})

OUTPUT
- Only the class code body (no extra prose, no fences).
"""


class ScorerCodeGenerator:
    def __init__(self, llm_model: str = "gpt-4o-mini", api_key: str | None = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.llm_model = llm_model

    def _strip_fences(self, text: str) -> str:
        t = text.strip()
        if t.startswith("```"):
            t = re.sub(r"^```[a-zA-Z0-9_+-]*\n", "", t)
            if t.endswith("```"):
                t = t[:-3]
        return t.strip()

    def _ensure_typed_and_imports(self, code: str) -> str:
        # Enforce typed overrides required by Pydantic
        code = re.sub(r"\bscore_type\s*=\s*", "score_type: str = ", code)
        code = re.sub(r"\bthreshold\s*=\s*", "threshold: float = ", code)
        code = re.sub(r"\bname\s*=\s*", "name: str = ", code)
        # Normalize import + base class reference
        code = code.replace(
            "from trajectory.scorers import trajectory_scorer",
            "from trajectory.scorers.trajectory_scorer import TrajectoryScorer",
        )
        code = re.sub(
            r"class\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*trajectory_scorer\.TrajectoryScorer\s*\)",
            r"class \1(TrajectoryScorer)",
            code,
        )
        return code

    def generate_code(
        self, natural_language_spec: str, class_name: str | None = None
    ) -> str:
        user_prompt = f"""Specification:\n{natural_language_spec}\n\nIf a class name is not specified, infer a concise PascalCase name ending with 'Scorer'."""
        resp = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        code = resp.choices[0].message.content or ""
        code = self._strip_fences(code)
        code = self._ensure_typed_and_imports(code)
        if class_name:
            code = self._force_class_name(code, class_name)
        return code

    def _force_class_name(self, code: str, class_name: str) -> str:
        return re.sub(
            r"class\s+[A-Za-z_][A-Za-z0-9_]*\s*\(",
            f"class {class_name}(",
            code,
            count=1,
        )

    def save_code(self, code: str, out_path: str) -> None:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code)

    def compile_and_load(
        self,
        code: str,
        module_name: str = "generated_scorer",
        class_name: str | None = None,
    ):
        import inspect

        mod = types.ModuleType(module_name)
        ns = mod.__dict__
        exec(code, ns, ns)

        if class_name and class_name in ns and isinstance(ns[class_name], type):
            return ns[class_name]

        # Prefer a concrete subclass that defines score_trajectory itself (not the abstract base)
        from trajectory.scorers.trajectory_scorer import TrajectoryScorer

        candidates = []
        for v in ns.values():
            if (
                isinstance(v, type)
                and issubclass(v, TrajectoryScorer)
                and v is not TrajectoryScorer
            ):
                # method defined on this class (not just inherited abstract)
                if "score_trajectory" in v.__dict__ and callable(
                    v.__dict__["score_trajectory"]
                ):
                    candidates.append(v)
        if candidates:
            return candidates[0]

        # Fallback: any subclass that is not abstract
        for v in ns.values():
            if (
                isinstance(v, type)
                and issubclass(v, TrajectoryScorer)
                and v is not TrajectoryScorer
            ):
                if not inspect.isabstract(v):
                    return v

        raise ValueError("No concrete scorer class found in generated code.")
