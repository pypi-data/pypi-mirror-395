"""
Shared variables for controlling code execution flow.

This module provides flags to control pause/resume of decorated functions.
Uses file-based IPC to work across different terminal processes.
Supports per-function control to manage multiple decorated functions independently.
"""

import threading
import os
import json
import time


# File-based flag storage for inter-process communication
_FLAG_DIR = "/tmp/flow_control_flags"
_FLAG_FILE = os.path.join(_FLAG_DIR, "control_flags.json")
_REGISTRY_FILE = os.path.join(_FLAG_DIR, "function_registry.json")


def _ensure_flag_dir():
    """Ensure flag directory exists."""
    os.makedirs(_FLAG_DIR, exist_ok=True)


def _read_flags() -> dict:
    """Read flags from file."""
    _ensure_flag_dir()
    
    if not os.path.exists(_FLAG_FILE):
        return {
            'stop': {},      # {func_name: bool} - per-function stop flags
            'resume': {},    # {func_name: bool} - per-function resume flags
            'kill': {},      # {func_name: bool} - per-function kill flags
            'monitoring': {} # {func_name: bool} - per-function monitoring status
        }
    
    try:
        with open(_FLAG_FILE, 'r') as f:
            flags = json.load(f)
            # Ensure all flag types exist and are dicts
            for key in ['stop', 'resume', 'kill', 'monitoring']:
                if key not in flags or not isinstance(flags[key], dict):
                    flags[key] = {}
            return flags
    except (json.JSONDecodeError, IOError):
        return {
            'stop': {},
            'resume': {},
            'kill': {},
            'monitoring': {}
        }


def _write_flags(flags: dict):
    """Write flags to file."""
    _ensure_flag_dir()
    
    try:
        with open(_FLAG_FILE, 'w') as f:
            json.dump(flags, f)
    except IOError as e:
        print(f"[WARNING] Could not write flags: {e}")


