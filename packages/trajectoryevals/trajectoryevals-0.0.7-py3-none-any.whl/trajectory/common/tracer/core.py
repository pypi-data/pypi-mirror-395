"""
Tracing system for trajectory that allows for function tracing using decorators.
"""

from __future__ import annotations

import asyncio
import atexit
import contextvars
import functools
import importlib
import inspect
import json
import os
import sys
import threading
import time
import traceback
import types
import uuid
from collections.abc import Callable, Generator
from contextlib import (
    contextmanager,
)
from datetime import UTC, datetime
from typing import (
    Any,
    Optional,
    TypeAlias,
    Union,
)

from anthropic import Anthropic, AsyncAnthropic
from google import genai
from litellm import cost_per_token as _original_cost_per_token
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ParsedChatCompletion
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.responses.response import Response
from together import AsyncTogether, Together

from trajectory.common.api.constants import ROOT_API
from trajectory.common.local_trace_storage import (
    LocalTraceStorage,
    get_local_storage_dir,
    is_local_tracing_enabled,
    is_only_local_tracing_enabled,
)
from trajectory.common.logger import (
    configure_trajectory_logger,
    reconfigure_logger,
    trajectory_logger,
)
from trajectory.common.tracer.constants import _TRACE_FILEPATH_BLOCKLIST
from trajectory.common.tracer.otel_span_processor import TrajectorySpanProcessor
from trajectory.common.tracer.span_processor import SpanProcessorBase
from trajectory.common.tracer.trace_manager import TraceManagerClient
from trajectory.common.utils import ExcInfo, validate_api_key
from trajectory.data import Example, Trace, TraceSpan, TraceUsage
from trajectory.evaluation_run import EvaluationRun
from trajectory.scorers import APIScorerConfig, BaseScorer
from trajectory.verifiers.models import VerifierConfig
from trajectory.verifiers.runner import AsyncVerifierRunner

try:
    # Optional import used to access context tracer during evaluation runs
    from trajectory.run_evaluation import TRACE_VAR as EVAL_TRACE_VAR
except Exception:
    EVAL_TRACE_VAR = None

try:
    # Optional dependency used for posting verification results to a backend
    import requests  # type: ignore
except Exception:
    requests = None  # type: ignore

try:
    # Internal optional storage backend
    from trajectory.common.storage.s3_storage import S3Storage
except Exception:
    S3Storage = None  # type: ignore


current_trace_var = contextvars.ContextVar[Optional["TraceClient"]](
    "current_trace", default=None
)
current_span_var = contextvars.ContextVar[Optional[str]]("current_span", default=None)

# Add conversation context variable
conversation_id_var = contextvars.ContextVar("conversation_id", default=None)
user_id_var = contextvars.ContextVar("user_id", default=None)


# Global evaluation metadata - single source of truth
GLOBAL_EVALUATION_METADATA: Optional[dict[str, Any]] = None

# Context variable to store the score from the current evaluation
_evaluation_score_var = contextvars.ContextVar("_evaluation_score", default=None)
_evaluation_trace_id_var = contextvars.ContextVar("_evaluation_trace_id", default=None)


def set_global_evaluation_metadata(metadata: Optional[dict[str, Any]]) -> None:
    """
    Set evaluation metadata for the current worker process.

    Expected structure:
    {
        "evaluation_id": "uuid-string",
        "scorer": {
            "fn": "module_path:function_name",
            "args": {...}
        },
        "task_id": "uuid-string",  # dataset_example UUID
        "user_id": "user-uuid",
        ... any other metadata
    }
    """
    global GLOBAL_EVALUATION_METADATA
    GLOBAL_EVALUATION_METADATA = metadata or {}

    if metadata:
        trajectory_logger.debug("Set evaluation metadata")
        trajectory_logger.debug(f"evaluation_id: {metadata.get('evaluation_id')}")
        trajectory_logger.debug(f"task_id: {metadata.get('task_id')}")
        trajectory_logger.debug(f"user_id: {metadata.get('user_id')}")
        scorer = metadata.get("scorer")
        trajectory_logger.debug(f"scorer: {scorer.get('fn') if scorer else None}")


def get_global_evaluation_metadata() -> Optional[dict[str, Any]]:
    """Get the full evaluation metadata dict"""
    return GLOBAL_EVALUATION_METADATA or {}


def get_last_evaluation_score() -> Optional[Any]:
    """Get the score from the last evaluation that ran in this context"""
    try:
        return _evaluation_score_var.get()
    except Exception:
        return None


def get_last_evaluation_trace_id() -> Optional[str]:
    """Get the trace_id from the last evaluation that ran in this context"""
    try:
        return _evaluation_trace_id_var.get()
    except Exception:
        return None


def _set_evaluation_score(score: Any) -> None:
    """Internal: Store the score from an evaluation"""
    try:
        _evaluation_score_var.set(score)
    except Exception:
        pass


def _set_evaluation_trace_id(trace_id: str) -> None:
    """Internal: Store the trace_id from an evaluation"""
    try:
        _evaluation_trace_id_var.set(trace_id)
    except Exception:
        pass


def create_evaluation_result(
    evaluation_id: str,
    task_id: str,
    trace_id: str,
    user_id: str,
    results: dict[str, Any],
    run_index: int = 0,
) -> None:
    """Create an evaluation_results record in Supabase after scorer runs"""
    try:
        import requests

        if not all([evaluation_id, task_id, trace_id, user_id]):
            trajectory_logger.warning("Missing required fields for evaluation_results")
            return

        payload = {
            "evaluation_id": evaluation_id,
            "task_id": task_id,
            "trace_id": trace_id,
            "user_id": user_id,
            "results": results or {},
            "run_index": run_index,
        }

        # Try backend API
        backend_base = ROOT_API
        if backend_base:
            try:
                api_key = os.environ.get("TRAJECTORY_API_KEY")
                headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

                response = requests.post(
                    f"{backend_base}/api/evaluation-runs/{evaluation_id}/results/",
                    json=payload,
                    headers=headers,
                    timeout=10,
                )
                if response.status_code in (200, 201):
                    trajectory_logger.info(
                        f"Created evaluation_result for trace {trace_id}"
                    )
                    return
            except Exception as e:
                trajectory_logger.debug(f"Backend API failed: {e}")

        # Fallback to direct Supabase insert
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get(
            "SUPABASE_ANON_KEY"
        )

        if supabase_url and supabase_key:
            try:
                headers = {
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal",
                }

                response = requests.post(
                    f"{supabase_url}/rest/v1/evaluation_results",
                    json=payload,
                    headers=headers,
                    timeout=10,
                )
                if response.status_code in (200, 201):
                    trajectory_logger.info(
                        f"Created evaluation_result in Supabase for trace {trace_id}"
                    )
                elif response.status_code == 409:
                    # 409 Conflict means entry already exists (unique constraint) - this is fine
                    trajectory_logger.debug(
                        f"Evaluation result already exists for trace {trace_id}"
                    )
                else:
                    trajectory_logger.warning(
                        f"Supabase insert error: {response.status_code}"
                    )
            except Exception as e:
                trajectory_logger.warning(f"Supabase insert failed: {e}")

    except Exception as e:
        trajectory_logger.error(f"Error creating evaluation_result: {e}")


ApiClient: TypeAlias = Union[
    OpenAI,
    Together,
    Anthropic,
    AsyncOpenAI,
    AsyncAnthropic,
    AsyncTogether,
    genai.Client,
    genai.client.AsyncClient,
]
SpanType: TypeAlias = str


