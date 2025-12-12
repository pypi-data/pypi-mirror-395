"""
`judgeval` tool order scorer
"""

# Internal imports
from typing import Any

from trajectory.constants import APIScorerType
from trajectory.scorers.api_scorer import APIScorerConfig


class ToolOrderScorer(APIScorerConfig):
    score_type: APIScorerType = APIScorerType.TOOL_ORDER
    threshold: float = 1.0
    exact_match: bool = False

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        base = super().model_dump(*args, **kwargs)
        base_fields = set(APIScorerConfig.model_fields.keys())
        all_fields = set(self.__class__.model_fields.keys())

        extra_fields = all_fields - base_fields - {"kwargs"}

        base["kwargs"] = {
            k: getattr(self, k) for k in extra_fields if getattr(self, k) is not None
        }

        return base
