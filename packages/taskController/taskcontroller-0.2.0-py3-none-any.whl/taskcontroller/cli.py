#!/usr/bin/env python
"""
PyController CLI - Command-line interface for controlling decorated functions.

This module provides CLI commands that can be called directly from terminal:
    pycontroller ps              - List all running decorated functions
    pycontroller stop <func>     - Stop/pause a function
    pycontroller resume <func>   - Resume a paused function
    pycontroller kill <func>     - Kill a function
    pycontroller status [func]   - Show status of function(s)
    pycontroller reset           - Reset all flags
"""

import sys
import json
import argparse
from .shared_var import control_flags as controller


def format_table(headers, rows):
    """Format data as a table."""
    if not rows:
        return ""
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Create format string
    row_format = "  ".join([f"{{:<{w}}}" for w in col_widths])
    
    # Build table
    lines = []
    lines.append(row_format.format(*headers))
    lines.append("-" * (sum(col_widths) + 2 * (len(headers) - 1)))
    for row in rows:
        lines.append(row_format.format(*[str(cell) for cell in row]))
    
    return "\n".join(lines)


def cmd_ps(args):
    """List all running decorated functions (like 'ps' command)."""
    functions = controller.list_functions()
    
    if not functions:
        print("No decorated functions are currently running.")
        return 0
    
    # Get status for all functions
    all_status = controller.status()
    func_statuses = all_status.get('functions', {})
    
    # Build table data
    headers = ["FUNCTION", "PID", "STATUS", "MONITORING"]
    rows = []
    
    for func_name in sorted(functions.keys()):
        metadata = functions[func_name]
        status = func_statuses.get(func_name, {})
        
        pid = metadata.get('pid', 'N/A')
        
        # Determine status
        if status.get('kill', False):
            status_str = "KILLING"
        elif status.get('stop', False):
            status_str = "PAUSED"
        elif status.get('resume', False):
            status_str = "RESUMING"
        elif status.get('monitoring', False):
            status_str = "RUNNING"
        else:
            status_str = "IDLE"
        
        monitoring = "✓" if status.get('monitoring', False) else "✗"
        
        rows.append([func_name, pid, status_str, monitoring])
    
    print(format_table(headers, rows))
    print(f"\nTotal: {len(functions)} function(s)")
    
    return 0


def cmd_stop(args):
    """Stop/pause a function."""
    func_name = args.function
    
    # Check if function exists
    functions = controller.list_functions()
    if func_name not in functions:
        print(f"Error: Function '{func_name}' is not running.")
        print(f"Available functions: {', '.join(functions.keys()) if functions else 'none'}")
        return 1
    
    controller.stop_function(func_name)
    print(f"✓ Stop signal sent to '{func_name}'")
    return 0


def cmd_resume(args):
    """Resume a paused function."""
    func_name = args.function
    
    # Check if function exists
    functions = controller.list_functions()
    if func_name not in functions:
        print(f"Error: Function '{func_name}' is not running.")
        print(f"Available functions: {', '.join(functions.keys()) if functions else 'none'}")
        return 1
    
    controller.resume_function(func_name)
    print(f"✓ Resume signal sent to '{func_name}'")
    return 0


def cmd_kill(args):
    """Kill a function."""
    func_name = args.function
    
    # Check if function exists
    functions = controller.list_functions()
    if func_name not in functions:
        print(f"Error: Function '{func_name}' is not running.")
        print(f"Available functions: {', '.join(functions.keys()) if functions else 'none'}")
        return 1
    
    controller.kill_function(func_name)
    print(f"✓ Kill signal sent to '{func_name}'")
    return 0


def cmd_stop_all(args):
    """Stop all running functions."""
    functions = controller.list_functions()
    if not functions:
        print("No functions are currently running.")
        return 0
    
    controller.stop_all()
    print(f"✓ Stop signal sent to all {len(functions)} function(s)")
    return 0


def cmd_resume_all(args):
    """Resume all paused functions."""
    functions = controller.list_functions()
    if not functions:
        print("No functions are currently running.")
        return 0
    
    controller.resume_all()
    print(f"✓ Resume signal sent to all {len(functions)} function(s)")
    return 0


def cmd_kill_all(args):
    """Kill all running functions."""
    functions = controller.list_functions()
    if not functions:
        print("No functions are currently running.")
        return 0
    
    controller.kill_all()
    print(f"✓ Kill signal sent to all {len(functions)} function(s)")
    return 0


def cmd_status(args):
    """Show detailed status of function(s)."""
    func_name = args.function if hasattr(args, 'function') else None
    
    if func_name:
        # Check if function exists
        functions = controller.list_functions()
        if func_name not in functions:
            print(f"Error: Function '{func_name}' is not running.")
            print(f"Available functions: {', '.join(functions.keys()) if functions else 'none'}")
            return 1
        
        status = controller.status(func_name)
        print(f"\nStatus of '{func_name}':")
        print(json.dumps(status, indent=2))
    else:
        status = controller.status()
        print("\nGlobal Status:")
        print(json.dumps(status, indent=2))
    
    return 0


def cmd_reset(args):
    """Reset all control flags."""
    controller.reset()
    print("✓ All control flags have been reset")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='pycontroller',
        description='Control decorated Python functions from the command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pycontroller ps                    # List all running functions
  pycontroller stop my_function      # Pause a specific function
  pycontroller resume my_function    # Resume a specific function
  pycontroller kill my_function      # Kill a specific function
  pycontroller status                # Show status of all functions
  pycontroller status my_function    # Show status of specific function
  pycontroller reset                 # Reset all flags
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # ps command
    ps_parser = subparsers.add_parser('ps', help='List all running decorated functions')
    ps_parser.set_defaults(func=cmd_ps)
    
    # stop command
    stop_parser = subparsers.add_parser('stop', help='Stop/pause a function')
    stop_parser.add_argument('function', help='Name of the function to stop')
    stop_parser.set_defaults(func=cmd_stop)
    
    # resume command
    resume_parser = subparsers.add_parser('resume', help='Resume a paused function')
    resume_parser.add_argument('function', help='Name of the function to resume')
    resume_parser.set_defaults(func=cmd_resume)
    
    # kill command
    kill_parser = subparsers.add_parser('kill', help='Kill a function')
    kill_parser.add_argument('function', help='Name of the function to kill')
    kill_parser.set_defaults(func=cmd_kill)
    
    # stop-all command
    stop_all_parser = subparsers.add_parser('stop-all', help='Stop all running functions')
    stop_all_parser.set_defaults(func=cmd_stop_all)
    
    # resume-all command
    resume_all_parser = subparsers.add_parser('resume-all', help='Resume all paused functions')
    resume_all_parser.set_defaults(func=cmd_resume_all)
    
    # kill-all command
    kill_all_parser = subparsers.add_parser('kill-all', help='Kill all running functions')
    kill_all_parser.set_defaults(func=cmd_kill_all)
    
    # status command
    status_parser = subparsers.add_parser('status', help='Show status of function(s)')
    status_parser.add_argument('function', nargs='?', help='Name of the function (optional)')
    status_parser.set_defaults(func=cmd_status)
    
    # reset command
    reset_parser = subparsers.add_parser('reset', help='Reset all control flags')
    reset_parser.set_defaults(func=cmd_reset)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    try:
        return args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
