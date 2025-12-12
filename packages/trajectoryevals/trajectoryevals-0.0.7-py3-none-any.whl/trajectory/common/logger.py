# logger.py

import logging
import os
import sys

from .constants import (
    DEFAULT_LOG_DATE_FORMAT,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOGGING_LEVEL,
    SUPPORTED_LOGGING_LEVELS,
    TRAJECTORY_LOGGING_LEVEL_ENV,
)

# ANSI escape sequences
RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
GRAY = "\033[90m"


class ColorFormatter(logging.Formatter):
    """
    Wrap the final formatted log record in ANSI color codes based on level.
    """

    COLORS = {
        logging.DEBUG: GRAY,
        logging.INFO: GRAY,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED,
    }

    def __init__(self, fmt=None, datefmt=None, use_color=True):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.use_color = use_color and sys.stdout.isatty()

    def format(self, record):
        message = super().format(record)
        if self.use_color:
            color = self.COLORS.get(record.levelno, "")
            if color:
                message = f"{color}{message}{RESET}"
        return message


class TrajectoryLogger:
    """
    Configurable logger for Trajectory SDK with support for environment-based configuration
    """

    def __init__(
        self,
        level: str | None = None,
        format_string: str | None = None,
        date_format: str | None = None,
        use_color: bool | None = None,
    ):
        """
        Initialize TrajectoryLogger with optional configuration

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format_string: Log message format string
            date_format: Date format string
            use_color: Whether to use colored output
        """
        self.level = level or self._get_logging_level_from_env()
        self.format_string = format_string or DEFAULT_LOG_FORMAT
        self.date_format = date_format or DEFAULT_LOG_DATE_FORMAT
        self.use_color = (
            use_color
            if use_color is not None
            else (sys.stdout.isatty() and os.getenv("NO_COLOR") is None)
        )

        self._logger = None
        self._setup_logger()

    def _get_logging_level_from_env(self) -> str:
        """Get logging level from environment variable"""
        env_level = os.getenv(
            TRAJECTORY_LOGGING_LEVEL_ENV, DEFAULT_LOGGING_LEVEL
        ).upper()
        if env_level in SUPPORTED_LOGGING_LEVELS:
            return env_level
        else:
            print(
                f"Warning: Invalid logging level '{env_level}' from {TRAJECTORY_LOGGING_LEVEL_ENV}. Using default: {DEFAULT_LOGGING_LEVEL}"
            )
            return DEFAULT_LOGGING_LEVEL

    def _setup_logger(self):
        """Setup the logger with current configuration"""
        # Remove existing handlers to avoid duplicates
        logger = logging.getLogger("trajectory")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Create new handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, self.level))
        handler.setFormatter(
            ColorFormatter(
                fmt=self.format_string,
                datefmt=self.date_format,
                use_color=self.use_color,
            )
        )

        logger.setLevel(getattr(logging, self.level))
        logger.addHandler(handler)
        self._logger = logger
        try:
            # Emit a confirmation message to verify logging configuration is active
            self._logger.debug(
                f"Trajectory logger configured | level={self.level} color={self.use_color}"
            )
        except Exception:
            pass

    def configure(
        self,
        level: str | None = None,
        format_string: str | None = None,
        date_format: str | None = None,
        use_color: bool | None = None,
    ):
        """
        Reconfigure the logger with new settings

        Args:
            level: New logging level
            format_string: New log message format
            date_format: New date format
            use_color: Whether to use colored output
        """
        if level is not None:
            if level.upper() in SUPPORTED_LOGGING_LEVELS:
                self.level = level.upper()
            else:
                print(
                    f"Warning: Invalid logging level '{level}'. Keeping current level: {self.level}"
                )

        if format_string is not None:
            self.format_string = format_string

        if date_format is not None:
            self.date_format = date_format

        if use_color is not None:
            self.use_color = use_color

        self._setup_logger()

    def get_logger(self):
        """Get the underlying logger instance"""
        return self._logger

    def debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message"""
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message"""
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self._logger.critical(message, *args, **kwargs)


# Global logger instance
_trajectory_logger_instance = TrajectoryLogger()


# Convenience functions for backward compatibility
def _setup_trajectory_logger():
    """Legacy function for backward compatibility"""
    return _trajectory_logger_instance.get_logger()


def configure_trajectory_logger(
    level: str | None = None,
    format_string: str | None = None,
    date_format: str | None = None,
    use_color: bool | None = None,
):
    """
    Configure the global trajectory logger

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Log message format string
        date_format: Date format string
        use_color: Whether to use colored output
    """
    _trajectory_logger_instance.configure(level, format_string, date_format, use_color)
    # Update the global logger reference
    global trajectory_logger
    trajectory_logger = _trajectory_logger_instance.get_logger()


# Global logger you can import elsewhere (backward compatibility)
# Configure logger based on environment variable on import
env_level = os.getenv(TRAJECTORY_LOGGING_LEVEL_ENV)
if env_level:
    configure_trajectory_logger(level=env_level)

trajectory_logger = _trajectory_logger_instance.get_logger()


# Function to reconfigure logger when environment variables change
def reconfigure_logger():
    """Reconfigure the logger with current environment variables"""
    global trajectory_logger
    env_level = os.getenv(TRAJECTORY_LOGGING_LEVEL_ENV)
    if env_level:
        configure_trajectory_logger(level=env_level)
        trajectory_logger = _trajectory_logger_instance.get_logger()
