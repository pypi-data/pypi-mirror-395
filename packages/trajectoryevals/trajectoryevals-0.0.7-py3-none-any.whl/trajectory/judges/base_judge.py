"""
Implements the base class for all Trajectory Judge models.
"""

from abc import ABC, abstractmethod


class TrajectoryJudge(ABC):
    def __init__(self, model_name: str | None = None, *args, **kwargs):
        self.model_name = model_name
        self.model = self.load_model(*args, **kwargs)

    @abstractmethod
    def load_model(self, *args, **kwargs):
        """Loads a model, that will be responsible for scoring.

        Returns:
            A model object
        """

    @abstractmethod
    def generate(self, *args, **kwargs) -> str:
        """Runs the model to output LLM response.

        Returns:
            A string.
        """

    @abstractmethod
    async def a_generate(self, *args, **kwargs) -> str:
        """Runs the model to output LLM response.

        Returns:
            A string.
        """

    @abstractmethod
    def get_model_name(self, *args, **kwargs) -> str:
        pass
