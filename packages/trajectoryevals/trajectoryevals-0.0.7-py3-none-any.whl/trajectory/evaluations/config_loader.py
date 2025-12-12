from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class EvaluationConfigError(ValueError):
    """Raised when the evaluation config file is invalid."""


@dataclass(frozen=True)
class MockAppConfig:
    docker_remote_image: str
    port: int
    name: str | None = None
    base_url: str | None = None

    def resolved_base_url(self) -> str:
        base = self.base_url or f"http://localhost:{self.port}"
        return base.rstrip("/")


@dataclass(frozen=True)
class DatasetConfig:
    dataset_id: str
    dataset_name: str
    env_variable_to_override: str
    task_ids: list[str] | None = None


@dataclass(frozen=True)
class EvaluationConfig:
    datasets: list[DatasetConfig]
    mock_app: MockAppConfig

    @classmethod
    def from_file(cls, path: str | Path) -> EvaluationConfig:
        config_path = Path(path).expanduser().resolve()
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)

        if not isinstance(data, dict):
            raise EvaluationConfigError("Config file must be a mapping.")

        mock_app = cls._parse_mock_app(data.get("mock_app"))
        datasets_raw = data.get("datasets")
        if not isinstance(datasets_raw, list) or not datasets_raw:
            raise EvaluationConfigError(
                "Config must contain a non-empty 'datasets' list."
            )

        datasets = [cls._parse_dataset(entry) for entry in datasets_raw]
        return cls(datasets=datasets, mock_app=mock_app)

    @staticmethod
    def _parse_mock_app(raw: Any) -> MockAppConfig:
        if not isinstance(raw, dict):
            raise EvaluationConfigError("'mock_app' must be a mapping.")

        image = raw.get("docker_remote_image")
        port = raw.get("port")
        if not image or not isinstance(image, str):
            raise EvaluationConfigError("'mock_app.docker_remote_image' is required.")
        if not isinstance(port, int):
            raise EvaluationConfigError("'mock_app.port' must be an integer.")

        name = raw.get("name")
        base_url = raw.get("base_url")

        if name is not None and not isinstance(name, str):
            raise EvaluationConfigError("'mock_app.name' must be a string if provided.")
        if base_url is not None and not isinstance(base_url, str):
            raise EvaluationConfigError(
                "'mock_app.base_url' must be a string if provided."
            )

        return MockAppConfig(
            docker_remote_image=image,
            port=port,
            name=name,
            base_url=base_url,
        )

    @staticmethod
    def _parse_dataset(raw: Any) -> DatasetConfig:
        if not isinstance(raw, dict):
            raise EvaluationConfigError("Each dataset entry must be a mapping.")

        dataset_id = raw.get("dataset_id")
        dataset_name = raw.get("dataset_name")
        env_var = raw.get("env_variable_to_override")

        if not dataset_id or not isinstance(dataset_id, str):
            raise EvaluationConfigError("dataset_id is required for each dataset.")
        if not dataset_name or not isinstance(dataset_name, str):
            raise EvaluationConfigError("dataset_name is required for each dataset.")
        if not env_var or not isinstance(env_var, str):
            raise EvaluationConfigError(
                "env_variable_to_override is required for each dataset."
            )

        task_ids_raw = raw.get("task_ids")
        task_ids: list[str] | None = None
        if task_ids_raw:
            if not isinstance(task_ids_raw, list) or any(
                not isinstance(task_id, str) for task_id in task_ids_raw
            ):
                raise EvaluationConfigError("task_ids must be a list of strings.")
            task_ids = task_ids_raw

        return DatasetConfig(
            dataset_id=dataset_id,
            dataset_name=dataset_name,
            env_variable_to_override=env_var,
            task_ids=task_ids,
        )
