from abc import abstractmethod

from trajectory.common.logger import error, warning
from trajectory.data import Trace
from trajectory.scorers.base_scorer import BaseScorer


class AgentScorer(BaseScorer):
    @abstractmethod
    async def a_score_trace(
        self, trace: Trace, tools: list | None = None, *args, **kwargs
    ) -> float:
        """
        Asynchronously measures the score on a trace
        """
        warning("Attempting to call unimplemented a_score_trace method")
        error("a_score_trace method not implemented")
        raise NotImplementedError(
            "You must implement the `a_score_trace` method in your custom scorer"
        )
