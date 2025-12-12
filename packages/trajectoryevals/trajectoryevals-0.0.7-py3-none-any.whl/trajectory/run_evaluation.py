import asyncio
import concurrent.futures
import copy
import json
import sys
import threading
import time
import uuid
from collections.abc import Callable
from contextvars import ContextVar, copy_context
from typing import Any, Union

from langchain_core.callbacks import BaseCallbackHandler
from rich import print as rprint

from trajectory.common.api import TrajectoryApiClient
from trajectory.common.api.api import TrajectoryAPIException
from trajectory.common.exceptions import TrajectoryAPIError
from trajectory.common.logger import trajectory_logger
from trajectory.common.tracer import Tracer
from trajectory.constants import (
    MAX_CONCURRENT_EVALUATIONS,
)
from trajectory.data import Example, ScorerData, ScoringResult, Trace
from trajectory.data.trace_run import TraceRun
from trajectory.evaluation_run import EvaluationRun
from trajectory.scorers import APIScorerConfig, BaseScorer
from trajectory.scorers.score import a_execute_scoring
from trajectory.scorers.trajectory_scorers import RubricBasedScorer, ToolCallOrderScorer

# Create a context variable to hold the current tracer
TRACE_VAR: ContextVar["Tracer"] = ContextVar("TRACE_VAR", default=None)


def safe_run_async(coro):
    """
    Safely run an async coroutine whether or not there's already an event loop running.

    Args:
        coro: The coroutine to run

    Returns:
        The result of the coroutine
    """
    try:
        # Try to get the running loop
        asyncio.get_running_loop()
        # If we get here, there's already a loop running
        # Run in a separate thread to avoid "asyncio.run() cannot be called from a running event loop"
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        # No event loop is running, safe to use asyncio.run()
        return asyncio.run(coro)


def send_to_rabbitmq(evaluation_run: EvaluationRun) -> dict[str, Any]:
    """
    Sends an evaluation run to the RabbitMQ evaluation queue.
    """
    if not evaluation_run.trajectory_api_key or not evaluation_run.organization_id:
        raise ValueError("API key and organization ID are required")
    if not evaluation_run.eval_name or not evaluation_run.project_name:
        raise ValueError("Eval name and project name are required")
    api_client = TrajectoryApiClient(
        evaluation_run.trajectory_api_key, evaluation_run.organization_id
    )
    return api_client.add_to_evaluation_queue(
        evaluation_run.eval_name, evaluation_run.project_name
    )


def execute_api_eval(evaluation_run: EvaluationRun) -> dict:
    """
    Executes an evaluation of a list of `Example`s using one or more `TrajectoryScorer`s via the Trajectory API.

    Args:
        evaluation_run (EvaluationRun): The evaluation run object containing the examples, scorers, and metadata

    Returns:
        List[Dict]: The results of the evaluation. Each result is a dictionary containing the fields of a `ScoringResult`
                    object.
    """

    try:
        # submit API request to execute evals
        if not evaluation_run.trajectory_api_key or not evaluation_run.organization_id:
            raise ValueError("API key and organization ID are required")
        api_client = TrajectoryApiClient(
            evaluation_run.trajectory_api_key, evaluation_run.organization_id
        )
        return api_client.run_evaluation(evaluation_run.model_dump())
    except Exception as e:
        trajectory_logger.error(f"Error: {e}")

        details = "No details provided"
        if isinstance(e, TrajectoryAPIException):
            details = e.response_json.get("detail", "No details provided")

        raise TrajectoryAPIError(
            "An error occurred while executing the Trajectory API request: " + details
        )


def execute_api_trace_eval(trace_run: TraceRun, trajectory_api_key: str) -> dict:
    """
    Executes an evaluation of a list of `Trace`s using one or more `TrajectoryScorer`s via the Trajectory API.
    """

    try:
        # submit API request to execute evals
        if not trajectory_api_key or not trace_run.organization_id:
            raise ValueError("API key and organization ID are required")
        api_client = TrajectoryApiClient(trajectory_api_key, trace_run.organization_id)
        return api_client.run_trace_evaluation(trace_run.model_dump(warnings=False))
    except Exception as e:
        trajectory_logger.error(f"Error: {e}")

        details = "An unknown error occurred."
        if isinstance(e, TrajectoryAPIException):
            details = e.response_json.get("detail", "An unknown error occurred.")

        raise TrajectoryAPIError(
            "An error occurred while executing the Trajectory API request: " + details
        )


