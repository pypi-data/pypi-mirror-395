"""
Validation logic for WorkLog CLI Tool.

This module provides centralized validation for all user inputs including
dates, times, task names, and other data with consistent error messages.
"""

from datetime import datetime
from typing import Tuple
from .config import WorkLogConfig


class WorkLogValidator:
    """
    Centralized validation logic for WorkLog inputs.
    
    Provides consistent validation with clear error messages for
    dates, times, task names, and other user inputs.
    """
    
    @staticmethod
    def validate_date_format(date_str: str, config: WorkLogConfig) -> None:
        """
        Validate date string format matches configuration.
        
        Args:
            date_str: Date string to validate
            config: WorkLogConfig instance with date format
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            datetime.strptime(date_str, config.date_format)
        except ValueError:
            raise ValueError(f"Invalid date format: '{date_str}'. Expected format: {config.date_format}")
    
    @staticmethod
    def validate_time_format(time_str: str) -> Tuple[int, int]:
        """
        Validate and parse HH:MM time format.
        
        Args:
            time_str: Time string in HH:MM format
            
        Returns:
            Tuple of (hours, minutes) as integers
            
        Raises:
            ValueError: If time format is invalid or out of range
        """
        try:
            if ':' not in time_str:
                raise ValueError("Time must contain exactly one colon")
            
            parts = time_str.split(':')
            if len(parts) != 2:
                raise ValueError("Time must contain exactly one colon")
            
            hours = int(parts[0])
            minutes = int(parts[1])
            
            if not (0 <= hours <= 23):
                raise ValueError(f"Hours must be between 00-23, got {hours}")
            if not (0 <= minutes <= 59):
                raise ValueError(f"Minutes must be between 00-59, got {minutes}")
                
            return hours, minutes
            
        except (ValueError, IndexError) as e:
            if "invalid literal" in str(e):
                raise ValueError(f"Invalid time format '{time_str}': Non-numeric values found")
            raise ValueError(f"Invalid time format '{time_str}': {e}")
    
    @staticmethod
    def validate_datetime_format(datetime_str: str) -> datetime:
        """
        Validate and parse datetime string with optional date component.
        
        Supports two formats:
        - "HH:MM" - Time only, uses today's date
        - "YYYY-MM-DD HH:MM" - Full datetime
        
        Args:
            datetime_str: Datetime string in HH:MM or YYYY-MM-DD HH:MM format
            
        Returns:
            datetime: Parsed datetime object
            
        Raises:
            ValueError: If format is invalid
        """
        datetime_str = datetime_str.strip()
        
        # Check if it contains a date (has space separator)
        if ' ' in datetime_str:
            # Format: YYYY-MM-DD HH:MM
            parts = datetime_str.split(' ')
            if len(parts) != 2:
                raise ValueError(f"Invalid datetime format '{datetime_str}': Expected 'YYYY-MM-DD HH:MM' or 'HH:MM'")
            
            date_str, time_str = parts
            
            # Validate date
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format '{date_str}': Expected YYYY-MM-DD")
            
            # Validate time
            hours, minutes = WorkLogValidator.validate_time_format(time_str)
            
            return datetime.combine(
                date_obj,
                datetime.min.time().replace(hour=hours, minute=minutes)
            )
        else:
            # Format: HH:MM (use today's date)
            hours, minutes = WorkLogValidator.validate_time_format(datetime_str)
            
            today = datetime.now().date()
            return datetime.combine(
                today,
                datetime.min.time().replace(hour=hours, minute=minutes)
            )
    
    @staticmethod
    def validate_time_sequence(start_time: str, stop_time: str) -> None:
        """
        Validate that stop time is after start time.
        
        Args:
            start_time: Start time string
            stop_time: Stop time string
            
        Raises:
            ValueError: If stop time is not after start time
        """
        start_dt = datetime.fromisoformat(start_time)
        stop_dt = datetime.fromisoformat(stop_time)
        
        if stop_dt <= start_dt:
            raise ValueError(f"Stop time ({stop_time}) must be after start time ({start_time})")
    
    @staticmethod
    def validate_task_name(task_name: str) -> str:
        """
        Validate task name is not empty and doesn't contain problematic characters.
        
        Args:
            task_name: Task name to validate
            
        Returns:
            str: Cleaned and validated task name
            
        Raises:
            ValueError: If task name is invalid
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        cleaned_name = task_name.strip()
        if len(cleaned_name) > 100:
            raise ValueError("Task name cannot exceed 100 characters")
        
        return cleaned_name
        
        # Check for problematic characters that might break file operations
        problematic_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in problematic_chars:
            if char in task_name:
                raise ValueError(f"Task name cannot contain '{char}' character")