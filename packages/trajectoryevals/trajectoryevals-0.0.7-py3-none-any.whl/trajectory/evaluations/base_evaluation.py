from __future__ import annotations

import concurrent.futures as cf
import os
import pickle
import uuid
from collections.abc import Callable
from typing import Any

import requests

from trajectory.common.api.constants import ROOT_API
from trajectory.common.logger import trajectory_logger
from trajectory.evaluations.config_loader import (
    DatasetConfig,
    EvaluationConfig,
    MockAppConfig,
)

try:
    import cloudpickle as cp  # type: ignore[import]
except Exception:  # pragma: no cover - cloudpickle optional
    cp = None


logger = trajectory_logger


class BaseEvaluation:
    """Base class for running dataset-driven agent evaluations."""

    DATASET_TIMEOUT_SECONDS = 30
    HEALTH_TIMEOUT_SECONDS = 10
    EVAL_UPDATE_TIMEOUT_SECONDS = 10

    def run_agent(self, task: str, **agent_kwargs: Any) -> dict[str, Any]:
        """Override in subclasses to execute the actual agent."""
        return {"task": task, "output": None, "trace_id": None}

    def run(
        self,
        config_path: str,
        use_concurrency: bool = False,
        max_workers: int | None = None,
        evaluation_id: str | None = None,
        trace_scorer: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
        num_runs: int = 1,
        **agent_kwargs: Any,
    ) -> list[dict[str, Any]]:
        config = EvaluationConfig.from_file(config_path)
        service_base_url = config.mock_app.resolved_base_url()

        logger.info(
            "Loaded %s dataset configuration(s) from %s",
            len(config.datasets),
            config_path,
        )

        self._ensure_service_is_ready(config.mock_app, service_base_url)

        all_results: list[dict[str, Any]] = []
        for dataset_index, dataset_cfg in enumerate(config.datasets, start=1):
            dataset_results = self._run_single_dataset(
                dataset_config=dataset_cfg,
                service_base_url=service_base_url,
                dataset_idx=dataset_index,
                total_datasets=len(config.datasets),
                use_concurrency=use_concurrency,
                max_workers=max_workers,
                evaluation_id=evaluation_id,
                trace_scorer=trace_scorer,
                num_runs=num_runs,
                **agent_kwargs,
            )
            all_results.extend(dataset_results)

        logger.info(
            "Completed %s dataset run(s). Total collected results: %s",
            len(config.datasets),
            len(all_results),
        )
        return all_results

    def _run_single_dataset(
        self,
        dataset_config: DatasetConfig,
        service_base_url: str,
        dataset_idx: int,
        total_datasets: int,
        use_concurrency: bool = False,
        max_workers: int | None = None,
        evaluation_id: str | None = None,
        trace_scorer: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
        num_runs: int = 1,
        **agent_kwargs: Any,
    ) -> list[dict[str, Any]]:
        if num_runs < 1:
            raise ValueError("num_runs must be >= 1")

        api_base = self._get_required_api_base()
        api_headers = self._build_api_headers()
        dataset = self._fetch_dataset(api_base, dataset_config.dataset_id, api_headers)
        dataset_name = dataset_config.dataset_name or dataset.get(
            "name", dataset_config.dataset_id
        )
        examples = dataset.get("examples") or []

        if dataset_config.task_ids:
            allowed_ids = set(dataset_config.task_ids)
            examples = [
                ex for ex in examples if ex.get("id") and ex.get("id") in allowed_ids
            ]
            logger.info(
                "Dataset %s filtered to %s task(s) based on config",
                dataset_name,
                len(examples),
            )

        logger.info(
            "Dataset %s/%s (%s) contains %s example(s)",
            dataset_idx,
            total_datasets,
            dataset_name,
            len(examples),
        )

        jobs = self._prepare_jobs(
            dataset_config=dataset_config,
            examples=examples,
            service_base_url=service_base_url,
        )

        if not jobs:
            logger.warning(
                "Dataset %s (%s) has no executable jobs. Skipping.",
                dataset_name,
                dataset_config.dataset_id,
            )
            return []

        eval_id = evaluation_id or str(uuid.uuid4())
        logger.info(
            "Starting evaluation %s for dataset %s (%s). Jobs=%s, runs/job=%s",
            eval_id,
            dataset_name,
            dataset_config.dataset_id,
            len(jobs),
            num_runs,
        )

        pickler = cp or pickle
        pickled_self = pickler.dumps(self)

        results: list[dict[str, Any]] = []
        scores_by_example: dict[str, list[float]] = {}

        worker_count = max_workers or len(jobs) or 1
        if not use_concurrency:
            worker_count = 1

        with cf.ProcessPoolExecutor(max_workers=worker_count) as pool:
            futures: list[tuple[tuple[str | None, str | None, int], cf.Future]] = []
            for run_idx in range(num_runs):
                for job in jobs:
                    metadata = {
                        **(job.get("metadata") or {}),
                        "run_index": run_idx,
                    }
                    future = pool.submit(
                        _worker_run_pickled,
                        pickled_self,
                        job["task"],
                        metadata,
                        job["env"],
                        agent_kwargs,
                        eval_id,
                    )
                    futures.append(
                        (
                            (job.get("dataset_id"), job.get("example_id"), run_idx),
                            future,
                        )
                    )

            logger.info(
                "Submitted %s execution(s) using %s process worker(s)",
                len(futures),
                worker_count,
            )

            for (did, eid, run_idx), fut in futures:
                out = fut.result()
                trace_id = (out or {}).get("trace_id")
                score = (out or {}).get("score")

                score_from_callback = None
                if trace_id and trace_scorer:
                    try:
                        score_from_callback = trace_scorer(
                            trace_id,
                            {
                                "dataset_id": did,
                                "example_id": eid,
                                "task": (out or {}).get("task"),
                                "evaluation_id": eval_id,
                            },
                        )
                    except Exception as exc:  # pragma: no cover - user hook
                        logger.warning(
                            "trace_scorer raised for example %s run %s: %s",
                            eid,
                            run_idx,
                            exc,
                        )

                final_score = score if score is not None else score_from_callback
                if eid and final_score is not None:
                    scores_by_example.setdefault(eid, []).append(float(final_score))

                results.append(
                    {
                        "dataset_id": did,
                        "example_id": eid,
                        "evaluation_id": eval_id,
                        "run_index": run_idx,
                        **(out or {}),
                        **({"score": final_score} if final_score is not None else {}),
                    }
                )

        results_summary = self._summarize_scores(
            scores_by_example=scores_by_example,
            num_runs=num_runs,
        )

        self._update_evaluation_run(
            api_base=api_base,
            headers=api_headers,
            eval_id=eval_id,
            jobs_total=len(jobs),
            dataset_ids=[dataset_config.dataset_id],
            results_summary=results_summary,
            completed_examples=len(scores_by_example) or len(jobs),
        )

        return results

    def _prepare_jobs(
        self,
        dataset_config: DatasetConfig,
        examples: list[dict[str, Any]],
        service_base_url: str,
    ) -> list[dict[str, Any]]:
        jobs: list[dict[str, Any]] = []
        for idx, example in enumerate(examples, start=1):
            task_prompt = (example.get("task_prompt") or "").strip()
            if not task_prompt:
                logger.warning(
                    "Example %s missing task_prompt. Skipping.", example.get("id")
                )
                continue

            instance_id = str(example.get("id") or uuid.uuid4())
            env_overrides = {
                dataset_config.env_variable_to_override: f"{service_base_url.rstrip('/')}/{instance_id}",
            }

            scorer_cfg: dict[str, Any] = {}
            if example.get("scorer"):
                if isinstance(example["scorer"], dict):
                    scorer_cfg = example["scorer"]
            elif example.get("scorer_fn") or example.get("scorer_args"):
                scorer_cfg = {
                    "fn": example.get("scorer_fn"),
                    "args": example.get("scorer_args") or {},
                }
            else:
                scorer_cfg = self._default_scorer_for_index(idx)

            metadata = {
                "example_id": example.get("id"),
                "user_id": example.get("user_id"),
                "instance_id": instance_id,
            }
            if scorer_cfg:
                metadata["scorer"] = scorer_cfg

            jobs.append(
                {
                    "dataset_id": dataset_config.dataset_id,
                    "example_id": example.get("id"),
                    "instance_id": instance_id,
                    "task": task_prompt,
                    "env": env_overrides,
                    "metadata": metadata,
                }
            )

        logger.info(
            "Prepared %s job(s) for dataset %s",
            len(jobs),
            dataset_config.dataset_name,
        )
        return jobs

    def _default_scorer_for_index(self, example_index: int) -> dict[str, Any]:
        if example_index == 1:
            return {
                "fn": "trajectory.evaluations.base_evaluation:demo_score_task_a",
                "args": {"expected": "create", "weight": 2},
            }
        if example_index == 2:
            return {
                "fn": "trajectory.evaluations.base_evaluation:demo_score_task_b",
                "args": {"expected": "approve", "weight": 1},
            }
        return {}

    def _get_required_api_base(self) -> str:
        return ROOT_API.rstrip("/")

    def _build_api_headers(self) -> dict[str, str]:
        api_key = os.environ.get("TRAJECTORY_API_KEY")
        if not api_key:
            raise RuntimeError("TRAJECTORY_API_KEY must be set for evaluations.")
        return {"Authorization": f"Bearer {api_key}"}

    def _fetch_dataset(
        self,
        api_base: str,
        dataset_id: str,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        url = f"{api_base}/api/datasets/{dataset_id}/"
        try:
            response = requests.get(
                url, headers=headers, timeout=self.DATASET_TIMEOUT_SECONDS
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to fetch dataset {dataset_id}: {exc}") from exc
        data = response.json() or {}
        if "examples" not in data:
            raise ValueError(f"Dataset {dataset_id} response missing 'examples'")
        return data

    def _ensure_service_is_ready(self, mock_app: MockAppConfig, base_url: str) -> None:
        health_url = f"{base_url}/health"
        try:
            response = requests.get(health_url, timeout=self.HEALTH_TIMEOUT_SECONDS)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(
                f"{mock_app.name or 'Application'} backend is unavailable. "
                "Start it with `traj up --config-file <path>` or ensure the "
                f"service at {base_url} is reachable."
            ) from exc

    def _summarize_scores(
        self,
        scores_by_example: dict[str, list[float]],
        num_runs: int,
    ) -> dict[str, Any] | None:
        if num_runs <= 1 or not scores_by_example:
            return None

        try:
            import numpy as np  # type: ignore
        except Exception:  # pragma: no cover - optional dependency
            logger.warning("NumPy unavailable. Skipping evaluation statistics.")
            return None

        per_example: dict[str, dict[str, float | int]] = {}
        all_scores: list[float] = []
        for example_id, scores in scores_by_example.items():
            if not scores:
                continue

            scores_arr = np.array(scores)
            per_example[example_id] = {
                "mean": float(np.mean(scores_arr)),
                "std_dev": float(np.std(scores_arr)),
                "median": float(np.percentile(scores_arr, 50)),
                "p95": float(np.percentile(scores_arr, 95)),
                "p99": float(np.percentile(scores_arr, 99)),
                "min": float(np.min(scores_arr)),
                "max": float(np.max(scores_arr)),
                "count": len(scores),
            }
            all_scores.extend(scores)

        if not all_scores:
            return None

        all_scores_arr = np.array(all_scores)
        overall = {
            "mean": float(np.mean(all_scores_arr)),
            "std_dev": float(np.std(all_scores_arr)),
            "median": float(np.percentile(all_scores_arr, 50)),
            "p95": float(np.percentile(all_scores_arr, 95)),
            "p99": float(np.percentile(all_scores_arr, 99)),
            "min": float(np.min(all_scores_arr)),
            "max": float(np.max(all_scores_arr)),
            "count": len(all_scores),
            "num_examples": len(scores_by_example),
        }

        logger.info(
            "Evaluation statistics: mean=%s median=%s std=%s "
            "min=%s max=%s total_runs=%s",
            overall["mean"],
            overall["median"],
            overall["std_dev"],
            overall["min"],
            overall["max"],
            overall["count"],
        )

        return {"per_example": per_example, "overall": overall, "num_runs": num_runs}

    def _update_evaluation_run(
        self,
        api_base: str,
        headers: dict[str, str],
        eval_id: str,
        jobs_total: int,
        dataset_ids: list[str],
        results_summary: dict[str, Any] | None,
        completed_examples: int,
    ) -> None:
        payload: dict[str, Any] = {
            "status": "completed",
            "completed_examples": completed_examples,
            "total_examples": jobs_total,
            "dataset_ids": dataset_ids,
        }
        if results_summary:
            payload["results_summary"] = results_summary

        url = f"{api_base}/api/evaluation-runs/{eval_id}/update/"
        try:
            response = requests.patch(
                url,
                json=payload,
                headers=headers,
                timeout=self.EVAL_UPDATE_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to update evaluation {eval_id}: {exc}") from exc


def demo_score_task_a(
    trace: dict[str, Any], args: dict[str, Any], ctx: dict[str, Any]
) -> dict[str, Any]:
    logger.debug(
        "[demo scorer A] trace_id=%s args=%s ctx=%s",
        trace.get("trace_id"),
        args,
        ctx,
    )
    return {"score": 1, "scorer": "demo_task_a", "args": args}


def demo_score_task_b(
    trace: dict[str, Any], args: dict[str, Any], ctx: dict[str, Any]
) -> dict[str, Any]:
    logger.debug(
        "[demo scorer B] trace_id=%s args=%s ctx=%s",
        trace.get("trace_id"),
        args,
        ctx,
    )
    return {"score": 0, "scorer": "demo_task_b", "args": args}


def _worker_run_pickled(
    pickled_self: bytes,
    task: str,
    metadata: dict[str, Any] | None,
    env_overrides: dict[str, str] | None,
    agent_kwargs: dict[str, Any],
    evaluation_id: str | None,
) -> dict[str, Any]:
    prev_env: dict[str, str | None] = {}
    try:
        if env_overrides:
            for key, value in env_overrides.items():
                prev_env[key] = os.environ.get(key)
                os.environ[key] = value

        try:
            from trajectory.common.tracer.core import set_global_evaluation_metadata

            eval_metadata = {
                "evaluation_id": evaluation_id,
                "scorer": (metadata or {}).get("scorer"),
                "task_id": (metadata or {}).get("example_id"),
                "user_id": (metadata or {}).get("user_id"),
                "run_index": (metadata or {}).get("run_index", 0),
            }
            set_global_evaluation_metadata(eval_metadata)
        except Exception as exc:  # pragma: no cover - logging best effort
            logger.warning("Could not set evaluation metadata: %s", exc)

        pickler = cp or pickle
        base_eval: BaseEvaluation = pickler.loads(pickled_self)
        result = base_eval.run_agent(
            task=task, metadata=metadata, **(agent_kwargs or {})
        )

        trace_id = None
        score = None
        try:
            from trajectory.common.tracer.core import (
                get_last_evaluation_score,
                get_last_evaluation_trace_id,
            )

            score = get_last_evaluation_score()
            trace_id = get_last_evaluation_trace_id()
            logger.debug(
                "Worker finished task with trace_id=%s score=%s", trace_id, score
            )
        except Exception as exc:  # pragma: no cover - logging best effort
            logger.warning("Could not read evaluation score metadata: %s", exc)

        return {**result, "trace_id": trace_id, "score": score}
    finally:
        if env_overrides:
            for key, previous_value in prev_env.items():
                if previous_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = previous_value
