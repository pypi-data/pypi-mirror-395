# Trajectory SDK Local Tracing

## Overview

The Trajectory SDK now supports local tracing, allowing traces to be saved locally instead of being sent to the remote server. This feature is useful for development, testing, and scenarios where you want to keep traces local for privacy or offline work.

## Features

### 1. Environment Variable Configuration

Local tracing can be enabled using environment variables:

```bash
# Enable local tracing
export TRAJECTORY_TRACING_LOCAL=true

# Optional: Specify custom storage directory
export TRAJECTORY_TRACING_LOCAL_DIR=/path/to/your/traces
```

### 2. Programmatic Configuration

Local tracing can also be configured programmatically when creating a Tracer instance:

```python
from trajectory import Tracer

# Enable local tracing with default directory
tracer = Tracer(
    api_key="your-api-key",
    organization_id="your-org-id",
    enable_local_tracing=True
)

# Enable local tracing with custom directory
tracer = Tracer(
    api_key="your-api-key",
    organization_id="your-org-id",
    enable_local_tracing=True,
    local_tracing_dir="/custom/trace/directory"
)
```

### 3. Automatic Fallback

If local tracing is enabled but fails to initialize, the system automatically falls back to remote tracing to ensure your application continues to work.

## Storage Format

### Trace Files

Traces are saved as JSON files with the following naming convention:
- `trace_YYYYMMDD_HHMMSS_{trace_id_8_chars}.json`

Example: `trace_20241201_143022_a1b2c3d4.json`

### Trace File Structure

```json
{
  "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2024-12-01T14:30:22.123456",
  "storage_type": "local",
  "data": {
    "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "my_trace",
    "project_name": "my_project",
    "created_at": "2024-12-01T14:30:22.123456Z",
    "duration": 1.234,
    "trace_spans": [...],
    "evaluation_runs": [...],
    "offline_mode": true,
    "parent_trace_id": null,
    "parent_name": null,
    "customer_id": null,
    "tags": [],
    "metadata": {},
    "update_id": 1,
    "evaluation_id": null,
    "is_evaluation": false
  }
}
```

### Span Files

Individual spans are also saved as separate JSON files:
- `span_YYYYMMDD_HHMMSS_{span_id_8_chars}.json`

## Local Storage Management

### Listing Traces

```python
from trajectory.common.local_trace_storage import LocalTraceStorage

storage = LocalTraceStorage("/path/to/traces")
traces = storage.list_traces()

for trace in traces:
    print(f"Trace: {trace['trace_id']} - {trace['timestamp']} - {trace['size']} bytes")
```

### Retrieving Specific Traces

```python
# Get a specific trace by ID
trace_data = storage.get_trace("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
if trace_data:
    print(f"Found trace: {trace_data['data']['name']}")
```

### Cleanup Old Traces

```python
# Clean up traces older than 30 days
storage.cleanup_old_traces(days_to_keep=30)
```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TRAJECTORY_TRACING_LOCAL` | Enable local tracing (true/false) | `false` |
| `TRAJECTORY_TRACING_LOCAL_DIR` | Directory for local traces | `./trajectory_traces` |

### Tracer Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `enable_local_tracing` | bool | Enable local tracing | `None` (check env var) |
| `local_tracing_dir` | str | Directory for local traces | `None` (use env var or default) |

## Usage Examples

### Basic Local Tracing

```python
import os
from trajectory import Tracer

# Set environment variable
os.environ["TRAJECTORY_TRACING_LOCAL"] = "true"

# Create tracer (will use local tracing)
tracer = Tracer(
    api_key="your-api-key",
    organization_id="your-org-id"
)

# Use tracer as normal - traces will be saved locally
with tracer.trace("my_operation") as trace:
    # Your code here
    pass
```

### Custom Storage Directory

```python
from trajectory import Tracer

tracer = Tracer(
    api_key="your-api-key",
    organization_id="your-org-id",
    enable_local_tracing=True,
    local_tracing_dir="/my/custom/traces"
)
```

### Checking Local Tracing Status

```python
from trajectory.common.local_trace_storage import is_local_tracing_enabled

if is_local_tracing_enabled():
    print("Local tracing is enabled")
else:
    print("Remote tracing is enabled")
```

## Integration with Existing Code

Local tracing is designed to be a drop-in replacement for remote tracing. Existing code that uses the Trajectory SDK will work without modification when local tracing is enabled.

### TraceClient Response

When local tracing is enabled, the `save()` method returns a modified response:

```python
{
    "ui_results_url": "file:///path/to/traces/trace_*_a1b2c3d4.json",
    "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "saved_locally",
    "local_tracing": True
}
```

## Error Handling

- If local tracing fails to initialize, the system falls back to remote tracing
- File I/O errors are logged but don't crash the application
- Invalid directory paths are handled gracefully

## Performance Considerations

- Local tracing has minimal performance impact
- File I/O is asynchronous where possible
- Trace files are compressed JSON for efficient storage
- Old traces can be cleaned up to manage disk space

## Security and Privacy

- Traces are stored locally and never sent to remote servers
- File permissions follow system defaults
- Sensitive data in traces remains on your local system
- Useful for compliance with data residency requirements

## Development and Testing

Local tracing is particularly useful for:

- Development and debugging
- Testing without affecting production traces
- Offline development
- Compliance with data privacy requirements
- Performance analysis without network overhead
