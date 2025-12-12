"""
Utility modules for WorkLog CLI Tool.

Provides common utility functions and decorators used throughout
the worklog system.
"""

from .decorators import requires_data, auto_save

__all__ = ['requires_data', 'auto_save']