class TraceClient:
    """Client for managing a single trace context"""

    def __init__(
        self,
        tracer: Tracer,
        trace_id: str | None = None,
        name: str = "default",
        project_name: str | None = None,
        enable_monitoring: bool = True,
        enable_evaluations: bool = True,
        parent_trace_id: str | None = None,
        parent_name: str | None = None,
        evaluation_id: str | None = None,
        is_evaluation: bool = False,
    ):
        self.name = name
        self.trace_id = trace_id or str(uuid.uuid4())
        self.project_name = project_name or "default_project"
        self.tracer = tracer
        self.enable_monitoring = enable_monitoring
        self.enable_evaluations = enable_evaluations
        self.parent_trace_id = parent_trace_id
        self.parent_name = parent_name
        self.customer_id: str | None = None
        self.tags: list[Union[str, set, tuple]] = []
        self.metadata: dict[str, Any] = {}
        self.has_notification: bool | None = False
        self.update_id: int = 1
        self.trace_spans: list[TraceSpan] = []
        self.span_id_to_span: dict[str, TraceSpan] = {}
        self.evaluation_runs: list[EvaluationRun] = []
        self.start_time: Optional[float] = None
        eval_metadata = get_global_evaluation_metadata()
        self.evaluation_id: Optional[str] = (
            eval_metadata.get("evaluation_id") if eval_metadata else None
        )
        self.is_evaluation: bool = self.evaluation_id is not None
        self.trace_manager_client = TraceManagerClient(
            tracer.api_key, tracer.organization_id, tracer
        )
        self._span_depths: dict[str, int] = {}
        eval_metadata = get_global_evaluation_metadata()
        self.evaluation_id: Optional[str] = (
            eval_metadata.get("evaluation_id") if eval_metadata else None
        )
        self.is_evaluation: bool = self.evaluation_id is not None
        self.otel_span_processor = tracer.otel_span_processor

        # Get conversation ID from context
        self.conversation_id = conversation_id_var.get()
        self.user_id = user_id_var.get()

        trajectory_logger.info(
            f"🎯 TraceClient using span processor for trace {self.trace_id}"
        )
        trajectory_logger.debug(f"TraceClient created with trace_id: {self.trace_id}")

    def get_current_span(self):
        """Get the current span from the context var"""
        return self.tracer.get_current_span()

    def set_current_span(self, span: Any):
        """Set the current span from the context var"""
        return self.tracer.set_current_span(span)

    def reset_current_span(self, token: Any):
        """Reset the current span from the context var"""
        self.tracer.reset_current_span(token)

    @contextmanager
    def span(self, name: str, span_type: SpanType = "span"):
        """Context manager for creating a trace span, managing the current span via contextvars"""
        is_first_span = len(self.trace_spans) == 0
        if is_first_span:
            try:
                self.save(final_save=False)
            except Exception as e:
                trajectory_logger.warning(
                    f"Failed to save initial trace for live tracking: {e}"
                )
        start_time = time.time()

        span_id = str(uuid.uuid4())

        parent_span_id = self.get_current_span()
        token = self.set_current_span(span_id)

        current_depth = 0
        if parent_span_id and parent_span_id in self._span_depths:
            current_depth = self._span_depths[parent_span_id] + 1

        self._span_depths[span_id] = current_depth

        span = TraceSpan(
            span_id=span_id,
            trace_id=self.trace_id,
            depth=current_depth,
            message=name,
            created_at=start_time,
            span_type=span_type,
            parent_span_id=parent_span_id,
            function=name,
        )
        self.add_span(span)

        # attach end-user / tenant info onto the span
        try:
            meta = getattr(span, "additional_metadata", None) or {}
            if self.customer_id:
                meta["tenant.id"] = self.customer_id
            if self.end_user_id:
                meta["enduser.id"] = self.end_user_id
            span.additional_metadata = meta
        except Exception:
            pass

        trajectory_logger.debug(
            f"Span started | trace_id={self.trace_id} span_id={span_id} name={name} type={span_type} depth={current_depth} parent={parent_span_id}"
        )
        self.otel_span_processor.queue_span_update(span, span_state="input")

        try:
            yield self
        finally:
            duration = time.time() - start_time
            span.duration = duration

            trajectory_logger.debug(
                f"Span completed | trace_id={self.trace_id} span_id={span_id} duration={duration:.3f}s"
            )
            self.otel_span_processor.queue_span_update(span, span_state="completed")

            if span_id in self._span_depths:
                del self._span_depths[span_id]
            self.reset_current_span(token)

    def async_evaluate(
        self,
        scorers: list[Union[APIScorerConfig, BaseScorer]],
        example: Example | None = None,
        input: str | None = None,
        actual_output: Union[str, list[str]] | None = None,
        expected_output: Union[str, list[str]] | None = None,
        context: list[str] | None = None,
        retrieval_context: list[str] | None = None,
        tools_called: list[str] | None = None,
        expected_tools: list[str] | None = None,
        additional_metadata: dict[str, Any] | None = None,
        model: str | None = None,
        span_id: str | None = None,
    ):
        if not self.enable_evaluations:
            return

        start_time = time.time()

        try:
            if not scorers:
                trajectory_logger.warning("No valid scorers available for evaluation")
                return

        except Exception as e:
            trajectory_logger.warning(f"Failed to load scorers: {e!s}")
            return

        if example is None:
            if any(
                param is not None
                for param in [
                    input,
                    actual_output,
                    expected_output,
                    context,
                    retrieval_context,
                    tools_called,
                    expected_tools,
                    additional_metadata,
                ]
            ):
                example = Example(
                    input=input,
                    actual_output=actual_output,
                    expected_output=expected_output,
                    context=context,
                    retrieval_context=retrieval_context,
                    tools_called=tools_called,
                    expected_tools=expected_tools,
                    additional_metadata=additional_metadata,
                )
            else:
                raise ValueError(
                    "Either 'example' or at least one of the individual parameters (input, actual_output, etc.) must be provided"
                )

        span_id_to_use = span_id if span_id is not None else self.get_current_span()

        eval_run = EvaluationRun(
            organization_id=self.tracer.organization_id,
            project_name=self.project_name,
            eval_name=f"{self.name.capitalize()}-"
            f"{span_id_to_use}-"
            f"[{','.join(scorer.score_type.capitalize() for scorer in scorers)}]",
            examples=[example],
            scorers=scorers,
            model=model,
            trajectory_api_key=self.tracer.api_key,
            trace_span_id=span_id_to_use,
        )

        self.add_eval_run(eval_run, start_time)

        if span_id_to_use:
            current_span = self.span_id_to_span.get(span_id_to_use)
            if current_span:
                self.otel_span_processor.queue_evaluation_run(
                    eval_run, span_id=span_id_to_use, span_data=current_span
                )

    def add_eval_run(self, eval_run: EvaluationRun, start_time: float):
        current_span_id = eval_run.trace_span_id

        if current_span_id:
            span = self.span_id_to_span[current_span_id]
            span.has_evaluation = True
        self.evaluation_runs.append(eval_run)

    def record_input(self, inputs: dict):
        current_span_id = self.get_current_span()
        if current_span_id:
            span = self.span_id_to_span[current_span_id]
            inputs.pop("self", None)
            span.inputs = inputs
            trajectory_logger.debug(
                f"Recorded inputs | trace_id={self.trace_id} span_id={current_span_id} keys={list(inputs.keys())}"
            )
            try:
                self.otel_span_processor.queue_span_update(span, span_state="input")
            except Exception as e:
                trajectory_logger.warning(f"Failed to queue span with input data: {e}")

    def record_agent_name(self, agent_name: str):
        current_span_id = self.get_current_span()
        if current_span_id:
            span = self.span_id_to_span[current_span_id]
            span.agent_name = agent_name

            self.otel_span_processor.queue_span_update(span, span_state="agent_name")

    def record_state_before(self, state: dict):
        """Records the agent's state before a tool execution on the current span.

        Args:
            state: A dictionary representing the agent's state.
        """
        current_span_id = self.get_current_span()
        if current_span_id:
            span = self.span_id_to_span[current_span_id]
            span.state_before = state

            self.otel_span_processor.queue_span_update(span, span_state="state_before")

    def record_state_after(self, state: dict):
        """Records the agent's state after a tool execution on the current span.

        Args:
            state: A dictionary representing the agent's state.
        """
        current_span_id = self.get_current_span()
        if current_span_id:
            span = self.span_id_to_span[current_span_id]
            span.state_after = state

            self.otel_span_processor.queue_span_update(span, span_state="state_after")

    async def _update_coroutine(self, span: TraceSpan, coroutine: Any, field: str):
        """Helper method to update the output of a trace entry once the coroutine completes"""
        try:
            result = await coroutine
            setattr(span, field, result)

            if field == "output":
                self.otel_span_processor.queue_span_update(span, span_state="output")

            return result
        except Exception as e:
            setattr(span, field, f"Error: {e!s}")

            if field == "output":
                self.otel_span_processor.queue_span_update(span, span_state="output")

            raise

    def record_output(self, output: Any):
        current_span_id = self.get_current_span()
        if current_span_id:
            span = self.span_id_to_span[current_span_id]
            span.output = "<pending>" if inspect.iscoroutine(output) else output
            trajectory_logger.debug(
                f"Recorded output | trace_id={self.trace_id} span_id={current_span_id} is_coroutine={inspect.iscoroutine(output)}"
            )
            if inspect.iscoroutine(output):
                asyncio.create_task(self._update_coroutine(span, output, "output"))

            if not inspect.iscoroutine(output):
                self.otel_span_processor.queue_span_update(span, span_state="output")

            return span
        return None

    def record_usage(self, usage: TraceUsage):
        current_span_id = self.get_current_span()
        if current_span_id:
            span = self.span_id_to_span[current_span_id]
            span.usage = usage
            trajectory_logger.debug(
                f"Recorded usage | trace_id={self.trace_id} span_id={current_span_id} tokens={getattr(usage, 'total_tokens', None)}"
            )
            self.otel_span_processor.queue_span_update(span, span_state="usage")

            return span
        return None

    def record_error(self, error: dict[str, Any]):
        current_span_id = self.get_current_span()
        if current_span_id:
            span = self.span_id_to_span[current_span_id]
            span.error = error
            trajectory_logger.error(
                f"Recorded error | trace_id={self.trace_id} span_id={current_span_id} error={error.get('type', 'Unknown')}"
            )
            self.otel_span_processor.queue_span_update(span, span_state="error")

            return span
        return None

    def add_span(self, span: TraceSpan):
        """Add a trace span to this trace context"""
        self.trace_spans.append(span)
        self.span_id_to_span[span.span_id] = span
        return self

    def print(self):
        """Print the complete trace with proper visual structure"""
        for span in self.trace_spans:
            span.print_span()

    def get_duration(self) -> float:
        """
        Get the total duration of this trace
        """
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time

    def save(self, final_save: bool = False) -> tuple[str, dict]:
        """
        Save the current trace to the database with rate limiting checks.
        First checks usage limits, then upserts the trace if allowed.

        Args:
            final_save: Whether this is the final save (updates usage counters)

        Returns a tuple of (trace_id, server_response) where server_response contains the UI URL and other metadata.
        """
        trajectory_logger.debug(
            f"Starting trace save | trace_id={self.trace_id} final_save={final_save}"
        )

        if final_save:
            try:
                trajectory_logger.debug(
                    f"Flushing pending spans for trace {self.trace_id}"
                )
                self.otel_span_processor.flush_pending_spans()
                trajectory_logger.debug(
                    f"Flushed pending spans | trace_id={self.trace_id}"
                )
            except Exception as e:
                trajectory_logger.warning(
                    f"Error flushing spans for trace {self.trace_id}: {e}"
                )

        total_duration = self.get_duration()
        trajectory_logger.debug(
            f"Trace summary | duration={total_duration:.3f}s spans={len(self.trace_spans)}"
        )

        trace_data = {
            "trace_id": self.trace_id,
            "name": self.name,
            "project_name": self.project_name,
            "created_at": datetime.fromtimestamp(
                self.start_time or time.time(), UTC
            ).isoformat(),
            "duration": total_duration,
            "trace_spans": [span.model_dump() for span in self.trace_spans],
            "evaluation_runs": [run.model_dump() for run in self.evaluation_runs],
            "offline_mode": self.tracer.offline_mode,
            "parent_trace_id": self.parent_trace_id,
            "parent_name": self.parent_name,
            "customer_id": self.customer_id,
            "tags": self.tags,
            "metadata": self.metadata,
            "update_id": self.update_id,
            "evaluation_id": self.evaluation_id,
            "is_evaluation": self.is_evaluation,
        }

        # Only add conversation_id if it exists in context
        if self.conversation_id:
            trace_data["conversation_id"] = self.conversation_id
            trajectory_logger.debug(
                f"Added conversation_id to trace: {self.conversation_id}"
            )

        if self.user_id:
            trace_data["user_id"] = self.user_id
            trajectory_logger.debug(f"Added user_id to trace: {self.user_id}")

        # Handle local tracing if enabled
        if self.tracer.enable_local_tracing and self.tracer.local_trace_storage:
            # Run scorer if this is an evaluation AND this is the final save (all spans complete)
            try:
                if self.is_evaluation and final_save:
                    eval_metadata = get_global_evaluation_metadata()
                    scorer_cfg = eval_metadata.get("scorer") if eval_metadata else None
                    trajectory_logger.debug(f"Scorer config: {scorer_cfg}")
                    if (
                        scorer_cfg
                        and isinstance(scorer_cfg, dict)
                        and scorer_cfg.get("fn")
                    ):
                        mod_func = str(scorer_cfg.get("fn") or "")
                        if ":" in mod_func:
                            mod_name, fn_name = mod_func.split(":", 1)
                            task_id = eval_metadata.get("task_id")
                            user_id = eval_metadata.get("user_id")
                            run_index = eval_metadata.get("run_index", 0)
                            scorer_result: dict[str, Any] | None = None
                            scorer_error: dict[str, Any] | None = None
                            try:
                                args = scorer_cfg.get("args") or {}
                                ctx = {
                                    "evaluation_id": self.evaluation_id,
                                    "project_name": self.project_name,
                                    "task_id": task_id,
                                    "user_id": user_id,
                                }
                                trajectory_logger.info(
                                    f"Running scorer fn={mod_name}:{fn_name} args={args} trace_id={trace_data.get('trace_id')} eval_id={self.evaluation_id}"
                                )

                                # Try to import scorer - check multiple locations
                                fn: Any = None

                                # First, try trajectory.scorers module directly
                                try:
                                    scorer_module = importlib.import_module(
                                        "trajectory.scorers"
                                    )
                                    if hasattr(scorer_module, fn_name):
                                        fn = getattr(scorer_module, fn_name)
                                        trajectory_logger.debug(
                                            f"Found scorer in trajectory.scorers: {fn_name}"
                                        )
                                except (ImportError, AttributeError):
                                    pass

                                # If not found, try trajectory.scorers.{mod_name} (e.g., trajectory.scorers.workday_tool_scorer)
                                if fn is None:
                                    try:
                                        scorer_submodule = importlib.import_module(
                                            f"trajectory.scorers.{mod_name}"
                                        )
                                        if hasattr(scorer_submodule, fn_name):
                                            fn = getattr(scorer_submodule, fn_name)
                                            trajectory_logger.debug(
                                                f"Found scorer in trajectory.scorers.{mod_name}: {fn_name}"
                                            )
                                    except (ImportError, AttributeError):
                                        pass

                                # Finally, fall back to dynamic import from specified module
                                if fn is None:
                                    try:
                                        fn = getattr(
                                            importlib.import_module(mod_name), fn_name
                                        )
                                        trajectory_logger.debug(
                                            f"Found scorer via dynamic import: {mod_name}:{fn_name}"
                                        )
                                    except (ImportError, AttributeError) as import_err:
                                        raise ImportError(
                                            f"Could not import scorer {mod_name}:{fn_name}. "
                                            f"Tried: trajectory.scorers.{fn_name}, trajectory.scorers.{mod_name}.{fn_name}, and {mod_name}.{fn_name}. "
                                            f"Make sure the scorer is available in trajectory.scorers or the specified module."
                                        ) from import_err

                                result: Any = None
                                try:
                                    # Preferred: fn(trace_data, args, ctx)
                                    result = fn(trace_data, args, ctx)
                                except TypeError:
                                    # Fallback: fn(trace_data, ctx)
                                    result = fn(trace_data, ctx)
                                trajectory_logger.debug(
                                    f"Scorer result for trace {trace_data.get('trace_id')}: {result}"
                                )
                                if isinstance(result, dict):
                                    scorer_result = result
                                    # Minimal contract: coerce score to int if present and numeric
                                    try:
                                        if (
                                            "score" in scorer_result
                                            and scorer_result["score"] is not None
                                        ):
                                            sc = scorer_result["score"]
                                            if isinstance(sc, bool):
                                                sc = int(sc)
                                            elif isinstance(sc, (int, float, str)):
                                                sc = int(float(sc))
                                            scorer_result["score"] = sc
                                    except Exception:
                                        pass
                                    md = trace_data.get("metadata") or {}
                                    md["trace_score"] = scorer_result
                                    trace_data["metadata"] = md
                                    self.metadata = md

                                    # Store the score and trace_id so they can be retrieved by the evaluation framework
                                    score_value = scorer_result.get("score")
                                    _set_evaluation_score(score_value)
                                    _set_evaluation_trace_id(trace_data.get("trace_id"))
                                elif result is not None:
                                    scorer_result = {"result": result}
                            except Exception as e:
                                scorer_error = {
                                    "error": "scorer_failed",
                                    "message": str(e),
                                    "scorer_fn": mod_func,
                                }
                                trajectory_logger.warning(
                                    f"Issue running per-task scorer: {e}"
                                )
                                md = trace_data.get("metadata") or {}
                                md["trace_score_error"] = scorer_error
                                trace_data["metadata"] = md
                                self.metadata = md
                            finally:
                                if (
                                    task_id
                                    and self.evaluation_id
                                    and trace_data.get("trace_id")
                                ):
                                    create_evaluation_result(
                                        evaluation_id=self.evaluation_id,
                                        task_id=task_id,
                                        trace_id=trace_data.get("trace_id"),
                                        user_id=user_id or self.user_id or "system",
                                        results=scorer_result
                                        or scorer_error
                                        or {"status": "scorer_not_run"},
                                        run_index=run_index,
                                    )
            except Exception as e:
                trajectory_logger.warning(f"Issue in evaluation scoring hook: {e}")

            # Now save/upsert the trace (regardless of scorer success/failure)
            try:
                trajectory_logger.info(
                    f"Local tracing enabled - saving trace locally: {self.trace_id}"
                )
                trajectory_logger.debug(
                    f"Trace data size: {len(str(trace_data))} characters"
                )
                trajectory_logger.debug(
                    f"Number of spans in trace: {len(trace_data.get('trace_spans', []))}"
                )

                self.tracer.local_trace_storage.save_trace(
                    trace_data, self.trace_id, final_save=final_save
                )
                trajectory_logger.info(
                    f"Saved trace locally | trace_id={self.trace_id}"
                )

                # If not in only-local mode, also upsert remotely
                if not self.tracer.only_local_tracing:
                    trajectory_logger.debug(
                        "Local tracing enabled and only_local_tracing is false; upserting trace remotely as well"
                    )
                    server_response = self.trace_manager_client.upsert_trace(
                        trace_data,
                        offline_mode=self.tracer.offline_mode,
                        show_link=not final_save,
                        final_save=final_save,
                    )
                else:
                    # Create a mock server response for local-only tracing
                    server_response = {
                        "ui_results_url": f"file://{self.tracer.local_tracing_dir}/trace_*_{self.trace_id[:8]}.json",
                        "trace_id": self.trace_id,
                        "status": "saved_locally",
                        "local_tracing": True,
                    }
                    trajectory_logger.debug(
                        f"Created local tracing response: {server_response}"
                    )
            except Exception as e:
                trajectory_logger.error(f"Failed to save trace locally: {e}")
                trajectory_logger.debug(f"Local tracing error details: {e!s}")
                # Only fall back to remote tracing if not in only_local_tracing mode
                if not self.tracer.only_local_tracing:
                    trajectory_logger.info(
                        f"Falling back to remote tracing for trace: {self.trace_id}"
                    )
                    server_response = self.trace_manager_client.upsert_trace(
                        trace_data,
                        offline_mode=self.tracer.offline_mode,
                        show_link=not final_save,
                        final_save=final_save,
                    )
                else:
                    # In only_local_tracing mode, create a mock response even if local save fails
                    trajectory_logger.warning(
                        f"Only local tracing enabled but local save failed: {e}"
                    )
                    server_response = {
                        "ui_results_url": f"file://{self.tracer.local_tracing_dir}/trace_*_{self.trace_id[:8]}.json",
                        "trace_id": self.trace_id,
                        "status": "local_save_failed",
                        "local_tracing": True,
                        "error": str(e),
                    }
        else:
            # Use remote tracing only if not in only_local_tracing mode
            if not self.tracer.only_local_tracing:
                server_response = self.trace_manager_client.upsert_trace(
                    trace_data,
                    offline_mode=self.tracer.offline_mode,
                    show_link=not final_save,
                    final_save=final_save,
                )
            else:
                # In only_local_tracing mode but no local storage, create mock response
                server_response = {
                    "ui_results_url": "file://local_tracing_disabled",
                    "trace_id": self.trace_id,
                    "status": "only_local_tracing_enabled_but_no_local_storage",
                    "local_tracing": True,
                }

        if self.start_time is None:
            self.start_time = time.time()

        self.update_id += 1

        return self.trace_id, server_response

    def delete(self):
        return self.trace_manager_client.delete_trace(self.trace_id)

    def update_metadata(self, metadata: dict):
        """
        Set metadata for this trace.

        Args:
            metadata: Metadata as a dictionary

        Supported keys:
        - customer_id: ID of the customer using this trace
        - tags: List of tags for this trace
        - has_notification: Whether this trace has a notification
        - name: Name of the trace
        """
        for k, v in metadata.items():
            if k == "customer_id":
                if v is not None:
                    self.customer_id = str(v)
                else:
                    self.customer_id = None
            elif k == "tags":
                if isinstance(v, list):
                    for item in v:
                        if not isinstance(item, (str, set, tuple)):
                            raise ValueError(
                                f"Tags must be a list of strings, sets, or tuples, got item of type {type(item)}"
                            )
                    self.tags = v
                else:
                    raise ValueError(
                        f"Tags must be a list of strings, sets, or tuples, got {type(v)}"
                    )
            elif k == "has_notification":
                if not isinstance(v, bool):
                    raise ValueError(
                        f"has_notification must be a boolean, got {type(v)}"
                    )
                self.has_notification = v
            elif k == "name":
                self.name = v
            else:
                self.metadata[k] = v

    def set_customer_id(self, customer_id: str):
        """
        Set the customer ID for this trace.

        Args:
            customer_id: The customer ID to set
        """
        self.update_metadata({"customer_id": customer_id})

    def set_tags(self, tags: list[Union[str, set, tuple]]):
        """
        Set the tags for this trace.

        Args:
            tags: List of tags to set
        """
        self.update_metadata({"tags": tags})

    def set_reward_score(self, reward_score: Union[float, dict[str, float]]):
        """
        Set the reward score for this trace to be used for RL or SFT.

        Args:
            reward_score: The reward score to set
        """
        self.update_metadata({"reward_score": reward_score})

    def log_metric(
        self,
        event_name: str,
        properties: dict[str, Any] | None = None,
        value: float | None = None,
        unit: str | None = None,
        tags: list[str] | None = None,
        context_override: dict[str, Any] | None = None,
        persist: bool = False,
    ):
        try:
            ctx_user_id = (context_override or {}).get("user_id", self.user_id)
            ctx_conversation_id = (context_override or {}).get(
                "conversation_id", self.conversation_id
            )

            metrics = self.metadata.get("user_metrics") or []
            metrics.append(
                {
                    "ts": datetime.now(UTC).isoformat(),
                    "event_name": event_name,
                    "value": value,
                    "unit": unit,
                    "tags": tags or [],
                    "properties": properties or {},
                    "user_id": ctx_user_id,
                    "conversation_id": ctx_conversation_id,
                }
            )
            self.metadata["user_metrics"] = metrics

        except Exception as e:
            trajectory_logger.warning(f"Failed to record metric '{event_name}': {e}")