def check_missing_scorer_data(results: list[ScoringResult]) -> list[ScoringResult]:
    """
    Checks if any `ScoringResult` objects are missing `scorers_data`.

    If any are missing, logs an error and returns the results.
    """
    for i, result in enumerate(results):
        if not result.scorers_data:
            trajectory_logger.error(
                f"Scorer data is missing for example {i}. "
                "This is usually caused when the example does not contain "
                "the fields required by the scorer. "
                "Check that your example contains the fields required by the scorers. "
                "TODO add docs link here for reference."
            )
    return results


def check_experiment_type(
    eval_name: str,
    project_name: str,
    trajectory_api_key: str,
    organization_id: str,
    is_trace: bool,
) -> None:
    """
    Checks if the current experiment, if one exists, has the same type (examples of traces)
    """
    api_client = TrajectoryApiClient(trajectory_api_key, organization_id)

    try:
        api_client.check_experiment_type(eval_name, project_name, is_trace)
    except TrajectoryAPIException as e:
        if e.response.status_code == 422:
            trajectory_logger.error(f"{e.response_json}")
            raise ValueError(f"{e.response_json}")
        else:
            raise e
    except Exception as e:
        trajectory_logger.error(f"Failed to check if experiment type exists: {e!s}")
        raise TrajectoryAPIError(f"Failed to check if experiment type exists: {e!s}")


def check_eval_run_name_exists(
    eval_name: str, project_name: str, trajectory_api_key: str, organization_id: str
) -> None:
    """
    Checks if an evaluation run name already exists for a given project.

    Args:
        eval_name (str): Name of the evaluation run
        project_name (str): Name of the project
        trajectory_api_key (str): API key for authentication

    Raises:
        ValueError: If the evaluation run name already exists
        TrajectoryAPIError: If there's an API error during the check
    """
    api_client = TrajectoryApiClient(trajectory_api_key, organization_id)
    try:
        api_client.check_eval_run_name_exists(eval_name, project_name)
    except TrajectoryAPIException as e:
        if e.response.status_code == 409:
            error_str = f"Eval run name '{eval_name}' already exists for this project. Please choose a different name, set the `override` flag to true, or set the `append` flag to true. See https://docs.trajectorylabs.ai/sdk-reference/trajectory-client#override for more information."
            trajectory_logger.error(error_str)
            raise ValueError(error_str)
        else:
            raise e

    except Exception as e:
        trajectory_logger.error(f"Failed to check if eval run name exists: {e!s}")
        raise TrajectoryAPIError(f"Failed to check if eval run name exists: {e!s}")


def log_evaluation_results(
    scoring_results: list[ScoringResult],
    run: Union[EvaluationRun, TraceRun],
    trajectory_api_key: str,
) -> str:
    """
    Logs evaluation results to the Trajectory API database.

    Args:
        merged_results (List[ScoringResult]): The results to log
        evaluation_run (EvaluationRun): The evaluation run containing project info and API key
        trajectory_api_key (str): The API key for the Trajectory API

    Raises:
        TrajectoryAPIError: If there's an API error during logging
        ValueError: If there's a validation error with the results
    """
    try:
        if not trajectory_api_key or not run.organization_id:
            raise ValueError("API key and organization ID are required")

        api_client = TrajectoryApiClient(trajectory_api_key, run.organization_id)
        response = api_client.log_evaluation_results(
            scoring_results,
            run.model_dump(warnings=False),
        )
        url = response.get("ui_results_url")
        return url

    except Exception as e:
        trajectory_logger.error(f"Failed to save evaluation results to DB: {e!s}")
        raise TrajectoryAPIError(
            f"Request failed while saving evaluation results to DB: {e!s}"
        )


