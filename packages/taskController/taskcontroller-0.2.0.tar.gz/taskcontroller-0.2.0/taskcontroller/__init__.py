"""
PyController - Python Task Flow Control Library

A simple library for pause/resume/kill control of Python functions across processes.

Supports per-function control: you can control multiple decorated functions independently.

Usage:
    from pycontroller import task_controller, controller
    
    @task_controller
    def task_a():
        # Your code here
        pass
    
    @task_controller
    def task_b():
        # Your code here
        pass
    
    # Control specific functions from another process/terminal:
    controller.stop_function('task_a')    # Pause task_a only
    controller.resume_function('task_a')  # Resume task_a only
    controller.kill_function('task_b')    # Kill task_b only
    
    # Or control all functions at once:
    controller.stop_all()     # Pause all decorated functions
    controller.resume_all()   # Resume all decorated functions
    controller.kill_all()     # Kill all decorated functions
    
    # List and check status:
    controller.list_functions()         # See all registered functions
    controller.status('task_a')         # Check status of specific function
    controller.status()                 # Check status of all functions
    
    # Legacy global control (still supported for backward compatibility):
    controller.stop = True    # Pause all functions
    controller.resume = True  # Resume all functions
    controller.kill = True    # Kill all functions
"""

from .flow_control_decorator import task_controller
from .shared_var import control_flags as controller

__version__ = "0.2.0"
__all__ = ["task_controller", "controller"]
