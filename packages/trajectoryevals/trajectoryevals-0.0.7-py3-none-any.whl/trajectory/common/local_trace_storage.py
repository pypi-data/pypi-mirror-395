"""
Local trace storage for Trajectory SDK when remote tracing is disabled
"""

import json
import os
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from .constants import (
    DEFAULT_LOCAL_TRACING_DIR,
    TRAJECTORY_ONLY_LOCAL_TRACING_ENV,
    TRAJECTORY_TRACING_LOCAL_DIR_ENV,
    TRAJECTORY_TRACING_LOCAL_ENV,
)
from .logger import trajectory_logger


class LocalTraceStorage:
    """
    Handles local storage of traces when remote tracing is disabled
    """

    def __init__(self, storage_dir: str | None = None):
        """
        Initialize local trace storage

        Args:
            storage_dir: Directory to store traces. If None, uses environment variable or default
        """
        self.storage_dir = self._get_storage_directory(storage_dir)
        self._ensure_storage_directory()
        # Maintain stable filenames per trace_id across multiple saves
        self._trace_file_map: dict[str, str] = {}

        trajectory_logger.info(
            f"Local trace storage initialized at: {self.storage_dir}"
        )

    def _json_default(self, obj: Any):
        """Best-effort JSON serializer for complex objects (e.g., LangChain messages)."""
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, set):
                return list(obj)
            # Pydantic models or similar
            if hasattr(obj, "model_dump") and callable(obj.model_dump):
                return obj.model_dump()
            if hasattr(obj, "dict") and callable(obj.dict):
                return obj.dict()
            if hasattr(obj, "__dict__"):
                # Shallow conversion for unknown objects
                return {k: v for k, v in obj.__dict__.items() if not k.startswith("__")}
            return str(obj)
        except Exception:
            return repr(obj)

    def _get_storage_directory(self, storage_dir: str | None = None) -> str:
        """Get the storage directory from parameter, environment, or default"""
        if storage_dir:
            return storage_dir

        env_dir = os.getenv(TRAJECTORY_TRACING_LOCAL_DIR_ENV)
        if env_dir:
            return env_dir

        return DEFAULT_LOCAL_TRACING_DIR

    def _ensure_storage_directory(self):
        """Ensure the storage directory exists"""
        Path(self.storage_dir).mkdir(parents=True, exist_ok=True)

    def save_trace(
        self,
        trace_data: dict[str, Any],
        trace_id: str | None = None,
        final_save: bool = False,
    ) -> str:
        """
        Save a trace to local storage

        Args:
            trace_data: The trace data to save
            trace_id: Optional trace ID. If not provided, generates one

        Returns:
            The trace ID used for saving
        """
        if trace_id is None:
            trace_id = str(uuid.uuid4())

        # Add metadata
        trace_data_with_metadata = {
            "trace_id": trace_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "storage_type": "local",
            "data": trace_data,
        }

        # Determine stable filename for a given trace_id. Create once per trace.
        if trace_id in self._trace_file_map:
            filepath = self._trace_file_map[trace_id]
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trace_{timestamp}_{trace_id[:8]}.json"
            filepath = os.path.join(self.storage_dir, filename)
            self._trace_file_map[trace_id] = filepath

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(
                    trace_data_with_metadata,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=self._json_default,
                )

            trajectory_logger.debug(f"Trace saved locally: {filepath}")
            trajectory_logger.debug(
                f"Trace file size: {os.path.getsize(filepath)} bytes"
            )
            # If this was the final save, clear the mapping to allow new filename for future traces
            if final_save and trace_id in self._trace_file_map:
                self._trace_file_map.pop(trace_id, None)
            return trace_id

        except Exception as e:
            trajectory_logger.error(f"Failed to save trace locally: {e!s}")
            raise

    def save_span(
        self, span_data: dict[str, Any], trace_id: str, span_id: str | None = None
    ) -> str:
        """
        Save a span to local storage

        Args:
            span_data: The span data to save
            trace_id: The trace ID this span belongs to
            span_id: Optional span ID. If not provided, generates one

        Returns:
            The span ID used for saving
        """
        if span_id is None:
            span_id = str(uuid.uuid4())

        # Add metadata
        span_data_with_metadata = {
            "span_id": span_id,
            "trace_id": trace_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "storage_type": "local",
            "data": span_data,
        }

        # Write span data into the same trace file to avoid multiple files per trace_id
        # Ensure a filepath is established for the trace
        if trace_id in self._trace_file_map:
            filepath = self._trace_file_map[trace_id]
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trace_{timestamp}_{trace_id[:8]}.json"
            filepath = os.path.join(self.storage_dir, filename)
            self._trace_file_map[trace_id] = filepath

        try:
            # Merge span into existing trace file structure
            base_payload = None
            if os.path.exists(filepath):
                try:
                    with open(filepath, encoding="utf-8") as rf:
                        base_payload = json.load(rf)
                except Exception:
                    base_payload = None

            if not base_payload or not isinstance(base_payload, dict):
                base_payload = {
                    "trace_id": trace_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "storage_type": "local",
                    "data": {
                        "trace_id": trace_id,
                        "trace_spans": [],
                    },
                }

            # Append span data
            spans_list = base_payload.setdefault("data", {}).setdefault(
                "trace_spans", []
            )
            spans_list.append(span_data_with_metadata.get("data", span_data))

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(
                    base_payload,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=self._json_default,
                )

            trajectory_logger.debug(f"Span merged into trace file: {filepath}")
            return span_id

        except Exception as e:
            trajectory_logger.error(f"Failed to save span locally: {e!s}")
            raise

    def list_traces(self) -> list[dict[str, Any]]:
        """
        List all traces in the storage directory

        Returns:
            List of trace metadata
        """
        traces = []

        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith("trace_") and filename.endswith(".json"):
                    filepath = os.path.join(self.storage_dir, filename)
                    try:
                        with open(filepath, encoding="utf-8") as f:
                            trace_data = json.load(f)
                            traces.append(
                                {
                                    "filename": filename,
                                    "filepath": filepath,
                                    "trace_id": trace_data.get("trace_id"),
                                    "timestamp": trace_data.get("timestamp"),
                                    "size": os.path.getsize(filepath),
                                }
                            )
                    except Exception as e:
                        trajectory_logger.warning(
                            f"Failed to read trace file {filename}: {e!s}"
                        )

        except Exception as e:
            trajectory_logger.error(f"Failed to list traces: {e!s}")

        return sorted(traces, key=lambda x: x["timestamp"], reverse=True)

    def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        """
        Get a specific trace by ID

        Args:
            trace_id: The trace ID to retrieve

        Returns:
            The trace data if found, None otherwise
        """
        for filename in os.listdir(self.storage_dir):
            if filename.startswith("trace_") and filename.endswith(".json"):
                if trace_id in filename:
                    filepath = os.path.join(self.storage_dir, filename)
                    try:
                        with open(filepath, encoding="utf-8") as f:
                            return json.load(f)
                    except Exception as e:
                        trajectory_logger.warning(
                            f"Failed to read trace file {filename}: {e!s}"
                        )

        return None

    def cleanup_old_traces(self, days_to_keep: int = 30):
        """
        Clean up traces older than specified days

        Args:
            days_to_keep: Number of days to keep traces
        """
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        removed_count = 0

        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith(("trace_", "span_")) and filename.endswith(
                    ".json"
                ):
                    filepath = os.path.join(self.storage_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))

                    if file_time < cutoff_date:
                        os.remove(filepath)
                        removed_count += 1
                        trajectory_logger.debug(f"Removed old trace file: {filename}")

            trajectory_logger.info(
                f"Cleanup completed: removed {removed_count} old trace files"
            )

        except Exception as e:
            trajectory_logger.error(f"Failed to cleanup old traces: {e!s}")


def is_local_tracing_enabled() -> bool:
    """
    Check if local tracing is enabled via environment variable

    Returns:
        True if local tracing is enabled, False otherwise
    """
    return os.getenv(TRAJECTORY_TRACING_LOCAL_ENV, "false").lower() == "true"


def is_only_local_tracing_enabled() -> bool:
    """
    Check if only local tracing is enabled (no remote server calls)

    Returns:
        True if only local tracing is enabled, False otherwise
    """
    return os.getenv(TRAJECTORY_ONLY_LOCAL_TRACING_ENV, "false").lower() == "true"


def get_local_storage_dir() -> str:
    """
    Get the local storage directory from environment or default

    Returns:
        The local storage directory path
    """
    return os.getenv(TRAJECTORY_TRACING_LOCAL_DIR_ENV, DEFAULT_LOCAL_TRACING_DIR)
