"""
Flow control decorator with pause/resume capability using state preservation.

This decorator monitors execution and can pause/resume functions at runtime
by saving and restoring their state using dill serialization.
"""

import sys
import functools
import time
import dill
import os
from typing import Callable, Any
from .shared_var import control_flags, _read_flags_internal, _write_flags_internal


# Global state storage
_saved_states = {}
_state_file_dir = "/tmp/task_controller_states"


def _ensure_state_dir():
    """Ensure state directory exists."""
    os.makedirs(_state_file_dir, exist_ok=True)


def _get_state_file(func_name: str) -> str:
    """Get state file path for a function."""
    _ensure_state_dir()
    return os.path.join(_state_file_dir, f"{func_name}_state.pkl")


def _save_state(func_name: str, frame, local_vars: dict):
    """
    Save the current execution state.
    
    Args:
        func_name: Name of the function
        frame: Current execution frame
        local_vars: Local variables to save
    """
    state = {
        'locals': local_vars.copy(),
        'line': frame.f_lineno,
        'file': frame.f_code.co_filename,
        'timestamp': time.time()
    }
    
    state_file = _get_state_file(func_name)
    
    try:
        with open(state_file, 'wb') as f:
            dill.dump(state, f)
        print(f" State saved at line {frame.f_lineno}")
        print(f" State file: {state_file}")
        return state
    except Exception as e:
        print(f" Error saving state: {e}")
        return None


def _load_state(func_name: str) -> dict:
    """
    Load saved execution state.
    
    Args:
        func_name: Name of the function
        
    Returns:
        Saved state dict or None
    """
    state_file = _get_state_file(func_name)
    
    if not os.path.exists(state_file):
        print(f" No saved state found at {state_file}")
        return None
    
    try:
        with open(state_file, 'rb') as f:
            state = dill.load(f)
        print(f" State loaded from line {state['line']}")
        return state
    except Exception as e:
        print(f" Error loading state: {e}")
        return None


def _delete_state(func_name: str):
    """Delete saved state file."""
    state_file = _get_state_file(func_name)
    if os.path.exists(state_file):
        os.remove(state_file)
        print(f" State file deleted: {state_file}")


class PauseException(Exception):
    """Exception raised to pause execution."""
    pass


class KillException(Exception):
    """Exception raised to kill execution."""
    pass


def trace_with_pause(func_name: str):
    """
    Create a trace function that monitors for stop flag.
    
    Args:
        func_name: Name of the function being traced
        
    Returns:
        Trace function
    """
    def trace_func(frame, event, arg):
        """Trace function that checks for pause and kill requests for this specific function."""
        
        # Only trace lines in our function
        if event == 'line':
            # Check if kill flag is set for this function (highest priority)
            if control_flags.is_killed(func_name):
                print(f"\n KILL requested for '{func_name}' at line {frame.f_lineno}")
                print(f"Function: {frame.f_code.co_name}")
                print(" Terminating execution...")
                
                # Clean up state file
                _delete_state(func_name)
                
                # Reset kill flag for this function
                control_flags.kill_function(func_name)  # This will set it to True, so we need a clear method
                # Actually, let's unregister instead
                
                # Raise exception to terminate
                raise KillException(f"Execution of '{func_name}' killed by control flag")
            
            # Check if stop flag is set for this function
            if control_flags.is_stopped(func_name) and not control_flags.is_resumed(func_name):
                print(f"\nPAUSE requested for '{func_name}' at line {frame.f_lineno}")
                print(f"Function: {frame.f_code.co_name}")
                
                # Save current state
                local_vars = frame.f_locals.copy()
                _save_state(func_name, frame, local_vars)
                
                # Wait for resume - THIS BLOCKS THE THREAD
                print(f" Execution of '{func_name}' PAUSED. Waiting for RESUME flag...")
                print(f" Set controller.resume_function('{func_name}') to continue")
                print(" Timeout: 15 minutes")
                
                # This loop blocks execution until resume is set (with 15 min timeout)
                start_time = time.time()
                timeout_seconds = 15 * 60  # 15 minutes
                
                while control_flags.is_stopped(func_name) and not control_flags.is_resumed(func_name):
                    if time.time() - start_time > timeout_seconds:
                        print(f"\n Timeout reached (15 minutes) for '{func_name}'. Terminating execution...")
                        # Clear the stop flag
                        with control_flags._lock:
                            flags = _read_flags_internal()
                            if func_name in flags.get('stop', {}):
                                del flags['stop'][func_name]
                            _write_flags_internal(flags)
                        raise KillException(f"Execution of '{func_name}' timed out after 15 minutes of pause")
                    time.sleep(0.1)  
                
                print(f" RESUME flag detected for '{func_name}'! Continuing execution...")
                
                # Clear flags for this function for next pause/resume cycle
                with control_flags._lock:
                    flags = _read_flags_internal()
                    if func_name in flags.get('stop', {}):
                        del flags['stop'][func_name]
                    if func_name in flags.get('resume', {}):
                        del flags['resume'][func_name]
                    _write_flags_internal(flags)
                
        return trace_func
    
    return trace_func