def check_examples(
    examples: list[Example], scorers: list[Union[APIScorerConfig, BaseScorer]]
) -> None:
    """
    Checks if the example contains the necessary parameters for the scorer.
    """
    prompt_user = False
    for scorer in scorers:
        for example in examples:
            missing_params = []
            for param in scorer.required_params:
                if getattr(example, param.value) is None:
                    missing_params.append(f"{param.value}")
            if missing_params:
                rprint(
                    f"[yellow]⚠️  WARNING:[/yellow] Example is missing required parameters for scorer [bold]{scorer.score_type.value}[/bold]"
                )
                rprint(f"Missing parameters: {', '.join(missing_params)}")
                rprint(f"Example: {json.dumps(example.model_dump(), indent=2)}")
                rprint("-" * 40)
                prompt_user = True

    if prompt_user:
        user_input = input("Do you want to continue? (y/n)")
        if user_input.lower() != "y":
            sys.exit(0)
        else:
            rprint("[green]Continuing...[/green]")


def copy_tracer(tracer: Tracer, evaluation_id: str = None) -> Tracer:
    """Create a deep copy of the tracer with all its configuration"""
    # Create a new tracer with the same configuration
    new_tracer = Tracer(
        api_key=tracer.api_key,
        organization_id=tracer.organization_id,
        project_name=tracer.project_name,
        deep_tracing=tracer.deep_tracing,
        enable_monitoring=True,  # Enable monitoring for the copy
        enable_evaluations=tracer.enable_evaluations,
        use_s3=tracer.use_s3,
        s3_bucket_name=getattr(tracer, "s3_bucket_name", None),
        s3_aws_access_key_id=getattr(tracer, "s3_aws_access_key_id", None),
        s3_aws_secret_access_key=getattr(tracer, "s3_aws_secret_access_key", None),
        s3_region_name=getattr(tracer, "s3_region_name", None),
        trace_across_async_contexts=tracer.trace_across_async_contexts,
        span_batch_size=tracer.span_batch_size,
        span_flush_interval=tracer.span_flush_interval,
        span_max_queue_size=tracer.span_max_queue_size,
        span_export_timeout=tracer.span_export_timeout,
        evaluation_id=evaluation_id,
        is_evaluation=evaluation_id is not None,
    )

    # Copy verifiers
    new_tracer._verifiers = copy.deepcopy(tracer._verifiers)

    # Copy other relevant attributes
    new_tracer.class_identifiers = copy.deepcopy(tracer.class_identifiers)
    new_tracer.offline_mode = tracer.offline_mode

    # Set evaluation-specific attributes
    new_tracer.evaluation_id = evaluation_id
    new_tracer.is_evaluation = evaluation_id is not None
    print(f"🔍 New tracer evaluation_id: {new_tracer.evaluation_id}")
    return new_tracer


def run_single_example(example: Example, function: Callable, tracer: Tracer) -> Trace:
    """Run a single example and return its trace"""
    print(f"🔍 Tracer: {tracer}")
    # Set example context for verifiers
    tracer._current_example = example

    # Run the function
    if example.input:
        if isinstance(example.input, str):
            function(example.input)
        elif isinstance(example.input, dict):
            function(**example.input)
        else:
            raise ValueError(f"Input must be string or dict, got {type(example.input)}")
    else:
        function()

    # Get the trace

    if tracer.traces:
        trace = tracer.traces[-1]  # Get the last trace
        return Trace(**trace)

    return None


