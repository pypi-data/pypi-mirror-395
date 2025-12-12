# Import key components that should be publicly accessible
from trajectory.clients import client, together_client
from trajectory.common.tracer import Tracer, wrap
from trajectory.trajectory_client import TrajectoryClient
from trajectory.version_check import check_latest_version

# Preferred public alias
TrajectoryClient = TrajectoryClient

check_latest_version()

__all__ = [
    # Clients
    "client",
    "together_client",
    # Tracing
    "Tracer",
    "wrap",
    # Preferred public name
    "TrajectoryClient",
    # Backward-compat
    "TrajectoryClient",
]
