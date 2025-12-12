#!/usr/bin/env python3
"""
UCUP Build Wrapper

Wraps common build commands to display UCUP benefits.
Can be used as: ucup-build <command>
"""

import sys
import time
import subprocess
from typing import List, Optional

from .metrics import record_build_metrics, show_build_benefits


def run_build_command(command: List[str]) -> int:
    """Run a build command and track metrics"""
    print("\n🚀 Starting UCUP-enhanced build...\n")
    
    start_time = time.time()
    
    try:
        # Run the actual build command
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Parse output for metrics (basic implementation)
        output = result.stdout
        duration = time.time() - start_time
        
        # Count errors and warnings in output
        lines = output.split('\n')
        errors = sum(1 for line in lines if 'error' in line.lower())
        warnings = sum(1 for line in lines if 'warning' in line.lower())
        
        # Print the output
        print(output)
        
        # Record metrics
        record_build_metrics(
            duration=duration,
            errors_detected=errors,
            warnings_detected=warnings,
            uncertainty_checks=1,
            validation_runs=1,
            tests_run=0,
            tests_passed=0,
            tests_failed=0
        )
        
        # Show benefits
        show_build_benefits()
        
        return result.returncode
        
    except Exception as e:
        print(f"Error running build command: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for ucup-build command"""
    if len(sys.argv) < 2:
        print("Usage: ucup-build <command> [args...]")
        print("\nExamples:")
        print("  ucup-build python setup.py build")
        print("  ucup-build pip install -e .")
        print("  ucup-build python -m build")
        sys.exit(1)
    
    command = sys.argv[1:]
    exit_code = run_build_command(command)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
