"""
CLI package for WorkLog application.

This package contains all command-line interface components including
Typer command definitions, argument parsing, and user interaction.
"""

from .commands import app, main

__all__ = ['app', 'main']