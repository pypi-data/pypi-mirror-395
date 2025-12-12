# Trajectory SDK Logging System

## Overview

The Trajectory SDK now includes a comprehensive logging system that provides detailed logging for all important steps in tracing. The logging system is configurable and supports different logging levels and formats.

## Features

### 1. Configurable Logging Levels

The logging system supports the following levels:
- `DEBUG`: Detailed information for debugging
- `INFO`: General information about program execution
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for serious problems
- `CRITICAL`: Critical error messages

### 2. Environment Variable Configuration

The logging level can be configured using the `TRAJECTORY_LOGGING_LEVEL` environment variable:

```bash
export TRAJECTORY_LOGGING_LEVEL=DEBUG
```

### 3. Programmatic Configuration

The logging system can also be configured programmatically after import:

```python
from trajectory.common.logger import configure_trajectory_logger

# Configure logging level
configure_trajectory_logger(level="DEBUG")

# Configure custom format
configure_trajectory_logger(
    level="INFO",
    format_string="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    date_format="%Y-%m-%d %H:%M:%S"
)

# Disable colored output
configure_trajectory_logger(use_color=False)
```

### 4. Default Configuration

- **Default Logging Level**: `INFO`
- **Default Format**: `%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s`
- **Default Date Format**: `%Y-%m-%d %H:%M:%S`
- **Colored Output**: Enabled by default (when terminal supports it)

The default format includes the filename and line number where the log was generated, making it easier to debug issues.

## Usage Examples

### Basic Usage

```python
from trajectory.common.logger import trajectory_logger

# Log messages at different levels
trajectory_logger.debug("Debug message")
trajectory_logger.info("Info message")
trajectory_logger.warning("Warning message")
trajectory_logger.error("Error message")
trajectory_logger.critical("Critical message")
```

### Advanced Configuration

```python
from trajectory.common.logger import TrajectoryLogger

# Create a custom logger instance
custom_logger = TrajectoryLogger(
    level="DEBUG",
    format_string="[%(levelname)s] %(name)s: %(message)s",
    use_color=False
)

# Use the custom logger
custom_logger.info("Custom logger message")
```

## Implementation Details

### Constants

All environment variable names are defined in `trajectory.common.constants` to avoid hardcoding:

- `TRAJECTORY_LOGGING_LEVEL_ENV`: Environment variable name for logging level
- `DEFAULT_LOGGING_LEVEL`: Default logging level
- `DEFAULT_LOG_FORMAT`: Default log format string
- `DEFAULT_LOG_DATE_FORMAT`: Default date format string
- `SUPPORTED_LOGGING_LEVELS`: List of supported logging levels

### Backward Compatibility

The logging system maintains backward compatibility with existing code. The global `trajectory_logger` instance continues to work as before, while new configuration options are available through the `TrajectoryLogger` class and `configure_trajectory_logger` function.

## Error Handling

- Invalid logging levels are handled gracefully with warnings
- The system falls back to default values when configuration fails
- Color output is automatically disabled when not supported by the terminal

## Integration with Tracing

The logging system is integrated throughout the Trajectory SDK:

- Trace initialization and configuration
- Local trace storage operations
- Remote trace operations
- Error handling and debugging
- Performance monitoring

This provides comprehensive visibility into the tracing process and helps with debugging and monitoring.
