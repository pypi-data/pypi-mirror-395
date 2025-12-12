import os
from typing import Any, TypedDict

ROOT_API = os.getenv("TRAJECTORY_API_URL", "http://api.trajectoryevals.com")
# Traces API
TRAJECTORY_TRACES_FETCH_API_URL = f"{ROOT_API}/traces/fetch/"
TRAJECTORY_TRACES_SAVE_API_URL = f"{ROOT_API}/traces/save/"
TRAJECTORY_TRACES_UPSERT_API_URL = f"{ROOT_API}/traces/upsert/"
TRAJECTORY_TRACES_DELETE_API_URL = f"{ROOT_API}/traces/delete/"
TRAJECTORY_TRACES_SPANS_BATCH_API_URL = f"{ROOT_API}/traces/spans/batch/"
TRAJECTORY_TRACES_EVALUATION_RUNS_BATCH_API_URL = (
    f"{ROOT_API}/traces/evaluation_runs/batch/"
)


class TraceFetchPayload(TypedDict):
    trace_id: str


class TraceDeletePayload(TypedDict):
    trace_ids: list[str]


class SpansBatchPayload(TypedDict):
    spans: list[dict[str, Any]]
    organization_id: str


class EvaluationEntryResponse(TypedDict):
    evaluation_run: dict[str, Any]
    associated_span: dict[str, Any]
    queued_at: float | None


class EvaluationRunsBatchPayload(TypedDict):
    organization_id: str
    evaluation_entries: list[EvaluationEntryResponse]


# Evaluation API
TRAJECTORY_EVAL_API_URL = f"{ROOT_API}/evaluate/"
TRAJECTORY_TRACE_EVAL_API_URL = f"{ROOT_API}/evaluate_trace/"
TRAJECTORY_EVAL_LOG_API_URL = f"{ROOT_API}/log_eval_results/"
TRAJECTORY_EVAL_FETCH_API_URL = f"{ROOT_API}/fetch_experiment_run/"
TRAJECTORY_EVAL_DELETE_API_URL = (
    f"{ROOT_API}/delete_eval_results_by_project_and_run_names/"
)
TRAJECTORY_EVAL_DELETE_PROJECT_API_URL = f"{ROOT_API}/delete_eval_results_by_project/"
TRAJECTORY_ADD_TO_RUN_EVAL_QUEUE_API_URL = f"{ROOT_API}/add_to_run_eval_queue/"
TRAJECTORY_GET_EVAL_STATUS_API_URL = f"{ROOT_API}/get_evaluation_status/"
TRAJECTORY_CHECK_EXPERIMENT_TYPE_API_URL = f"{ROOT_API}/check_experiment_type/"
TRAJECTORY_EVAL_RUN_NAME_EXISTS_API_URL = f"{ROOT_API}/eval-run-name-exists/"


# Evaluation API Payloads
class EvalRunRequestBody(TypedDict):
    eval_name: str
    project_name: str
    trajectory_api_key: str


class DeleteEvalRunRequestBody(TypedDict):
    eval_names: list[str]
    project_name: str
    trajectory_api_key: str


class EvalLogPayload(TypedDict):
    results: list[dict[str, Any]]
    run: dict[str, Any]


class EvalStatusPayload(TypedDict):
    eval_name: str
    project_name: str
    trajectory_api_key: str


class CheckExperimentTypePayload(TypedDict):
    eval_name: str
    project_name: str
    trajectory_api_key: str
    is_trace: bool


class EvalRunNameExistsPayload(TypedDict):
    eval_name: str
    project_name: str
    trajectory_api_key: str


# Datasets API
TRAJECTORY_DATASETS_PUSH_API_URL = f"{ROOT_API}/datasets/push/"
TRAJECTORY_DATASETS_APPEND_EXAMPLES_API_URL = f"{ROOT_API}/datasets/insert_examples/"
TRAJECTORY_DATASETS_PULL_API_URL = f"{ROOT_API}/datasets/pull_for_trajectory/"
TRAJECTORY_DATASETS_DELETE_API_URL = f"{ROOT_API}/datasets/delete/"
TRAJECTORY_DATASETS_EXPORT_JSONL_API_URL = f"{ROOT_API}/datasets/export_jsonl/"
TRAJECTORY_DATASETS_PROJECT_STATS_API_URL = (
    f"{ROOT_API}/datasets/fetch_stats_by_project/"
)
TRAJECTORY_DATASETS_INSERT_API_URL = f"{ROOT_API}/datasets/insert_examples/"


class DatasetPushPayload(TypedDict):
    dataset_alias: str
    project_name: str
    examples: list[dict[str, Any]]
    traces: list[dict[str, Any]]
    overwrite: bool


class DatasetAppendPayload(TypedDict):
    dataset_alias: str
    project_name: str
    examples: list[dict[str, Any]]


class DatasetPullPayload(TypedDict):
    dataset_alias: str
    project_name: str


class DatasetDeletePayload(TypedDict):
    dataset_alias: str
    project_name: str


class DatasetExportPayload(TypedDict):
    dataset_alias: str
    project_name: str


class DatasetStatsPayload(TypedDict):
    project_name: str


# Projects API
TRAJECTORY_PROJECT_DELETE_API_URL = f"{ROOT_API}/projects/delete/"
TRAJECTORY_PROJECT_CREATE_API_URL = f"{ROOT_API}/projects/add/"


class ProjectDeletePayload(TypedDict):
    project_list: list[str]


class ProjectCreatePayload(TypedDict):
    project_name: str


TRAJECTORY_SCORER_SAVE_API_URL = f"{ROOT_API}/save_scorer/"
TRAJECTORY_SCORER_FETCH_API_URL = f"{ROOT_API}/fetch_scorer/"
TRAJECTORY_SCORER_EXISTS_API_URL = f"{ROOT_API}/scorer_exists/"


class ScorerSavePayload(TypedDict):
    name: str
    prompt: str
    options: dict


class ScorerFetchPayload(TypedDict):
    name: str


class ScorerExistsPayload(TypedDict):
    name: str
