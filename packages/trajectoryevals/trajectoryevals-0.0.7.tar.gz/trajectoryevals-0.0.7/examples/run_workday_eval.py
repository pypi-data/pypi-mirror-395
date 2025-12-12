from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

from trajectory.common.logger import trajectory_logger
from trajectory.evaluations import BaseEvaluation

logger = trajectory_logger

_THIS_DIR = Path(__file__).resolve().parent
_AGENT_FILE = _THIS_DIR / "simple_workday_agent.py"
spec = importlib.util.spec_from_file_location("simple_workday_agent", str(_AGENT_FILE))
if spec is None or spec.loader is None:
    raise ImportError("Unable to load simple_workday_agent.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
run_agent = module.run_agent


class WorkdayEval(BaseEvaluation):
    def run_agent(self, task: str, **_: Any) -> dict[str, Any]:
        output = run_agent(task)
        return {"task": task, "output": output, "trace_id": None}


def main() -> None:
    if len(sys.argv) < 2:
        logger.error("Usage: python run_workday_eval.py <config.yaml>")
        sys.exit(1)
    config_path = Path(sys.argv[1]).expanduser().resolve()
    if not config_path.exists():
        logger.error("Config file not found: %s", config_path)
        sys.exit(1)

    logger.info("Starting workday evaluation using %s", config_path)
    WorkdayEval().run(
        str(config_path),
        use_concurrency=True,
        max_workers=4,
        num_runs=1,
    )


if __name__ == "__main__":
    main()
