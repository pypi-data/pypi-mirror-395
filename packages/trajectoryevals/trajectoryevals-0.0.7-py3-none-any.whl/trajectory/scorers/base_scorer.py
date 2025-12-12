"""
Base class for all scorers.
"""

from typing import Any

from pydantic import BaseModel, Field, model_validator

from trajectory.judges.utils import create_judge


class BaseScorer(BaseModel):
    """
    If you want to create a scorer that does not fall under any of the ready-made Trajectory scorers,
    you can create a custom scorer by extending this class. This is best used for special use cases
    where none of Trajectory's scorers are suitable.
    """

    score_type: str  # type of your scorer (Faithfulness, PromptScorer)
    threshold: float = (
        0.5  # The threshold to pass a test while using this scorer as a scorer
    )
    name: str | None = (
        None  # name of your scorer (Faithfulness, PromptScorer-randomslug)
    )
    score: float | None = None  # The float score of the scorer run on the test case
    score_breakdown: dict | None = None
    reason: str | None = ""
    using_native_model: bool | None = None  # Whether the model is a native model
    success: bool | None = None  # Whether the test case passed or failed
    model: str | None = None  # The name of the model used to evaluate the test case
    model_client: Any | None = Field(
        default=None, exclude=True
    )  # The model used to evaluate the test case
    strict_mode: bool = False  # Whether to run the scorer in strict mode
    error: str | None = None  # The error message if the scorer failed
    additional_metadata: dict | None = None  # Additional metadata for the scorer
    user: str | None = None  # The user ID of the scorer

    @model_validator(mode="before")
    @classmethod
    def enforce_strict_threshold(cls, data: dict):
        if data.get("strict_mode"):
            data["threshold"] = 1.0
        return data

    @model_validator(mode="after")
    @classmethod
    def default_name(cls, m: "BaseScorer") -> "BaseScorer":
        if not m.name:
            # Try to use the class name if it exists and is not empty
            class_name = getattr(m, "__class__", None)
            if class_name and getattr(m.__class__, "__name__", None):
                m.name = m.__class__.__name__
            else:
                m.name = m.score_type
        return m

    def _add_model(self, model: str):
        """
        Adds the evaluation model to the BaseScorer instance

        This method is used at eval time
        """
        self.model_client, self.using_native_model = create_judge(model)
        self.model = self.model_client.get_model_name() or model

    def success_check(self) -> bool:
        """
        For unit testing, determines whether the test case passes or fails
        """
        if self.error:
            return False
        if self.score is None:
            return False
        return self.score >= self.threshold
