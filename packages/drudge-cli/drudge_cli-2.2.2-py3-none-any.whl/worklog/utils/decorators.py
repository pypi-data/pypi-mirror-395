"""
Utility decorators for WorkLog CLI Tool.

This module provides decorators for common functionality like
data loading requirements and automatic saving.
"""

from functools import wraps
import logging

logger = logging.getLogger(__name__)


def requires_data(func):
    """
    Decorator to ensure data is loaded before method execution.
    
    Automatically calls _load_data() if self.data is None before
    executing the decorated method. Provides transparent data loading
    for methods that need access to worklog data.
    
    Args:
        func: Method to decorate
        
    Returns:
        Decorated method that ensures data is loaded
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._data is None:
            logger.debug(f"Loading data for {func.__name__}")
            self._data = self._load_data()
        return func(self, *args, **kwargs)
    return wrapper


def auto_save(func):
    """
    Decorator to automatically save data after method execution.
    
    Calls _save_data() after successful execution of the decorated method
    if the WorkLogConfig.auto_save setting is enabled. Provides automatic
    persistence without explicit save calls throughout the codebase.
    
    Args:
        func: Method to decorate
        
    Returns:
        Decorated method that automatically saves data
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if hasattr(self, 'config') and self.config.auto_save:
            logger.debug(f"Auto-saving after {func.__name__}")
            self._save_data()
        return result
    return wrapper