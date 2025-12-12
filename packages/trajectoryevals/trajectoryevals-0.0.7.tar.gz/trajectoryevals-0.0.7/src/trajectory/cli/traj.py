from __future__ import annotations

import argparse
import atexit
import base64
import os
import signal
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from trajectory.common.logger import trajectory_logger
from trajectory.evaluations.config_loader import EvaluationConfig

CONFIG_MOUNT_PATH = "/app/runtime/eval_config.yaml"


logger = trajectory_logger

# Load .env from current directory
load_dotenv()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="traj",
        description="Trajectory mock application runner.",
    )
    sub_parsers = parser.add_subparsers(dest="command", required=True)

    up_parser = sub_parsers.add_parser(
        "up",
        help="Start the mock application defined in the evaluation config.",
    )
    up_parser.add_argument(
        "--config-file",
        required=True,
        help="Path to the structured evaluation config file.",
    )

    args = parser.parse_args(argv)

    try:
        if args.command == "up":
            _handle_up(args)
        else:  # pragma: no cover
            raise ValueError(f"Unsupported command {args.command}")
    except KeyboardInterrupt:
        logger.info("Interrupted. Shutting down...")
        sys.exit(130)
    except Exception as exc:  # pragma: no cover - CLI level
        logger.error("%s", exc)
        sys.exit(1)


def _handle_up(args: argparse.Namespace) -> None:
    # Ensure TRAJECTORY_API_KEY is set
    api_key = os.environ.get("TRAJECTORY_API_KEY")
    if not api_key:
        raise ValueError(
            "TRAJECTORY_API_KEY not found in environment. "
            "Please set it in your .env file or environment variables."
        )

    config_path = Path(args.config_file).expanduser().resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = EvaluationConfig.from_file(config_path)
    mock_app = config.mock_app

    # Pull remote image
    logger.info("Pulling remote image %s...", mock_app.docker_remote_image)
    pull_result = subprocess.run(
        ["docker", "pull", mock_app.docker_remote_image],
        capture_output=True,
        text=True,
    )
    if pull_result.returncode != 0:
        raise RuntimeError(
            f"Failed to pull image {mock_app.docker_remote_image}: {pull_result.stderr}"
        )

    # Generate unique container name
    container_name = f"traj-{mock_app.name or 'app'}-{uuid.uuid4().hex[:8]}"

    # Read config file content and base64 encode it to pass as env var
    # This avoids Docker mount permission issues
    with open(config_path, "rb") as f:
        config_content = base64.b64encode(f.read()).decode("utf-8")

    cmd = [
        "docker",
        "run",
        "--name",
        container_name,
        "--rm",
        "-p",
        f"{mock_app.port}:{mock_app.port}",
        "-e",
        f"TRAJECTORY_API_KEY={api_key}",
        "-e",
        f"EVALUATION_CONFIG_PATH={CONFIG_MOUNT_PATH}",
        "-e",
        f"EVALUATION_CONFIG_CONTENT={config_content}",
        mock_app.docker_remote_image,
    ]

    logger.info(
        "Starting %s (%s) on port %s. Press Ctrl+C to stop.",
        mock_app.name or "application",
        mock_app.docker_remote_image,
        mock_app.port,
    )
    _run_foreground(cmd, container_name)


def _run_foreground(cmd: list[str], container_name: str) -> None:
    # Store process reference for signal handler
    process: Optional[subprocess.Popen[str]] = None

    # Function to stop the container
    def stop_container() -> None:
        try:
            subprocess.run(
                ["docker", "stop", container_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
        except Exception:
            pass  # Ignore errors when stopping

    # Register cleanup function
    atexit.register(stop_container)

    # Set up signal handlers for graceful shutdown
    def signal_handler(signum: int, frame) -> None:
        logger.info(
            "Received signal %s, stopping container %s...", signum, container_name
        )
        stop_container()
        # Terminate the subprocess if it's still running
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run the container and wait for it
    try:
        process = subprocess.Popen(cmd, text=True)
        process.wait()
        if process.returncode != 0:
            raise RuntimeError(f"Container exited with code {process.returncode}")
    except KeyboardInterrupt:
        # This should be caught by signal handler, but just in case
        signal_handler(signal.SIGINT, None)


if __name__ == "__main__":  # pragma: no cover
    main()