def run_examples_concurrently(
    examples: list[Example], function: Callable, tracer: Tracer
) -> list[Trace]:
    """Run multiple examples concurrently"""

    # Generate evaluation ID for this batch of examples
    evaluation_id = str(uuid.uuid4())
    print(f"🎯 Generated evaluation_id: {evaluation_id} for {len(examples)} examples")

    def run_example_with_copied_tracer(example: Example) -> Trace:
        # Create a copy of the entire tracer object with evaluation_id
        example_tracer = copy_tracer(tracer, evaluation_id)

        # Register example-specific verifiers on the copied tracer
        for function_name, verifiers in example.component_verifiers.items():
            for verifier in verifiers:
                example_tracer.register_verifier(verifier)

        print(
            f"🔍 Registered verifiers for example: {list(example_tracer._verifiers.keys())}"
        )

        # Set the copied tracer in the context
        TRACE_VAR.set(example_tracer)
        print(
            f"🎯 Set context tracer: {example_tracer} with verifiers: {list(example_tracer._verifiers.keys())}"
        )

        try:
            # Now run the function - it will use the copied tracer from context
            return run_single_example(example, function, example_tracer)
        finally:
            # Clear the context
            TRACE_VAR.set(None)

    # Run examples concurrently using ThreadPoolExecutor with context propagation
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(examples)) as executor:
        # Submit all examples and store futures in order
        futures = []
        for example in examples:
            # Capture the current context and run the example in that context
            ctx = copy_context()
            future = executor.submit(
                lambda: ctx.run(run_example_with_copied_tracer, example)
            )
            futures.append(future)

        # Wait for all futures to complete and collect results in order
        traces = []
        for future in futures:
            try:
                trace = future.result()
                print(f"🔍 Trace: {trace}")
                traces.append(trace)
            except Exception as e:
                print(f"Error running example: {e}")
                traces.append(None)

    print(f"🔍 Traces: {traces}")
    return traces


async def evaluate_trajectories_async(
    traces: list[Trace], examples: list[Example]
) -> list[dict[str, Any]]:
    """Evaluate trajectories using trajectory-level scorers"""

    def create_scorer(scorer_config):
        """Create scorer instance from config"""
        if isinstance(scorer_config, str):
            # Handle string format like "RubricBasedScorer:gpt-4o-mini" or "ToolCallOrderScorer:exact_match"
            if ":" in scorer_config:
                scorer_name, parameter = scorer_config.split(":", 1)
            else:
                scorer_name = scorer_config
                parameter = None
        else:
            # Handle dict format
            scorer_name = scorer_config.get("name")
            parameter = scorer_config.get("config", {})

        print(f"🔍 Creating scorer: {scorer_name} with parameter: {parameter}")

        if scorer_name == "RubricBasedScorer":
            if parameter:
                return RubricBasedScorer(llm_model=parameter)
            else:
                return RubricBasedScorer()  # Use default model
        elif scorer_name == "ToolCallOrderScorer":
            if parameter:
                return ToolCallOrderScorer(mode=parameter)
            else:
                return ToolCallOrderScorer()  # Use default mode (ordering_match)
        else:
            raise ValueError(f"Unknown trajectory scorer: {scorer_name}")

    async def evaluate_single_trajectory(
        trace: Trace, example: Example
    ) -> dict[str, Any]:
        """Evaluate a single trajectory asynchronously"""
        if trace is None:
            return {"error": "Trace generation failed", "trace_id": None}

        example_results = {}
        print(f"🔍 Example trajectory scorers: {example.trajectory_scorers}")

        # Create tasks for all trajectory scorers
        scorer_tasks = []
        for scorer_config in example.trajectory_scorers:
            try:
                scorer = create_scorer(scorer_config)

                # Run scorer in thread pool since it's synchronous
                loop = asyncio.get_event_loop()
                task = loop.run_in_executor(
                    None, scorer.score_trajectory, trace, example
                )
                scorer_tasks.append((scorer.name, task))
            except Exception as e:
                print(f"⚠️ Error creating scorer {scorer_config}: {e}")
                example_results[f"scorer_{len(example_results)}"] = {
                    "error": f"Scorer creation failed: {e!s}",
                    "score": 0.0,
                    "passed": False,
                }

        # Wait for all scorer tasks to complete
        if scorer_tasks:
            scorer_names, tasks = zip(*scorer_tasks)
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for scorer_name, result in zip(scorer_names, results):
                if isinstance(result, Exception):
                    example_results[scorer_name] = {
                        "error": str(result),
                        "score": 0.0,
                        "passed": False,
                    }
                else:
                    example_results[scorer_name] = result

        # Add trace_id to the results
        example_results["trace_id"] = trace.trace_id
        return example_results

    # Create tasks for all trajectory evaluations
    evaluation_tasks = [
        evaluate_single_trajectory(trace, example)
        for trace, example in zip(traces, examples)
    ]

    # Wait for all evaluations to complete
    results = await asyncio.gather(*evaluation_tasks, return_exceptions=True)

    # Handle any exceptions
    final_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            final_results.append(
                {
                    "error": f"Trajectory evaluation failed: {result!s}",
                    "score": 0.0,
                    "passed": False,
                    "trace_id": traces[i].trace_id if i < len(traces) else None,
                }
            )
        else:
            final_results.append(result)

    return final_results


