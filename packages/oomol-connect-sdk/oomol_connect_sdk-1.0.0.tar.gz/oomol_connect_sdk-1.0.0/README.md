# Oomol Connect SDK for Python

[中文文档](README_zh.md)

Official Python SDK for Oomol Connect API. This SDK provides a complete, type-safe interface for interacting with Oomol Connect services.

## Features

- ✨ **Complete API Coverage** - Full support for all Oomol Connect API endpoints
- 🔄 **Smart Polling** - Intelligent polling with exponential backoff strategy
- 📊 **Progress Monitoring** - Real-time callbacks for task progress and logs
- 📁 **File Upload** - Support for single and multiple file uploads
- 🎯 **Type Safe** - Full type annotations with TypedDict support
- ⚡ **Async First** - Modern async design based on asyncio and httpx
- 🛡️ **Error Handling** - Comprehensive error classification and handling

## Installation

```bash
pip install oomol-connect-sdk
```

## Quick Start

```python
import asyncio
from oomol_connect_sdk import OomolConnectClient

async def main():
    async with OomolConnectClient(
        base_url="http://localhost:3000/api",
        api_token="your-api-token"
    ) as client:
        # Run a task and get results
        result = await client.tasks.run({
            "manifest": "audio-lab::text-to-audio",
            "inputValues": {"text": "Hello, World"}
        })

        print(f"Task ID: {result['task_id']}")
        print(f"Result: {result['result']}")

asyncio.run(main())
```

## Core Concepts

### Client Initialization

```python
from oomol_connect_sdk import OomolConnectClient

client = OomolConnectClient(
    base_url="/api",              # API base URL
    api_token="your-token",       # API token (auto-added as Bearer token)
    default_headers={},           # Custom headers (optional)
    timeout=30.0                  # Request timeout in seconds
)
```

### Task Management

```python
# Simple task execution (recommended)
result = await client.tasks.run({
    "manifest": "flow-name",
    "inputValues": {"input1": "value1"}
})

# With progress monitoring
result = await client.tasks.run(
    {
        "manifest": "flow-name",
        "inputValues": {"input": "value"}
    },
    {
        "interval_ms": 1000,
        "timeout_ms": 60000,
        "on_progress": lambda task: print(f"Status: {task['status']}"),
        "on_log": lambda log: print(f"Log: {log['type']}")
    }
)
```

### Input Value Formats

The SDK automatically normalizes three input formats:

```python
# Format 1: Simple object (most common)
{"input1": "value1", "input2": 123}

# Format 2: Array format
[
    {"handle": "input1", "value": "value1"},
    {"handle": "input2", "value": 123}
]

# Format 3: Node format (for multi-node scenarios)
[
    {
        "nodeId": "node1",
        "inputs": [{"handle": "input1", "value": "value1"}]
    }
]
```

### File Upload

```python
# Single file upload
with open("test.txt", "rb") as f:
    result = await client.tasks.run_with_files(
        "pkg::file-processor",
        {"input1": "value"},
        f
    )

# Multiple files upload
with open("file1.txt", "rb") as f1, open("file2.txt", "rb") as f2:
    result = await client.tasks.run_with_files(
        "pkg::multi-file-processor",
        {"input1": "value"},
        [f1, f2]
    )
```

## API Reference

### Tasks Client

Core API for task management:

- `list()` - List all tasks
- `create(request)` - Create a task (JSON format)
- `create_with_files(manifest, input_values, files)` - Create task with file upload
- `get(task_id)` - Get task details
- `stop(task_id)` - Stop a task
- `get_logs(task_id)` - Get task logs
- `wait_for_completion(task_id, options)` - Poll until task completes
- `create_and_wait(request, polling_options)` - Create and wait for completion
- `run(request, polling_options)` - **Recommended** - One-step run and get results
- `run_with_files(manifest, input_values, files, polling_options)` - One-step run with files

### Flows Client

```python
# List all flows
flows_response = await client.flows.list()
for flow in flows_response["flows"]:
    print(flow["name"], flow["path"])
```

### Blocks Client

```python
# List all blocks
blocks_response = await client.blocks.list()
for block in blocks_response["blocks"]:
    print(block["package"], block["name"])
```

### Packages Client

```python
# List installed packages
packages = await client.packages.list()

# Install a package
install_task = await client.packages.install("package-name", "1.0.0")

# Install and wait for completion
install_task = await client.packages.install_and_wait("package-name", "1.0.0")
```

## Polling Options

```python
from oomol_connect_sdk import BackoffStrategy

polling_options = {
    "interval_ms": 2000,                    # Polling interval (milliseconds)
    "timeout_ms": 300000,                   # Timeout (milliseconds)
    "max_interval_ms": 10000,               # Maximum interval (milliseconds)
    "backoff_strategy": BackoffStrategy.EXPONENTIAL,  # Backoff strategy
    "backoff_factor": 1.5,                  # Backoff factor
    "on_progress": lambda task: ...,        # Progress callback
    "on_log": lambda log: ...               # Log callback
}
```

## Error Handling

```python
from oomol_connect_sdk import (
    OomolConnectError,      # Base class
    ApiError,               # HTTP errors
    TaskFailedError,        # Task execution failed
    TaskStoppedError,       # Task was stopped
    TimeoutError,           # Polling timeout
    InstallFailedError      # Package installation failed
)

try:
    result = await client.tasks.run({
        "manifest": "flow-1",
        "inputValues": {"input": "test"}
    })
except TaskFailedError as e:
    print(f"Task failed: {e.task_id}")
except ApiError as e:
    print(f"HTTP {e.status}: {e.message}")
```

## Advanced Usage

### Concurrent Tasks

```python
import asyncio

tasks = [
    client.tasks.run({
        "manifest": "flow-1",
        "inputValues": {"input": f"test-{i}"}
    })
    for i in range(5)
]

results = await asyncio.gather(*tasks)
```

### Custom Backoff Strategy

```python
from oomol_connect_sdk import BackoffStrategy

result = await client.tasks.run(
    {"manifest": "long-running-flow", "inputValues": {}},
    {
        "interval_ms": 1000,
        "max_interval_ms": 5000,
        "backoff_strategy": BackoffStrategy.EXPONENTIAL,
        "backoff_factor": 2.0
    }
)
```

## Examples

See `examples/` directory for more examples:

- `basic_usage.py` - Basic usage examples
- `advanced_usage.py` - Advanced features and patterns

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy oomol_connect_sdk
```

## Requirements

- Python >= 3.8
- httpx >= 0.27.0

## License

MIT License - see [LICENSE](LICENSE) file for details

## Links

- **PyPI**: https://pypi.org/project/oomol-connect-sdk/
- **Source Code**: https://github.com/oomol/oomol-connect-sdk-py
- **Issue Tracker**: https://github.com/oomol/oomol-connect-sdk-py/issues
- **TypeScript Version**: https://github.com/oomol/oomol-connect-sdk-ts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
