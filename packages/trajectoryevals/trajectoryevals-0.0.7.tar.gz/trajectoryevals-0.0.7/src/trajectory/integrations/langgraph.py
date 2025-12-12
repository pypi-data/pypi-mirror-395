import time
import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.messages.base import BaseMessage
from langchain_core.outputs import LLMResult

from trajectory.common.logger import trajectory_logger
from trajectory.common.tracer import (
    SpanType,
    TraceClient,
    Tracer,
    TraceSpan,
    cost_per_token,
)
from trajectory.data.trace import TraceUsage

# TODO: Figure out how to handle context variables. Current solution is to keep track of current span id in Tracer class


class TrajectoryCallbackHandler(BaseCallbackHandler):
    """
    LangChain Callback Handler using run_id/parent_run_id for hierarchy.
    Manages its own internal TraceClient instance created upon first use.
    Includes verbose logging and defensive checks.
    """

    # Make all properties ignored by LangChain's callback system
    # to prevent unexpected serialization issues.
    lc_serializable = False
    lc_kwargs: dict = {}

    def __init__(self, tracer: Tracer):
        self.tracer = tracer
        self.executed_nodes: list[str] = []
        self._reset_state()

    def _reset_state(self):
        """Reset only the critical execution state for reuse across multiple executions"""
        # Reset core execution state that must be cleared between runs
        self._trace_client: TraceClient | None = None
        self._run_id_to_span_id: dict[UUID, str] = {}
        self._span_id_to_start_time: dict[str, float] = {}
        self._span_id_to_depth: dict[str, int] = {}
        self._root_run_id: UUID | None = None
        self._trace_saved: bool = False
        self.span_id_to_token: dict[str, Any] = {}
        self.trace_id_to_token: dict[str, Any] = {}

        # Add timestamp to track when we last reset
        self._last_reset_time: float = time.time()

        # Also reset tracking/logging variables
        self.executed_nodes: list[str] = []

    def reset(self):
        """Public method to manually reset handler execution state for reuse"""
        self._reset_state()

    def reset_all(self):
        """Public method to reset ALL handler state including tracking/logging data"""
        self._reset_state()

    def _ensure_trace_client(
        self, run_id: UUID, parent_run_id: UUID | None, event_name: str
    ) -> TraceClient | None:
        """
        Ensures the internal trace client is initialized, creating it only once
        per handler instance lifecycle (effectively per graph invocation).
        Returns the client or None.
        """
        trajectory_logger.debug(
            f"Ensuring trace client for run_id: {run_id}, parent_run_id: {parent_run_id}, event_name: {event_name}"
        )

        # If this is a potential new root execution (no parent_run_id) and we had a previous trace saved,
        # reset state to allow reuse of the handler
        if parent_run_id is None and self._trace_saved:
            trajectory_logger.debug(f"Resetting state for new root execution: {run_id}")
            self._reset_state()

        # If a client already exists, return it.
        if self._trace_client:
            trajectory_logger.debug(
                f"Using existing trace client: {self._trace_client.trace_id}"
            )
            return self._trace_client

        # If no client exists, initialize it NOW.
        trace_id = str(uuid.uuid4())
        project = self.tracer.project_name
        trajectory_logger.info(
            f"Creating new trace client: {trace_id} for event: {event_name}"
        )

        try:
            # Use event_name as the initial trace name, might be updated later by on_chain_start if root
            client_instance = TraceClient(
                self.tracer,
                trace_id,
                event_name,
                project_name=project,
                enable_monitoring=self.tracer.enable_monitoring,
                enable_evaluations=self.tracer.enable_evaluations,
            )
            self._trace_client = client_instance
            token = self.tracer.set_current_trace(self._trace_client)
            if token:
                self.trace_id_to_token[trace_id] = token

            if self._trace_client:
                self._root_run_id = run_id
                self._trace_saved = False
                self.tracer._active_trace_client = self._trace_client
                self._trace_client.update_metadata({"is_langgraph": True})
                trajectory_logger.debug(
                    f"Set root run_id: {run_id} for trace: {trace_id}"
                )

                try:
                    trajectory_logger.debug(
                        f"Saving initial trace for live tracking: {trace_id}"
                    )
                    self._trace_client.save(final_save=False)
                    trajectory_logger.debug(
                        f"Successfully saved initial trace: {trace_id}"
                    )
                except Exception as e:
                    trajectory_logger.warning(
                        f"Failed to save initial trace for live tracking: {e}"
                    )
                    import warnings

                    warnings.warn(
                        f"Failed to save initial trace for live tracking: {e}"
                    )

                return self._trace_client
            else:
                trajectory_logger.error("Failed to create trace client")
                return None
        except Exception as e:
            trajectory_logger.error(f"Exception creating trace client: {e}")
            self._trace_client = None
            self._root_run_id = None
            return None

    def _start_span_tracking(
        self,
        trace_client: TraceClient,
        run_id: UUID,
        parent_run_id: UUID | None,
        name: str,
        span_type: SpanType = "span",
        inputs: dict[str, Any] | None = None,
    ) -> None:
        """Start tracking a span, ensuring trace client exists"""
        start_time = time.time()
        span_id = str(uuid.uuid4())
        parent_span_id: str | None = None
        current_depth = 0

        trajectory_logger.debug(
            f"Starting span tracking - span_id: {span_id}, name: {name}, type: {span_type}"
        )
        trajectory_logger.debug(
            f"Parent run_id: {parent_run_id}, current run_id: {run_id}"
        )

        if parent_run_id and parent_run_id in self._run_id_to_span_id:
            parent_span_id = self._run_id_to_span_id[parent_run_id]
            if parent_span_id in self._span_id_to_depth:
                current_depth = self._span_id_to_depth[parent_span_id] + 1
            trajectory_logger.debug(
                f"Found parent span: {parent_span_id}, depth: {current_depth}"
            )

        self._run_id_to_span_id[run_id] = span_id
        self._span_id_to_start_time[span_id] = start_time
        self._span_id_to_depth[span_id] = current_depth

        # create span
        new_span = TraceSpan(
            span_id=span_id,
            trace_id=trace_client.trace_id,
            parent_span_id=parent_span_id,
            function=name,
            depth=current_depth,
            created_at=start_time,
            span_type=span_type,
        )

        # Detect agent name from metadata/tags/kwargs; fallback to node/chain name
        agent_name = None
        try:
            md = (inputs or {}).get("metadata") or {}
            kw = (inputs or {}).get("kwargs") or {}
            tags_list = (inputs or {}).get("tags") or []
            ser = (inputs or {}).get("serialized") or {}

            # 1) explicit metadata keys
            agent_name = (
                md.get("agent_name")
                or md.get("agent")
                or md.get("langgraph_agent")
                or md.get("langgraph_node")  # nodes are often agents in LangGraph
            )

            # 2) tags like "agent:<name>", "role:<name>", "actor:<name>"
            if not agent_name and isinstance(tags_list, (list, tuple)):
                for t in tags_list:
                    if isinstance(t, str) and ":" in t:
                        k, v = t.split(":", 1)
                        if k in ("agent", "role", "actor") and v:
                            agent_name = v
                            break

            # 3) runtime config
            if not agent_name:
                cfg = kw.get("configurable") or {}
                agent_name = cfg.get("agent") or cfg.get("agent_name")

            # 4) serialized hints
            if not agent_name:
                agent_name = ser.get("agent_name") or ser.get("id") or ser.get("name")

            # 5) final fallback – use the node/chain name
            if not agent_name:
                agent_name = name
        except Exception:
            # safety: never block span creation on detection
            agent_name = name

        # store on span so downstream processors/exporters can use it
        new_span.agent_name = agent_name

        # Separate metadata from inputs
        if inputs:
            metadata = {}
            clean_inputs = {}

            # Extract metadata fields
            metadata_fields = ["tags", "metadata", "kwargs", "serialized"]
            for field in metadata_fields:
                if field in inputs:
                    metadata[field] = inputs.pop(field)

            # Store the remaining inputs
            clean_inputs = inputs

            # Set both fields on the span
            new_span.inputs = clean_inputs
            new_span.additional_metadata = metadata
            trajectory_logger.debug(
                f"Span inputs processed - clean_inputs keys: {list(clean_inputs.keys())}, metadata keys: {list(metadata.keys())}"
            )
        else:
            new_span.inputs = {}
            new_span.additional_metadata = {}

        trace_client.add_span(new_span)
        trajectory_logger.debug(
            f"Added span to trace client. Total spans: {len(trace_client.trace_spans)}"
        )

        trace_client.otel_span_processor.queue_span_update(new_span, span_state="input")

        token = self.tracer.set_current_span(span_id)
        if token:
            self.span_id_to_token[span_id] = token
            trajectory_logger.debug(f"Set current span context: {span_id}")

    def _end_span_tracking(
        self,
        trace_client: TraceClient,
        run_id: UUID,
        outputs: Any | None = None,
        error: BaseException | None = None,
    ) -> None:
        """End tracking a span, ensuring trace client exists"""
        from trajectory.common.logger import trajectory_logger

        # Get span ID and check if it exists
        span_id = self._run_id_to_span_id.get(run_id)
        trajectory_logger.debug(
            f"Ending span tracking - run_id: {run_id}, span_id: {span_id}"
        )

        if span_id:
            token = self.span_id_to_token.pop(span_id, None)
            self.tracer.reset_current_span(token, span_id)

        start_time = self._span_id_to_start_time.get(span_id) if span_id else None
        duration = time.time() - start_time if start_time is not None else None

        # Add exit entry (only if span was tracked)
        if span_id:
            trace_span = trace_client.span_id_to_span.get(span_id)
            if trace_span:
                trace_span.duration = duration
                trajectory_logger.debug(
                    f"Updated span duration: {duration:.3f}s for span: {span_id}"
                )

                # Handle outputs and error
                if error:
                    trace_span.output = error
                    trajectory_logger.debug(
                        f"Span {span_id} completed with error: {error}"
                    )
                elif outputs:
                    # Separate metadata from outputs
                    metadata = {}
                    clean_outputs = {}

                    # Extract metadata fields
                    metadata_fields = ["tags", "kwargs"]
                    if isinstance(outputs, dict):
                        for field in metadata_fields:
                            if field in outputs:
                                metadata[field] = outputs.pop(field)

                        # Store the remaining outputs
                        clean_outputs = outputs
                    else:
                        clean_outputs = outputs

                    # Set both fields on the span
                    trace_span.output = clean_outputs
                    if metadata:
                        # Merge with existing metadata
                        existing_metadata = trace_span.additional_metadata or {}
                        trace_span.additional_metadata = {
                            **existing_metadata,
                            **metadata,
                        }
                    trajectory_logger.debug(
                        f"Span {span_id} completed with outputs - keys: {list(clean_outputs.keys()) if isinstance(clean_outputs, dict) else 'non-dict'}"
                    )

                span_state = "error" if error else "completed"
                trace_client.otel_span_processor.queue_span_update(
                    trace_span, span_state=span_state
                )
                trajectory_logger.debug(
                    f"Queued span update for {span_id} with state: {span_state}"
                )

            # Clean up dictionaries for this specific span
            if span_id in self._span_id_to_start_time:
                del self._span_id_to_start_time[span_id]
            if span_id in self._span_id_to_depth:
                del self._span_id_to_depth[span_id]

        # Check if this is the root run ending
        if run_id == self._root_run_id:
            trajectory_logger.info(
                f"Root run ending: {run_id}, trace_id: {trace_client.trace_id}"
            )
            try:
                self._root_run_id = None
                if (
                    self._trace_client and not self._trace_saved
                ):  # Check if not already saved
                    trajectory_logger.info(
                        f"Preparing to save complete trace: {self._trace_client.trace_id}"
                    )
                    trajectory_logger.debug(
                        f"Trace has {len(self._trace_client.trace_spans)} spans"
                    )

                    # Force flush any remaining spans
                    if hasattr(self.tracer, "flush_background_spans"):
                        self.tracer.flush_background_spans()

                    complete_trace_data = {
                        "trace_id": self._trace_client.trace_id,
                        "name": self._trace_client.name,
                        "created_at": datetime.fromtimestamp(
                            self._trace_client.start_time, UTC
                        ).isoformat(),
                        "duration": self._trace_client.get_duration(),
                        "trace_spans": [
                            span.model_dump() for span in self._trace_client.trace_spans
                        ],
                        "offline_mode": self.tracer.offline_mode,
                        "parent_trace_id": self._trace_client.parent_trace_id,
                        "parent_name": self._trace_client.parent_name,
                    }

                    trajectory_logger.debug(
                        "Flushing background spans before final save"
                    )
                    self.tracer.flush_background_spans()

                    trajectory_logger.info(
                        f"Performing final save for trace: {self._trace_client.trace_id}"
                    )
                    trace_id, trace_data = self._trace_client.save(
                        final_save=True,  # Final save with usage counter updates
                    )
                    token = self.trace_id_to_token.pop(trace_id, None)
                    self.tracer.reset_current_trace(token, trace_id)

                    # Store complete trace data instead of server response
                    self.tracer.traces.append(complete_trace_data)
                    self._trace_saved = True  # Set flag only after successful save
                    trajectory_logger.info(
                        f"Successfully saved complete trace: {trace_id}"
                    )
            except Exception as e:
                trajectory_logger.error(f"Error during final trace save: {e}")
                trajectory_logger.debug(f"Final trace save error details: {e!s}")
            finally:
                # This block executes regardless of save success/failure
                # Reset root run id
                self._root_run_id = None
                # Reset input storage for this handler instance
                if self.tracer._active_trace_client == self._trace_client:
                    self.tracer._active_trace_client = None
                trajectory_logger.debug("Cleaned up trace client references")

    # --- Callback Methods ---
    # Each method now ensures the trace client exists before proceeding

    def on_retriever_start(
        self,
        serialized: dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        serialized_name = (
            serialized.get("name", "Unknown")
            if serialized
            else "Unknown (Serialized=None)"
        )

        name = f"RETRIEVER_{(serialized_name).upper()}"
        trace_client = self._ensure_trace_client(run_id, parent_run_id, name)
        if not trace_client:
            return

        inputs = {
            "query": query,
            "tags": tags,
            "metadata": metadata,
            "kwargs": kwargs,
            "serialized": serialized,
        }
        self._start_span_tracking(
            trace_client,
            run_id,
            parent_run_id,
            name,
            span_type="retriever",
            inputs=inputs,
        )

    def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        trace_client = self._ensure_trace_client(run_id, parent_run_id, "RetrieverEnd")
        if not trace_client:
            return
        doc_summary = [
            {
                "index": i,
                "page_content": (
                    doc.page_content[:100] + "..."
                    if len(doc.page_content) > 100
                    else doc.page_content
                ),
                "metadata": doc.metadata,
            }
            for i, doc in enumerate(documents)
        ]
        outputs = {
            "document_count": len(documents),
            "documents": doc_summary,
            "kwargs": kwargs,
        }
        self._end_span_tracking(trace_client, run_id, outputs=outputs)

    def on_chain_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        serialized_name = (
            serialized.get("name") if serialized else "Unknown (Serialized=None)"
        )

        # --- Determine Name and Span Type ---
        span_type: SpanType = "chain"
        name = serialized_name if serialized_name else "Unknown Chain"
        node_name = metadata.get("langgraph_node") if metadata else None
        is_langgraph_root_kwarg = (
            kwargs.get("name") == "LangGraph"
        )  # Check kwargs for explicit root name
        # More robust root detection: Often the first chain event with parent_run_id=None *is* the root.
        is_potential_root_event = parent_run_id is None

        trajectory_logger.debug(
            f"Chain start - run_id: {run_id}, parent_run_id: {parent_run_id}, serialized_name: {serialized_name}"
        )
        trajectory_logger.debug(
            f"Node name: {node_name}, is_root: {is_potential_root_event}, is_langgraph_root: {is_langgraph_root_kwarg}"
        )

        if node_name:
            name = node_name  # Use node name if available
            if name not in self.executed_nodes:
                self.executed_nodes.append(
                    name
                )  # Leaving this in for now but can probably be removed
                trajectory_logger.debug(f"Added new executed node: {name}")
        elif is_langgraph_root_kwarg and is_potential_root_event:
            name = "LangGraph"  # Explicit root detected
            trajectory_logger.debug("Detected LangGraph root chain")
        # Add handling for other potential LangChain internal chains if needed, e.g., "RunnableSequence"

        trace_client = self._ensure_trace_client(run_id, parent_run_id, name)
        if not trace_client:
            trajectory_logger.warning(
                f"Failed to ensure trace client for chain: {name}"
            )
            return

        if (
            is_potential_root_event
            and run_id == self._root_run_id
            and trace_client.name != name
        ):
            trajectory_logger.debug(
                f"Updating trace client name from {trace_client.name} to {name}"
            )
            trace_client.name = name

        combined_inputs = {
            "inputs": inputs,
            "tags": tags,
            "metadata": metadata,
            "kwargs": kwargs,
            "serialized": serialized,
        }
        trajectory_logger.debug(f"Starting chain span tracking for: {name}")
        self._start_span_tracking(
            trace_client,
            run_id,
            parent_run_id,
            name,
            span_type=span_type,
            inputs=combined_inputs,
        )

    def on_chain_end(
        self,
        outputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> Any:
        trajectory_logger.debug(
            f"Chain end - run_id: {run_id}, parent_run_id: {parent_run_id}"
        )
        trajectory_logger.debug(
            f"Outputs keys: {list(outputs.keys()) if isinstance(outputs, dict) else 'non-dict'}"
        )

        trace_client = self._ensure_trace_client(run_id, parent_run_id, "ChainEnd")
        if not trace_client:
            trajectory_logger.warning(
                f"Failed to ensure trace client for chain end: {run_id}"
            )
            return

        span_id = self._run_id_to_span_id.get(run_id)
        if not span_id and run_id != self._root_run_id:
            trajectory_logger.debug(f"No span_id found for run_id: {run_id}, skipping")
            return

        combined_outputs = {"outputs": outputs, "tags": tags, "kwargs": kwargs}
        trajectory_logger.debug(f"Ending chain span tracking for run_id: {run_id}")

        self._end_span_tracking(trace_client, run_id, outputs=combined_outputs)

        if run_id == self._root_run_id:
            trajectory_logger.info(f"Root chain ending: {run_id}")
            if trace_client and not self._trace_saved:
                trajectory_logger.info(
                    f"Preparing to save complete trace from chain end: {trace_client.trace_id}"
                )
                complete_trace_data = {
                    "trace_id": trace_client.trace_id,
                    "name": trace_client.name,
                    "created_at": datetime.fromtimestamp(
                        trace_client.start_time, UTC
                    ).isoformat(),
                    "duration": trace_client.get_duration(),
                    "trace_spans": [
                        span.model_dump() for span in trace_client.trace_spans
                    ],
                    "offline_mode": self.tracer.offline_mode,
                    "parent_trace_id": trace_client.parent_trace_id,
                    "parent_name": trace_client.parent_name,
                }

                trajectory_logger.debug(
                    "Flushing background spans before chain end save"
                )
                self.tracer.flush_background_spans()

                trajectory_logger.info(
                    f"Performing final save from chain end for trace: {trace_client.trace_id}"
                )
                trace_client.save(
                    final_save=True,
                )

                self.tracer.traces.append(complete_trace_data)
                self._trace_saved = True
                trajectory_logger.info(
                    f"Successfully saved complete trace from chain end: {trace_client.trace_id}"
                )
                if self.tracer._active_trace_client == trace_client:
                    self.tracer._active_trace_client = None

            self._root_run_id = None
            trajectory_logger.debug("Reset root run_id")

    def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        trace_client = self._ensure_trace_client(run_id, parent_run_id, "ChainError")
        if not trace_client:
            return

        span_id = self._run_id_to_span_id.get(run_id)

        if not span_id and run_id != self._root_run_id:
            return

        self._end_span_tracking(trace_client, run_id, error=error)

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        inputs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        name = (
            serialized.get("name", "Unnamed Tool")
            if serialized
            else "Unknown Tool (Serialized=None)"
        )

        trace_client = self._ensure_trace_client(run_id, parent_run_id, name)
        if not trace_client:
            return

        combined_inputs = {
            "input_str": input_str,
            "inputs": inputs,
            "tags": tags,
            "metadata": metadata,
            "kwargs": kwargs,
            "serialized": serialized,
        }
        self._start_span_tracking(
            trace_client,
            run_id,
            parent_run_id,
            name,
            span_type="tool",
            inputs=combined_inputs,
        )

    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        trace_client = self._ensure_trace_client(run_id, parent_run_id, "ToolEnd")
        if not trace_client:
            return
        outputs = {"output": output, "kwargs": kwargs}
        self._end_span_tracking(trace_client, run_id, outputs=outputs)

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        trace_client = self._ensure_trace_client(run_id, parent_run_id, "ToolError")
        if not trace_client:
            return
        self._end_span_tracking(trace_client, run_id, error=error)

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        invocation_params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> Any:
        llm_name = name or serialized.get("name", "LLM Call")

        trace_client = self._ensure_trace_client(run_id, parent_run_id, llm_name)
        if not trace_client:
            return
        inputs = {
            "prompts": prompts,
            "invocation_params": invocation_params or kwargs,
            "options": options,
            "tags": tags,
            "metadata": metadata,
            "serialized": serialized,
        }
        self._start_span_tracking(
            trace_client,
            run_id,
            parent_run_id,
            llm_name,
            span_type="llm",
            inputs=inputs,
        )

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        trace_client = self._ensure_trace_client(run_id, parent_run_id, "LLMEnd")
        if not trace_client:
            return
        outputs = {"response": response, "kwargs": kwargs}

        prompt_tokens = None
        completion_tokens = None
        total_tokens = None
        model_name = None

        # Extract model name from response if available
        if (
            hasattr(response, "llm_output")
            and response.llm_output
            and isinstance(response.llm_output, dict)
        ):
            model_name = response.llm_output.get(
                "model_name"
            ) or response.llm_output.get("model")

        # Try to get model from the first generation if available
        if not model_name and response.generations and len(response.generations) > 0:
            if (
                hasattr(response.generations[0][0], "generation_info")
                and response.generations[0][0].generation_info
            ):
                gen_info = response.generations[0][0].generation_info
                model_name = gen_info.get("model") or gen_info.get("model_name")

        if response.llm_output and isinstance(response.llm_output, dict):
            # Check for OpenAI/standard 'token_usage' first
            if "token_usage" in response.llm_output:
                token_usage = response.llm_output.get("token_usage")
                if token_usage and isinstance(token_usage, dict):
                    prompt_tokens = token_usage.get("prompt_tokens")
                    completion_tokens = token_usage.get("completion_tokens")
                    total_tokens = token_usage.get(
                        "total_tokens"
                    )  # OpenAI provides total
            # Check for Anthropic 'usage'
            elif "usage" in response.llm_output:
                token_usage = response.llm_output.get("usage")
                if token_usage and isinstance(token_usage, dict):
                    prompt_tokens = token_usage.get(
                        "input_tokens"
                    )  # Anthropic uses input_tokens
                    completion_tokens = token_usage.get(
                        "output_tokens"
                    )  # Anthropic uses output_tokens
                    # Calculate total if possible
                    if prompt_tokens is not None and completion_tokens is not None:
                        total_tokens = prompt_tokens + completion_tokens

            if prompt_tokens is not None or completion_tokens is not None:
                prompt_cost = None
                completion_cost = None
                total_cost_usd = None

                if (
                    model_name
                    and prompt_tokens is not None
                    and completion_tokens is not None
                ):
                    try:
                        prompt_cost, completion_cost = cost_per_token(
                            model=model_name,
                            prompt_tokens=prompt_tokens,
                            completion_tokens=completion_tokens,
                        )
                        total_cost_usd = (
                            (prompt_cost + completion_cost)
                            if prompt_cost and completion_cost
                            else None
                        )
                    except Exception as e:
                        # If cost calculation fails, continue without costs
                        import warnings

                        warnings.warn(
                            f"Failed to calculate token costs for model {model_name}: {e}"
                        )

                usage = TraceUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens
                    or (
                        prompt_tokens + completion_tokens
                        if prompt_tokens and completion_tokens
                        else None
                    ),
                    prompt_tokens_cost_usd=prompt_cost,
                    completion_tokens_cost_usd=completion_cost,
                    total_cost_usd=total_cost_usd,
                    model_name=model_name,
                )

                span_id = self._run_id_to_span_id.get(run_id)
                if span_id and span_id in trace_client.span_id_to_span:
                    trace_span = trace_client.span_id_to_span[span_id]
                    trace_span.usage = usage

        self._end_span_tracking(trace_client, run_id, outputs=outputs)

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        trace_client = self._ensure_trace_client(run_id, parent_run_id, "LLMError")
        if not trace_client:
            return
        self._end_span_tracking(trace_client, run_id, error=error)

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        invocation_params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> Any:
        chat_model_name = name or serialized.get("name", "ChatModel Call")
        is_openai = (
            any(
                key.startswith("openai") for key in serialized.get("secrets", {}).keys()
            )
            or "openai" in chat_model_name.lower()
        )
        is_anthropic = (
            any(
                key.startswith("anthropic")
                for key in serialized.get("secrets", {}).keys()
            )
            or "anthropic" in chat_model_name.lower()
            or "claude" in chat_model_name.lower()
        )
        is_together = (
            any(
                key.startswith("together")
                for key in serialized.get("secrets", {}).keys()
            )
            or "together" in chat_model_name.lower()
        )

        is_google = (
            any(
                key.startswith("google") for key in serialized.get("secrets", {}).keys()
            )
            or "google" in chat_model_name.lower()
            or "gemini" in chat_model_name.lower()
        )

        if is_openai and "OPENAI_API_CALL" not in chat_model_name:
            chat_model_name = f"{chat_model_name} OPENAI_API_CALL"
        elif is_anthropic and "ANTHROPIC_API_CALL" not in chat_model_name:
            chat_model_name = f"{chat_model_name} ANTHROPIC_API_CALL"
        elif is_together and "TOGETHER_API_CALL" not in chat_model_name:
            chat_model_name = f"{chat_model_name} TOGETHER_API_CALL"

        elif is_google and "GOOGLE_API_CALL" not in chat_model_name:
            chat_model_name = f"{chat_model_name} GOOGLE_API_CALL"

        trace_client = self._ensure_trace_client(run_id, parent_run_id, chat_model_name)
        if not trace_client:
            return
        inputs = {
            "messages": messages,
            "invocation_params": invocation_params or kwargs,
            "options": options,
            "tags": tags,
            "metadata": metadata,
            "serialized": serialized,
        }
        self._start_span_tracking(
            trace_client,
            run_id,
            parent_run_id,
            chat_model_name,
            span_type="llm",
            inputs=inputs,
        )

    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        action_tool = action.tool
        name = f"AGENT_ACTION_{(action_tool).upper()}"
        trace_client = self._ensure_trace_client(run_id, parent_run_id, name)
        if not trace_client:
            return

        inputs = {
            "tool_input": action.tool_input,
            "log": action.log,
            "messages": action.messages,
            "kwargs": kwargs,
        }
        self._start_span_tracking(
            trace_client, run_id, parent_run_id, name, span_type="agent", inputs=inputs
        )

    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        trace_client = self._ensure_trace_client(run_id, parent_run_id, "AgentFinish")
        if not trace_client:
            return

        outputs = {
            "return_values": finish.return_values,
            "log": finish.log,
            "messages": finish.messages,
            "kwargs": kwargs,
        }
        self._end_span_tracking(trace_client, run_id, outputs=outputs)
