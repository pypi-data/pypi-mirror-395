"""
Classes for representing examples in a dataset.
"""

from datetime import datetime
from enum import Enum

from trajectory.data.trajectory_types import ExampleTrajectoryType
from trajectory.verifiers.models import VerifierConfig


class ExampleParams(str, Enum):
    INPUT = "input"
    ACTUAL_OUTPUT = "actual_output"
    EXPECTED_OUTPUT = "expected_output"
    CONTEXT = "context"
    RETRIEVAL_CONTEXT = "retrieval_context"
    TOOLS_CALLED = "tools_called"
    EXPECTED_TOOLS = "expected_tools"
    REASONING = "reasoning"
    ADDITIONAL_METADATA = "additional_metadata"


class Example(ExampleTrajectoryType):
    example_id: str = ""

    # New fields for component-level verifiers and trajectory-level scorers
    component_verifiers: dict[str, list[VerifierConfig]] | None = None
    trajectory_scorers: list[str] | None = None

    def __init__(self, **data):
        if "created_at" not in data:
            data["created_at"] = datetime.now().isoformat()
        super().__init__(**data)
        self.example_id = None

        # Initialize verifiers and scorers if not provided
        if self.component_verifiers is None:
            self.component_verifiers = {}
        if self.trajectory_scorers is None:
            self.trajectory_scorers = []

    def add_component_verifier(self, function_name: str, verifier: VerifierConfig):
        """Add a verifier for a specific component/function"""
        if function_name not in self.component_verifiers:
            self.component_verifiers[function_name] = []
        self.component_verifiers[function_name].append(verifier)

    def add_trajectory_scorer(self, scorer_name: str):
        """Add a trajectory-level scorer"""
        if scorer_name not in self.trajectory_scorers:
            self.trajectory_scorers.append(scorer_name)

    def to_dict(self):
        return {
            "input": self.input,
            "actual_output": self.actual_output,
            "expected_output": self.expected_output,
            "context": self.context,
            "retrieval_context": self.retrieval_context,
            "additional_metadata": self.additional_metadata,
            "tools_called": self.tools_called,
            "expected_tools": self.expected_tools,
            "name": self.name,
            "example_id": self.example_id,
            "example_index": self.example_index,
            "created_at": self.created_at,
        }

    def __str__(self):
        return (
            f"Example(input={self.input}, "
            f"actual_output={self.actual_output}, "
            f"expected_output={self.expected_output}, "
            f"context={self.context}, "
            f"retrieval_context={self.retrieval_context}, "
            f"additional_metadata={self.additional_metadata}, "
            f"tools_called={self.tools_called}, "
            f"expected_tools={self.expected_tools}, "
            f"name={self.name}, "
            f"example_id={self.example_id}, "
            f"example_index={self.example_index}, "
            f"created_at={self.created_at}, "
        )