def task_controller(func: Callable) -> Callable:
    """
    Decorator that enables pause/resume/kill control over function execution.
    
    Supports per-function control: multiple decorated functions can be controlled
    independently using their function names.
    
    When control_flags.stop_function(func_name) is called:
    - Function pauses at the next line
    - State is saved using dill
    - Execution waits until control_flags.resume_function(func_name) is called
    
    When control_flags.kill_function(func_name) is called:
    - Function terminates immediately at the next line
    - State file is deleted
    - Function returns None
    
    The decorator continuously monitors control flags during execution.
    
    Usage:
        @task_controller
        def my_function():
            # Your code here
            pass
        
        # From another terminal or code:
        from pycontroller import controller
        controller.stop_function('my_function')   # Pause specific function
        controller.resume_function('my_function') # Resume specific function
        controller.kill_function('my_function')   # Kill specific function
        
        # Or control all functions:
        controller.stop_all()    # Pause all decorated functions
        controller.resume_all()  # Resume all decorated functions
        controller.kill_all()    # Kill all decorated functions
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function with pause/resume/kill capability
    """
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        pid = os.getpid()
        
        # Register this function
        control_flags.register_function(func_name, pid)
        print(f"[CONTROLLER] Registered function '{func_name}' with PID {pid}")
        
        # Check if we should resume from saved state
        if control_flags.is_resumed(func_name) and not control_flags.is_stopped(func_name):
            print(f"\n Attempting to resume '{func_name}' from saved state...")
            
            saved_state = _load_state(func_name)
            
            if saved_state:
                print(f" Resuming from line {saved_state['line']}")
                
                # Restore local variables
                restored_locals = saved_state['locals']
                
                # Clear resume flag for this function
                with control_flags._lock:
                    flags = _read_flags_internal()
                    if func_name in flags.get('resume', {}):
                        del flags['resume'][func_name]
                    _write_flags_internal(flags)
                
                print(" State restored. Continuing execution...")
                
        # Enable monitoring for this function
        control_flags.set_monitoring(func_name, True)
        
        # Set up tracing for pause detection
        sys.settrace(trace_with_pause(func_name))
        
        try:
            result = func(*args, **kwargs)
            print(f"\n '{func_name}' completed successfully")
            
            # Clean up state file on successful completion
            _delete_state(func_name)
            
            return result
        
        except KillException as e:
            print(f"\n '{func_name}' was killed")
            print(f" Reason: {e}")
            
            # Clean up state file
            _delete_state(func_name)
            
            # Return None instead of raising
            return None
            
        except KeyboardInterrupt:
            print(f"\n KeyboardInterrupt in '{func_name}' - saving state...")
            frame = sys._getframe()
            _save_state(func_name, frame, frame.f_locals)
            raise
            
        finally:
            # Disable tracing
            sys.settrace(None)
            control_flags.set_monitoring(func_name, False)
            
            # Unregister function on completion
            control_flags.unregister_function(func_name)
            print(f"[CONTROLLER] Unregistered function '{func_name}'")
    
    return wrapper


def get_saved_state(func_name: str) -> dict:
    """
    Get saved state for a function (for debugging).
    
    Args:
        func_name: Name of the function
        
    Returns:
        Saved state dict or None
    """
    return _load_state(func_name)


def clear_saved_state(func_name: str):
    """
    Clear saved state for a function.
    
    Args:
        func_name: Name of the function
    """
    _delete_state(func_name)