def send_trajectory_results_to_backend(
    trajectory_results: list[dict[str, Any]], trajectory_api_key: str
) -> None:
    """Send trajectory results to backend for storage"""

    import requests

    try:
        # Prepare the data for the backend
        payload = {"trajectory_results": trajectory_results}

        # Send to backend endpoint
        response = requests.post(
            "http://localhost:8000/api/trajectory-results/",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {trajectory_api_key}",
            },
            timeout=30,
        )

        if response.status_code == 201:
            print("✅ Trajectory results sent to backend successfully")
        else:
            print(
                f"⚠️ Failed to send trajectory results: {response.status_code} - {response.text}"
            )

    except Exception as e:
        print(f"❌ Error sending trajectory results to backend: {e}")


def run_trace_eval(
    trace_run: TraceRun,
    trajectory_api_key: str,
    override: bool = False,
    function: Callable | None = None,
    tracer: Union[Tracer, BaseCallbackHandler] | None = None,
    examples: list[Example] | None = None,
) -> bool:
    # Call endpoint to check to see if eval run name exists (if we DON'T want to override and DO want to log results)
    # if not override and not trace_run.append:
    #     check_eval_run_name_exists(
    #         trace_run.eval_name,
    #         trace_run.project_name,
    #         trajectory_api_key,
    #         trace_run.organization_id,
    #     )

    # if trace_run.append:
    #     # Check that the current experiment, if one exists, has the same type (examples or traces)
    #     check_experiment_type(
    #         trace_run.eval_name,
    #         trace_run.project_name,
    #         trajectory_api_key,
    #         trace_run.organization_id,
    #         True,
    #     )
    if function and tracer and examples is not None:
        new_traces: list[Trace] = []

        # Handle case where tracer is actually a callback handler
        actual_tracer = tracer
        if hasattr(tracer, "tracer") and hasattr(tracer.tracer, "traces"):
            # This is a callback handler, get the underlying tracer
            actual_tracer = tracer.tracer

        if trace_run.project_name != actual_tracer.project_name:
            raise ValueError(
                f"Project name mismatch between run_trace_eval and tracer. "
                f"Trace run: {trace_run.project_name}, "
                f"Tracer: {actual_tracer.project_name}"
            )

        # Run examples concurrently
        print(f"🔍 Running examples concurrently with tracer: {actual_tracer}")
        new_traces = run_examples_concurrently(examples, function, actual_tracer)

        # Evaluate trajectories asynchronously
        async def run_trajectory_evaluation():
            return await evaluate_trajectories_async(new_traces, examples)

        # Run the async evaluation in a new event loop
        def run_async_eval():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(run_trajectory_evaluation())
            finally:
                loop.close()

        trajectory_results = run_async_eval()
        print(f"🔍 Trajectory results: {trajectory_results}")

        # Send trajectory results to backend
        send_trajectory_results_to_backend(trajectory_results, trajectory_api_key)

        # Add trajectory results to trace metadata
        # for trace, trajectory_result in zip(new_traces, trajectory_results):
        #     if trace:
        #         trace.additional_metadata = {
        #             **(trace.additional_metadata or {}),
        #             "trajectory_evaluation": trajectory_result
        #         }

        trace_run.traces = new_traces
        actual_tracer.traces = []

    # Execute evaluation using Trajectory API
    try:  # execute an EvaluationRun with just TrajectoryScorers
        trajectory_logger.info("Executing Trace Evaluation... ")
        response_data: dict = execute_api_trace_eval(trace_run, trajectory_api_key)
        # scoring_results = [
        #     ScoringResult(**result) for result in response_data["results"]
        # ]
    except TrajectoryAPIError as e:
        raise TrajectoryAPIError(
            f"An error occurred while executing the Trajectory API request: {e!s}"
        )
    except ValueError as e:
        raise ValueError(
            f"Please check your TraceRun object, one or more fields are invalid: {e!s}"
        )

    # Convert the response data to `ScoringResult` objects
    # TODO: allow for custom scorer on traces

    # url = log_evaluation_results(
    #     response_data["agent_results"], trace_run, trajectory_api_key
    # )
    # rprint(
    #     f"\n🔍 You can view your evaluation results here: [rgb(106,0,255)][link={url}]View Results[/link]\n"
    # )
    # return scoring_results
    return True


