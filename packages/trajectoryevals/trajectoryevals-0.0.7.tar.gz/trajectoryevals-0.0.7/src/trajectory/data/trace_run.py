from typing import Any, Union

from pydantic import BaseModel

from trajectory.data import Trace
from trajectory.rules import Rule
from trajectory.scorers import APIScorerConfig, BaseScorer


class TraceRun(BaseModel):
    """
    Stores example and evaluation scorers together for running an eval task

    Args:
        project_name (str): The name of the project the evaluation results belong to
        eval_name (str): A name for this evaluation run
        traces (List[Trace]): The traces to evaluate
        scorers (List[Union[TrajectoryScorer, BaseScorer]]): A list of scorers to use for evaluation
        model (str): The model used as a judge when using LLM as a Judge
        metadata (Optional[Dict[str, Any]]): Additional metadata to include for this evaluation run, e.g. comments, dataset name, purpose, etc.
        rules (Optional[List[Rule]]): Rules to evaluate against scoring results
        append (Optional[bool]): Whether to append to existing evaluation results
        tools (Optional[List[Dict[str, Any]]]): List of tools to use for evaluation
    """

    organization_id: str | None = None
    project_name: str | None = None
    eval_name: str | None = None
    traces: list[Trace] | None = None
    scorers: list[Union[APIScorerConfig, BaseScorer]]
    model: str | None = "gpt-4.1"
    trace_span_id: str | None = None
    append: bool | None = False
    override: bool | None = False
    rules: list[Rule] | None = None
    tools: list[dict[str, Any]] | None = None

    class Config:
        arbitrary_types_allowed = True
