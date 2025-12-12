from trajectory.constants import APIScorerType
from trajectory.data import ExampleParams
from trajectory.scorers.api_scorer import APIScorerConfig


class AnswerRelevancyScorer(APIScorerConfig):
    score_type: APIScorerType = APIScorerType.ANSWER_RELEVANCY
    required_params: list[ExampleParams] = [
        ExampleParams.INPUT,
        ExampleParams.ACTUAL_OUTPUT,
    ]
