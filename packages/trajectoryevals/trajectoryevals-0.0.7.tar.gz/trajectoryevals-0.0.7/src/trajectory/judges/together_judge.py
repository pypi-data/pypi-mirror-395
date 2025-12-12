"""
Implementation of using TogetherAI inference for judges.
"""

from typing import Union

from pydantic import BaseModel

from trajectory.common.logger import trajectory_logger
from trajectory.common.utils import (
    afetch_together_api_response,
    fetch_together_api_response,
)
from trajectory.judges import TrajectoryJudge

BASE_CONVERSATION = [
    {"role": "system", "content": "You are a helpful assistant."},
]


class TogetherJudge(TrajectoryJudge):
    def __init__(self, model: str = "Qwen/Qwen2.5-72B-Instruct-Turbo", **kwargs):
        self.model = model
        self.kwargs = kwargs
        super().__init__(model_name=model)

    # TODO: Fix cost for generate and a_generate
    def generate(self, input: Union[str, list[dict]], schema: BaseModel = None) -> str:
        if isinstance(input, str):
            convo = BASE_CONVERSATION + [{"role": "user", "content": input}]
            return fetch_together_api_response(
                self.model, convo, response_format=schema
            )
        elif isinstance(input, list):
            convo = input
            return fetch_together_api_response(
                self.model, convo, response_format=schema
            )
        else:
            trajectory_logger.error(f"Invalid input type received: {type(input)}")
            raise TypeError("Input must be a string or a list of dictionaries.")

    async def a_generate(
        self, input: Union[str, list[dict]], schema: BaseModel = None
    ) -> str:
        if isinstance(input, str):
            convo = BASE_CONVERSATION + [{"role": "user", "content": input}]
            res = await afetch_together_api_response(
                self.model, convo, response_format=schema
            )
            return res
        elif isinstance(input, list):
            convo = input
            res = await afetch_together_api_response(
                self.model, convo, response_format=schema
            )
            return res
        else:
            trajectory_logger.error(f"Invalid input type received: {type(input)}")
            raise TypeError("Input must be a string or a list of dictionaries.")

    def load_model(self) -> str:
        return self.model

    def get_model_name(self) -> str:
        return self.model