def _capture_exception_for_trace(current_trace: TraceClient | None, exc_info: ExcInfo):
    if not current_trace:
        return

    exc_type, exc_value, exc_traceback_obj = exc_info
    formatted_exception = {
        "type": exc_type.__name__ if exc_type else "UnknownExceptionType",
        "message": str(exc_value) if exc_value else "No exception message",
        "traceback": (
            traceback.format_tb(exc_traceback_obj) if exc_traceback_obj else []
        ),
    }

    # This is where we specially handle exceptions that we might want to collect additional data for.
    # When we do this, always try checking the module from sys.modules instead of importing. This will
    # Let us support a wider range of exceptions without needing to import them for all clients.

    # Most clients (requests, httpx, urllib) support the standard format of exposing error.request.url and error.response.status_code
    # The alternative is to hand select libraries we want from sys.modules and check for them:
    # As an example:  requests_module = sys.modules.get("requests", None) // then do things with requests_module;

    # General HTTP Like errors
    try:
        url = getattr(getattr(exc_value, "request", None), "url", None)
        status_code = getattr(getattr(exc_value, "response", None), "status_code", None)
        if status_code:
            formatted_exception["http"] = {
                "url": url if url else "Unknown URL",
                "status_code": status_code if status_code else None,
            }
    except Exception:
        pass

    current_trace.record_error(formatted_exception)


