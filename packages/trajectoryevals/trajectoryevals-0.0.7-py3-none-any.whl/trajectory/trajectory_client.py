"""
Implements the TrajectoryClient to interact with the Trajectory API.
"""

import os
from collections.abc import Callable
from typing import Any, Union
from uuid import uuid4

from langchain_core.callbacks import BaseCallbackHandler
from pydantic import BaseModel

from trajectory.common.api import TrajectoryApiClient
from trajectory.common.exceptions import TrajectoryAPIError
from trajectory.common.logger import trajectory_logger
from trajectory.common.tracer import Tracer
from trajectory.common.utils import validate_api_key
from trajectory.data import (
    Example,
    ScoringResult,
    Trace,
)
from trajectory.data.datasets import EvalDataset, EvalDatasetClient
from trajectory.data.trace_run import TraceRun
from trajectory.evaluation_run import EvaluationRun
from trajectory.run_evaluation import (
    assert_test,
    run_eval,
    run_trace_eval,
)
from trajectory.scorers import (
    APIScorerConfig,
    BaseScorer,
)


class EvalRunRequestBody(BaseModel):
    eval_name: str
    project_name: str


class DeleteEvalRunRequestBody(BaseModel):
    eval_names: list[str]
    project_name: str


class SingletonMeta(type):
    _instances: dict[type, "TrajectoryClient"] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TrajectoryClient(metaclass=SingletonMeta):
    def __init__(
        self,
        api_key: str | None = os.getenv("TRAJECTORY_API_KEY"),
        organization_id: str | None = os.getenv("TRAJECTORY_ORG_ID"),
    ):
        if not api_key:
            raise ValueError(
                "api_key parameter must be provided. Please provide a valid API key value or set the TRAJECTORY_API_KEY environment variable."
            )

        if not organization_id:
            raise ValueError(
                "organization_id parameter must be provided. Please provide a valid organization ID value or set the TRAJECTORY_ORG_ID environment variable."
            )

        self.trajectory_api_key = api_key
        self.organization_id = organization_id
        self.api_client = TrajectoryApiClient(api_key, organization_id)
        self.eval_dataset_client = EvalDatasetClient(api_key, organization_id)

        # Verify API key is valid
        result, response = validate_api_key(api_key)
        if not result:
            # May be bad to output their invalid API key...
            raise TrajectoryAPIError(
                f"Issue with passed in Trajectory API key: {response}"
            )
        else:
            trajectory_logger.info("Successfully initialized TrajectoryClient!")

    def run_trace_evaluation(
        self,
        scorers: list[Union[APIScorerConfig, BaseScorer]],
        examples: list[Example] | None = None,
        function: Callable | None = None,
        tracer: Union[Tracer, BaseCallbackHandler] | None = None,
        traces: list[Trace] | None = None,
        tools: list[dict[str, Any]] | None = None,
        project_name: str = "default_project",
        eval_run_name: str = "default_eval_trace",
        model: str | None = "gpt-4.1",
        append: bool = False,
        override: bool = False,
    ) -> bool:
        try:
            if examples and not function:
                raise ValueError("Cannot pass in examples without a function")

            if traces and function:
                raise ValueError("Cannot pass in traces and function")

            if examples and traces:
                raise ValueError("Cannot pass in both examples and traces")

            trace_run = TraceRun(
                project_name=project_name,
                eval_name=eval_run_name,
                traces=traces,
                scorers=scorers,
                model=model,
                append=append,
                organization_id=self.organization_id,
                tools=tools,
            )
            return run_trace_eval(
                trace_run, self.trajectory_api_key, override, function, tracer, examples
            )
        except ValueError as e:
            raise ValueError(
                f"Please check your TraceRun object, one or more fields are invalid: \n{e!s}"
            )
        except Exception as e:
            raise Exception(f"An unexpected error occurred during evaluation: {e!s}")

    def run_evaluation(
        self,
        examples: list[Example],
        scorers: list[Union[APIScorerConfig, BaseScorer]],
        model: str | None = "gpt-4.1",
        project_name: str = "default_project",
        eval_run_name: str = "default_eval_run",
        override: bool = False,
        append: bool = False,
    ) -> list[ScoringResult]:
        """
        Executes an evaluation of `Example`s using one or more `Scorer`s

        Args:
            examples (List[Example]): The examples to evaluate
            scorers (List[Union[APIScorerConfig, BaseScorer]]): A list of scorers to use for evaluation
            model (str): The model used as a judge when using LLM as a Judge
            project_name (str): The name of the project the evaluation results belong to
            eval_run_name (str): A name for this evaluation run
            override (bool): Whether to override an existing evaluation run with the same name
            append (bool): Whether to append to an existing evaluation run with the same name

        Returns:
            List[ScoringResult]: The results of the evaluation
        """
        if override and append:
            raise ValueError(
                "Cannot set both override and append to True. Please choose one."
            )

        try:
            eval = EvaluationRun(
                append=append,
                override=override,
                project_name=project_name,
                eval_name=eval_run_name,
                examples=examples,
                scorers=scorers,
                model=model,
                organization_id=self.organization_id,
            )
            return run_eval(
                eval,
                self.trajectory_api_key,
                override,
            )
        except ValueError as e:
            raise ValueError(
                f"Please check your EvaluationRun object, one or more fields are invalid: \n{e!s}"
            )
        except Exception as e:
            raise Exception(f"An unexpected error occurred during evaluation: {e!s}")

    def create_dataset(self) -> EvalDataset:
        return self.eval_dataset_client.create_dataset()

    def push_dataset(
        self,
        alias: str,
        dataset: EvalDataset,
        project_name: str,
        overwrite: bool | None = False,
    ) -> bool:
        """
        Uploads an `EvalDataset` to the Trajectory platform for storage.

        Args:
            alias (str): The name to use for the dataset
            dataset (EvalDataset): The dataset to upload to Trajectory
            overwrite (Optional[bool]): Whether to overwrite the dataset if it already exists

        Returns:
            bool: Whether the dataset was successfully uploaded
        """
        # Set trajectory_api_key just in case it was not set
        dataset.trajectory_api_key = self.trajectory_api_key
        return self.eval_dataset_client.push(dataset, alias, project_name, overwrite)

    def append_dataset(
        self, alias: str, examples: list[Example], project_name: str
    ) -> bool:
        """
        Appends an `EvalDataset` to the Trajectory platform for storage.
        """
        return self.eval_dataset_client.append_examples(alias, examples, project_name)

    def pull_dataset(self, alias: str, project_name: str) -> EvalDataset:
        """
        Retrieves a saved `EvalDataset` from the Trajectory platform.

        Args:
            alias (str): The name of the dataset to retrieve

        Returns:
            EvalDataset: The retrieved dataset
        """
        return self.eval_dataset_client.pull(alias, project_name)

    def delete_dataset(self, alias: str, project_name: str) -> bool:
        """
        Deletes a saved `EvalDataset` from the Trajectory platform.
        """
        return self.eval_dataset_client.delete(alias, project_name)

    def pull_project_dataset_stats(self, project_name: str) -> dict:
        """
        Retrieves all dataset stats from the Trajectory platform for the project.

        Args:
            project_name (str): The name of the project to retrieve

        Returns:
            dict: The retrieved dataset stats
        """
        return self.eval_dataset_client.pull_project_dataset_stats(project_name)

    # Maybe add option where you can pass in the EvaluationRun object and it will pull the eval results from the backend
    def pull_eval(
        self, project_name: str, eval_run_name: str
    ) -> list[dict[str, Union[str, list[ScoringResult]]]]:
        """Pull evaluation results from the server.

        Args:
            project_name (str): Name of the project
            eval_run_name (str): Name of the evaluation run

        Returns:
            Dict[str, Union[str, List[ScoringResult]]]: Dictionary containing:
                - id (str): The evaluation run ID
                - results (List[ScoringResult]): List of scoring results
        """
        return self.api_client.fetch_evaluation_results(project_name, eval_run_name)

    def create_project(self, project_name: str) -> bool:
        """
        Creates a project on the server.
        """
        self.api_client.create_project(project_name)
        return True

    def delete_project(self, project_name: str) -> bool:
        """
        Deletes a project from the server. Which also deletes all evaluations and traces associated with the project.
        """
        self.api_client.delete_project(project_name)
        return True

    def assert_test(
        self,
        examples: list[Example],
        scorers: list[Union[APIScorerConfig, BaseScorer]],
        model: str | None = "gpt-4.1",
        project_name: str = "default_test",
        eval_run_name: str = str(uuid4()),
        override: bool = False,
        append: bool = False,
    ) -> None:
        """
        Asserts a test by running the evaluation and checking the results for success

        Args:
            examples (List[Example]): The examples to evaluate.
            scorers (List[Union[APIScorerConfig, BaseScorer]]): A list of scorers to use for evaluation
            model (str): The model used as a judge when using LLM as a Judge
            project_name (str): The name of the project the evaluation results belong to
            eval_run_name (str): A name for this evaluation run
            override (bool): Whether to override an existing evaluation run with the same name
            append (bool): Whether to append to an existing evaluation run with the same name
            async_execution (bool): Whether to run the evaluation asynchronously
        """

        results: list[ScoringResult]

        results = self.run_evaluation(
            examples=examples,
            scorers=scorers,
            model=model,
            project_name=project_name,
            eval_run_name=eval_run_name,
            override=override,
            append=append,
        )
        assert_test(results)

    def assert_trace_test(
        self,
        scorers: list[Union[APIScorerConfig, BaseScorer]],
        examples: list[Example] | None = None,
        function: Callable | None = None,
        tracer: Union[Tracer, BaseCallbackHandler] | None = None,
        traces: list[Trace] | None = None,
        tools: list[dict[str, Any]] | None = None,
        model: str | None = "gpt-4.1",
        project_name: str = "default_test",
        eval_run_name: str = str(uuid4()),
        override: bool = False,
        append: bool = False,
        async_execution: bool = False,
    ) -> None:
        """
        Asserts a test by running the evaluation and checking the results for success

        Args:
            examples (List[Example]): The examples to evaluate.
            scorers (List[Union[APIScorerConfig, BaseScorer]]): A list of scorers to use for evaluation
            model (str): The model used as a judge when using LLM as a Judge
            project_name (str): The name of the project the evaluation results belong to
            eval_run_name (str): A name for this evaluation run
            override (bool): Whether to override an existing evaluation run with the same name
            append (bool): Whether to append to an existing evaluation run with the same name
            function (Optional[Callable]): A function to use for evaluation
            tracer (Optional[Union[Tracer, BaseCallbackHandler]]): A tracer to use for evaluation
            tools (Optional[List[Dict[str, Any]]]): A list of tools to use for evaluation
            async_execution (bool): Whether to run the evaluation asynchronously
        """

        # Check for enable_param_checking and tools
        for scorer in scorers:
            if hasattr(scorer, "kwargs") and scorer.kwargs is not None:
                if scorer.kwargs.get("enable_param_checking") is True:
                    if not tools:
                        raise ValueError(
                            f"You must provide the 'tools' argument to assert_test when using a scorer with enable_param_checking=True. If you do not want to do param checking, explicitly set enable_param_checking=False for the {scorer.__name__} scorer."
                        )

        # results: List[ScoringResult]

        results = self.run_trace_evaluation(
            examples=examples,
            traces=traces,
            scorers=scorers,
            model=model,
            project_name=project_name,
            eval_run_name=eval_run_name,
            override=override,
            append=append,
            function=function,
            tracer=tracer,
            tools=tools,
        )
