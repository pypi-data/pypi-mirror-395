- To build/push updated mock app images from `/mock_apps`, run:

```bash
cd mock_apps
python scripts/manage_apps.py build --app workday --tag dev --push
```

This script reads `global_config.yaml` for the default registry and backend URL, ensuring every app under `apps/` can be built and published with a single command.
# Evaluation CLI & Configuration

## Overview

Evaluations now rely on a single structured config file (replacing `datasets.yaml`) and a simplified `traj up` command that starts the required mock application. `BaseEvaluation` reads the same config to discover datasets, task filters, and environment overrides—no more embedded Workday assumptions or on-the-fly Docker management.

## Config File Schema

Example (`examples/datasets.yaml`):

```yaml
mock_app:
  name: "workday-demo"
  docker_remote_image: "ghcr.io/trajectory/workday-mock:latest"
  port: 8003

datasets:
  - dataset_id: "ef3d385a-5293-457a-af7c-06cb55d256f5"
    dataset_name: "Workday Demo Dataset"
    env_variable_to_override: "WORKDAY_API_BASE"
    task_ids: []  # leave empty or omit to evaluate every example
```

Required fields:

- `mock_app.docker_remote_image` – image pulled/run by the CLI.
- `mock_app.port` – container port exposed on the host (and used for health checks).
- `datasets[].dataset_id` – dataset UUID pulled from the API.
- `datasets[].dataset_name` – label used for logging/metrics.
- `datasets[].env_variable_to_override` – agent env var that will be set to the mock app base URL.
- `datasets[].task_ids` – optional list of example IDs to evaluate; omit/empty = all examples.

- `traj up` mounts the same config inside the container at `/app/runtime/eval_config.yaml` so the mock app can prepare its own databases.
- The CLI now focuses solely on running the mock app in the foreground:

```bash
traj up --config-file /abs/path/to/datasets.yaml --env EXTRA_VAR
```

- Reads `mock_app` from the config.
- Automatically forwards `TRAJECTORY_API_KEY` and `TRAJECTORY_ORG_ID`, plus any `--env` flags you add.
- Executes `docker run --rm -p <port>:<port> <docker_remote_image>` with the forwarded env vars and a bind-mount of the config file.
- Runs in the foreground; press `Ctrl+C` to stop the container and exit.

## BaseEvaluation Changes

- Loads the same config via `EvaluationConfig.from_file`.
- Ensures the mock app is healthy at `http://localhost:<port>/health`.
- Filters dataset examples according to `task_ids`.
- Sets only the env var specified in each dataset entry (no more Workday-specific defaults).
- Raises immediately if required environment variables (`TRAJECTORY_API_URL`, `TRAJECTORY_API_KEY`) are missing or API calls fail.

## Running an Evaluation

1. Start the mock app:

   ```bash
   traj up --config-file /abs/path/to/datasets.yaml --env EXTRA_VAR
   ```

2. In a separate terminal, run your evaluator (example):

   ```bash
   python examples/run_workday_eval.py /abs/path/to/datasets.yaml
   ```

3. Stop the mock app with `Ctrl+C` once the evaluation finishes.

Environment variables to export before step 2:

- `TRAJECTORY_API_URL` (or `BACKEND_BASE`)
- `TRAJECTORY_API_KEY`

If the mock backend or API credentials are misconfigured, `BaseEvaluation` logs the error and raises so the calling script can fail fast.

