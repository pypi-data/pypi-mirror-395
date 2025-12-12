from rich.progress import Progress, SpinnerColumn, TextColumn

from trajectory.common.api import TrajectoryApiClient
from trajectory.common.logger import trajectory_logger
from trajectory.data import Example, Trace
from trajectory.data.datasets import EvalDataset


class EvalDatasetClient:
    def __init__(self, trajectory_api_key: str, organization_id: str):
        self.api_client = TrajectoryApiClient(trajectory_api_key, organization_id)

    def create_dataset(self) -> EvalDataset:
        return EvalDataset(trajectory_api_key=self.api_client.api_key)

    def push(
        self,
        dataset: EvalDataset,
        alias: str,
        project_name: str,
        overwrite: bool | None = False,
    ) -> bool:
        if overwrite:
            trajectory_logger.warning(f"Overwrite enabled for alias '{alias}'")
        """
        Pushes the dataset to Trajectory platform

        Mock request:
        dataset = {
            "alias": alias,
            "examples": [...],
            "overwrite": overwrite
        } ==>
        {
            "_alias": alias,
            "_id": "..."  # ID of the dataset
        }
        """
        with Progress(
            SpinnerColumn(style="rgb(106,0,255)"),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as progress:
            task_id = progress.add_task(
                f"Pushing [rgb(106,0,255)]'{alias}' to Trajectory...",
                total=100,
            )
            try:
                payload = self.api_client.push_dataset(
                    dataset_alias=alias,
                    project_name=project_name,
                    examples=[e.to_dict() for e in dataset.examples],
                    traces=[t.model_dump() for t in dataset.traces],
                    overwrite=overwrite or False,
                )
            except Exception as e:
                trajectory_logger.error(f"Error during push: {e}")
                raise
            dataset._alias = payload.get("_alias")
            dataset._id = payload.get("_id")
            progress.update(
                task_id,
                description=f"{progress.tasks[task_id].description} [rgb(25,227,160)]Done!)",
            )
            return True

    def append_examples(
        self, alias: str, examples: list[Example], project_name: str
    ) -> bool:
        """
        Appends the dataset to Trajectory platform

        Mock request:
        dataset = {
            "alias": alias,
            "examples": [...],
            "project_name": project_name
        } ==>
        {
            "_alias": alias,
            "_id": "..."  # ID of the dataset
        }
        """
        with Progress(
            SpinnerColumn(style="rgb(106,0,255)"),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as progress:
            task_id = progress.add_task(
                f"Appending [rgb(106,0,255)]'{alias}' to Trajectory...",
                total=100,
            )
            try:
                self.api_client.append_examples(
                    dataset_alias=alias,
                    project_name=project_name,
                    examples=[e.to_dict() for e in examples],
                )
            except Exception as e:
                trajectory_logger.error(f"Error during append: {e}")
                raise

            progress.update(
                task_id,
                description=f"{progress.tasks[task_id].description} [rgb(25,227,160)]Done!)",
            )
            return True

    def pull(self, alias: str, project_name: str) -> EvalDataset:
        """
        Pulls the dataset from Trajectory platform

        Mock request:
        {
            "alias": alias,
            "project_name": project_name
        }
        ==>
        {
            "examples": [...],
            "_alias": alias,
            "_id": "..."  # ID of the dataset
        }
        """
        # Make a POST request to the Trajectory API to get the dataset
        dataset = self.create_dataset()

        with Progress(
            SpinnerColumn(style="rgb(106,0,255)"),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as progress:
            task_id = progress.add_task(
                f"Pulling [rgb(106,0,255)]'{alias}'[/rgb(106,0,255)] from Trajectory...",
                total=100,
            )
            try:
                payload = self.api_client.pull_dataset(
                    dataset_alias=alias,
                    project_name=project_name,
                )
            except Exception as e:
                trajectory_logger.error(f"Error pulling dataset: {e!s}")
                raise
            dataset.examples = [Example(**e) for e in payload.get("examples", [])]
            dataset.traces = [Trace(**t) for t in payload.get("traces", [])]
            dataset._alias = payload.get("alias")
            dataset._id = payload.get("id")
            progress.update(
                task_id,
                description=f"{progress.tasks[task_id].description} [rgb(25,227,160)]Done!)",
            )

            return dataset

    def delete(self, alias: str, project_name: str) -> bool:
        with Progress(
            SpinnerColumn(style="rgb(106,0,255)"),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as progress:
            progress.add_task(
                f"Deleting [rgb(106,0,255)]'{alias}'[/rgb(106,0,255)] from Trajectory...",
                total=100,
            )
            try:
                self.api_client.delete_dataset(
                    dataset_alias=alias,
                    project_name=project_name,
                )
            except Exception as e:
                trajectory_logger.error(f"Error deleting dataset: {e!s}")
                raise

            return True

    def pull_project_dataset_stats(self, project_name: str) -> dict:
        """
        Pulls the project datasets stats from Trajectory platform

        Mock request:
        {
            "project_name": project_name
        }
        ==>
        {
            "test_dataset_1": {"examples_count": len(dataset1.examples)},
            "test_dataset_2": {"examples_count": len(dataset2.examples)},
            ...
        }
        """
        # Make a POST request to the Trajectory API to get the dataset

        with Progress(
            SpinnerColumn(style="rgb(106,0,255)"),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as progress:
            task_id = progress.add_task(
                "Pulling [rgb(106,0,255)]' datasets'[/rgb(106,0,255)] from Trajectory...",
                total=100,
            )
            try:
                payload = self.api_client.get_project_dataset_stats(project_name)
            except Exception as e:
                trajectory_logger.error(f"Error pulling dataset: {e!s}")
                raise

            progress.update(
                task_id,
                description=f"{progress.tasks[task_id].description} [rgb(25,227,160)]Done!)",
            )

            return payload
