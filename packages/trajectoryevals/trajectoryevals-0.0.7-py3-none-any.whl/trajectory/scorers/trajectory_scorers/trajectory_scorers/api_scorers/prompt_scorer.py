import os
from collections.abc import Mapping
from typing import Any

from trajectory.common.api import TrajectoryApiClient, TrajectoryAPIException
from trajectory.common.exceptions import TrajectoryAPIError
from trajectory.constants import APIScorerType
from trajectory.scorers.api_scorer import APIScorerConfig


def push_prompt_scorer(
    name: str,
    prompt: str,
    options: Mapping[str, float],
    trajectory_api_key: str = os.getenv("TRAJECTORY_API_KEY") or "",
    organization_id: str = os.getenv("TRAJECTORY_ORG_ID") or "",
) -> str:
    client = TrajectoryApiClient(trajectory_api_key, organization_id)
    try:
        r = client.save_scorer(name, prompt, dict(options))
    except TrajectoryAPIException as e:
        if e.status_code == 500:
            raise TrajectoryAPIError(
                f"The server is temporarily unavailable. Please try your request again in a few moments. Error details: {e.error_detail}"
            )
        raise TrajectoryAPIError(f"Failed to save classifier scorer: {e.error_detail}")
    return r["name"]


def fetch_prompt_scorer(
    name: str,
    trajectory_api_key: str = os.getenv("TRAJECTORY_API_KEY") or "",
    organization_id: str = os.getenv("TRAJECTORY_ORG_ID") or "",
):
    client = TrajectoryApiClient(trajectory_api_key, organization_id)
    try:
        scorer_config = client.fetch_scorer(name)
        scorer_config.pop("created_at")
        scorer_config.pop("updated_at")
        return scorer_config
    except TrajectoryAPIException as e:
        if e.status_code == 500:
            raise TrajectoryAPIError(
                f"The server is temporarily unavailable. Please try your request again in a few moments. Error details: {e.error_detail}"
            )
        raise TrajectoryAPIError(
            f"Failed to fetch classifier scorer '{name}': {e.error_detail}"
        )


def scorer_exists(
    name: str,
    trajectory_api_key: str = os.getenv("TRAJECTORY_API_KEY") or "",
    organization_id: str = os.getenv("TRAJECTORY_ORG_ID") or "",
):
    client = TrajectoryApiClient(trajectory_api_key, organization_id)
    try:
        return client.scorer_exists(name)["exists"]
    except TrajectoryAPIException as e:
        if e.status_code == 500:
            raise TrajectoryAPIError(
                f"The server is temporarily unavailable. Please try your request again in a few moments. Error details: {e.error_detail}"
            )
        raise TrajectoryAPIError(f"Failed to check if scorer exists: {e.error_detail}")


class PromptScorer(APIScorerConfig):
    """
    In the Trajectory backend, this scorer is implemented as a PromptScorer that takes
    1. a system role that may involve the Example object
    2. options for scores on the example

    and uses a judge to execute the evaluation from the system role and classify into one of the options
    """

    prompt: str
    options: Mapping[str, float]
    score_type: APIScorerType = APIScorerType.PROMPT_SCORER
    trajectory_api_key: str = os.getenv("TRAJECTORY_API_KEY") or ""
    organization_id: str = os.getenv("TRAJECTORY_ORG_ID") or ""

    @classmethod
    def get(
        cls,
        name: str,
        trajectory_api_key: str = os.getenv("TRAJECTORY_API_KEY") or "",
        organization_id: str = os.getenv("TRAJECTORY_ORG_ID") or "",
    ):
        scorer_config = fetch_prompt_scorer(name, trajectory_api_key, organization_id)
        return cls(
            name=name,
            prompt=scorer_config["prompt"],
            options=scorer_config["options"],
            trajectory_api_key=trajectory_api_key,
            organization_id=organization_id,
        )

    @classmethod
    def create(
        cls,
        name: str,
        prompt: str,
        options: Mapping[str, float],
        trajectory_api_key: str = os.getenv("TRAJECTORY_API_KEY") or "",
        organization_id: str = os.getenv("TRAJECTORY_ORG_ID") or "",
    ):
        if not scorer_exists(name, trajectory_api_key, organization_id):
            push_prompt_scorer(
                name, prompt, options, trajectory_api_key, organization_id
            )
            return cls(
                name=name,
                prompt=prompt,
                options=options,
                trajectory_api_key=trajectory_api_key,
                organization_id=organization_id,
            )
        else:
            raise TrajectoryAPIError(
                f"Scorer with name {name} already exists. Either use the existing scorer with the get() method or use a new name."
            )

    # Setter functions. Each setter function pushes the scorer to the DB.
    def set_name(self, name: str):
        """
        Updates the name of the scorer.
        """
        self.name = name
        self.push_prompt_scorer()

    def set_threshold(self, threshold: float):
        """
        Updates the threshold of the scorer.
        """
        self.threshold = threshold
        self.push_prompt_scorer()

    def set_prompt(self, prompt: str):
        """
        Updates the prompt with the new prompt.

        Sample prompt:
        "Did the chatbot answer the user's question in a kind way?"
        """
        self.prompt = prompt
        self.push_prompt_scorer()

    def set_options(self, options: Mapping[str, float]):
        """
        Updates the options with the new options.

        Sample options:
        {"yes": 1, "no": 0}
        """
        self.options = options
        self.push_prompt_scorer()

    def append_to_prompt(self, prompt_addition: str):
        """
        Appends a string to the prompt.
        """
        self.prompt += prompt_addition
        self.push_prompt_scorer()

    # Getters
    def get_prompt(self) -> str | None:
        """
        Returns the prompt of the scorer.
        """
        return self.prompt

    def get_options(self) -> Mapping[str, float] | None:
        """
        Returns the options of the scorer.
        """
        return self.options

    def get_name(self) -> str | None:
        """
        Returns the name of the scorer.
        """
        return self.name

    def get_config(self) -> dict:
        """
        Returns a dictionary with all the fields in the scorer.
        """
        return {
            "name": self.name,
            "prompt": self.prompt,
            "options": self.options,
        }

    def push_prompt_scorer(self):
        """
        Pushes the scorer to the DB.
        """
        push_prompt_scorer(
            self.name,
            self.prompt,
            self.options,
            self.trajectory_api_key,
            self.organization_id,
        )

    def __str__(self):
        return f"PromptScorer(name={self.name}, prompt={self.prompt}, options={self.options})"

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        base = super().model_dump(*args, **kwargs)
        base_fields = set(APIScorerConfig.model_fields.keys())
        all_fields = set(self.__class__.model_fields.keys())

        extra_fields = all_fields - base_fields - {"kwargs"}

        base["kwargs"] = {
            k: getattr(self, k) for k in extra_fields if getattr(self, k) is not None
        }
        return base
