"""
`judgeval` answer relevancy scorer

TODO add link to docs page for this scorer

"""

# Internal imports

from trajectory.constants import APIScorerType
from trajectory.data import ExampleParams
from trajectory.scorers.api_scorer import APIScorerConfig


class AnswerCorrectnessScorer(APIScorerConfig):
    score_type: APIScorerType = APIScorerType.ANSWER_CORRECTNESS
    required_params: list[ExampleParams] = [
        ExampleParams.INPUT,
        ExampleParams.ACTUAL_OUTPUT,
        ExampleParams.EXPECTED_OUTPUT,
    ]
