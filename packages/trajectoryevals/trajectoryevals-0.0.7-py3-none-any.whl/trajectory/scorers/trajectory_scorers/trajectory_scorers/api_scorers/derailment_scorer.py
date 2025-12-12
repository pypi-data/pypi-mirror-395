"""
`judgeval` answer relevancy scorer

TODO add link to docs page for this scorer

"""

# Internal imports
from trajectory.constants import APIScorerType
from trajectory.scorers.api_scorer import APIScorerConfig


class DerailmentScorer(APIScorerConfig):
    score_type: APIScorerType = APIScorerType.DERAILMENT
