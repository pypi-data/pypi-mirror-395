"""
Daily file management for WorkLog CLI Tool.

This module handles all operations related to daily readable log files,
including formatting entries and maintaining chronological order.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
from functools import lru_cache
import logging

from ..config import WorkLogConfig

logger = logging.getLogger(__name__)


class DailyFileManager:
    """
    Manages daily human-readable log files with consistent formatting.
    
    Handles creation and maintenance of organized daily log files that
    provide a clean, readable view of daily work activities.
    """
    
    def __init__(self, config: Optional[WorkLogConfig] = None):
        """
        Initialize DailyFileManager with configuration.
        
        Args:
            config: Optional WorkLogConfig instance
        """
        self.config = config or WorkLogConfig()
    
    @lru_cache(maxsize=128)
    def _format_display_time(self, timestamp: str) -> str:
        """
        Format ISO timestamp for human-readable display.
        
        Cached method for efficient timestamp formatting in daily logs.
        
        Args:
            timestamp: ISO format timestamp string
            
        Returns:
            str: Formatted timestamp for display
        """
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime(self.config.display_time_format)
    
    def format_entry(
        self, 
        task_name: str, 
        action: str, 
        timestamp: str, 
        duration: Optional[str] = None
    ) -> str:
        """
        Format a single entry for the daily log file.
        
        Creates consistently formatted entries for different types of
        task actions (start, end, pause, resume, completed).
        
        Args:
            task_name: Name of the task
            action: Type of action ('start', 'end', 'pause', 'resume', 'completed')
            timestamp: ISO timestamp of the action
            duration: Optional duration string for completed tasks
            
        Returns:
            str: Formatted entry string
        """
        display_time = self._format_display_time(timestamp)
        display_name = "[ANONYMOUS WORK]" if task_name == "__ANONYMOUS_WORK__" else task_name
        
        # Format the log entry based on action type
        if action == 'start':
            return f"{display_time} {display_name} [ACTIVE]"
        elif action == 'end' and duration:
            return f"{display_time} {display_name} ({duration})"
        elif action == 'completed' and duration:
            # For retroactive entries, use start time from duration calculation
            start_dt = datetime.fromisoformat(timestamp)
            duration_parts = duration.split(':')
            hours, minutes, seconds = int(duration_parts[0]), int(duration_parts[1]), int(duration_parts[2])
            start_time = start_dt - timedelta(hours=hours, minutes=minutes, seconds=seconds)
            start_display = self._format_display_time(start_time.isoformat())
            return f"{start_display} {display_name} ({duration})"
        elif action == 'pause':
            return f"{display_time} {display_name} [PAUSED]"
        elif action == 'resume':
            return f"{display_time} {display_name} [RESUMED]"
        else:
            return f"{display_time} {display_name} [{action.upper()}]"
    
    def add_entry_chronologically(self, daily_file: Path, new_entry: str) -> None:
        """
        Add entry to daily file and maintain chronological order.
        
        Reads existing entries, adds the new entry, sorts by timestamp,
        and rewrites the file in chronological order. Removes duplicates
        for the same task when adding completion entries.
        
        Args:
            daily_file: Path to the daily log file
            new_entry: Formatted entry string to add
        """
        entries = []
        
        try:
            # Read existing entries if file exists
            if daily_file.exists():
                with open(daily_file, 'r', encoding='utf-8') as f:
                    entries = f.read().strip().split('\n')
                    entries = [entry for entry in entries if entry.strip()]
            
            # Extract task name from new entry for duplicate detection
            # Format: "YYYY-MM-DD HH:MM:SS TaskName [STATUS]" or "YYYY-MM-DD HH:MM:SS TaskName (duration)"
            new_entry_parts = new_entry.split(' ', 2)
            if len(new_entry_parts) >= 3:
                new_task_identifier = new_entry_parts[2]  # Everything after timestamp
                
                # If this is a completion entry (contains duration in parentheses), 
                # remove any existing entries for the same task
                if '(' in new_task_identifier and ')' in new_task_identifier:
                    task_name = new_task_identifier.split('(')[0].strip()
                    # Remove existing entries for this task (both [ACTIVE], [PAUSED], etc.)
                    entries = [entry for entry in entries if not (
                        len(entry.split(' ', 2)) >= 3 and
                        entry.split(' ', 2)[2].startswith(task_name + ' ')
                    )]
            
            # Add new entry
            entries.append(new_entry)
            
            # Sort entries chronologically by timestamp (first 19 characters: YYYY-MM-DD HH:MM:SS)
            entries.sort(key=lambda x: x[:19] if len(x) >= 19 else x)
            
            # Write sorted entries back to file
            daily_file.parent.mkdir(parents=True, exist_ok=True)
            with open(daily_file, 'w', encoding='utf-8') as f:
                for entry in entries:
                    f.write(f"{entry}\n")
                    
            logger.debug(f"Added entry to {daily_file}: {new_entry}")
            
        except Exception as e:
            logger.error(f"Failed to add entry to daily file {daily_file}: {e}")
            raise IOError(f"Daily file operation failed: {e}")