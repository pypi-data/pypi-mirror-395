import json
import os
from typing import TYPE_CHECKING, Any

from openai import OpenAI
from pydantic import ConfigDict, Field

from trajectory.scorers.trajectory_scorer import TrajectoryScorer

from .rubric_generator import RubricGenerator

if TYPE_CHECKING:
    from trajectory.data import Example, Trace


class RubricBasedScorer(TrajectoryScorer):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    llm_model: str = Field(
        default="gpt-4o-mini", description="LLM model to use for scoring"
    )
    client: OpenAI | None = Field(
        default=None, description="OpenAI client", exclude=True
    )
    rubric_generator: RubricGenerator | None = Field(
        default=None, description="Rubric generator", exclude=True
    )

    def __init__(self, llm_model: str = "gpt-4o-mini", **kwargs):
        super().__init__(
            score_type="rubric_based_trajectory",
            threshold=0.7,
            name="RubricBasedScorer",
            **kwargs,
        )
        self.llm_model = llm_model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.rubric_generator = RubricGenerator(llm_model)

    def score_trajectory(self, trace: "Trace", example: "Example") -> dict[str, Any]:
        """Score trajectory using generated rubrics"""

        # Extract data from trace and example
        actual_output = self._extract_final_output(trace)
        question = example.input.get("prompt", "")
        expected_answer = example.expected_output

        # Step 1: Generate rubrics
        rubrics = self.rubric_generator.generate_rubrics(question, expected_answer)

        # Step 2: Score using rubrics
        score_result = self._score_with_rubrics(
            question, expected_answer, actual_output, rubrics
        )

        return {
            "score": score_result["score"],
            "passed": score_result["passed"],
            "rubrics": rubrics,
            "detailed_scores": score_result["detailed_scores"],
            "reasoning": score_result["reasoning"],
            "question": question,
            "expected_answer": expected_answer,
            "actual_output": actual_output,
        }

    def _score_with_rubrics(
        self,
        question: str,
        expected_answer: str,
        actual_output: str,
        rubrics: list[dict],
    ) -> dict[str, Any]:
        """Score actual output against generated rubrics"""

        system_prompt = """You are an expert evaluator. Evaluate the response against the provided rubrics and assign scores. Be fair and consistent in your evaluation."""

        user_prompt = f"""Question: {question}
Expected Answer: {expected_answer}
Actual Output: {actual_output}

Rubrics:
{json.dumps(rubrics, indent=2)}

Evaluate each rubric and provide:
1. Individual scores for each rubric (0-5 scale, where 5 is perfect)
2. Overall weighted score
3. Brief reasoning for your scores

Return as JSON with keys: detailed_scores, overall_score, reasoning

Example format:
{{
  "detailed_scores": {{
    "Relevance": 4,
    "Accuracy": 3,
    "Clarity": 5
  }},
  "overall_score": 4.0,
  "reasoning": "The response addresses the question well but could be more accurate in some details."
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
            )

            content = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]

            result = json.loads(content)

            # Calculate weighted score
            weighted_score = self._calculate_weighted_score(
                result["detailed_scores"], rubrics
            )

            return {
                "score": weighted_score,
                "passed": weighted_score >= self.threshold,
                "detailed_scores": result["detailed_scores"],
                "reasoning": result["reasoning"],
            }

        except Exception as e:
            print(f"Error scoring with rubrics: {e}")
            # Return default scoring if evaluation fails
            return {
                "score": 0.5,
                "passed": False,
                "detailed_scores": {},
                "reasoning": f"Error in evaluation: {e!s}",
            }

    def _calculate_weighted_score(
        self, detailed_scores: dict, rubrics: list[dict]
    ) -> float:
        """Calculate weighted score based on rubric weights"""
        total_weight = 0
        weighted_sum = 0

        for rubric in rubrics:
            weight = abs(rubric["weight"])
            score = detailed_scores.get(rubric["title"], 0)

            if rubric["weight"] < 0:  # Pitfall criteria
                score = 5 - score  # Invert score for pitfalls

            weighted_sum += score * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0

    def _extract_final_output(self, trace: "Trace") -> str:
        """Extract the final output from the trace"""
        print(f"🔍 Extracting output from trace: {type(trace)}")
        print(f"🔍 Trace attributes: {dir(trace)}")

        # Handle case where trace might be a string or dict
        if isinstance(trace, str):
            print(f" Trace is a string: {trace}")
            return trace

        if isinstance(trace, dict):
            print(f" Trace is a dict: {trace}")
            # Try to extract output from dict
            if "trace_spans" in trace:
                for span in reversed(trace["trace_spans"]):
                    if span.get("output"):
                        return str(span["output"])
            return "No output found in trace dict"

        # Handle Trace object
        if hasattr(trace, "trace_spans") and trace.trace_spans:
            print(f" Found trace_spans: {len(trace.trace_spans)}")
            for span in reversed(trace.trace_spans):
                if hasattr(span, "output") and span.output:
                    return str(span.output)
        elif hasattr(trace, "spans") and trace.spans:
            print(f"🔍 Found spans: {len(trace.spans)}")
            for span in reversed(trace.spans):
                if hasattr(span, "output") and span.output:
                    return str(span.output)

        print(" No output found in trace")
        return "No output found in trace"