async def get_evaluation_status(
    eval_name: str, project_name: str, trajectory_api_key: str, organization_id: str
) -> dict:
    """
    Gets the status of an async evaluation run.

    Args:
        eval_name (str): Name of the evaluation run
        project_name (str): Name of the project
        trajectory_api_key (str): API key for authentication
        organization_id (str): Organization ID for the evaluation

    Returns:
        Dict: Status information including:
            - status: 'pending', 'running', 'completed', or 'failed'
            - results: List of ScoringResult objects if completed
            - error: Error message if failed
    """
    api_client = TrajectoryApiClient(trajectory_api_key, organization_id)
    try:
        return api_client.get_evaluation_status(eval_name, project_name)
    except Exception as e:
        raise TrajectoryAPIError(
            f"An error occurred while checking evaluation status: {e!s}"
        )


def retrieve_counts(result: dict):
    scorer_data_count = 0
    for example in result.get("examples", []):
        for scorer in example.get("scorer_data", []):
            scorer_data_count += 1
    return scorer_data_count


def _poll_evaluation_until_complete(
    eval_name: str,
    project_name: str,
    trajectory_api_key: str,
    organization_id: str,
    expected_scorer_data_count: int,
    poll_interval_seconds: float = 5,
    max_failures: int = 5,
    max_poll_count: int = 24,  # This should be equivalent to 120 seconds
) -> tuple[list[ScoringResult], str]:
    """
    Polls until the evaluation is complete and returns the results.

    Args:
        eval_name (str): Name of the evaluation run
        project_name (str): Name of the project
        trajectory_api_key (str): API key for authentication
        organization_id (str): Organization ID for the evaluation
        poll_interval_seconds (int, optional): Time between status checks in seconds. Defaults to 5.
        original_examples (List[Example], optional): The original examples sent for evaluation.
                                                    If provided, will match results with original examples.

    Returns:
        List[ScoringResult]: The evaluation results
    """
    poll_count = 0
    exception_count = 0
    api_client = TrajectoryApiClient(trajectory_api_key, organization_id)
    while poll_count < max_poll_count:
        poll_count += 1
        try:
            # Check status
            status_response = api_client.get_evaluation_status(eval_name, project_name)

            if status_response.get("status") != "completed":
                time.sleep(poll_interval_seconds)
                continue

            results_response = api_client.fetch_evaluation_results(
                project_name, eval_name
            )
            url = results_response.get("ui_results_url")

            if results_response.get("examples") is None:
                time.sleep(poll_interval_seconds)
                continue

            examples_data = results_response.get("examples", [])
            scoring_results = []
            scorer_data_count = 0

            for example_data in examples_data:
                scorer_data_list = []
                for raw_scorer_data in example_data.get("scorer_data", []):
                    scorer_data = ScorerData(**raw_scorer_data)
                    scorer_data_list.append(scorer_data)
                    scorer_data_count += 1

                example = Example(**example_data)

                success = all(scorer_data.success for scorer_data in scorer_data_list)
                scoring_result = ScoringResult(
                    success=success,
                    scorers_data=scorer_data_list,
                    data_object=example,
                )
                scoring_results.append(scoring_result)

            if scorer_data_count != expected_scorer_data_count:
                time.sleep(poll_interval_seconds)
                continue

            return scoring_results, url
        except Exception as e:
            exception_count += 1
            if isinstance(e, TrajectoryAPIError):
                raise

            trajectory_logger.error(f"Error checking evaluation status: {e!s}")
            if exception_count > max_failures:
                raise TrajectoryAPIError(
                    f"Error checking evaluation status after {poll_count} attempts: {e!s}"
                )

            time.sleep(poll_interval_seconds)

    raise TrajectoryAPIError(
        f"Error checking evaluation status after {poll_count} attempts"
    )


