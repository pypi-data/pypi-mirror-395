"""
Backup management for WorkLog CLI Tool.

This module provides centralized backup functionality for safe
data operations and recovery.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import logging

from ..models import TaskEntry
from ..config import WorkLogConfig

logger = logging.getLogger(__name__)


class BackupManager:
    """
    Centralized backup creation and management for WorkLog data.
    
    Handles creation of comprehensive backups before destructive operations,
    ensuring data safety with consistent backup format and error handling.
    """
    
    @staticmethod
    def create_backup(
        backup_dir: Path,
        date_str: str,
        entries: List[TaskEntry],
        daily_file: Optional[Path] = None,
        config: Optional[WorkLogConfig] = None
    ) -> Path:
        """
        Create a comprehensive backup file for a specific date.
        
        Args:
            backup_dir: Directory to store the backup
            date_str: Date string for backup naming
            entries: List of TaskEntry objects to backup
            daily_file: Optional daily file path to include in backup
            config: Optional configuration for formatting
            
        Returns:
            Path: Path to the created backup file
            
        Raises:
            IOError: If backup creation fails
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"{date_str}_backup_{timestamp}.txt"
        
        try:
            backup_content = []
            
            # Add header
            backup_content.extend([
                f"=== WorkLog Backup - {date_str} ===",
                f"Created: {datetime.now().isoformat()}",
                f"Entries: {len(entries)}",
                ""
            ])
            
            # Add JSON entries to backup
            if entries:
                backup_content.extend([
                    "=== JSON Entries ===",
                    ""
                ])
                for entry in entries:
                    if entry.end_time and entry.duration:
                        backup_content.append(
                            f"{entry.start_time} - {entry.end_time} {entry.task} ({entry.duration})"
                        )
                    else:
                        backup_content.append(f"{entry.start_time} - ACTIVE {entry.task}")
                backup_content.append("")
            
            # Add daily file content to backup
            if daily_file and daily_file.exists():
                backup_content.extend([
                    "=== Daily File Content ===",
                    ""
                ])
                try:
                    with open(daily_file, 'r', encoding='utf-8') as f:
                        backup_content.extend(line.rstrip() for line in f)
                except Exception as e:
                    backup_content.append(f"Error reading daily file: {e}")
            
            # Write backup file
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(backup_content))
            
            logger.info(f"Backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise IOError(f"Backup creation failed: {e}")
    
    @staticmethod
    def create_backup_from_data(
        backup_type: str,
        data: Dict[str, Any],
        backup_dir: Path,
        suffix: str = ""
    ) -> Path:
        """
        Create backup from arbitrary data dictionary.
        
        Args:
            backup_type: Type of backup (e.g., 'clean', 'migration')
            data: Data dictionary to backup
            backup_dir: Directory to store backup
            suffix: Optional suffix for backup filename
            
        Returns:
            Path: Path to created backup file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{backup_type}_{timestamp}"
        if suffix:
            backup_name += f"_{suffix}"
        backup_file = backup_dir / f"{backup_name}.json"
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Data backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Failed to create data backup: {e}")
            raise IOError(f"Data backup creation failed: {e}")