def _read_registry() -> dict:
    """Read function registry from file."""
    _ensure_flag_dir()
    
    if not os.path.exists(_REGISTRY_FILE):
        return {}
    
    try:
        with open(_REGISTRY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _write_registry(registry: dict):
    """Write function registry to file."""
    _ensure_flag_dir()
    
    try:
        with open(_REGISTRY_FILE, 'w') as f:
            json.dump(registry, f, indent=2)
    except IOError as e:
        print(f"[WARNING] Could not write registry: {e}")


# Make internal functions accessible to decorator module
def _read_flags_internal():
    """Internal function for decorator to read flags."""
    return _read_flags()


def _write_flags_internal(flags):
    """Internal function for decorator to write flags."""
    _write_flags(flags)


class ControlFlags:
    """
    Class to manage execution control flags using file-based IPC.
    
    Flags are stored in /tmp/flow_control_flags/control_flags.json
    so they can be shared across different terminal processes.
    
    Supports per-function control: you can pause/resume/kill specific functions
    by name, or control all functions at once.
    
    Flags:
        stop: Per-function or global stop flag - pauses execution and saves state
        resume: Per-function or global resume flag - resumes from saved state
        kill: Per-function or global kill flag - terminates execution immediately
        
    Methods:
        stop_function(func_name): Pause a specific function
        resume_function(func_name): Resume a specific function
        kill_function(func_name): Kill a specific function
        stop_all(): Pause all decorated functions
        resume_all(): Resume all decorated functions
        kill_all(): Kill all decorated functions
        list_functions(): List all registered decorated functions
        is_stopped(func_name): Check if a specific function is stopped
        is_resumed(func_name): Check if a specific function should resume
        is_killed(func_name): Check if a specific function should be killed
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ControlFlags, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._current_pid = os.getpid()
        
        # Initialize file if it doesn't exist
        if not os.path.exists(_FLAG_FILE):
            _write_flags({
                'stop': {},
                'resume': {},
                'kill': {},
                'monitoring': {}
            })
        if not os.path.exists(_REGISTRY_FILE):
            _write_registry({})
    
    # ==================== FUNCTION REGISTRATION ====================
    
    def register_function(self, func_name: str, pid: int):
        """Register a decorated function with its PID."""
        with self._lock:
            registry = _read_registry()
            registry[func_name] = {
                'pid': pid,
                'registered_at': time.time()
            }
            _write_registry(registry)
    
    def unregister_function(self, func_name: str):
        """Unregister a decorated function."""
        with self._lock:
            registry = _read_registry()
            if func_name in registry:
                del registry[func_name]
                _write_registry(registry)
            
            # Clean up flags for this function
            flags = _read_flags()
            for flag_type in ['stop', 'resume', 'kill', 'monitoring']:
                if func_name in flags[flag_type]:
                    del flags[flag_type][func_name]
            _write_flags(flags)
    
    def list_functions(self) -> dict:
        """List all registered decorated functions with their metadata."""
        return _read_registry()
    
    # ==================== PER-FUNCTION CONTROL ====================
    
    def stop_function(self, func_name: str):
        """Pause a specific function by name."""
        with self._lock:
            flags = _read_flags()
            flags['stop'][func_name] = True
            flags['resume'][func_name] = False
            _write_flags(flags)
            print(f"[CONTROL] STOP flag set for function '{func_name}'")
    
    def resume_function(self, func_name: str):
        """Resume a specific function by name."""
        with self._lock:
            flags = _read_flags()
            flags['resume'][func_name] = True
            flags['stop'][func_name] = False
            _write_flags(flags)
            print(f"[CONTROL] RESUME flag set for function '{func_name}'")
    
    def kill_function(self, func_name: str):
        """Kill a specific function by name."""
        with self._lock:
            flags = _read_flags()
            flags['kill'][func_name] = True
            _write_flags(flags)
            print(f"[CONTROL] KILL flag set for function '{func_name}'")
    
    # ==================== GLOBAL CONTROL ====================
    
    def stop_all(self):
        """Pause all registered decorated functions."""
        with self._lock:
            flags = _read_flags()
            registry = _read_registry()
            for func_name in registry:
                flags['stop'][func_name] = True
                flags['resume'][func_name] = False
            _write_flags(flags)
            print(f"[CONTROL] STOP flag set for ALL functions ({len(registry)} functions)")
    
    def resume_all(self):
        """Resume all registered decorated functions."""
        with self._lock:
            flags = _read_flags()
            registry = _read_registry()
            for func_name in registry:
                flags['resume'][func_name] = True
                flags['stop'][func_name] = False
            _write_flags(flags)
            print(f"[CONTROL] RESUME flag set for ALL functions ({len(registry)} functions)")
    
    def kill_all(self):
        """Kill all registered decorated functions."""
        with self._lock:
            flags = _read_flags()
            registry = _read_registry()
            for func_name in registry:
                flags['kill'][func_name] = True
            _write_flags(flags)
            print(f"[CONTROL] KILL flag set for ALL functions ({len(registry)} functions)")
    
    # ==================== FLAG CHECKERS ====================
    
    def is_stopped(self, func_name: str) -> bool:
        """Check if a specific function should stop."""
        flags = _read_flags()
        return flags.get('stop', {}).get(func_name, False)
    
    def is_resumed(self, func_name: str) -> bool:
        """Check if a specific function should resume."""
        flags = _read_flags()
        return flags.get('resume', {}).get(func_name, False)
    
    def is_killed(self, func_name: str) -> bool:
        """Check if a specific function should be killed."""
        flags = _read_flags()
        return flags.get('kill', {}).get(func_name, False)
    
    def is_monitoring(self, func_name: str) -> bool:
        """Check if a specific function is being monitored."""
        flags = _read_flags()
        return flags.get('monitoring', {}).get(func_name, False)
    
    def set_monitoring(self, func_name: str, value: bool):
        """Set monitoring state for a specific function."""
        with self._lock:
            flags = _read_flags()
            if value:
                flags['monitoring'][func_name] = True
            elif func_name in flags['monitoring']:
                del flags['monitoring'][func_name]
            _write_flags(flags)
        
    @property
    def stop(self) -> bool:
        """Get stop flag state from file."""
        flags = _read_flags()
        return flags.get('stop', False)
    
    @stop.setter
    def stop(self, value: bool):
        """Set stop flag in file."""
        with self._lock:
            flags = _read_flags()
            flags['stop'] = value
            _write_flags(flags)
            if value:
                print(f"[CONTROL] STOP flag set to True - will pause at next checkpoint")
    
    # ==================== LEGACY PROPERTIES (for backward compatibility) ====================
    # These work globally on all functions
    
    @property
    def stop(self) -> bool:
        """
        DEPRECATED: Use stop_function() or stop_all() instead.
        Get global stop flag state (returns True if any function is stopped).
        """
        flags = _read_flags()
        stop_flags = flags.get('stop', {})
        return any(stop_flags.values()) if stop_flags else False
    
    @stop.setter
    def stop(self, value: bool):
        """
        DEPRECATED: Use stop_function() or stop_all() instead.
        Set stop flag for all functions (for backward compatibility).
        """
        if value:
            self.stop_all()
        else:
            with self._lock:
                flags = _read_flags()
                flags['stop'] = {}
                _write_flags(flags)
    
    @property
    def resume(self) -> bool:
        """
        DEPRECATED: Use resume_function() or resume_all() instead.
        Get global resume flag state (returns True if any function should resume).
        """
        flags = _read_flags()
        resume_flags = flags.get('resume', {})
        return any(resume_flags.values()) if resume_flags else False
    
    @resume.setter
    def resume(self, value: bool):
        """
        DEPRECATED: Use resume_function() or resume_all() instead.
        Set resume flag for all functions (for backward compatibility).
        """
        if value:
            self.resume_all()
        else:
            with self._lock:
                flags = _read_flags()
                flags['resume'] = {}
                _write_flags(flags)
    
    @property
    def monitoring(self) -> bool:
        """
        DEPRECATED: Check is_monitoring(func_name) instead.
        Get global monitoring state (returns True if any function is being monitored).
        """
        flags = _read_flags()
        monitoring_flags = flags.get('monitoring', {})
        return any(monitoring_flags.values()) if monitoring_flags else False
    
    @monitoring.setter
    def monitoring(self, value: bool):
        """DEPRECATED: Use set_monitoring(func_name, value) instead."""
        pass  # No-op for backward compatibility
    
    @property
    def kill(self) -> bool:
        """
        DEPRECATED: Use kill_function() or kill_all() instead.
        Get global kill flag state (returns True if any function should be killed).
        """
        flags = _read_flags()
        kill_flags = flags.get('kill', {})
        return any(kill_flags.values()) if kill_flags else False
    
    @kill.setter
    def kill(self, value: bool):
        """
        DEPRECATED: Use kill_function() or kill_all() instead.
        Set kill flag for all functions (for backward compatibility).
        """
        if value:
            self.kill_all()
        else:
            with self._lock:
                flags = _read_flags()
                flags['kill'] = {}
                _write_flags(flags)
    
    # ==================== UTILITY METHODS ====================
    
    def get_pid(self) -> int:
        """Get current process ID."""
        return self._current_pid
    
    def reset(self):
        """Reset all flags to default state."""
        with self._lock:
            _write_flags({
                'stop': {},
                'resume': {},
                'kill': {},
                'monitoring': {}
            })
            print("[CONTROL] All flags reset")
    
    def status(self, func_name: str = None) -> dict:
        """
        Get current status of flags.
        
        Args:
            func_name: If provided, get status for specific function.
                      If None, get status for all functions.
        
        Returns:
            Dict with flag status
        """
        flags = _read_flags()
        registry = _read_registry()
        
        if func_name:
            # Status for specific function
            return {
                'function': func_name,
                'registered': func_name in registry,
                'pid': registry.get(func_name, {}).get('pid'),
                'stop': flags.get('stop', {}).get(func_name, False),
                'resume': flags.get('resume', {}).get(func_name, False),
                'kill': flags.get('kill', {}).get(func_name, False),
                'monitoring': flags.get('monitoring', {}).get(func_name, False)
            }
        else:
            # Status for all functions
            all_functions = set(registry.keys())
            for flag_type in ['stop', 'resume', 'kill', 'monitoring']:
                all_functions.update(flags.get(flag_type, {}).keys())
            
            return {
                'registered_functions': len(registry),
                'functions': {
                    fn: {
                        'registered': fn in registry,
                        'pid': registry.get(fn, {}).get('pid'),
                        'stop': flags.get('stop', {}).get(fn, False),
                        'resume': flags.get('resume', {}).get(fn, False),
                        'kill': flags.get('kill', {}).get(fn, False),
                        'monitoring': flags.get('monitoring', {}).get(fn, False)
                    }
                    for fn in sorted(all_functions)
                },
                'current_pid': self._current_pid
            }


# Global singleton instance
control_flags = ControlFlags()
