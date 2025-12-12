# TaskController

A Python library for pause/resume/kill control of functions across processes using file-based IPC.

## Features

- **Pause/Resume**: Pause function execution and resume later from saved state
- **Kill**: Terminate function execution gracefully
- **Cross-Process**: Control functions running in different terminals/processes
- **Per-Function Control**: Control multiple decorated functions independently
- **CLI Tool**: Control functions directly from terminal using `taskController` command
- **Simple API**: Easy-to-use decorator and control flags

## Installation

```bash
pip install taskController
```

This installs both the Python library and the `taskController` CLI command.

## Quick Start

### Basic Usage

```python
from taskcontroller import task_controller, controller
import time

@task_controller
def long_running_task():
    for i in range(100):
        print(f"Step {i}")
        time.sleep(1)

# Run the task
long_running_task()
```

### Controlling from CLI (New in v0.2.0!)

```bash
# List all running functions (like 'ps')
taskController ps

# Pause a specific function
taskController stop long_running_task

# Resume a specific function
taskController resume long_running_task

# Kill a specific function
taskController kill long_running_task

# See detailed status
taskController status
```

### Controlling from Another Terminal (Python API)

```python
from taskcontroller import controller

# NEW: Per-function control
controller.stop_function('long_running_task')    # Pause specific function
controller.resume_function('long_running_task')  # Resume specific function
controller.kill_function('long_running_task')    # Kill specific function

# Control all functions
controller.stop_all()     # Pause all
controller.resume_all()   # Resume all
controller.kill_all()     # Kill all

# Query functions
controller.list_functions()              # List all registered functions
controller.status('long_running_task')   # Check specific function status
controller.status()                      # Check all functions

# Legacy API (still supported - affects all functions)
controller.stop = True
controller.resume = True
controller.kill = True

# Check status
print(controller.status())

# Reset all flags
controller.reset()
```

## API Reference

### Decorator

#### `@task_controller`
Wraps a function to enable pause/resume/kill control.

```python
@task_controller
def my_function():
    # Your code here
    pass
```

### CLI Commands (New in v0.2.0!)

```bash
taskController ps                    # List all running functions with PID/status
taskController stop <func_name>      # Pause a specific function
taskController resume <func_name>    # Resume a specific function  
taskController kill <func_name>      # Kill a specific function
taskController stop-all              # Pause all functions
taskController resume-all            # Resume all functions
taskController kill-all              # Kill all functions
taskController status [func_name]    # Show detailed status
taskController reset                 # Reset all flags
```

See [CLI_USAGE.md](CLI_USAGE.md) for detailed CLI documentation.

### Controller Methods

#### Per-Function Control (New in v0.2.0!)

##### `controller.stop_function(func_name)`
Pause a specific function by name.

```python
controller.stop_function('my_function')
```

##### `controller.resume_function(func_name)`
Resume a specific function by name.

```python
controller.resume_function('my_function')
```

##### `controller.kill_function(func_name)`
Kill a specific function by name.

```python
controller.kill_function('my_function')
```

##### `controller.stop_all()`
Pause all registered decorated functions.

```python
controller.stop_all()
```

##### `controller.resume_all()`
Resume all registered decorated functions.

```python
controller.resume_all()
```

##### `controller.kill_all()`
Kill all registered decorated functions.

```python
controller.kill_all()
```

##### `controller.list_functions()`
List all registered decorated functions with their PIDs.

```python
functions = controller.list_functions()
# Returns: {'func_name': {'pid': 12345, 'registered_at': 1234567890.123}}
```

##### `controller.status(func_name=None)`
Get status of specific function or all functions.

```python
# Specific function
status = controller.status('my_function')

# All functions
status = controller.status()
```

#### Legacy Global Control (Deprecated)

##### `controller.stop`
Set to `True` to pause all functions (deprecated - use `stop_all()` or `stop_function()`).

```python
controller.stop = True
```

##### `controller.resume`
Set to `True` to resume all functions (deprecated - use `resume_all()` or `resume_function()`).

```python
controller.resume = True
```

##### `controller.kill`
Set to `True` to terminate all functions (deprecated - use `kill_all()` or `kill_function()`).

```python
controller.kill = True
```

#### `controller.reset()`
Reset all flags to default state.

```python
controller.reset()
```

## How It Works

- **File-based IPC**: Control flags are stored in `/tmp/flow_control_flags/control_flags.json`
- **Function Registry**: Active functions are tracked in `/tmp/flow_control_flags/function_registry.json`
- **Per-Function Flags**: Each function has its own control flags stored as `{func_name: bool}`
- **State Persistence**: Function state is saved to `/tmp/task_controller_states/` using dill serialization
- **Line-level Monitoring**: Uses Python's `sys.settrace()` to check flags at every line of execution
- **Timeout**: Paused execution times out after 15 minutes

## Examples

See the examples directory for complete usage examples:

- `example_usage.py` - Basic single function example
- `example_multi_function.py` - Multiple functions running concurrently
- `control.py` - Python-based control script
- `test_per_function_control.py` - Automated tests

## Documentation

- [CLI_USAGE.md](CLI_USAGE.md) - Detailed CLI command documentation
- [PER_FUNCTION_CONTROL.md](PER_FUNCTION_CONTROL.md) - Per-function control implementation details

## Advanced Features

### Multiple Functions Independent Control
Control multiple decorated functions independently - pause one while others continue running.

### CLI Integration
Use the `taskController` command from your terminal for easy process management.

### Pause with 15-Minute Timeout
When paused, execution automatically terminates if not resumed within 15 minutes.

### State Preservation
Function state (local variables, execution line) is saved when paused and can be restored on resume.

## Requirements

- Python >= 3.7
- dill >= 0.3.0

## Version History

### v0.2.0
- Added per-function control (stop/resume/kill specific functions)
- Added CLI tool (`pycontroller` command)
- Added function registry tracking
- Added `list_functions()` and enhanced `status()` methods
- Backward compatible with v0.1.0 API

### v0.1.0
- Initial release with global stop/resume/kill control

## License

MIT License

## Contributing

Contributions are welcome! Please submit issues and pull requests on GitHub.
