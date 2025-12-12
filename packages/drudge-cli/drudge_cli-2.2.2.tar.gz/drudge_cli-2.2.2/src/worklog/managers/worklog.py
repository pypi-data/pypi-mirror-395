"""
Core WorkLog management class.

This module contains the main WorkLog class that orchestrates all
time tracking functionality and integrates with other components.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Any, Union
from contextlib import contextmanager
from functools import lru_cache
import logging

from rich.console import Console
from rich.table import Table

from ..models import TaskEntry, PausedTask, WorkLogData
from ..config import WorkLogConfig
from ..validators import WorkLogValidator
from ..utils.decorators import requires_data, auto_save
from .backup import BackupManager
from .daily_file import DailyFileManager

# Initialize rich console for beautiful output
console = Console()
logger = logging.getLogger(__name__)


class WorkLog:
    """
    Modern WorkLog class with comprehensive time tracking capabilities.
    
    This class provides a complete solution for tracking work time on tasks,
    including single-task and parallel modes, pause/resume functionality,
    anonymous work sessions, and organized daily logs.
    
    Enhanced with configuration management, validation, and structured logging.
    """
    
    ANONYMOUS_TASK_NAME = "__ANONYMOUS_WORK__"
    
    def __init__(self, config: Optional[WorkLogConfig] = None) -> None:
        """
        Initialize WorkLog with directory setup and data migration.
        
        Creates the worklog directory structure and migrates any existing
        data from the old format. Initializes the data structure for tracking
        tasks, active sessions, and paused work.
        
        Args:
            config: Optional configuration override
        """
        self.config = config or WorkLogConfig()
        self.validator = WorkLogValidator()
        self.daily_file_manager = DailyFileManager(self.config)
        self.backup_manager = BackupManager()
        
        # Handle configurable worklog directory path
        if hasattr(self.config, 'worklog_dir') and self.config.worklog_dir:
            self.worklog_dir = Path(self.config.worklog_dir)
        else:
            self.worklog_dir = Path.home() / self.config.worklog_dir_name
        self.worklog_file = self.worklog_dir / 'worklog.json'
        self._data: Optional[WorkLogData] = None
        
        self._ensure_directory()
        self._migrate_old_file()
        
        logger.info(f"WorkLog initialized with directory: {self.worklog_dir}")
    
    @property
    def data(self) -> WorkLogData:
        """
        Lazy-loaded property for accessing worklog data.
        
        Returns:
            WorkLogData: Current worklog state with all tasks and sessions
        """
        if self._data is None:
            self._data = self._load_data()
        return self._data
    
    def _ensure_directory(self) -> None:
        """
        Create the worklog directory structure if it doesn't exist.
        
        Creates ~/.worklog directory with appropriate permissions for
        storing JSON database and daily text files.
        
        Raises:
            PermissionError: If unable to create directory due to permissions
            OSError: If directory creation fails for other reasons
        """
        try:
            self.worklog_dir.mkdir(exist_ok=True)
            logger.info(f"Directory ensured: {self.worklog_dir}")
        except PermissionError:
            console.print(
                f"❌ Permission denied creating worklog directory: {self.worklog_dir}\n"
                "💡 Try running with appropriate permissions or choose a different location.",
                style="red"
            )
            raise
        except OSError as e:
            console.print(
                f"❌ Failed to create worklog directory: {self.worklog_dir}\n"
                f"💥 Error: {e}",
                style="red"
            )
            raise
    
    def _migrate_old_file(self) -> None:
        """
        Migrate legacy worklog.json from home directory to new structure.
        
        Automatically detects and migrates existing ~/.worklog.json file
        to the new ~/.worklog/worklog.json location, preserving all
        historical data and maintaining backward compatibility.
        """
        old_file = Path.home() / '.worklog.json'
        if old_file.exists() and not self.worklog_file.exists():
            try:
                with open(old_file, 'r') as f:
                    data = f.read()
                with open(self.worklog_file, 'w') as f:
                    f.write(data)
                console.print(f"✅ Migrated worklog data to {self.worklog_file}")
                
                # Backup and remove old file
                backup_file = Path.home() / '.worklog.json.backup'
                old_file.rename(backup_file)
                console.print(f"📦 Backup created at {backup_file}")
                
            except Exception as e:
                logger.error(f"Migration failed: {e}")
                console.print(f"⚠️ Migration failed: {e}", style="yellow")
    
    @contextmanager
    def _file_operation(self, file_path: Path, mode: str = 'r'):
        """
        Context manager for safe file operations with error handling.
        
        Args:
            file_path: Path to the file
            mode: File opening mode ('r', 'w', 'a', etc.)
            
        Yields:
            file object: Opened file handle
            
        Example:
            >>> with worklog._file_operation(path, 'w') as f:
            ...     f.write(content)
        """
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                yield f
        except FileNotFoundError:
            if 'r' in mode:
                console.print(f"📄 File not found: {file_path}", style="yellow")
            raise
        except Exception as e:
            console.print(f"❌ File operation failed: {e}", style="red")
            raise
    
    def _load_data(self) -> WorkLogData:
        """
        Load worklog data from JSON file with error handling and validation.
        
        Loads the complete worklog state from the JSON database, handling
        legacy formats and providing sensible defaults for missing fields.
        Performs data validation and structure migration as needed.
        
        Returns:
            WorkLogData: Complete worklog state with all tasks and sessions
            
        Raises:
            json.JSONDecodeError: If JSON file is corrupted
            FileNotFoundError: If worklog file doesn't exist (creates new)
        """
        if not self.worklog_file.exists():
            console.print("📝 Creating new worklog database", style="green")
            return WorkLogData()
        
        try:
            with self._file_operation(self.worklog_file) as f:
                raw_data = json.load(f)
            
            # Convert raw dict to structured data with validation
            # Handle both old format (without project) and new format (with project)
            entries = []
            for entry in raw_data.get('entries', []):
                if isinstance(entry, dict):
                    # Filter out any fields that TaskEntry doesn't support
                    # This provides forward/backward compatibility
                    valid_fields = {'task', 'start_time', 'end_time', 'duration', 'project'}
                    filtered_entry = {k: v for k, v in entry.items() if k in valid_fields}
                    entries.append(TaskEntry(**filtered_entry))
                else:
                    entries.append(TaskEntry(*entry))
            
            paused_tasks = [
                PausedTask(**task) if isinstance(task, dict) else PausedTask(*task)
                for task in raw_data.get('paused_tasks', [])
            ]
            
            return WorkLogData(
                entries=entries,
                active_tasks=raw_data.get('active_tasks', {}),
                paused_tasks=paused_tasks,
                recent_tasks=raw_data.get('recent_tasks', []),
                active_task_projects=raw_data.get('active_task_projects', {})
            )
            
        except json.JSONDecodeError as e:
            console.print(f"❌ Corrupted worklog file: {e}", style="red")
            console.print("🔄 Creating backup and starting fresh", style="yellow")
            
            # Create backup of corrupted file
            backup_file = self.worklog_file.with_suffix('.json.corrupted')
            try:
                self.worklog_file.rename(backup_file)
                console.print(f"💾 Corrupted file saved as: {backup_file}", style="dim")
            except OSError as backup_error:
                console.print(f"⚠️  Could not backup corrupted file: {backup_error}", style="yellow")
            
            logger.warning(f"JSON corruption in {self.worklog_file}: {e}")
            return WorkLogData()
        except Exception as e:
            console.print(
                f"❌ Unexpected error loading worklog data: {e}\n"
                "💡 Please check file permissions and disk space.",
                style="red"
            )
            logger.error(f"Unexpected error loading data: {e}")
            raise
    
    def _save_data(self) -> None:
        """
        Save worklog data to JSON file with atomic writes and error handling.
        
        Performs atomic write operation to prevent data corruption during
        save operations. Converts dataclass objects to JSON-serializable
        format while preserving all structure and metadata.
        
        Automatically sorts entries chronologically by start_time to maintain
        proper time sequence in both JSON database and daily files.
        
        Raises:
            IOError: If unable to write to disk
            TypeError, ValueError: If data cannot be serialized to JSON
        """
        # Sort entries chronologically by start_time before saving (ISO strings sort correctly)
        self.data.entries.sort(key=lambda entry: entry.start_time if isinstance(entry.start_time, str) else entry.start_time.isoformat())
        
        # Convert dataclasses to dictionaries for JSON serialization
        data_dict = {
            'entries': [entry.__dict__ for entry in self.data.entries],
            'active_tasks': self.data.active_tasks,
            'paused_tasks': [task.__dict__ for task in self.data.paused_tasks],
            'recent_tasks': self.data.recent_tasks,
            'active_task_projects': self.data.active_task_projects
        }
        
        # Atomic write: write to temp file then rename
        temp_file = self.worklog_file.with_suffix('.tmp')
        try:
            with self._file_operation(temp_file, 'w') as f:
                json.dump(data_dict, f, indent=2, ensure_ascii=False)
            temp_file.replace(self.worklog_file)
            logger.debug(f"Data saved successfully to {self.worklog_file}")
        except (TypeError, ValueError) as e:
            # TypeError: Object not JSON serializable
            # ValueError: Circular reference or other JSON encoding issues
            console.print(f"❌ Failed to serialize worklog data: {e}", style="red")
            logger.error(f"JSON encoding error: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise
        except (IOError, OSError) as e:
            console.print(
                f"❌ Failed to save worklog data: {e}\n"
                "💡 Check available disk space and file permissions.",
                style="red"
            )
            logger.error(f"IO error saving data: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise
        except Exception as e:
            console.print(f"❌ Unexpected error saving data: {e}", style="red")
            logger.error(f"Unexpected error saving data: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise
    
    # ============================================================================
    # Time and Utility Methods
    # ============================================================================
    
    @staticmethod
    def _get_current_timestamp() -> str:
        """
        Get current timestamp in ISO format.
        
        Returns:
            str: Current timestamp in ISO format for consistency
        """
        return datetime.now().isoformat()
    
    @lru_cache(maxsize=128)
    def _format_display_time(self, timestamp: str) -> str:
        """
        Format ISO timestamp for human-readable display.
        
        Cached method for efficient timestamp formatting throughout the system.
        
        Args:
            timestamp: ISO format timestamp string
            
        Returns:
            str: Formatted timestamp for display
        """
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime(self.config.display_time_format)
    
    def _format_duration(self, start_time: str, end_time: str) -> str:
        """
        Calculate and format duration between two timestamps.
        
        Args:
            start_time: ISO timestamp string for start
            end_time: ISO timestamp string for end
            
        Returns:
            str: Formatted duration in HH:MM:SS format
        """
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
        
        duration = end_dt - start_dt
        if duration.total_seconds() < 0:
            return "00:00:00"  # Handle negative durations gracefully
        
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def _get_timestamp(self, custom_time: Optional[str]) -> str:
        """
        Get timestamp for task operations, with optional custom time.
        
        Args:
            custom_time: Optional HH:MM format time string
            
        Returns:
            str: ISO timestamp string
        """
        if custom_time:
            return self._parse_custom_time(custom_time)
        return self._get_current_timestamp()
    
    @staticmethod
    def _parse_custom_time(time_str: str) -> str:
        """
        Parse and validate time string for custom start/end times.
        
        Supports two formats:
        - HH:MM (e.g., "09:30", "14:45") - Uses today's date
        - YYYY-MM-DD HH:MM (e.g., "2025-12-10 09:30") - Uses specified date
        
        Args:
            time_str: Time string in HH:MM or YYYY-MM-DD HH:MM format
            
        Returns:
            str: ISO timestamp for the specified date and time
            
        Raises:
            ValueError: If time format is invalid or values out of range
        """
        # Use centralized validation that supports both formats
        custom_datetime = WorkLogValidator.validate_datetime_format(time_str)
        
        return custom_datetime.isoformat()
    
    def _get_daily_file_path(self, date_str: Optional[str] = None) -> Path:
        """
        Get path to daily log file for a specific date.
        
        Args:
            date_str: Optional date string (YYYY-MM-DD), defaults to today
            
        Returns:
            Path: Path to the daily log file
        """
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        daily_dir = self.worklog_dir / "daily"
        daily_dir.mkdir(exist_ok=True)
        return daily_dir / f"{date_str}.txt"
    
    def _update_daily_file(self, task_name: str, action: str, timestamp: str, duration: Optional[str] = None) -> None:
        """
        Update daily human-readable log file with task activity.
        
        Uses the DailyFileManager for consistent formatting and chronological ordering.
        
        Args:
            task_name: Name of the task being logged
            action: Type of action ('start', 'end', 'pause', 'resume', 'completed')
            timestamp: ISO timestamp of the action
            duration: Optional duration string for completed tasks
        """
        daily_file = self._get_daily_file_path()
        entry = self.daily_file_manager.format_entry(task_name, action, timestamp, duration)
        self.daily_file_manager.add_entry_chronologically(daily_file, entry)
    
    # ============================================================================
    # Task Management Methods  
    # ============================================================================
    
    @auto_save
    def start_task(self, task_name: Optional[str] = None, custom_time: str = None, force: bool = False, parallel: bool = False, project: Optional[str] = None) -> bool:
        """
        Start a new task or resume an existing one.
        
        Handles task validation, active task management, and proper time tracking
        with enhanced user experience and comprehensive error handling.
        
        Args:
            task_name: Name of the task to start (None for anonymous work session)
            custom_time: Optional HH:MM format time (e.g., "09:30") to use instead of current time
            force: If True, automatically ends any currently active tasks
            parallel: If True, allows starting task even when others are active (parallel mode)
            project: Optional project/category name for task organization
            
        Returns:
            bool: True if task started successfully, False otherwise
            
        Raises:
            ValueError: If task name is invalid or time format is wrong
        """
        try:
            # Handle anonymous work session
            if task_name is None or task_name.strip() == "":
                task_name = self.ANONYMOUS_TASK_NAME
                console.print("💡 Starting anonymous work session", style="blue")
            else:
                # Validate inputs using centralized validation
                task_name = WorkLogValidator.validate_task_name(task_name)
            timestamp = self._get_timestamp(custom_time)
            
            # Display formatted time for user confirmation
            display_time = self._format_display_time(timestamp)
            
            # Special case: If anonymous work is active and user provides a task name, rename it
            if (task_name != self.ANONYMOUS_TASK_NAME and 
                self.ANONYMOUS_TASK_NAME in self.data.active_tasks and 
                not parallel):
                # Convert anonymous task to named task
                anonymous_start_time = self.data.active_tasks[self.ANONYMOUS_TASK_NAME]
                del self.data.active_tasks[self.ANONYMOUS_TASK_NAME]
                self.data.active_tasks[task_name] = anonymous_start_time
                
                # Add to recent tasks
                if task_name not in self.data.recent_tasks:
                    self.data.recent_tasks.insert(0, task_name)
                    if len(self.data.recent_tasks) > self.config.max_recent_tasks:
                        self.data.recent_tasks = self.data.recent_tasks[:self.config.max_recent_tasks]
                
                console.print(f"✏️  Renamed anonymous work to '{task_name}'")
                logger.info(f"Converted anonymous task to: {task_name}")
                return True
            
            # Check for existing active tasks (skip if parallel mode)
            if self.data.active_tasks and not force and not parallel:
                active_list = ', '.join(self.data.active_tasks.keys())
                console.print(
                    f"⚠️ Active tasks: {active_list}\n"
                    "💡 Use 'worklog end <task>' first or --force to auto-end",
                    style="yellow"
                )
                return False
            
            # Auto-end active tasks if force is enabled
            if force and self.data.active_tasks:
                for active_task in list(self.data.active_tasks.keys()):
                    console.print(f"🏁 Auto-ending: {active_task}")
                    self.end_task(active_task, timestamp=timestamp)
            
            # Check if task is currently paused (resume it)
            paused_task = next(
                (task for task in self.data.paused_tasks if task.task == task_name), 
                None
            )
            
            if paused_task:
                # Resume paused task
                self.data.paused_tasks.remove(paused_task)
                self.data.active_tasks[task_name] = timestamp
                display_name = "[ANONYMOUS WORK]" if task_name == self.ANONYMOUS_TASK_NAME else task_name
                console.print(f"▶️ Resumed '{display_name}' at {display_time}")
                logger.info(f"Task resumed: {task_name} at {timestamp}")
                self._update_daily_file(task_name, "resume", timestamp)
                return True
            
            # Start new task
            self.data.active_tasks[task_name] = timestamp
            
            # Store project assignment if provided
            if project:
                self.data.active_task_projects[task_name] = project
            
            # Add to recent tasks (maintain max size) - but not anonymous tasks
            if task_name != self.ANONYMOUS_TASK_NAME and task_name not in self.data.recent_tasks:
                self.data.recent_tasks.insert(0, task_name)
                if len(self.data.recent_tasks) > self.config.max_recent_tasks:
                    self.data.recent_tasks = self.data.recent_tasks[:self.config.max_recent_tasks]
            
            # Display friendly name for output
            display_name = "[ANONYMOUS WORK]" if task_name == self.ANONYMOUS_TASK_NAME else task_name
            project_info = f" [{project}]" if project else ""
            console.print(f"🚀 Started '{display_name}'{project_info} at {display_time}")
            logger.info(f"Task started: {task_name} (project: {project or 'none'}) at {timestamp}")
            self._update_daily_file(task_name, "start", timestamp)
            return True
            
        except ValueError as e:
            console.print(f"❌ Invalid input: {e}", style="red")
            logger.warning(f"Task start failed - validation error: {e}")
            return False
        except Exception as e:
            console.print(f"❌ Failed to start task: {e}", style="red")
            logger.error(f"Unexpected error starting task {task_name}: {e}")
            return False
    
    @auto_save  
    def end_task(self, task_name: str, custom_time: str = None, timestamp: str = None) -> bool:
        """
        End an active task and record its completion.
        
        Creates a task entry with calculated duration and updates all tracking
        systems (JSON database, daily files, active tasks list).
        
        Args:
            task_name: Name of the task to end
            custom_time: Optional HH:MM format time for custom end time
            timestamp: Internal parameter for precise timestamp (used by auto-end)
            
        Returns:
            bool: True if task ended successfully, False otherwise
        """
        try:
            if task_name is None:
                raise ValueError("Task name cannot be None")
            task_name = WorkLogValidator.validate_task_name(task_name)
            
            # Check if task is active
            if task_name not in self.data.active_tasks:
                available_tasks = ', '.join(self.data.active_tasks.keys()) if self.data.active_tasks else 'No active tasks'
                console.print(
                    f"⚠️ '{task_name}' is not active\n"
                    f"📋 Active tasks: {available_tasks}",
                    style="yellow"
                )
                return False
            
            # Get end timestamp (either provided internally or from user input)
            end_timestamp = timestamp or self._get_timestamp(custom_time)
            
            # Find the start time for this task
            start_time = self._find_task_start_time(task_name)
            if not start_time:
                console.print(f"⚠️ Cannot find start time for '{task_name}'", style="yellow")
                return False
            
            # Calculate duration
            duration = self._format_duration(start_time, end_timestamp)
            display_end_time = self._format_display_time(end_timestamp)
            
            # Get project for this task
            task_project = self.data.active_task_projects.get(task_name)
            
            # Create task entry
            entry = TaskEntry(
                task=task_name,
                start_time=start_time,
                end_time=end_timestamp,
                duration=duration,
                project=task_project
            )
            
            # Update data structures
            self.data.entries.append(entry)
            del self.data.active_tasks[task_name]
            
            # Remove project tracking
            if task_name in self.data.active_task_projects:
                del self.data.active_task_projects[task_name]
            
            display_name = "[ANONYMOUS WORK]" if task_name == self.ANONYMOUS_TASK_NAME else task_name
            project_info = f" [{task_project}]" if task_project else ""
            console.print(f"🏁 Completed '{display_name}'{project_info} at {display_end_time} (Duration: {duration})")
            logger.info(f"Task completed: {task_name}, duration: {duration}")
            
            # Update daily file with completion info
            self._update_daily_file(task_name, "completed", end_timestamp, duration)
            return True
            
        except ValueError as e:
            console.print(f"❌ Invalid input: {e}", style="red")
            logger.warning(f"Task end failed - validation error: {e}")
            return False
        except Exception as e:
            console.print(f"❌ Failed to end task: {e}", style="red")
            logger.error(f"Unexpected error ending task {task_name}: {e}")
            return False
    
    @auto_save
    def end_all_tasks(self, custom_time: str = None, include_paused: bool = False) -> bool:
        """
        End all currently active tasks, optionally including paused tasks.
        
        Convenience method to end all active tasks at once. Useful when
        finishing work for the day or switching contexts.
        
        Args:
            custom_time: Optional HH:MM format time for custom end time
            include_paused: If True, also end all paused tasks
            
        Returns:
            bool: True if at least one task was ended successfully, False otherwise
        """
        has_tasks = self.data.active_tasks or (include_paused and self.data.paused_tasks)
        
        if not has_tasks:
            console.print("ℹ️  No tasks to end", style="blue")
            return False
        
        # Get list of active tasks (copy to avoid modification during iteration)
        active_task_names = list(self.data.active_tasks.keys())
        paused_task_names = [p.task for p in self.data.paused_tasks] if include_paused else []
        
        total_tasks = len(active_task_names) + len(paused_task_names)
        task_type = "active and paused" if include_paused else "active"
        console.print(f"🏁 Ending {total_tasks} {task_type} task(s)...\n")
        
        ended_count = 0
        
        # End active tasks
        for task_name in active_task_names:
            if self.end_task(task_name, custom_time=custom_time):
                ended_count += 1
        
        # End paused tasks if requested - need to resume them first then end
        if include_paused:
            for task_name in paused_task_names:
                # Resume the paused task (this will make it active)
                if self.resume_task(task_name, custom_time=custom_time):
                    # Now end it
                    if self.end_task(task_name, custom_time=custom_time):
                        ended_count += 1
        
        if ended_count > 0:
            console.print(f"\n✅ Ended {ended_count} task(s) successfully")
            return True
        else:
            console.print("\n⚠️  Failed to end any tasks", style="yellow")
            return False
    
    @auto_save
    def pause_task(self, task_name: str, custom_time: str = None) -> bool:
        """
        Pause an active task for later resumption.
        
        Moves task from active to paused state while preserving start time
        for accurate duration calculation when resumed and completed.
        
        Args:
            task_name: Name of the task to pause
            custom_time: Optional HH:MM format time for custom pause time
            
        Returns:
            bool: True if task paused successfully, False otherwise
        """
        try:
            if task_name is None:
                raise ValueError("Task name cannot be None")
            task_name = WorkLogValidator.validate_task_name(task_name)
            timestamp = self._get_timestamp(custom_time)
            
            if task_name not in self.data.active_tasks:
                console.print(f"⚠️ '{task_name}' is not currently active", style="yellow")
                return False
            
            # Find start time
            start_time = self._find_task_start_time(task_name)
            if not start_time:
                console.print(f"⚠️ Cannot find start time for '{task_name}'", style="yellow")
                return False
            
            # Create paused task entry
            paused_task = PausedTask(task=task_name, start_time=start_time)
            
            # Update data structures
            self.data.paused_tasks.append(paused_task)
            del self.data.active_tasks[task_name]
            
            display_time = self._format_display_time(timestamp)
            console.print(f"⏸️ Paused '{task_name}' at {display_time}")
            logger.info(f"Task paused: {task_name} at {timestamp}")
            
            self._update_daily_file(task_name, "pause", timestamp)
            return True
            
        except ValueError as e:
            console.print(f"❌ Invalid input: {e}", style="red")
            return False
        except Exception as e:
            console.print(f"❌ Failed to pause task: {e}", style="red")
            logger.error(f"Error pausing task {task_name}: {e}")
            return False
    
    def _find_task_start_time(self, task_name: str) -> Optional[str]:
        """
        Find the most recent start time for an active task.
        
        Uses the active_tasks dict to get the start time directly, or falls back
        to paused task records for accurate duration calculation.
        
        Args:
            task_name: Name of the task to find start time for
            
        Returns:
            Optional[str]: ISO timestamp of task start, or None if not found
        """
        # First check active tasks dict (most direct)
        if task_name in self.data.active_tasks:
            return self.data.active_tasks[task_name]
        
        # Then check if there's a paused task record 
        paused_task = next(
            (task for task in self.data.paused_tasks if task.task == task_name), 
            None
        )
        if paused_task:
            return paused_task.start_time
        
        # Fallback: estimate from recent entries or current time
        logger.warning(f"Start time not found for {task_name}, using current session estimate")
        
        # Look for recent completed entries of the same task to estimate session length
        recent_entries = [e for e in self.data.entries[-10:] if e.task == task_name]
        if recent_entries:
            # Use typical task duration as fallback
            latest_entry = recent_entries[-1]
            if latest_entry.duration:
                # This is a simple fallback - in practice, we'd track active starts better
                return datetime.now().isoformat()
        
        # Ultimate fallback: assume task started now (will result in 0 duration)
        return self._get_current_timestamp()
    
    def resume_task(self, task_name: str, custom_time: str = None) -> bool:
        """
        Resume a previously paused task.
        
        This is a convenience method that calls start_task, which handles
        paused task resumption automatically.
        
        Args:
            task_name: Name of the task to resume
            custom_time: Optional HH:MM format time for custom resume time
            
        Returns:
            bool: True if task resumed successfully, False otherwise
        """
        return self.start_task(task_name, custom_time)
    
    # ============================================================================
    # Status and Listing Methods
    # ============================================================================
    
    @requires_data
    def show_status(self) -> None:
        """
        Display current work status including active and paused tasks.
        
        Shows a comprehensive overview of the current session state with
        active tasks, paused tasks, and recent activity summary.
        """
        if not self.data.active_tasks and not self.data.paused_tasks:
            console.print("😴 No active or paused tasks", style="dim")
            return
        
        # Show active tasks
        if self.data.active_tasks:
            console.print("🚀 Active Tasks:", style="bold green")
            for task_name, start_time in self.data.active_tasks.items():
                # Calculate runtime for active tasks
                current_duration = self._format_duration(start_time, self._get_current_timestamp())
                console.print(f"  • {task_name} (Running: {current_duration})")
        
        # Show paused tasks
        if self.data.paused_tasks:
            console.print("\n⏸️ Paused Tasks:", style="bold yellow")
            for task in self.data.paused_tasks:
                console.print(f"  • {task.task}")
        
        # Show recent activity count
        if self.data.entries:
            today = datetime.now().strftime("%Y-%m-%d")
            today_entries = [e for e in self.data.entries if e.start_time.startswith(today)]
            if today_entries:
                console.print(f"\n📊 Completed today: {len(today_entries)} tasks")
    
    @requires_data
    def list_recent_tasks(self, limit: int = None) -> None:
        """
        Display recent completed task entries with full details.
        Shows date, start time, task name, and duration for each entry.
        
        Args:
            limit: Optional limit on number of tasks to show (default: 10)
        """
        # Get completed entries only
        completed_entries = [e for e in self.data.entries if e.end_time is not None]
        
        if not completed_entries:
            console.print("📝 No completed tasks found", style="dim")
            return
        
        # Use limit or default to 10
        display_limit = limit or 10
        recent_entries = completed_entries[-display_limit:]
        
        console.print(f"📝 Recent {len(recent_entries)} Completed Tasks:", style="bold")
        console.print()
        
        # Display in reverse order (most recent first)
        for entry in reversed(recent_entries):
            display_name = "[ANONYMOUS WORK]" if entry.task == self.ANONYMOUS_TASK_NAME else entry.task
            date_part = entry.start_time[:10]  # YYYY-MM-DD
            start_time = datetime.fromisoformat(entry.start_time).strftime("%H:%M")
            
            console.print(f"  {date_part} {start_time} {display_name} ({entry.duration})")
    
    @requires_data
    def list_entries(self, date: str = None, limit: int = None, task_filter: str = None, project_filter: str = None) -> None:
        """
        List completed task entries with optional filtering.
        Shows active tasks, paused tasks, and recent activity.
        
        Args:
            date: Optional date filter (YYYY-MM-DD format)
            limit: Optional limit on number of entries to show
            task_filter: Optional task name filter (partial match)
            project_filter: Optional project name filter (partial match)
        """
        # Show active tasks status first
        if self.data.active_tasks:
            console.print("🔥 [bold green]ACTIVE TASKS:[/bold green]")
            current_time = self._get_current_timestamp()
            for task_name, start_time in self.data.active_tasks.items():
                display_name = "[ANONYMOUS WORK]" if task_name == self.ANONYMOUS_TASK_NAME else task_name
                duration = self._format_duration(start_time, current_time)
                formatted_start = self._format_display_time(start_time)
                project = self.data.active_task_projects.get(task_name)
                project_info = f" [dim]({project})[/dim]" if project else ""
                console.print(f"  • {display_name}{project_info} - Started: {formatted_start} (Running: {duration})")
        
        # Show paused tasks
        if self.data.paused_tasks:
            console.print("\n⏸️  [bold yellow]PAUSED TASKS:[/bold yellow]")
            for task in self.data.paused_tasks:
                display_name = "[ANONYMOUS WORK]" if task.task == self.ANONYMOUS_TASK_NAME else task.task
                console.print(f"  • {display_name}")
        
        # Show today's completed tasks count
        if self.data.entries:
            today = datetime.now().strftime("%Y-%m-%d")
            today_entries = [e for e in self.data.entries if e.start_time.startswith(today)]
            if today_entries:
                console.print(f"\n📊 [bold]COMPLETED TODAY:[/bold] {len(today_entries)} tasks")
        
        # If only showing status (no filters), and there are active/paused tasks, stop here
        if not date and not task_filter and not limit and (self.data.active_tasks or self.data.paused_tasks):
            # When there are active/paused tasks, don't show completed entries unless explicitly filtered
            return
        
        # No active tasks - show message and recent completed tasks
        if not self.data.active_tasks and not self.data.paused_tasks:
            console.print("ℹ️  [blue]NO ACTIVE OR PAUSED TASKS[/blue]\n")
        
        entries = self.data.entries.copy()
        
        # Apply date filter
        if date:
            try:
                WorkLogValidator.validate_date_format(date, self.config)
                entries = [e for e in entries if e.start_time.startswith(date)]
            except ValueError as e:
                console.print(f"❌ Invalid date format: {e}", style="red")
                return
        
        # Apply task name filter
        if task_filter:
            entries = [e for e in entries if task_filter.lower() in e.task.lower()]
        
        # Apply project filter
        if project_filter:
            entries = [e for e in entries if e.project and project_filter.lower() in e.project.lower()]
        
        # If no filters applied, show only last 2 recent tasks
        if not date and not task_filter and not project_filter and not limit:
            entries = entries[-2:]  # Last 2 recent tasks
        elif limit:
            entries = entries[-limit:]  # Show most recent if limited
        
        if not entries:
            filters = []
            if date: filters.append(f"date={date}")
            if task_filter: filters.append(f"task={task_filter}")
            if project_filter: filters.append(f"project={project_filter}")
            filter_desc = f" (filtered: {', '.join(filters)})" if filters else ""
            console.print(f"📋 No completed tasks found{filter_desc}", style="dim")
            return
        
        # Display entries
        console.print(f"📋 Last {len(entries)} Completed Tasks:", style="bold")
        
        for entry in entries:
            display_name = "[ANONYMOUS WORK]" if entry.task == self.ANONYMOUS_TASK_NAME else entry.task
            start_display = self._format_display_time(entry.start_time)
            end_display = self._format_display_time(entry.end_time)
            project_info = f" [dim]({entry.project})[/dim]" if entry.project else ""
            console.print(
                f"  • {display_name}{project_info}\n"
                f"    {start_display} → {end_display} ({entry.duration})"
            )
    
    @requires_data
    def show_daily_summary(self, date: str = None) -> None:
        """
        Show summary of work done on a specific day.
        
        Args:
            date: Optional date (YYYY-MM-DD), defaults to today
        """
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        
        # Validate date format
        try:
            WorkLogValidator.validate_date_format(target_date, self.config)
        except ValueError as e:
            console.print(f"❌ Invalid date format: {e}", style="red")
            return
        
        # Filter entries for the date
        day_entries = [e for e in self.data.entries if e.start_time.startswith(target_date)]
        
        if not day_entries:
            console.print(f"📅 No tasks completed on {target_date}", style="dim")
            return
        
        # Calculate total time
        total_seconds = 0
        for entry in day_entries:
            start_dt = datetime.fromisoformat(entry.start_time)
            end_dt = datetime.fromisoformat(entry.end_time)
            total_seconds += (end_dt - start_dt).total_seconds()
        
        total_hours = total_seconds // 3600
        total_minutes = (total_seconds % 3600) // 60
        
        # Display summary
        console.print(f"📅 Daily Summary for {target_date}", style="bold")
        console.print(f"📊 Total: {len(day_entries)} tasks, {total_hours:.0f}h {total_minutes:.0f}m")
        
        # Group by task name
        task_durations = {}
        for entry in day_entries:
            if entry.task not in task_durations:
                task_durations[entry.task] = 0
            
            start_dt = datetime.fromisoformat(entry.start_time)
            end_dt = datetime.fromisoformat(entry.end_time)
            task_durations[entry.task] += (end_dt - start_dt).total_seconds()
        
        # Display task breakdown
        console.print("\n📋 Tasks:")
        for task_name, seconds in sorted(task_durations.items(), key=lambda x: x[1], reverse=True):
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            console.print(f"  • {task_name}: {hours:.0f}h {minutes:.0f}m")
    
    @requires_data
    @auto_save
    def clean_by_date(self, date: str) -> bool:
        """
        Clean/erase all entries for a specific date.
        
        Args:
            date: Date to clean (YYYY-MM-DD format)
            
        Returns:
            bool: True if entries were removed, False otherwise
        """
        # Validate date format
        try:
            WorkLogValidator.validate_date_format(date, self.config)
        except ValueError as e:
            console.print(f"❌ Invalid date format: {e}", style="red")
            return False
        
        # Find entries for the date
        entries_to_remove = [e for e in self.data.entries if e.start_time.startswith(date)]
        
        if not entries_to_remove:
            console.print(f"ℹ️  No entries found for {date}", style="dim")
            return False
        
        # Create backup before cleaning
        from ..managers.backup import BackupManager
        daily_file = self.worklog_dir / f"{date}.txt"
        BackupManager.create_backup(
            self.worklog_dir,
            f"clean_{date}",
            entries_to_remove,
            daily_file if daily_file.exists() else None,
            self.config
        )
        
        # Remove entries from data
        self.data.entries = [e for e in self.data.entries if not e.start_time.startswith(date)]
        
        # Remove daily file if exists
        if daily_file.exists():
            daily_file.unlink()
        
        console.print(f"✅ Cleaned {len(entries_to_remove)} entries for {date}", style="green")
        console.print("💾 Backup created for safety", style="dim")
        return True
    
    @requires_data
    @auto_save
    def clean_by_task(self, task_name: str, date: Optional[str] = None) -> bool:
        """
        Clean/erase entries for a specific task, optionally filtered by date.
        
        Args:
            task_name: Name of the task to clean
            date: Optional date filter (YYYY-MM-DD format)
            
        Returns:
            bool: True if entries were removed, False otherwise
        """
        # Validate date if provided
        if date:
            try:
                WorkLogValidator.validate_date_format(date, self.config)
            except ValueError as e:
                console.print(f"❌ Invalid date format: {e}", style="red")
                return False
        
        # Find entries to remove
        if date:
            entries_to_remove = [e for e in self.data.entries 
                               if e.task == task_name and e.start_time.startswith(date)]
        else:
            entries_to_remove = [e for e in self.data.entries if e.task == task_name]
        
        if not entries_to_remove:
            filter_msg = f" on {date}" if date else ""
            console.print(f"ℹ️  No entries found for task '{task_name}'{filter_msg}", style="dim")
            return False
        
        # Create backup before cleaning
        from ..managers.backup import BackupManager
        backup_date = date or "all_dates"
        BackupManager.create_backup(
            self.worklog_dir,
            f"clean_{backup_date}_{task_name.replace(' ', '_')}",
            entries_to_remove,
            None,
            self.config
        )
        
        # Remove entries from data
        if date:
            self.data.entries = [e for e in self.data.entries 
                               if not (e.task == task_name and e.start_time.startswith(date))]
        else:
            self.data.entries = [e for e in self.data.entries if e.task != task_name]
        
        # Rebuild affected daily files
        affected_dates = set(e.start_time[:10] for e in entries_to_remove)
        for affected_date in affected_dates:
            daily_file = self.worklog_dir / f"{affected_date}.txt"
            # Get remaining entries for this date
            remaining_entries = [e for e in self.data.entries if e.start_time.startswith(affected_date)]
            
            if remaining_entries:
                # Rebuild daily file with remaining entries
                daily_file.write_text("")  # Clear file
                for entry in remaining_entries:
                    # Determine action based on entry state
                    if entry.end_time and entry.duration:
                        # Completed entry
                        formatted_entry = self.daily_file_manager.format_entry(
                            entry.task,
                            'completed',
                            entry.end_time,
                            entry.duration
                        )
                    else:
                        # Active entry (shouldn't happen in clean context, but handle it)
                        formatted_entry = self.daily_file_manager.format_entry(
                            entry.task,
                            'start',
                            entry.start_time
                        )
                    self.daily_file_manager.add_entry_chronologically(daily_file, formatted_entry)
            elif daily_file.exists():
                # No entries left for this date, remove daily file
                daily_file.unlink()
        
        filter_msg = f" on {date}" if date else ""
        console.print(f"✅ Cleaned {len(entries_to_remove)} entries for task '{task_name}'{filter_msg}", style="green")
        console.print("💾 Backup created for safety", style="dim")
        return True
    
    @requires_data
    @auto_save
    def clean_all(self) -> bool:
        """
        Clean all worklog entries and daily files.
        
        Returns:
            bool: True if entries were removed, False otherwise
        """
        if not self.data.entries:
            console.print("ℹ️  No entries to clean", style="dim")
            return False
        
        # Create comprehensive backup of all entries
        from ..managers.backup import BackupManager
        BackupManager.create_backup(
            self.worklog_dir,
            "all_entries",
            self.data.entries,
            None,
            self.config
        )
        
        # Count entries
        entry_count = len(self.data.entries)
        
        # Clear all data
        self.data.entries = []
        self.data.active_tasks = {}
        self.data.paused_tasks = []
        
        # Remove all daily files
        daily_files = list(self.worklog_dir.glob("*.txt"))
        removed_files = 0
        for daily_file in daily_files:
            if daily_file.name != "worklog.log":  # Don't remove log file
                daily_file.unlink()
                removed_files += 1
        
        console.print(f"✅ Cleaned {entry_count} entries and {removed_files} daily files", style="green")
        console.print("💾 Backup created for safety", style="dim")
        return True