"""
Main entry point for the Drudge CLI application.

This module allows the package to be executed directly with:
    python -m worklog
    
Or with the drudge command:
    drudge start "My Task"
"""

from .cli import main

if __name__ == "__main__":
    main()