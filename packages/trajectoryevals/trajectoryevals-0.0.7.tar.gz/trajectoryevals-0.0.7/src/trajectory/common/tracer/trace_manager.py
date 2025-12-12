from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from trajectory.common.tracer import Tracer

from rich import print as rprint

from trajectory.common.api import TrajectoryApiClient
from trajectory.common.logger import trajectory_logger


class TraceManagerClient:
    """
    Client for handling trace endpoints with the Trajectory API
    """

    def __init__(
        self,
        trajectory_api_key: str,
        organization_id: str,
        tracer: Tracer | None = None,
    ):
        self.api_client = TrajectoryApiClient(trajectory_api_key, organization_id)
        self.tracer = tracer
        self._background_tasks = set()
        self._executor = ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="trace_upsert"
        )

    def fetch_trace(self, trace_id: str):
        """
        Fetch a trace by its id
        """
        return self.api_client.fetch_trace(trace_id)

    def upsert_trace(
        self,
        trace_data: dict,
        offline_mode: bool = False,
        show_link: bool = True,
        final_save: bool = True,
    ):
        # fire-and-forget in background thread
        self._executor.submit(
            self._upsert_trace_sync, trace_data, offline_mode, show_link, final_save
        )
        return {
            "ui_results_url": None,
            "trace_id": trace_data.get("trace_id"),
            "status": "processing",
            "async": True,
        }

    def _upsert_trace_sync(
        self, trace_data: dict, offline_mode: bool, show_link: bool, final_save: bool
    ):
        try:
            server_response = self.api_client.upsert_trace(trace_data)
            if self.tracer and self.tracer.use_s3 and final_save:
                try:
                    s3_key = self.tracer.s3_storage.save_trace(
                        trace_data=trace_data,
                        trace_id=trace_data["trace_id"],
                        project_name=trace_data["project_name"],
                    )
                    trajectory_logger.info(f"Trace also saved to S3 at key: {s3_key}")
                except Exception as e:
                    trajectory_logger.warning(f"Failed to save trace to S3: {e!s}")
            if not offline_mode and show_link and "ui_results_url" in server_response:
                rprint(
                    f"\n🔍 You can view your trace data here: [rgb(106,0,255)][link={server_response['ui_results_url']}]View Trace[/link]\n"
                )
        except Exception as e:
            trajectory_logger.warning(
                f"Failed to upsert trace {trace_data.get('trace_id')}: {e}"
            )

    def delete_trace(self, trace_id: str):
        """
        Delete a trace from the database.
        """
        return self.api_client.delete_trace(trace_id)

    def delete_traces(self, trace_ids: list[str]):
        """
        Delete a batch of traces from the database.
        """
        return self.api_client.delete_traces(trace_ids)

    def delete_project(self, project_name: str):
        """
        Deletes a project from the server. Which also deletes all evaluations and traces associated with the project.
        """
        return self.api_client.delete_project(project_name)
