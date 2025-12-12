"""
Data models for WorkLog CLI Tool.

This module contains all dataclass definitions used throughout the worklog system:
- TaskEntry: Individual task tracking records
- PausedTask: Paused task state management  
- WorkLogData: Complete worklog state container
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class TaskEntry:
    """
    Data class representing a single work task entry.
    
    Tracks complete task lifecycle from start to completion with precise
    timing information. Supports both active tasks (no end_time) and
    completed tasks (with duration calculations). Includes optional project
    categorization for better organization and haunts integration.
    
    Attributes:
        task: Task name or description
        start_time: ISO timestamp when task began
        end_time: ISO timestamp when task ended (None for active tasks)
        duration: Formatted duration string (HH:MM:SS format)
        project: Optional project/category name for task organization
    """
    task: str
    start_time: str  # ISO timestamp string for JSON compatibility
    end_time: Optional[str] = None
    duration: Optional[str] = None
    project: Optional[str] = None


@dataclass 
class PausedTask:
    """
    Data class representing a paused task with start time tracking.
    
    Stores the task name and original start time so that duration
    can be accurately calculated when the task is resumed and completed.
    
    Attributes:
        task: Task name or identifier
        start_time: ISO timestamp when task was originally started
    """
    task: str
    start_time: str


@dataclass
class WorkLogData:
    """
    Container for all worklog application state and data.
    
    Serves as the primary data structure for the worklog application,
    containing all task entries, active sessions, paused tasks, and
    recent task history. Designed for JSON serialization compatibility.
    
    Attributes:
        entries: List of all completed and active task entries
        active_tasks: Dict mapping task names to their start timestamps
        paused_tasks: List of currently paused tasks with accumulated time
        recent_tasks: List of recently used task names for quick access
        active_task_projects: Dict mapping task names to their project assignments
    """
    entries: List[TaskEntry] = field(default_factory=list)
    active_tasks: Dict[str, str] = field(default_factory=dict)  # task_name -> start_time
    paused_tasks: List[PausedTask] = field(default_factory=list)
    recent_tasks: List[str] = field(default_factory=list)
    active_task_projects: Dict[str, str] = field(default_factory=dict)  # task_name -> project