def progress_logger(stop_event, msg="Working...", interval=5):
    start = time.time()
    while not stop_event.is_set():
        elapsed = int(time.time() - start)
        trajectory_logger.info(f"{msg} ({elapsed} sec)")
        stop_event.wait(interval)


def run_eval(
    evaluation_run: EvaluationRun,
    trajectory_api_key: str,
    override: bool = False,
) -> list[ScoringResult]:
    """
    Executes an evaluation of `Example`s using one or more `Scorer`s

    Args:
        evaluation_run (EvaluationRun): Stores example and evaluation together for running
        override (bool, optional): Whether to override existing evaluation run with same name. Defaults to False.

    Returns:
        List[ScoringResult]: A list of ScoringResult objects
    """

    # Call endpoint to check to see if eval run name exists (if we DON'T want to override and DO want to log results)
    # if not override and not evaluation_run.append:
    #     check_eval_run_name_exists(
    #         evaluation_run.eval_name,
    #         evaluation_run.project_name,
    #         trajectory_api_key,
    #         evaluation_run.organization_id,
    #     )

    # if evaluation_run.append:
    #     # Check that the current experiment, if one exists, has the same type (examples of traces)
    #     check_experiment_type(
    #         evaluation_run.eval_name,
    #         evaluation_run.project_name,
    #         trajectory_api_key,
    #         evaluation_run.organization_id,
    #         False,
    #     )

    # Set example IDs if not already set
    for idx, example in enumerate(evaluation_run.examples):
        example.example_index = idx  # Set numeric index

    trajectory_scorers: list[APIScorerConfig] = []
    local_scorers: list[BaseScorer] = []
    for scorer in evaluation_run.scorers:
        if isinstance(scorer, APIScorerConfig):
            trajectory_scorers.append(scorer)
        else:
            local_scorers.append(scorer)

    results: list[ScoringResult] = []
    url = ""

    if len(local_scorers) > 0 and len(trajectory_scorers) > 0:
        error_msg = "We currently do not support running both local and Trajectory API scorers at the same time. Please run your evaluation with either local scorers or Trajectory API scorers, but not both."
        trajectory_logger.error(error_msg)
        raise ValueError(error_msg)

    if len(trajectory_scorers) > 0:
        check_examples(evaluation_run.examples, trajectory_scorers)
        stop_event = threading.Event()
        t = threading.Thread(
            target=progress_logger, args=(stop_event, "Running evaluation...")
        )
        t.start()
        try:
            api_client = TrajectoryApiClient(
                trajectory_api_key, evaluation_run.organization_id
            )
            response = api_client.add_to_evaluation_queue(
                evaluation_run.model_dump(warnings=False)
            )

            if not response.get("success", False):
                error_message = response.error
                trajectory_logger.error(
                    f"Error adding evaluation to queue: {error_message}"
                )
                raise TrajectoryAPIError(error_message)

            old_scorer_data_count = 0
            if evaluation_run.append:
                try:
                    results_response = api_client.fetch_evaluation_results(
                        evaluation_run.project_name, evaluation_run.eval_name
                    )
                    old_scorer_data_count = retrieve_counts(results_response)
                except Exception:
                    # This usually means the user did append = True but the eval run name doesn't exist yet
                    pass

            results, url = _poll_evaluation_until_complete(
                eval_name=evaluation_run.eval_name,
                project_name=evaluation_run.project_name,
                trajectory_api_key=trajectory_api_key,
                organization_id=evaluation_run.organization_id,
                expected_scorer_data_count=(
                    len(evaluation_run.scorers) * len(evaluation_run.examples)
                )
                + old_scorer_data_count,
            )
        finally:
            stop_event.set()
            t.join()

    if len(local_scorers) > 0:
        results = safe_run_async(
            a_execute_scoring(
                evaluation_run.examples,
                local_scorers,
                model=evaluation_run.model,
                throttle_value=0,
                max_concurrent=MAX_CONCURRENT_EVALUATIONS,
            )
        )

        send_results = [
            scoring_result.model_dump(warnings=False) for scoring_result in results
        ]
        print(send_results)

        url = log_evaluation_results(send_results, evaluation_run, trajectory_api_key)
    rprint(
        f"\n🔍 You can view your evaluation results here: [rgb(106,0,255)][link={url}]View Results[/link]\n"
    )
    return results


