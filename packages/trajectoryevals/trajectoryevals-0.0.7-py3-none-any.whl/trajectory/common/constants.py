"""
Constants for Trajectory SDK configuration
"""

# Environment variable names
TRAJECTORY_LOGGING_LEVEL_ENV = "TRAJECTORY_LOGGING_LEVEL"
TRAJECTORY_TRACING_LOCAL_ENV = "TRAJECTORY_TRACING_LOCAL"
TRAJECTORY_TRACING_LOCAL_DIR_ENV = "TRAJECTORY_TRACING_LOCAL_DIR"
TRAJECTORY_ONLY_LOCAL_TRACING_ENV = "TRAJECTORY_ONLY_LOCAL_TRACING"

# Default values
DEFAULT_LOGGING_LEVEL = "INFO"
DEFAULT_LOCAL_TRACING_DIR = "./trajectory_traces"

# Logging configuration
DEFAULT_LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)
DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Supported logging levels
SUPPORTED_LOGGING_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