class _DeepTracer:
    _instance: _DeepTracer | None = None
    _lock: threading.Lock = threading.Lock()
    _refcount: int = 0
    _span_stack: contextvars.ContextVar[list[dict[str, Any]]] = contextvars.ContextVar(
        "_deep_profiler_span_stack", default=[]
    )
    _skip_stack: contextvars.ContextVar[list[str]] = contextvars.ContextVar(
        "_deep_profiler_skip_stack", default=[]
    )
    _original_sys_trace: Callable | None = None
    _original_threading_trace: Callable | None = None

    def __init__(self, tracer: Tracer):
        self._tracer = tracer

    def _get_qual_name(self, frame) -> str:
        func_name = frame.f_code.co_name
        module_name = frame.f_globals.get("__name__", "unknown_module")

        try:
            func = frame.f_globals.get(func_name)
            if func is None:
                return f"{module_name}.{func_name}"
            if hasattr(func, "__qualname__"):
                return f"{module_name}.{func.__qualname__}"
            return f"{module_name}.{func_name}"
        except Exception:
            return f"{module_name}.{func_name}"

    def __new__(cls, tracer: Tracer):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def _should_trace(self, frame):
        # Skip stack is maintained by the tracer as an optimization to skip earlier
        # frames in the call stack that we've already determined should be skipped
        skip_stack = self._skip_stack.get()
        if len(skip_stack) > 0:
            return False

        func_name = frame.f_code.co_name
        module_name = frame.f_globals.get("__name__", None)
        func = frame.f_globals.get(func_name)
        if func and (
            hasattr(func, "_trajectory_span_name")
            or hasattr(func, "_trajectory_span_type")
        ):
            return False

        if (
            not module_name
            or func_name.startswith("<")  # ex: <listcomp>
            or (func_name.startswith("__") and func_name != "__call__")  # dunders
            or not self._is_user_code(frame.f_code.co_filename)
        ):
            return False

        return True

    @functools.cache
    def _is_user_code(self, filename: str):
        return (
            bool(filename)
            and not filename.startswith("<")
            and not os.path.realpath(filename).startswith(_TRACE_FILEPATH_BLOCKLIST)
        )

    def _cooperative_sys_trace(self, frame: types.FrameType, event: str, arg: Any):
        """Cooperative trace function for sys.settrace that chains with existing tracers."""
        # First, call the original sys trace function if it exists
        original_result = None
        if self._original_sys_trace:
            try:
                original_result = self._original_sys_trace(frame, event, arg)
            except Exception:
                pass

        our_result = self._trace(frame, event, arg, self._cooperative_sys_trace)

        if original_result is None and self._original_sys_trace:
            return None

        return our_result or original_result

    def _cooperative_threading_trace(
        self, frame: types.FrameType, event: str, arg: Any
    ):
        """Cooperative trace function for threading.settrace that chains with existing tracers."""
        original_result = None
        if self._original_threading_trace:
            try:
                original_result = self._original_threading_trace(frame, event, arg)
            except Exception:
                pass

        our_result = self._trace(frame, event, arg, self._cooperative_threading_trace)

        if original_result is None and self._original_threading_trace:
            return None

        return our_result or original_result

    def _trace(
        self, frame: types.FrameType, event: str, arg: Any, continuation_func: Callable
    ):
        frame.f_trace_lines = False
        frame.f_trace_opcodes = False

        if not self._should_trace(frame):
            return

        if event not in ("call", "return", "exception"):
            return

        current_trace = self._tracer.get_current_trace()
        if not current_trace:
            return

        parent_span_id = self._tracer.get_current_span()
        if not parent_span_id:
            return

        qual_name = self._get_qual_name(frame)
        instance_name = None
        if "self" in frame.f_locals:
            instance = frame.f_locals["self"]
            class_name = instance.__class__.__name__
            class_identifiers = getattr(self._tracer, "class_identifiers", {})
            instance_name = get_instance_prefixed_name(
                instance, class_name, class_identifiers
            )
        skip_stack = self._skip_stack.get()

        if event == "call":
            # If we have entries in the skip stack and the current qual_name matches the top entry,
            # push it again to track nesting depth and skip
            # As an optimization, we only care about duplicate qual_names.
            if skip_stack:
                if qual_name == skip_stack[-1]:
                    skip_stack.append(qual_name)
                    self._skip_stack.set(skip_stack)
                return

            should_trace = self._should_trace(frame)

            if not should_trace:
                if not skip_stack:
                    self._skip_stack.set([qual_name])
                return
        elif event == "return":
            # If we have entries in skip stack and current qual_name matches the top entry,
            # pop it to track exiting from the skipped section
            if skip_stack and qual_name == skip_stack[-1]:
                skip_stack.pop()
                self._skip_stack.set(skip_stack)
                return

            if skip_stack:
                return

        span_stack = self._span_stack.get()
        if event == "call":
            if not self._should_trace(frame):
                return

            span_id = str(uuid.uuid4())

            parent_depth = current_trace._span_depths.get(parent_span_id, 0)
            depth = parent_depth + 1

            current_trace._span_depths[span_id] = depth

            start_time = time.time()

            span_stack.append(
                {
                    "span_id": span_id,
                    "parent_span_id": parent_span_id,
                    "function": qual_name,
                    "start_time": start_time,
                }
            )
            self._span_stack.set(span_stack)

            token = self._tracer.set_current_span(span_id)
            frame.f_locals["_trajectory_span_token"] = token

            span = TraceSpan(
                span_id=span_id,
                trace_id=current_trace.trace_id,
                depth=depth,
                message=qual_name,
                created_at=start_time,
                span_type="span",
                parent_span_id=parent_span_id,
                function=qual_name,
                agent_name=instance_name,
            )
            current_trace.add_span(span)

            inputs = {}
            try:
                args_info = inspect.getargvalues(frame)
                for arg in args_info.args:
                    try:
                        inputs[arg] = args_info.locals.get(arg)
                    except Exception:
                        inputs[arg] = "<<Unserializable>>"
                current_trace.record_input(inputs)
            except Exception as e:
                current_trace.record_input({"error": str(e)})

        elif event == "return":
            if not span_stack:
                return

            current_id = self._tracer.get_current_span()

            span_data = None
            for i, entry in enumerate(reversed(span_stack)):
                if entry["span_id"] == current_id:
                    span_data = span_stack.pop(-(i + 1))
                    self._span_stack.set(span_stack)
                    break

            if not span_data:
                return

            start_time = span_data["start_time"]
            duration = time.time() - start_time

            current_trace.span_id_to_span[span_data["span_id"]].duration = duration

            if arg is not None:
                # exception handling will take priority.
                current_trace.record_output(arg)

            if span_data["span_id"] in current_trace._span_depths:
                del current_trace._span_depths[span_data["span_id"]]

            if span_stack:
                self._tracer.set_current_span(span_stack[-1]["span_id"])
            else:
                self._tracer.set_current_span(span_data["parent_span_id"])

            if "_trajectory_span_token" in frame.f_locals:
                self._tracer.reset_current_span(
                    frame.f_locals["_trajectory_span_token"]
                )

        elif event == "exception":
            exc_type = arg[0]
            if issubclass(exc_type, (StopIteration, StopAsyncIteration, GeneratorExit)):
                return
            _capture_exception_for_trace(current_trace, arg)

        return continuation_func

    def __enter__(self):
        with self._lock:
            self._refcount += 1
            if self._refcount == 1:
                # Store the existing trace functions before setting ours
                self._original_sys_trace = sys.gettrace()
                self._original_threading_trace = threading.gettrace()

                self._skip_stack.set([])
                self._span_stack.set([])

                sys.settrace(self._cooperative_sys_trace)
                threading.settrace(self._cooperative_threading_trace)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self._lock:
            self._refcount -= 1
            if self._refcount == 0:
                # Restore the original trace functions instead of setting to None
                sys.settrace(self._original_sys_trace)
                threading.settrace(self._original_threading_trace)

                # Clean up the references
                self._original_sys_trace = None
                self._original_threading_trace = None


