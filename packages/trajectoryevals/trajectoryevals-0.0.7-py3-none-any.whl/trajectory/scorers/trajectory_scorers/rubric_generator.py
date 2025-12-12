import json
import os
from typing import Any

from openai import OpenAI


class RubricGenerator:
    def __init__(self, llm_model: str = "gpt-4o-mini"):
        self.llm_model = llm_model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_rubrics(
        self, question: str, reference_answer: str
    ) -> list[dict[str, Any]]:
        """Generate rubrics based on question and reference answer"""

        system_prompt = """You are an expert rubric writer. Your job is to generate a self-contained set of evaluation criteria ("rubrics") for judging how good a response is to a given question. Rubrics can cover aspects of a response such as, but not limited to, factual correctness, ideal-response characteristics, style, completeness, helpfulness, depth of reasoning, contextual relevance, and clarity. Each item must be self-contained – non expert readers should not need to infer anything or consult external information. Begin each description with its category: "Essential Criteria: . . . ", "Important Criteria: . . . ", "Optional Criteria: . . . ", or "Pitfall Criteria: Does not mention . . . ".

Inputs:
• question: The full question text.
• reference_answer: The ideal answer, including any specific facts, explanations, or advice.

Total items:
• Choose 7–20 rubric items based on the complexity of the question.

Each rubric item:
• title (2–4 words).
• description: One sentence starting with its category prefix that explicitly states exactly what to look for.
• weight: For Essential/Important/Optional, use 1–5 (5 = most important); for Pitfall, use –1 or –2.

Category guidance:
• Essential: Critical facts or safety checks; if missing, the response is invalid (weight 5).
• Important: Key reasoning, completeness, or clarity; strongly affects quality (weight 3–4).
• Optional: Helpful style or extra depth; nice to have but not deal-breaking (weight 1–2).
• Pitfall: Common mistakes or omissions specific to this prompt—identify things a respondent often forgets or misstates.

Output: Provide a JSON array of rubric objects. Each object must contain exactly three keys—title, description, and weight."""

        user_prompt = f"""Question: {question}
Reference Answer: {reference_answer}

Generate the rubric as described."""

        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
            )

            # Parse JSON response
            content = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]

            rubrics = json.loads(content)
            return rubrics

        except Exception as e:
            print(f"Error generating rubrics: {e}")
            # Return default rubrics if generation fails
            return [
                {
                    "title": "Relevance",
                    "description": "Essential Criteria: Addresses the main question directly and completely.",
                    "weight": 5,
                },
                {
                    "title": "Accuracy",
                    "description": "Important Criteria: Provides accurate and factual information.",
                    "weight": 4,
                },
                {
                    "title": "Clarity",
                    "description": "Important Criteria: Presents information clearly and understandably.",
                    "weight": 3,
                },
            ]