def assert_test(scoring_results: list[ScoringResult]) -> None:
    """
    Collects all failed scorers from the scoring results.

    Args:
        ScoringResults (List[ScoringResult]): List of scoring results to check

    Returns:
        None. Raises exceptions for any failed test cases.
    """
    failed_cases: list[ScorerData] = []

    for result in scoring_results:
        if not result.success:
            # Create a test case context with all relevant fields
            test_case: dict = {"failed_scorers": []}
            if result.scorers_data:
                # If the result was not successful, check each scorer_data
                for scorer_data in result.scorers_data:
                    if not scorer_data.success:
                        if scorer_data.name == "Tool Order":
                            # Remove threshold, evaluation model for Tool Order scorer
                            scorer_data.threshold = None
                            scorer_data.evaluation_model = None
                        test_case["failed_scorers"].append(scorer_data)
            failed_cases.append(test_case)

    if failed_cases:
        error_msg = "The following test cases failed: \n"
        for fail_case in failed_cases:
            for fail_scorer in fail_case["failed_scorers"]:
                error_msg += (
                    f"\nScorer Name: {fail_scorer.name}\n"
                    f"Threshold: {fail_scorer.threshold}\n"
                    f"Success: {fail_scorer.success}\n"
                    f"Score: {fail_scorer.score}\n"
                    f"Reason: {fail_scorer.reason}\n"
                    f"Strict Mode: {fail_scorer.strict_mode}\n"
                    f"Evaluation Model: {fail_scorer.evaluation_model}\n"
                    f"Error: {fail_scorer.error}\n"
                    f"Additional Metadata: {fail_scorer.additional_metadata}\n"
                )
            error_msg += "-" * 100

        total_tests = len(scoring_results)
        failed_tests = len(failed_cases)
        passed_tests = total_tests - failed_tests

        # Print summary with colors
        rprint("\n" + "=" * 80)
        if failed_tests == 0:
            rprint(
                f"[bold green]🎉 ALL TESTS PASSED! {passed_tests}/{total_tests} tests successful[/bold green]"
            )
        else:
            rprint(
                f"[bold red]⚠️  TEST RESULTS: {passed_tests}/{total_tests} passed ({failed_tests} failed)[/bold red]"
            )
        rprint("=" * 80 + "\n")

        # Print individual test cases
        for i, result in enumerate(scoring_results):
            test_num = i + 1
            if result.success:
                rprint(f"[green]✓ Test {test_num}: PASSED[/green]")
            else:
                rprint(f"[red]✗ Test {test_num}: FAILED[/red]")
                if result.scorers_data:
                    for scorer_data in result.scorers_data:
                        if not scorer_data.success:
                            rprint(f"  [yellow]Scorer: {scorer_data.name}[/yellow]")
                            rprint(f"  [red]  Score: {scorer_data.score}[/red]")
                            rprint(f"  [red]  Reason: {scorer_data.reason}[/red]")
                            if scorer_data.error:
                                rprint(f"  [red]  Error: {scorer_data.error}[/red]")
                rprint("  " + "-" * 40)

        rprint("\n" + "=" * 80)
        if failed_tests > 0:
            raise AssertionError(failed_cases)