class Tracer:
    # Tracer.current_trace class variable is currently used in wrap()
    # TODO: Keep track of cross-context state for current trace and current span ID solely through class variables instead of instance variables?
    # Should be fine to do so as long as we keep Tracer as a singleton
    current_trace: TraceClient | None = None
    # current_span_id: Optional[str] = None

    trace_across_async_contexts: bool = (
        False  # BY default, we don't trace across async contexts
    )

    def __init__(
        self,
        api_key: str | None = os.getenv("TRAJECTORY_API_KEY"),
        organization_id: str | None = os.getenv("TRAJECTORY_ORG_ID"),
        project_name: str | None = None,
        deep_tracing: bool = False,  # Deep tracing is disabled by default
        enable_monitoring: bool = os.getenv("TRAJECTORY_MONITORING", "true").lower()
        == "true",
        enable_evaluations: bool = os.getenv("TRAJECTORY_EVALUATIONS", "true").lower()
        == "true",
        # S3 configuration
        use_s3: bool = False,
        s3_bucket_name: str | None = None,
        s3_aws_access_key_id: str | None = None,
        s3_aws_secret_access_key: str | None = None,
        s3_region_name: str | None = None,
        trace_across_async_contexts: bool = False,  # BY default, we don't trace across async contexts
        span_batch_size: int = 50,
        span_flush_interval: float = 1.0,
        span_max_queue_size: int = 2048,
        span_export_timeout: int = 30000,
        # Evaluation-specific fields
        evaluation_id: Optional[str] = None,
        is_evaluation: bool = False,
        # Local tracing configuration
        enable_local_tracing: bool = None,  # None means check environment variable
        local_tracing_dir: str
        | None = None,  # None means use environment variable or default
        only_local_tracing: bool = None,  # None means check environment variable
    ):
        # Reconfigure logger with current environment variables
        # Reconfigure based on the latest environment; then force level from env if provided
        reconfigure_logger()
        logging_level = os.getenv("TRAJECTORY_LOGGING_LEVEL", "INFO")
        configure_trajectory_logger(level=logging_level)
        trajectory_logger.debug(
            f"Initializing Tracer | logging_level={logging_level} deep_tracing={deep_tracing} "
            f"monitoring={enable_monitoring} evaluations={enable_evaluations}"
        )
        try:
            # In only-local tracing mode, we don't require real API credentials
            if not api_key or not organization_id:
                if is_only_local_tracing_enabled():
                    trajectory_logger.info(
                        "Only-local tracing enabled; bypassing API key/org validation"
                    )
                    api_key = api_key or "local_only_key"
                    organization_id = organization_id or "local_only_org"
                else:
                    raise ValueError(
                        "api_key and organization_id are required unless TRAJECTORY_ONLY_LOCAL_TRACING=true"
                    )

            try:
                if not is_only_local_tracing_enabled():
                    result, response = validate_api_key(api_key)
                else:
                    result, response = True, None
            except Exception as e:
                trajectory_logger.error(
                    f"Issue verifying API key, disabling monitoring: {e}"
                )
                enable_monitoring = False
            #     trajectory_logger.error(
            #         f"Issue with verifying API key, disabling monitoring: {e}"
            #     )
            #     enable_monitoring = False
            #     result = True

            # if not result:
            #     raise ValueError(f"Issue with passed in Trajectory API key: {response}")

            # if use_s3 and not s3_bucket_name:
            #     raise ValueError("S3 bucket name must be provided when use_s3 is True")

            self.api_key: str = api_key
            self.project_name: str = project_name or "default_project"
            self.organization_id: str = organization_id
            self.traces: list[Trace] = []
            self.enable_monitoring: bool = enable_monitoring
            self.enable_evaluations: bool = enable_evaluations
            self.class_identifiers: dict[
                str, str
            ] = {}  # Dictionary to store class identifiers
            self.span_id_to_previous_span_id: dict[str, str | None] = {}
            self.trace_id_to_previous_trace: dict[str, TraceClient | None] = {}
            self.current_span_id: str | None = None
            self.current_trace: TraceClient | None = None
            self.trace_across_async_contexts: bool = trace_across_async_contexts
            Tracer.trace_across_async_contexts = trace_across_async_contexts

            # Initialize S3 storage if enabled
            self.use_s3 = use_s3
            if use_s3 and S3Storage is not None:
                try:
                    self.s3_storage = S3Storage(
                        bucket_name=s3_bucket_name,
                        aws_access_key_id=s3_aws_access_key_id,
                        aws_secret_access_key=s3_aws_secret_access_key,
                        region_name=s3_region_name,
                    )
                except Exception as e:
                    trajectory_logger.error(
                        f"Issue with initializing S3 storage, disabling S3: {e}"
                    )
                    self.use_s3 = False
            elif use_s3 and S3Storage is None:
                trajectory_logger.warning(
                    "S3 storage requested but not available; disabling S3"
                )
                self.use_s3 = False

            self.offline_mode = True  # Differentiate experiments vs monitoring
            self.deep_tracing: bool = deep_tracing

            self.span_batch_size = span_batch_size
            self.span_flush_interval = span_flush_interval
            self.span_max_queue_size = span_max_queue_size
            self.span_export_timeout = span_export_timeout
            self.otel_span_processor: SpanProcessorBase

            if enable_monitoring and not is_only_local_tracing_enabled():
                self.otel_span_processor = TrajectorySpanProcessor(
                    trajectory_api_key=api_key,
                    organization_id=organization_id,
                    batch_size=span_batch_size,
                    flush_interval=span_flush_interval,
                    max_queue_size=span_max_queue_size,
                    export_timeout=span_export_timeout,
                )
            else:
                self.otel_span_processor = SpanProcessorBase()

            atexit.register(self._cleanup_on_exit)

            # Add verifier support
            self._verifiers: dict[str, list[VerifierConfig]] = {}
            self.verifier_runner = (
                AsyncVerifierRunner()
            )  # No llm_client parameter needed

            # Add trace cache for verifier callbacks
            self._trace_cache: dict[str, dict[str, Any]] = {}
            self._pending_verifiers: dict[str, int] = {}
            self._verifier_callbacks: dict[str, Callable] = {}

            eval_metadata = get_global_evaluation_metadata()
            self.evaluation_id = (
                eval_metadata.get("evaluation_id") if eval_metadata else None
            )
            self.is_evaluation = self.evaluation_id is not None
            # Initialize judgment client for run_trace_evaluation
            if api_key and organization_id:
                try:
                    from trajectory import TrajectoryClient

                    self.trajectory_client = TrajectoryClient(
                        api_key=api_key, organization_id=organization_id
                    )
                except Exception as e:
                    trajectory_logger.warning(
                        f"Could not initialize TrajectoryClient: {e}"
                    )
                    self.trajectory_client = None
            else:
                self.trajectory_client = None

            # Add batching support for verifier results
            self._pending_verifications: dict[
                str, dict[str, Any]
            ] = {}  # trace_id -> {span_id -> results}
            self._verification_lock = threading.Lock()

            # Initialize local tracing
            self.enable_local_tracing = self._determine_local_tracing_setting(
                enable_local_tracing
            )
            self.only_local_tracing = self._determine_only_local_tracing_setting(
                only_local_tracing
            )
            self.local_tracing_dir = local_tracing_dir or get_local_storage_dir()
            self.local_trace_storage = None

            trajectory_logger.debug(
                f"Local tracing settings - enabled: {self.enable_local_tracing}, only_local: {self.only_local_tracing}"
            )
            trajectory_logger.debug(
                f"Local tracing directory: {self.local_tracing_dir}"
            )

            if self.enable_local_tracing:
                try:
                    trajectory_logger.info(
                        f"Initializing local trace storage at: {self.local_tracing_dir}"
                    )
                    self.local_trace_storage = LocalTraceStorage(self.local_tracing_dir)
                    if self.only_local_tracing:
                        trajectory_logger.info(
                            f"Only local tracing enabled. Storage directory: {self.local_tracing_dir}"
                        )
                        trajectory_logger.info(
                            "Disabling remote monitoring and evaluations for local-only mode"
                        )
                        # Disable remote monitoring when only local tracing is enabled
                        self.enable_monitoring = False
                        self.enable_evaluations = False
                    else:
                        trajectory_logger.info(
                            f"Local tracing enabled alongside remote tracing. Storage directory: {self.local_tracing_dir}"
                        )
                except Exception as e:
                    trajectory_logger.error(
                        f"Failed to initialize local trace storage: {e}"
                    )
                    trajectory_logger.debug(f"Local trace storage error details: {e!s}")
                    self.enable_local_tracing = False
            else:
                trajectory_logger.debug("Local tracing disabled")

        except Exception as e:
            trajectory_logger.error(
                f"Issue initializing Tracer, disabling monitoring/evaluations: {e}"
            )
            self.enable_monitoring = False
            self.enable_evaluations = False

    def _determine_local_tracing_setting(
        self, enable_local_tracing: bool | None
    ) -> bool:
        """
        Determine if local tracing should be enabled based on parameter and environment

        Args:
            enable_local_tracing: Explicit setting from constructor parameter

        Returns:
            True if local tracing should be enabled, False otherwise
        """
        if enable_local_tracing is not None:
            return enable_local_tracing

        return is_local_tracing_enabled()

    def _determine_only_local_tracing_setting(
        self, only_local_tracing: bool | None
    ) -> bool:
        """
        Determine if only local tracing should be enabled based on parameter and environment

        Args:
            only_local_tracing: Explicit setting from constructor parameter

        Returns:
            True if only local tracing should be enabled, False otherwise
        """
        if only_local_tracing is not None:
            return only_local_tracing

        return is_only_local_tracing_enabled()

    def set_current_span(self, span_id: str) -> contextvars.Token[str | None] | None:
        self.span_id_to_previous_span_id[span_id] = self.current_span_id
        self.current_span_id = span_id
        Tracer.current_span_id = span_id
        try:
            token = current_span_var.set(span_id)
        except Exception:
            token = None
        return token

    def log_metric(
        self,
        event_name: str,
        properties: dict[str, Any] | None = None,
        value: float | None = None,
        unit: str | None = None,
        tags: list[str] | None = None,
        context_override: dict[str, Any] | None = None,
        persist: bool = False,
    ):
        try:
            current_trace = self.get_current_trace()
            if not current_trace:
                with self.trace("metrics_buffer") as t:
                    t.log_metric(
                        event_name=event_name,
                        properties=properties,
                        value=value,
                        unit=unit,
                        tags=tags,
                        context_override=context_override,
                        persist=persist,
                    )
                return
            current_trace.log_metric(
                event_name=event_name,
                properties=properties,
                value=value,
                unit=unit,
                tags=tags,
                context_override=context_override,
                persist=persist,
            )
        except Exception as e:
            trajectory_logger.warning(f"Issue logging metric '{event_name}': {e}")

    def get_current_span(self) -> str | None:
        try:
            current_span_var_val = current_span_var.get()
        except Exception:
            current_span_var_val = None
        return (
            (self.current_span_id or current_span_var_val)
            if self.trace_across_async_contexts
            else current_span_var_val
        )

    def reset_current_span(
        self,
        token: contextvars.Token[str | None] | None = None,
        span_id: str | None = None,
    ):
        try:
            if token:
                current_span_var.reset(token)
        except Exception:
            pass
        if not span_id:
            span_id = self.current_span_id
        if span_id:
            self.current_span_id = self.span_id_to_previous_span_id.get(span_id)
            Tracer.current_span_id = self.current_span_id

    def set_current_trace(
        self, trace: TraceClient
    ) -> contextvars.Token[TraceClient | None] | None:
        """
        Set the current trace context in contextvars
        """
        self.trace_id_to_previous_trace[trace.trace_id] = self.current_trace
        self.current_trace = trace
        Tracer.current_trace = trace
        try:
            token = current_trace_var.set(trace)
        except Exception:
            token = None
        return token

    def get_current_trace(self) -> TraceClient | None:
        """
        Get the current trace context.

        Tries to get the trace client from the context variable first.
        If not found (e.g., context lost across threads/tasks),
        it falls back to the active trace client managed by the callback handler.
        """
        try:
            current_trace_var_val = current_trace_var.get()
        except Exception:
            current_trace_var_val = None
        return (
            (self.current_trace or current_trace_var_val)
            if self.trace_across_async_contexts
            else current_trace_var_val
        )

    def reset_current_trace(
        self,
        token: contextvars.Token[TraceClient | None] | None = None,
        trace_id: str | None = None,
    ):
        try:
            if token:
                current_trace_var.reset(token)
        except Exception:
            pass
        if not trace_id and self.current_trace:
            trace_id = self.current_trace.trace_id
        if trace_id:
            self.current_trace = self.trace_id_to_previous_trace.get(trace_id)
            Tracer.current_trace = self.current_trace

    @contextmanager
    def trace(
        self, name: str, project_name: str | None = None
    ) -> Generator[TraceClient, None, None]:
        """Start a new trace context using a context manager"""
        trace_id = str(uuid.uuid4())
        project = project_name if project_name is not None else self.project_name

        # Get parent trace info from context
        parent_trace = self.get_current_trace()
        parent_trace_id = None
        parent_name = None

        if parent_trace:
            parent_trace_id = parent_trace.trace_id
            parent_name = parent_trace.name

        eval_metadata = get_global_evaluation_metadata()
        evaluation_id = eval_metadata.get("evaluation_id") if eval_metadata else None
        is_evaluation = evaluation_id is not None
        trace = TraceClient(
            self,
            trace_id,
            name,
            project_name=project,
            enable_monitoring=self.enable_monitoring,
            enable_evaluations=self.enable_evaluations,
            parent_trace_id=parent_trace_id,
            parent_name=parent_name,
            evaluation_id=evaluation_id,
            is_evaluation=is_evaluation,
        )

        # Set the current trace in context variables
        token = self.set_current_trace(trace)

        trajectory_logger.debug(
            f"Starting trace | trace_id={trace_id} name={name} project={project}"
        )
        with trace.span(name or "unnamed_trace"):
            try:
                # Save the trace to the database to handle Evaluations' trace_id referential integrity
                yield trace
            finally:
                try:
                    trajectory_logger.debug(
                        f"Finalizing trace | trace_id={trace.trace_id} span_count={len(trace.trace_spans)}"
                    )
                    # Ensure all spans are flushed and the final snapshot is saved locally/remotely as configured
                    trace.save(final_save=True)
                except Exception as e:
                    trajectory_logger.warning(
                        f"Failed to finalize trace {trace.trace_id}: {e}"
                    )
                # Reset the context variable
                self.reset_current_trace(token)

    @contextmanager
    def conversation(self, conversation_id: str, user_id: str | None = None):
        """Set conversation context for all spans within this block"""
        token = conversation_id_var.set(conversation_id)
        user_token = None
        try:
            if user_id is not None:
                user_token = user_id_var.set(user_id)
            yield
        finally:
            if user_token is not None:
                user_id_var.reset(user_token)
            conversation_id_var.reset(token)

    def identify(
        self,
        identifier: str,
        track_state: bool = False,
        track_attributes: list[str] | None = None,
        field_mappings: dict[str, str] | None = None,
    ):
        """
        Class decorator that associates a class with a custom identifier and enables state tracking.

        This decorator creates a mapping between the class name and the provided
        identifier, which can be useful for tagging, grouping, or referencing
        classes in a standardized way. It also enables automatic state capture
        for instances of the decorated class when used with tracing.

        Args:
            identifier: The identifier to associate with the decorated class.
                    This will be used as the instance name in traces.
            track_state: Whether to automatically capture the state (attributes)
                        of instances before and after function execution. Defaults to False.
            track_attributes: Optional list of specific attribute names to track.
                            If None, all non-private attributes (not starting with '_')
                            will be tracked when track_state=True.
            field_mappings: Optional dictionary mapping internal attribute names to
                        display names in the captured state. For example:
                        {"system_prompt": "instructions"} will capture the
                        'instructions' attribute as 'system_prompt' in the state.

        Example:
            @tracer.identify(identifier="user_model", track_state=True, track_attributes=["name", "age"], field_mappings={"system_prompt": "instructions"})
            class User:
                # Class implementation
        """

        def decorator(cls):
            class_name = cls.__name__
            self.class_identifiers[class_name] = {
                "identifier": identifier,
                "track_state": track_state,
                "track_attributes": track_attributes,
                "field_mappings": field_mappings or {},
            }
            return cls

        return decorator

    def _capture_instance_state(
        self, instance: Any, class_config: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Capture the state of an instance based on class configuration.
        Args:
            instance: The instance to capture the state of.
            class_config: Configuration dictionary for state capture,
                          expected to contain 'track_attributes' and 'field_mappings'.
        """
        track_attributes = class_config.get("track_attributes")
        field_mappings = class_config.get("field_mappings")

        if track_attributes:
            state = {attr: getattr(instance, attr, None) for attr in track_attributes}
        else:
            state = {
                k: v for k, v in instance.__dict__.items() if not k.startswith("_")
            }

        if field_mappings:
            state["field_mappings"] = field_mappings

        return state

    def _get_instance_state_if_tracked(self, args):
        """
        Extract instance state if the instance should be tracked.

        Returns the captured state dict if tracking is enabled, None otherwise.
        """
        if args and hasattr(args[0], "__class__"):
            instance = args[0]
            class_name = instance.__class__.__name__
            if (
                class_name in self.class_identifiers
                and isinstance(self.class_identifiers[class_name], dict)
                and self.class_identifiers[class_name].get("track_state", False)
            ):
                return self._capture_instance_state(
                    instance, self.class_identifiers[class_name]
                )

    def _conditionally_capture_and_record_state(
        self, trace_client_instance: TraceClient, args: tuple, is_before: bool
    ):
        """Captures instance state if tracked and records it via the trace_client."""
        state = self._get_instance_state_if_tracked(args)
        if state:
            if is_before:
                trace_client_instance.record_state_before(state)
            else:
                trace_client_instance.record_state_after(state)

    def observe(
        self,
        func=None,
        *,
        name=None,
        span_type: SpanType = "span",
    ):
        """
        Decorator to trace function execution with detailed entry/exit information.

        Args:
            func: The function to decorate
            name: Optional custom name for the span (defaults to function name)
            span_type: Type of span (default "span").
        """
        # If monitoring is disabled, return the function as is
        try:
            if not self.enable_monitoring:
                return func if func else lambda f: f

            if func is None:
                return lambda f: self.observe(
                    f,
                    name=name,
                    span_type=span_type,
                )

            # Use provided name or fall back to function name
            original_span_name = name or func.__name__

            # Store custom attributes on the function object
            func._trajectory_span_name = original_span_name
            func._trajectory_span_type = span_type

        except Exception:
            return func

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                # MINIMAL CHANGE: Retrieve context tracer and print it
                eval_metadata = None  # Initialize to avoid UnboundLocalError
                try:
                    from trajectory.run_evaluation import TRACE_VAR

                    context_tracer = TRACE_VAR.get()
                    trajectory_logger.debug(
                        f"Retrieved context tracer: {context_tracer} with verifiers: {list(context_tracer._verifiers.keys()) if context_tracer and hasattr(context_tracer, '_verifiers') else 'None'}"
                    )
                    eval_metadata = get_global_evaluation_metadata()
                    trajectory_logger.debug(
                        f"Context tracer evaluation_id: {eval_metadata.get('evaluation_id') if eval_metadata else None}"
                    )
                except Exception as e:
                    trajectory_logger.warning(f"Error retrieving context tracer: {e}")
                    context_tracer = None

                nonlocal original_span_name
                class_name = None
                agent_name = None
                span_name = original_span_name

                if len(args) > 0 and hasattr(args[0], "__class__"):
                    class_name = args[0].__class__.__name__
                    if hasattr(args[0], "agent_name"):
                        agent_name = args[0].agent_name

                # Get tracer from context or use self
                current_tracer = context_tracer if context_tracer is not None else self
                current_trace = current_tracer.get_current_trace()

                if not current_trace:
                    trace_id = str(uuid.uuid4())
                    project = self.project_name

                    eval_metadata = get_global_evaluation_metadata()
                    current_trace = TraceClient(
                        self,
                        trace_id,
                        span_name,
                        project_name=project,
                        enable_monitoring=self.enable_monitoring,
                        enable_evaluations=self.enable_evaluations,
                        evaluation_id=eval_metadata.get("evaluation_id")
                        if eval_metadata
                        else None,
                        is_evaluation=(
                            eval_metadata.get("evaluation_id")
                            if eval_metadata
                            else None
                        )
                        is not None,
                    )
                    trajectory_logger.debug(
                        f"Current tracer evaluation_id: {eval_metadata.get('evaluation_id') if eval_metadata else None}"
                    )
                    trace_token = self.set_current_trace(current_trace)

                    try:
                        with current_trace.span(span_name, span_type=span_type) as span:
                            inputs = self._capture_function_inputs(func, args, kwargs)
                            # print(f"Inputs: {inputs}")
                            span.record_input(inputs)
                            if agent_name:
                                span.record_agent_name(agent_name)

                            self._conditionally_capture_and_record_state(
                                span, args, is_before=True
                            )

                            try:
                                if self.deep_tracing:
                                    with _DeepTracer(self):
                                        result = await func(*args, **kwargs)
                                else:
                                    result = await func(*args, **kwargs)
                            except Exception as e:
                                _capture_exception_for_trace(
                                    current_trace, sys.exc_info()
                                )
                                raise e

                            self._conditionally_capture_and_record_state(
                                span, args, is_before=False
                            )

                            span.record_output(result)

                            if hasattr(current_tracer, "_verifiers"):
                                current_tracer._run_verifiers_for_span(
                                    span, inputs, result
                                )
                        return result
                    finally:
                        try:
                            complete_trace_data = {
                                "trace_id": current_trace.trace_id,
                                "name": current_trace.name,
                                "created_at": datetime.fromtimestamp(
                                    current_trace.start_time or time.time(),
                                    UTC,
                                ).isoformat(),
                                "duration": current_trace.get_duration(),
                                "trace_spans": [
                                    span.model_dump()
                                    for span in current_trace.trace_spans
                                ],
                                "offline_mode": self.offline_mode,
                                "parent_trace_id": current_trace.parent_trace_id,
                                "parent_name": current_trace.parent_name,
                                "evaluation_id": eval_metadata.get("evaluation_id")
                                if eval_metadata
                                else None,
                                "is_evaluation": (
                                    eval_metadata.get("evaluation_id")
                                    if eval_metadata
                                    else None
                                )
                                is not None,
                            }
                            trajectory_logger.debug(
                                f"Current trace evaluation_id: {eval_metadata.get('evaluation_id') if eval_metadata else None}"
                            )
                            trace_id, server_response = current_trace.save(
                                final_save=True
                            )

                            current_tracer.traces.append(complete_trace_data)

                            self.reset_current_trace(trace_token)
                        except Exception as e:
                            trajectory_logger.warning(f"Issue with async_wrapper: {e}")
                else:
                    with current_trace.span(span_name, span_type=span_type) as span:
                        inputs = self._capture_function_inputs(func, args, kwargs)
                        # print(f"Inputs: {inputs}")
                        span.record_input(inputs)
                        if agent_name:
                            span.record_agent_name(agent_name)

                        # Capture state before execution
                        self._conditionally_capture_and_record_state(
                            span, args, is_before=True
                        )

                        try:
                            if self.deep_tracing:
                                with _DeepTracer(self):
                                    result = await func(*args, **kwargs)
                            else:
                                result = await func(*args, **kwargs)
                        except Exception as e:
                            _capture_exception_for_trace(current_trace, sys.exc_info())
                            raise e

                        # Capture state after execution
                        self._conditionally_capture_and_record_state(
                            span, args, is_before=False
                        )

                        span.record_output(result)

                        if hasattr(current_tracer, "_verifiers"):
                            current_tracer._run_verifiers_for_span(span, inputs, result)
                    return result

            return async_wrapper
        else:
            # Non-async function implementation with deep tracing
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # MINIMAL CHANGE: Retrieve context tracer and print it
                eval_metadata = None  # Initialize to avoid UnboundLocalError
                try:
                    from trajectory.run_evaluation import TRACE_VAR

                    context_tracer = TRACE_VAR.get()
                    trajectory_logger.debug(
                        f"Retrieved context tracer: {context_tracer} with verifiers: {list(context_tracer._verifiers.keys()) if context_tracer and hasattr(context_tracer, '_verifiers') else 'None'}"
                    )
                    eval_metadata = get_global_evaluation_metadata()
                    trajectory_logger.debug(
                        f"Context tracer evaluation_id: {eval_metadata.get('evaluation_id') if eval_metadata else None}"
                    )
                except Exception as e:
                    trajectory_logger.warning(f"Error retrieving context tracer: {e}")
                    context_tracer = None

                nonlocal original_span_name
                class_name = None
                span_name = original_span_name
                agent_name = None
                if args and hasattr(args[0], "__class__"):
                    class_name = args[0].__class__.__name__
                    agent_name = get_instance_prefixed_name(
                        args[0], class_name, self.class_identifiers
                    )
                # Get current trace from context

                current_tracer = context_tracer if context_tracer is not None else self
                current_trace = current_tracer.get_current_trace()

                # If there's no current trace, create a root trace
                if not current_trace:
                    trace_id = str(uuid.uuid4())
                    project = self.project_name

                    # Create a new trace client to serve as the root
                    current_trace = TraceClient(
                        self,
                        trace_id,
                        span_name,
                        project_name=project,
                        enable_monitoring=self.enable_monitoring,
                        enable_evaluations=self.enable_evaluations,
                        evaluation_id=eval_metadata.get("evaluation_id")
                        if eval_metadata
                        else None,
                        is_evaluation=(
                            eval_metadata.get("evaluation_id")
                            if eval_metadata
                            else None
                        )
                        is not None,
                    )

                    trace_token = self.set_current_trace(current_trace)
                    trajectory_logger.debug(
                        f"Current trace evaluation_id: {eval_metadata.get('evaluation_id') if eval_metadata else None}"
                    )
                    try:
                        with current_trace.span(span_name, span_type=span_type) as span:
                            # Record inputs
                            inputs = self._capture_function_inputs(func, args, kwargs)
                            # print(f"Inputs: {inputs}")
                            span.record_input(inputs)
                            if agent_name:
                                span.record_agent_name(agent_name)
                            # Capture state before execution
                            self._conditionally_capture_and_record_state(
                                span, args, is_before=True
                            )

                            try:
                                if self.deep_tracing:
                                    with _DeepTracer(self):
                                        result = func(*args, **kwargs)
                                else:
                                    result = func(*args, **kwargs)
                            except Exception as e:
                                _capture_exception_for_trace(
                                    current_trace, sys.exc_info()
                                )
                                raise e

                            # Capture state after execution
                            self._conditionally_capture_and_record_state(
                                span, args, is_before=False
                            )

                            # Record output
                            span.record_output(result)

                            if hasattr(current_tracer, "_verifiers"):
                                current_tracer._run_verifiers_for_span(
                                    span, inputs, result
                                )
                        return result
                    finally:
                        try:
                            eval_metadata = get_global_evaluation_metadata()
                            trajectory_logger.debug(
                                f"Current trace evaluation_id: {eval_metadata.get('evaluation_id') if eval_metadata else None}"
                            )
                            trace_id, server_response = current_trace.save(
                                final_save=True
                            )

                            complete_trace_data = {
                                "trace_id": current_trace.trace_id,
                                "name": current_trace.name,
                                "created_at": datetime.fromtimestamp(
                                    current_trace.start_time or time.time(),
                                    UTC,
                                ).isoformat(),
                                "duration": current_trace.get_duration(),
                                "trace_spans": [
                                    span.model_dump()
                                    for span in current_trace.trace_spans
                                ],
                                "offline_mode": self.offline_mode,
                                "parent_trace_id": current_trace.parent_trace_id,
                                "parent_name": current_trace.parent_name,
                                "evaluation_id": eval_metadata.get("evaluation_id")
                                if eval_metadata
                                else None,
                                "is_evaluation": (
                                    eval_metadata.get("evaluation_id")
                                    if eval_metadata
                                    else None
                                )
                                is not None,
                            }
                            current_tracer.traces.append(complete_trace_data)
                            self.reset_current_trace(trace_token)
                        except Exception as e:
                            trajectory_logger.warning(f"Issue with save: {e}")
                else:
                    with current_trace.span(span_name, span_type=span_type) as span:
                        inputs = self._capture_function_inputs(func, args, kwargs)
                        span.record_input(inputs)
                        if agent_name:
                            span.record_agent_name(agent_name)

                        # Capture state before execution
                        self._conditionally_capture_and_record_state(
                            span, args, is_before=True
                        )

                        try:
                            if self.deep_tracing:
                                with _DeepTracer(self):
                                    result = func(*args, **kwargs)
                            else:
                                result = func(*args, **kwargs)
                        except Exception as e:
                            _capture_exception_for_trace(current_trace, sys.exc_info())
                            raise e

                        # Capture state after execution
                        self._conditionally_capture_and_record_state(
                            span, args, is_before=False
                        )

                        span.record_output(result)

                        if hasattr(current_tracer, "_verifiers"):
                            current_tracer._run_verifiers_for_span(span, inputs, result)
                    return result

            return wrapper

    def observe_tools(
        self,
        cls=None,
        *,
        exclude_methods: list[str] | None = None,
        include_private: bool = False,
        warn_on_double_decoration: bool = True,
    ):
        """
        Automatically adds @observe(span_type="tool") to all methods in a class.

        Args:
            cls: The class to decorate (automatically provided when used as decorator)
            exclude_methods: List of method names to skip decorating. Defaults to common magic methods
            include_private: Whether to decorate methods starting with underscore. Defaults to False
            warn_on_double_decoration: Whether to print warnings when skipping already-decorated methods. Defaults to True
        """

        if exclude_methods is None:
            exclude_methods = ["__init__", "__new__", "__del__", "__str__", "__repr__"]

        def decorate_class(cls):
            if not self.enable_monitoring:
                return cls

            decorated = []
            skipped = []

            for name in dir(cls):
                method = getattr(cls, name)

                if (
                    not callable(method)
                    or name in exclude_methods
                    or (name.startswith("_") and not include_private)
                    or not hasattr(cls, name)
                ):
                    continue

                if hasattr(method, "_trajectory_span_name"):
                    skipped.append(name)
                    if warn_on_double_decoration:
                        trajectory_logger.info(
                            f"{cls.__name__}.{name} already decorated, skipping"
                        )
                    continue

                try:
                    decorated_method = self.observe(method, span_type="tool")
                    setattr(cls, name, decorated_method)
                    decorated.append(name)
                except Exception as e:
                    if warn_on_double_decoration:
                        trajectory_logger.warning(
                            f"Failed to decorate {cls.__name__}.{name}: {e}"
                        )

            return cls

        return decorate_class if cls is None else decorate_class(cls)

    def async_evaluate(self, *args, **kwargs):
        try:
            if not self.enable_monitoring or not self.enable_evaluations:
                return

            current_trace = self.get_current_trace()

            if current_trace:
                current_trace.async_evaluate(*args, **kwargs)
            else:
                trajectory_logger.warning(
                    "No trace found (context var or fallback), skipping evaluation"
                )
        except Exception as e:
            trajectory_logger.warning(f"Issue with async_evaluate: {e}")

    def update_metadata(self, metadata: dict):
        """
        Update metadata for the current trace.

        Args:
            metadata: Metadata as a dictionary
        """
        current_trace = self.get_current_trace()
        if current_trace:
            current_trace.update_metadata(metadata)
        else:
            trajectory_logger.warning("No current trace found, cannot set metadata")

    def set_customer_id(self, customer_id: str):
        """
        Set the customer ID for the current trace.

        Args:
            customer_id: The customer ID to set
        """
        current_trace = self.get_current_trace()
        if current_trace:
            current_trace.set_customer_id(customer_id)
        else:
            trajectory_logger.warning("No current trace found, cannot set customer ID")

    def set_tags(self, tags: list[Union[str, set, tuple]]):
        """
        Set the tags for the current trace.

        Args:
            tags: List of tags to set
        """
        current_trace = self.get_current_trace()
        if current_trace:
            current_trace.set_tags(tags)
        else:
            trajectory_logger.warning("No current trace found, cannot set tags")

    def set_reward_score(self, reward_score: Union[float, dict[str, float]]):
        """
        Set the reward score for this trace to be used for RL or SFT.

        Args:
            reward_score: The reward score to set
        """
        current_trace = self.get_current_trace()
        if current_trace:
            current_trace.set_reward_score(reward_score)
        else:
            trajectory_logger.warning("No current trace found, cannot set reward score")

    def get_otel_span_processor(self) -> SpanProcessorBase:
        """Get the OpenTelemetry span processor instance."""
        return self.otel_span_processor

    def flush_background_spans(self, timeout_millis: int = 30000):
        """Flush all pending spans in the background service."""
        self.otel_span_processor.force_flush(timeout_millis)

    def shutdown_background_service(self):
        """Shutdown the background span service."""
        self.otel_span_processor.shutdown()
        self.otel_span_processor = SpanProcessorBase()

    def _cleanup_on_exit(self):
        """Cleanup handler called on application exit to ensure spans are flushed."""
        try:
            self.flush_background_spans()
        except Exception as e:
            trajectory_logger.warning(f"Error during tracer cleanup: {e}")
        finally:
            try:
                self.shutdown_background_service()
            except Exception as e:
                trajectory_logger.warning(
                    f"Error during background service shutdown: {e}"
                )

    def register_verifier(self, config: VerifierConfig):
        """Register a verifier for a specific function"""
        trajectory_logger.debug(f"Registering verifier: {config}")
        if config.function_name not in self._verifiers:
            self._verifiers[config.function_name] = []
        self._verifiers[config.function_name].append(config)

    def _run_verifiers_for_span(self, span: TraceSpan, inputs: dict, output: Any):
        """Run verifiers for a span and add to batch"""
        # Handle both TraceSpan and TraceClient objects
        trajectory_logger.debug(f"Running verifiers for span: {span}")
        trajectory_logger.debug(f"Span type: {type(span)}")
        trajectory_logger.debug(
            f"Span function: {getattr(span, 'function', 'no function')}"
        )
        trajectory_logger.debug(
            f"Span type: {getattr(span, 'span_type', 'no span_type')}"
        )

        if hasattr(span, "function"):
            # This is a TraceSpan object
            function_name = span.function
            trace_id = span.trace_id
            span_id = span.span_id
            actual_span = span
            trajectory_logger.debug(f"Using TraceSpan directly: {function_name}")
        else:
            # This is a TraceClient object - we need to get the current span
            trajectory_logger.debug(
                "This is a TraceClient, trying to get current span..."
            )
            current_span_id = self.get_current_span()
            trajectory_logger.debug(f"Current span ID: {current_span_id}")

            if not current_span_id:
                trajectory_logger.warning(
                    "No current span found for verifier execution"
                )
                return

            # Get the actual TraceSpan object using the span_id
            if hasattr(span, "span_id_to_span"):
                actual_span = span.span_id_to_span.get(current_span_id)
                trajectory_logger.debug(f"Found span in span_id_to_span: {actual_span}")
            else:
                trajectory_logger.warning("TraceClient has no span_id_to_span mapping")
                return

            if not actual_span:
                trajectory_logger.warning(
                    f"Span {current_span_id} not found in span_id_to_span mapping"
                )
                trajectory_logger.debug(
                    f"Available spans: {list(span.span_id_to_span.keys()) if hasattr(span, 'span_id_to_span') else 'None'}"
                )
                return

            function_name = actual_span.function
            trace_id = actual_span.trace_id
            span_id = actual_span.span_id
            trajectory_logger.debug(
                f"Using TraceSpan from TraceClient: {function_name}"
            )

        trajectory_logger.debug(f"Function name: {function_name}")
        trajectory_logger.debug(f"Available verifiers: {list(self._verifiers.keys())}")

        verifiers = self._verifiers.get(function_name, [])
        trajectory_logger.debug(f"Verifiers dict: {self._verifiers}")
        trajectory_logger.debug(f"Verifiers for {function_name}: {len(verifiers)}")

        if not verifiers:
            trajectory_logger.warning(
                f"No verifiers found for function: {function_name}"
            )
            return

        trajectory_logger.debug(
            f"Running {len(verifiers)} verifiers for function: {function_name}"
        )

        # Define callback to add results to batch
        def add_to_batch(trace_id: str, span_id: str, results: dict[str, Any]):
            self._batch_verification_result(trace_id, span_id, results)

        # Run verifiers asynchronously
        self.verifier_runner.run_verifiers_async(
            verifiers,
            inputs,
            output,
            callback=add_to_batch,
            trace_id=trace_id,
            span_id=span_id,
        )

    def _call_evaluate_trace_backend(
        self, trace_id: str, span_id: str, verification_results: dict[str, Any]
    ):
        """Send verification results to backend"""
        try:
            trajectory_logger.info(
                f"Sending verification results for trace {trace_id}, span {span_id}"
            )

            # Prepare the data to send
            data = {
                "trace_id": trace_id,
                "span_id": span_id,
                "verification_results": verification_results,
            }

            trajectory_logger.debug(f"Data to send: {json.dumps(data, indent=2)}")

            # Send to backend
            import requests

            response = requests.post(
                "http://localhost:8000/verification_results/",
                json=data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                trajectory_logger.info("Verification results sent successfully")
            else:
                trajectory_logger.warning(
                    f"Failed to send verification results: {response.status_code} - {response.text}"
                )

        except Exception as e:
            trajectory_logger.error(f"Error sending verification results: {e!s}")

    def _capture_function_inputs(self, func, args, kwargs) -> dict[str, Any]:
        """Capture function inputs for verification"""
        import inspect

        try:
            # Get function signature
            sig = inspect.signature(func)

            # Bind arguments to parameters
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Convert to dict
            inputs = dict(bound_args.arguments)

            # Handle self parameter for methods
            inputs.pop("self", None)

            return inputs
        except Exception as e:
            # Fallback to simple args/kwargs
            return {"args": args, "kwargs": kwargs, "error": str(e)}

    def _batch_verification_result(
        self, trace_id: str, span_id: str, results: dict[str, Any]
    ):
        """Add verification result to batch and send when all complete"""
        with self._verification_lock:
            if trace_id not in self._pending_verifications:
                self._pending_verifications[trace_id] = {}

            self._pending_verifications[trace_id][span_id] = results

            trajectory_logger.debug(
                f"Added verification result for trace {trace_id}, span {span_id}"
            )
            trajectory_logger.debug(
                f"Pending verifications for trace {trace_id}: {len(self._pending_verifications[trace_id])}"
            )

            # Send after a small delay to allow batching
            threading.Timer(2.0, self._send_batched_results, args=[trace_id]).start()

    def _send_batched_results(self, trace_id: str):
        """Send all verification results for a trace in one request"""
        with self._verification_lock:
            if trace_id not in self._pending_verifications:
                return

            results = self._pending_verifications[trace_id]
            trajectory_logger.info(
                f"Sending batched results for trace {trace_id}: {len(results)} spans"
            )

            # Prepare batched data
            data = {"trace_id": trace_id, "verification_results": results}

            # Send to backend
            try:
                if requests is None:
                    raise RuntimeError("requests not available")
                response = requests.post(
                    "http://localhost:8000/verification_results/",
                    json=data,
                    headers={"Content-Type": "application/json"},
                )

                if response.status_code == 200:
                    trajectory_logger.info(
                        f"Batched verification results sent successfully for trace {trace_id}"
                    )
                    # Clear the pending results
                    del self._pending_verifications[trace_id]
                else:
                    trajectory_logger.warning(
                        f"Failed to send batched results: {response.status_code} - {response.text}"
                    )

            except Exception as e:
                trajectory_logger.error(f"Error sending batched results: {e!s}")


def _get_current_trace(
    trace_across_async_contexts: bool = Tracer.trace_across_async_contexts,
):
    if trace_across_async_contexts:
        return Tracer.current_trace
    else:
        return current_trace_var.get()


def wrap(
    client: Any,
    trace_across_async_contexts: bool = Tracer.trace_across_async_contexts,
    agent_name: str | None = None,
) -> Any:
    """
    Wraps an API client to add tracing capabilities.
    Supports OpenAI, Together, Anthropic, and Google GenAI clients.
    Patches both '.create' and Anthropic's '.stream' methods using a wrapper class.
    """
    from trajectory.common.logger import trajectory_logger

    (
        span_name,
        original_create,
        original_responses_create,
        original_stream,
        original_beta_parse,
    ) = _get_client_config(client)

    def process_span(span, response):
        """Format and record the output in the span"""
        output, usage = _format_output_data(client, response)
        span.record_output(output)
        span.record_usage(usage)

        return response

    def _effective_agent(kwargs: dict) -> str | None:
        # Allow per-call override and avoid leaking unknown kwargs to provider SDKs
        before = list(kwargs.keys())
        local = (
            kwargs.pop("agent_name", None)
            or kwargs.pop("agent", None)
            or kwargs.pop("judgeval_agent", None)
        )
        after = list(kwargs.keys())
        trajectory_logger.debug(
            f"trajectory.wrap::_effective_agent keys before={before} after={after} picked={local or agent_name or getattr(client, 'agent_name', None)}"
        )
        return local or agent_name or getattr(client, "agent_name", None)

    def wrapped(function):
        def wrapper(*args, **kwargs):
            trajectory_logger.debug(
                f"trajectory.wrap: intercepted sync call {getattr(function, '__qualname__', str(function))} initial_kwargs={list(kwargs.keys())}"
            )
            current_trace = _get_current_trace(trace_across_async_contexts)
            if not current_trace:
                # still strip agent_name to avoid SDK errors if user passed it
                _ = _effective_agent(kwargs)
                trajectory_logger.debug(
                    f"trajectory.wrap: no current_trace; forwarding with kwargs={list(kwargs.keys())}"
                )
                return function(*args, **kwargs)

            with current_trace.span(span_name, span_type="llm") as span:
                eff_agent = _effective_agent(kwargs)
                trajectory_logger.debug(
                    f"trajectory.wrap: span started; eff_agent={eff_agent} forwarding kwargs={list(kwargs.keys())}"
                )
                span.record_input(kwargs)
                if eff_agent:
                    span.record_agent_name(eff_agent)

                try:
                    response = function(*args, **kwargs)
                    return process_span(span, response)
                except Exception as e:
                    trajectory_logger.error(f"LLM call error in wrapped client: {e}")
                    _capture_exception_for_trace(current_trace, sys.exc_info())
                    raise e

        return wrapper

    def wrapped_async(function):
        async def wrapper(*args, **kwargs):
            trajectory_logger.debug(
                f"trajectory.wrap: intercepted async call {getattr(function, '__qualname__', str(function))} initial_kwargs={list(kwargs.keys())}"
            )
            current_trace = _get_current_trace(trace_across_async_contexts)
            if not current_trace:
                _ = _effective_agent(kwargs)
                trajectory_logger.debug(
                    f"trajectory.wrap: no current_trace (async); forwarding with kwargs={list(kwargs.keys())}"
                )
                return await function(*args, **kwargs)

            with current_trace.span(span_name, span_type="llm") as span:
                eff_agent = _effective_agent(kwargs)
                trajectory_logger.debug(
                    f"trajectory.wrap: span started (async); eff_agent={eff_agent} forwarding kwargs={list(kwargs.keys())}"
                )
                span.record_input(kwargs)
                if eff_agent:
                    span.record_agent_name(eff_agent)

                try:
                    response = await function(*args, **kwargs)
                    return process_span(span, response)
                except Exception as e:
                    trajectory_logger.error(
                        f"LLM async call error in wrapped client: {e}"
                    )
                    _capture_exception_for_trace(current_trace, sys.exc_info())
                    raise e

        return wrapper

    if isinstance(client, (OpenAI)):
        client.chat.completions.create = wrapped(original_create)
        client.responses.create = wrapped(original_responses_create)
        client.beta.chat.completions.parse = wrapped(original_beta_parse)
    elif isinstance(client, (AsyncOpenAI)):
        client.chat.completions.create = wrapped_async(original_create)
        client.responses.create = wrapped_async(original_responses_create)
        client.beta.chat.completions.parse = wrapped_async(original_beta_parse)
    elif isinstance(client, (Together)):
        client.chat.completions.create = wrapped(original_create)
    elif isinstance(client, (AsyncTogether)):
        client.chat.completions.create = wrapped_async(original_create)
    elif isinstance(client, (Anthropic)):
        client.messages.create = wrapped(original_create)
    elif isinstance(client, (AsyncAnthropic)):
        client.messages.create = wrapped_async(original_create)
    elif isinstance(client, (genai.Client)):
        client.models.generate_content = wrapped(original_create)
    elif isinstance(client, (genai.client.AsyncClient)):
        client.models.generate_content = wrapped_async(original_create)

    return client


# Helper functions for client-specific operations


def _get_client_config(
    client: ApiClient,
) -> tuple[str, Callable, Callable | None, Callable | None, Callable | None]:
    """Returns configuration tuple for the given API client.

    Args:
        client: An instance of OpenAI, Together, or Anthropic client

    Returns:
        tuple: (span_name, create_method, responses_method, stream_method, beta_parse_method)
            - span_name: String identifier for tracing
            - create_method: Reference to the client's creation method
            - responses_method: Reference to the client's responses method (if applicable)
            - stream_method: Reference to the client's stream method (if applicable)
            - beta_parse_method: Reference to the client's beta parse method (if applicable)

    Raises:
        ValueError: If client type is not supported
    """
    if isinstance(client, (OpenAI, AsyncOpenAI)):
        return (
            "OPENAI_API_CALL",
            client.chat.completions.create,
            client.responses.create,
            None,
            client.beta.chat.completions.parse,
        )
    elif isinstance(client, (Together, AsyncTogether)):
        return "TOGETHER_API_CALL", client.chat.completions.create, None, None, None
    elif isinstance(client, (Anthropic, AsyncAnthropic)):
        return (
            "ANTHROPIC_API_CALL",
            client.messages.create,
            None,
            client.messages.stream,
            None,
        )
    elif isinstance(client, (genai.Client, genai.client.AsyncClient)):
        return "GOOGLE_API_CALL", client.models.generate_content, None, None, None
    raise ValueError(f"Unsupported client type: {type(client)}")


def _format_output_data(
    client: ApiClient, response: Any
) -> tuple[str | None, TraceUsage | None]:
    """Format API response data based on client type."""
    prompt_tokens = 0
    completion_tokens = 0
    cache_read_input_tokens = 0
    cache_creation_input_tokens = 0
    model_name = None
    message_content = None

    if isinstance(client, (OpenAI, AsyncOpenAI)):
        if isinstance(response, ChatCompletion):
            model_name = response.model
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            cache_read_input_tokens = response.usage.prompt_tokens_details.cached_tokens

            if isinstance(response, ParsedChatCompletion):
                message_content = response.choices[0].message.parsed
            else:
                # Handle tool calls properly
                message = response.choices[0].message
                if message.content is not None:
                    message_content = message.content
                elif message.tool_calls:
                    # Extract tool call information
                    tool_calls = []
                    for tool_call in message.tool_calls:
                        tool_calls.append(
                            {
                                "id": tool_call.id,
                                "type": tool_call.type,
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments,
                                },
                            }
                        )
                    message_content = f"Tool calls: {tool_calls}"
                else:
                    message_content = "No content or tool calls"
        elif isinstance(response, Response):
            model_name = response.model
            prompt_tokens = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens
            cache_read_input_tokens = response.usage.input_tokens_details.cached_tokens
            message_content = "".join(seg.text for seg in response.output[0].content)

        # Note: LiteLLM seems to use cache_read_input_tokens to calculate the cost for OpenAI
    elif isinstance(client, (Together, AsyncTogether)):
        model_name = "together_ai/" + response.model
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        message_content = response.choices[0].message.content

        # As of 2025-07-14, Together does not do any input cache token tracking
    elif isinstance(client, (genai.Client, genai.client.AsyncClient)):
        model_name = response.model_version
        prompt_tokens = response.usage_metadata.prompt_token_count
        completion_tokens = response.usage_metadata.candidates_token_count
        message_content = response.candidates[0].content.parts[0].text

        if hasattr(response.usage_metadata, "cached_content_token_count"):
            cache_read_input_tokens = response.usage_metadata.cached_content_token_count
    elif isinstance(client, (Anthropic, AsyncAnthropic)):
        model_name = response.model
        prompt_tokens = response.usage.input_tokens
        completion_tokens = response.usage.output_tokens
        cache_read_input_tokens = response.usage.cache_read_input_tokens
        cache_creation_input_tokens = response.usage.cache_creation_input_tokens
        message_content = response.content[0].text
    else:
        trajectory_logger.warning(f"Unsupported client type: {type(client)}")
        return None, None

    prompt_cost, completion_cost = cost_per_token(
        model=model_name,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cache_read_input_tokens=cache_read_input_tokens,
        cache_creation_input_tokens=cache_creation_input_tokens,
    )
    total_cost_usd = (
        (prompt_cost + completion_cost) if prompt_cost and completion_cost else None
    )
    usage = TraceUsage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
        cache_read_input_tokens=cache_read_input_tokens,
        cache_creation_input_tokens=cache_creation_input_tokens,
        prompt_tokens_cost_usd=prompt_cost,
        completion_tokens_cost_usd=completion_cost,
        total_cost_usd=total_cost_usd,
        model_name=model_name,
    )
    return message_content, usage


def combine_args_kwargs(func, args, kwargs):
    """
    Combine positional arguments and keyword arguments into a single dictionary.

    Args:
        func: The function being called
        args: Tuple of positional arguments
        kwargs: Dictionary of keyword arguments

    Returns:
        A dictionary combining both args and kwargs
    """
    try:
        import inspect

        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())

        args_dict = {}
        for i, arg in enumerate(args):
            if i < len(param_names):
                args_dict[param_names[i]] = arg
            else:
                args_dict[f"arg{i}"] = arg

        return {**args_dict, **kwargs}
    except Exception:
        # Fallback if signature inspection fails
        return {**{f"arg{i}": arg for i, arg in enumerate(args)}, **kwargs}


def cost_per_token(*args, **kwargs):
    try:
        prompt_tokens_cost_usd_dollar, completion_tokens_cost_usd_dollar = (
            _original_cost_per_token(*args, **kwargs)
        )
        if (
            prompt_tokens_cost_usd_dollar == 0
            and completion_tokens_cost_usd_dollar == 0
        ):
            trajectory_logger.warning(
                "LiteLLM returned a total of 0 for cost per token"
            )
        return prompt_tokens_cost_usd_dollar, completion_tokens_cost_usd_dollar
    except Exception as e:
        trajectory_logger.warning(f"Error calculating cost per token: {e}")
        return None, None


# --- Helper function for instance-prefixed qual_name ---
def get_instance_prefixed_name(instance, class_name, class_identifiers):
    """
    Returns the agent name (prefix) if the class and attribute are found in class_identifiers.
    Otherwise, returns None.
    """
    if class_name in class_identifiers:
        class_config = class_identifiers[class_name]
        attr = class_config["identifier"]

        if hasattr(instance, attr):
            instance_name = getattr(instance, attr)
            return instance_name
        else:
            raise Exception(
                f"Attribute {attr} does not exist for {class_name}. Check your identify() decorator."
            )
    return None
