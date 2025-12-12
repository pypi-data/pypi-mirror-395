# Only Local Tracing Feature

## Overview

The `TRAJECTORY_ONLY_LOCAL_TRACING` feature allows you to completely bypass remote server calls and save all traces locally. This is useful for:

- **Offline development**: Work without internet connectivity
- **Privacy-sensitive environments**: Keep all trace data local
- **Testing and debugging**: Avoid network calls during development
- **Performance**: Eliminate network latency for trace operations

## Environment Variables

### `TRAJECTORY_ONLY_LOCAL_TRACING`

Set to `"true"` to enable only local tracing mode.

```bash
export TRAJECTORY_ONLY_LOCAL_TRACING="true"
```

When enabled:
- ✅ All traces are saved locally (no remote server calls)
- ✅ Monitoring is automatically disabled
- ✅ Evaluations are automatically disabled
- ✅ No API keys required for basic tracing

## Programmatic Usage

### Basic Setup

```python
from trajectory.common.tracer.core import Tracer

# Enable only local tracing
tracer = Tracer(
    project_name="my_project",
    enable_local_tracing=True,
    only_local_tracing=True,
    # API keys not required in only local mode
    api_key="dummy_key",
    organization_id="dummy_org"
)
```

### Using Environment Variables

```python
import os
from trajectory.common.tracer.core import Tracer

# Set environment variable
os.environ["TRAJECTORY_ONLY_LOCAL_TRACING"] = "true"

# Tracer will automatically detect and use only local tracing
tracer = Tracer(
    project_name="my_project",
    enable_local_tracing=True,
    api_key="dummy_key",
    organization_id="dummy_org"
)
```

## Behavior Differences

### Only Local Tracing Mode

| Feature | Only Local Mode | Regular Local Mode | Remote Mode |
|---------|----------------|-------------------|-------------|
| Local trace storage | ✅ Enabled | ✅ Enabled | ❌ Disabled |
| Remote server calls | ❌ Disabled | ✅ Enabled (fallback) | ✅ Enabled |
| Monitoring | ❌ Disabled | ✅ Enabled | ✅ Enabled |
| Evaluations | ❌ Disabled | ✅ Enabled | ✅ Enabled |
| API key required | ❌ No | ✅ Yes | ✅ Yes |

### Trace Storage

Traces are saved to the local directory specified by `TRAJECTORY_TRACING_LOCAL_DIR` (default: `./trajectory_traces`).

```python
# Check local trace files
import os
trace_dir = "./trajectory_traces"
trace_files = [f for f in os.listdir(trace_dir) if f.startswith("trace_") and f.endswith(".json")]
print(f"Found {len(trace_files)} local trace files")
```

## Example Usage

### Simple Trace

```python
from trajectory.common.tracer.core import Tracer

# Create tracer with only local tracing
tracer = Tracer(
    project_name="offline_analysis",
    enable_local_tracing=True,
    only_local_tracing=True,
    api_key="dummy_key",
    organization_id="dummy_org"
)

# Create a simple trace
with tracer.trace("data_processing") as trace:
    trace.update_metadata({"dataset": "customer_data"})
    trace.record_input({"query": "Process customer records"})
    
    # Your processing logic here
    result = process_data()
    
    trace.record_output({"processed_count": len(result)})
```

### LangGraph Integration

```python
from trajectory.integrations.langgraph import TrajectoryCallbackHandler

# Create tracer with only local tracing
tracer = Tracer(
    project_name="langgraph_offline",
    enable_local_tracing=True,
    only_local_tracing=True,
    api_key="dummy_key",
    organization_id="dummy_org"
)

# Use with LangGraph
callback_handler = TrajectoryCallbackHandler(tracer)

# Your LangGraph workflow will save traces locally
```

## Configuration

### Environment Variables

```bash
# Enable only local tracing
export TRAJECTORY_ONLY_LOCAL_TRACING="true"

# Optional: Custom local storage directory
export TRAJECTORY_TRACING_LOCAL_DIR="/path/to/my/traces"

# Optional: Logging level for debugging
export TRAJECTORY_LOGGING_LEVEL="DEBUG"
```

### Programmatic Configuration

```python
# Method 1: Constructor parameters
tracer = Tracer(
    project_name="my_project",
    enable_local_tracing=True,
    only_local_tracing=True,
    local_tracing_dir="/custom/path"
)

# Method 2: Environment variables
import os
os.environ["TRAJECTORY_ONLY_LOCAL_TRACING"] = "true"
os.environ["TRAJECTORY_TRACING_LOCAL_DIR"] = "/custom/path"

tracer = Tracer(
    project_name="my_project",
    enable_local_tracing=True
)
```

## Error Handling

### Graceful Degradation

If local trace storage fails, the behavior depends on the mode:

- **Only Local Mode**: Creates a mock response (no fallback to remote)
- **Regular Local Mode**: Falls back to remote tracing
- **Remote Mode**: Raises an error

### Common Issues

1. **Permission Denied**: Ensure write access to the trace directory
2. **Disk Space**: Monitor local storage usage
3. **File Conflicts**: Each trace gets a unique filename with timestamp

## Best Practices

1. **Use for Development**: Perfect for offline development and testing
2. **Monitor Storage**: Regularly clean up old trace files
3. **Backup Important Traces**: Copy important traces to version control
4. **Test Both Modes**: Verify your code works in both local and remote modes

## Migration from Remote to Only Local

```python
# Before: Remote tracing
tracer = Tracer(
    project_name="my_project",
    api_key="your_api_key",
    organization_id="your_org_id"
)

# After: Only local tracing
tracer = Tracer(
    project_name="my_project",
    enable_local_tracing=True,
    only_local_tracing=True,
    api_key="dummy_key",  # Not used
    organization_id="dummy_org"  # Not used
)
```

## Troubleshooting

### Check Trace Files

```python
import os
import json
from pathlib import Path

trace_dir = Path("./trajectory_traces")
if trace_dir.exists():
    trace_files = list(trace_dir.glob("trace_*.json"))
    print(f"Found {len(trace_files)} trace files")
    
    # Read the latest trace
    if trace_files:
        latest_trace = max(trace_files, key=os.path.getctime)
        with open(latest_trace, 'r') as f:
            trace_data = json.load(f)
            print(f"Latest trace ID: {trace_data.get('trace_id')}")
            print(f"Status: {trace_data.get('status')}")
```

### Debug Logging

```bash
export TRAJECTORY_LOGGING_LEVEL="DEBUG"
# Run your application to see detailed trace information
```

This feature provides a complete offline tracing solution while maintaining compatibility with the existing Trajectory SDK API.
