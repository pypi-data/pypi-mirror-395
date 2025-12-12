"""
Tests for Google Sheets sync functionality.

This module contains unit tests for:
- Hours formatting and rounding functions
- GoogleSheetsSync class methods
- Sync command integration
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

from src.worklog.sync.sheets import (
    round_hours,
    format_hours,
    GoogleSheetsSync
)
from src.worklog.config import WorkLogConfig, GoogleSheetsConfig
from src.worklog.models import TaskEntry


class TestHoursFormatting:
    """Test hours rounding and formatting functions."""
    
    def test_round_hours_quarter(self):
        """Test rounding to nearest 0.25 (15 minutes)."""
        assert round_hours(2.2, 0.25) == 2.25  # 2h 12m → 2h 15m
        assert round_hours(2.1, 0.25) == 2.0   # 2h 6m → 2h 0m
        assert round_hours(2.13, 0.25) == 2.25 # 2h 8m → 2h 15m
        assert round_hours(2.37, 0.25) == 2.25 # 2h 22m → 2h 15m
        assert round_hours(2.38, 0.25) == 2.5  # 2h 23m → 2h 30m
    
    def test_round_hours_half(self):
        """Test rounding to nearest 0.5 (30 minutes)."""
        assert round_hours(2.2, 0.5) == 2.0   # 2h 12m → 2h 0m
        assert round_hours(2.3, 0.5) == 2.5   # 2h 18m → 2h 30m
        assert round_hours(2.6, 0.5) == 2.5   # 2h 36m → 2h 30m
        assert round_hours(2.8, 0.5) == 3.0   # 2h 48m → 3h 0m
    
    def test_round_hours_full(self):
        """Test rounding to nearest 1.0 (full hour)."""
        assert round_hours(2.2, 1.0) == 2.0   # 2h 12m → 2h 0m
        assert round_hours(2.4, 1.0) == 2.0   # 2h 24m → 2h 0m
        assert round_hours(2.5, 1.0) == 2.0   # 2h 30m → 2h 0m (banker's rounding)
        assert round_hours(2.6, 1.0) == 3.0   # 2h 36m → 3h 0m
    
    def test_format_hours_quarter_increment(self):
        """Test formatting with 0.25 increment (2 decimal places)."""
        assert format_hours(2.2, 0.25) == "2,25"
        assert format_hours(1.5, 0.25) == "1,50"
        assert format_hours(0.75, 0.25) == "0,75"
    
    def test_format_hours_half_increment(self):
        """Test formatting with 0.5 increment (1 decimal place)."""
        assert format_hours(2.6, 0.5) == "2,5"
        assert format_hours(3.0, 0.5) == "3,0"
        assert format_hours(1.2, 0.5) == "1,0"
    
    def test_format_hours_full_increment(self):
        """Test formatting with 1.0 increment (0 decimal places)."""
        assert format_hours(2.4, 1.0) == "2"
        assert format_hours(3.6, 1.0) == "4"
        assert format_hours(1.0, 1.0) == "1"
    
    def test_format_hours_european_separator(self):
        """Test that comma is used as decimal separator (European format)."""
        result = format_hours(2.5, 0.5)
        assert "," in result
        assert "." not in result


class TestGoogleSheetsSyncMethods:
    """Test GoogleSheetsSync class methods."""
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration for testing."""
        config = WorkLogConfig()
        config.google_sheets = GoogleSheetsConfig(
            enabled=True,
            auto_sync=False,
            round_hours=0.5,
            use_haunts_format=False  # Disable haunts for unit tests
        )
        config.sheet_document_id = "test-sheet-id-123"
        return config
    
    @pytest.fixture
    def sample_task(self):
        """Create a sample completed task entry."""
        return TaskEntry(
            task="Test Task",
            start_time="2025-10-05T09:00:00",
            end_time="2025-10-05T11:30:00",
            duration="02:30:00",
            project="TestProject"
        )
    
    def test_calculate_hours(self, mock_config, sample_task):
        """Test hours calculation from ISO timestamps."""
        with patch('src.worklog.sync.sheets.Credentials'):
            sync = GoogleSheetsSync(mock_config)
            hours = sync._calculate_hours(sample_task)
            assert hours == 2.5  # 2 hours 30 minutes
    
    def test_calculate_hours_no_end_time(self, mock_config):
        """Test hours calculation with no end time."""
        task = TaskEntry(
            task="Active Task",
            start_time="2025-10-05T09:00:00",
            end_time=None
        )
        with patch('src.worklog.sync.sheets.Credentials'):
            sync = GoogleSheetsSync(mock_config)
            hours = sync._calculate_hours(task)
            assert hours == 0.0
    
    def test_format_date(self, mock_config, sample_task):
        """Test date formatting to DD/MM/YYYY."""
        with patch('src.worklog.sync.sheets.Credentials'):
            sync = GoogleSheetsSync(mock_config)
            formatted = sync._format_date(sample_task.end_time)
            assert formatted == "05/10/2025"
    
    def test_format_time(self, mock_config, sample_task):
        """Test time formatting to HH:MM."""
        with patch('src.worklog.sync.sheets.Credentials'):
            sync = GoogleSheetsSync(mock_config)
            formatted = sync._format_time(sample_task.start_time)
            assert formatted == "09:00"
    
    def test_sync_task_raises_without_end_time(self, mock_config):
        """Test that sync_task raises ValueError for incomplete tasks."""
        task = TaskEntry(
            task="Active Task",
            start_time="2025-10-05T09:00:00",
            end_time=None
        )
        with patch('src.worklog.sync.sheets.Credentials'):
            sync = GoogleSheetsSync(mock_config)
            with pytest.raises(ValueError, match="Cannot sync task without end_time"):
                sync.sync_task(task)
    
    def test_sync_tasks_filters_incomplete(self, mock_config):
        """Test that sync_tasks skips tasks without end_time."""
        tasks = [
            TaskEntry("Task 1", "2025-10-05T09:00:00", "2025-10-05T10:00:00", "01:00:00"),
            TaskEntry("Task 2", "2025-10-05T11:00:00", None),  # Incomplete
            TaskEntry("Task 3", "2025-10-05T13:00:00", "2025-10-05T14:00:00", "01:00:00"),
        ]
        
        with patch('src.worklog.sync.sheets.Credentials'):
            sync = GoogleSheetsSync(mock_config)
            with patch.object(sync, 'sync_task'):
                count = sync.sync_tasks(tasks)
                # Should sync only the 2 completed tasks
                assert count == 2


class TestSyncConvenienceMethods:
    """Test convenience methods for daily, monthly, date, and all sync."""
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration."""
        config = WorkLogConfig()
        config.google_sheets = GoogleSheetsConfig(
            enabled=True,
            auto_sync=False,
            round_hours=0.5,
            use_haunts_format=False  # Disable haunts for unit tests
        )
        config.sheet_document_id = "test-sheet-id"
        return config
    
    @pytest.fixture
    def mock_worklog_data(self):
        """Create mock worklog data with various task dates."""
        from src.worklog.models import WorkLogData
        
        data = WorkLogData()
        data.entries = [
            TaskEntry("Today Task 1", "2025-10-05T09:00:00", "2025-10-05T10:00:00", "01:00:00"),
            TaskEntry("Today Task 2", "2025-10-05T11:00:00", "2025-10-05T12:00:00", "01:00:00"),
            TaskEntry("Yesterday Task", "2025-10-04T09:00:00", "2025-10-04T10:00:00", "01:00:00"),
            TaskEntry("Last Month Task", "2025-09-15T09:00:00", "2025-09-15T10:00:00", "01:00:00"),
            TaskEntry("Active Task", "2025-10-05T14:00:00", None),  # No end_time
        ]
        return data
    
    @patch('src.worklog.sync.sheets.datetime')
    @patch('src.worklog.sync.sheets.Credentials')
    @patch('src.worklog.managers.worklog.WorkLog')
    def test_sync_daily_dry_run(self, mock_worklog_class, mock_creds, mock_datetime, mock_config, mock_worklog_data):
        """Test sync_daily in dry-run mode."""
        # Mock current date
        mock_now = datetime(2025, 10, 5, 15, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        # Mock WorkLog instance
        mock_worklog = Mock()
        mock_worklog.data = mock_worklog_data
        mock_worklog_class.return_value = mock_worklog
        
        sync = GoogleSheetsSync(mock_config)
        result = sync.sync_daily(dry_run=True)
        
        # Should count only today's completed tasks (2)
        assert result['count'] == 2
        assert 'October' in result['sheets_updated'][0]
    
    @patch('src.worklog.sync.sheets.datetime')
    @patch('src.worklog.sync.sheets.Credentials')
    @patch('src.worklog.managers.worklog.WorkLog')
    def test_sync_monthly_dry_run(self, mock_worklog_class, mock_creds, mock_datetime, mock_config, mock_worklog_data):
        """Test sync_monthly in dry-run mode."""
        # Mock current date
        mock_now = datetime(2025, 10, 5, 15, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        # Mock WorkLog instance
        mock_worklog = Mock()
        mock_worklog.data = mock_worklog_data
        mock_worklog_class.return_value = mock_worklog
        
        sync = GoogleSheetsSync(mock_config)
        result = sync.sync_monthly(dry_run=True)
        
        # Should count only current month's completed tasks (3: 2 today + 1 yesterday)
        assert result['count'] == 3
        assert result['sheets_updated'] == ['October']
    
    @patch('src.worklog.sync.sheets.Credentials')
    @patch('src.worklog.managers.worklog.WorkLog')
    def test_sync_date_dry_run(self, mock_worklog_class, mock_creds, mock_config, mock_worklog_data):
        """Test sync_date in dry-run mode."""
        # Mock WorkLog instance
        mock_worklog = Mock()
        mock_worklog.data = mock_worklog_data
        mock_worklog_class.return_value = mock_worklog
        
        sync = GoogleSheetsSync(mock_config)
        result = sync.sync_date("2025-10-04", dry_run=True)
        
        # Should count only tasks from 2025-10-04 (1)
        assert result['count'] == 1
        assert 'October' in result['sheets_updated'][0]
    
    @patch('src.worklog.sync.sheets.Credentials')
    @patch('src.worklog.managers.worklog.WorkLog')
    def test_sync_all_dry_run(self, mock_worklog_class, mock_creds, mock_config, mock_worklog_data):
        """Test sync_all in dry-run mode."""
        # Mock WorkLog instance
        mock_worklog = Mock()
        mock_worklog.data = mock_worklog_data
        mock_worklog_class.return_value = mock_worklog
        
        sync = GoogleSheetsSync(mock_config)
        result = sync.sync_all(dry_run=True)
        
        # Should count all completed tasks (4: active task excluded)
        assert result['count'] == 4
        # Should have sheets for both months (alphabetically sorted)
        assert result['sheets_updated'] == ['October', 'September']
    
    @patch('src.worklog.sync.sheets.Credentials')
    def test_sync_date_invalid_format(self, mock_creds, mock_config):
        """Test that sync_date raises ValueError for invalid date format."""
        sync = GoogleSheetsSync(mock_config)
        
        with pytest.raises(ValueError, match="Invalid date format"):
            sync.sync_date("2025/10/05", dry_run=True)
        
        with pytest.raises(ValueError, match="Invalid date format"):
            sync.sync_date("10-05-2025", dry_run=True)


class TestConfigurationValidation:
    """Test configuration validation in sync operations."""
    
    def test_disabled_sync_configuration(self):
        """Test that GoogleSheetsSync raises error when sync is disabled."""
        config = WorkLogConfig()
        config.google_sheets.enabled = False
        
        # Should raise ValueError when trying to create instance with disabled sync
        with patch('src.worklog.sync.sheets.Credentials'):
            with pytest.raises(ValueError, match="Google Sheets sync is not enabled"):
                sync = GoogleSheetsSync(config)
    
    def test_missing_document_id(self):
        """Test behavior when sheet_document_id is missing."""
        config = WorkLogConfig()
        config.google_sheets.enabled = True
        config.google_sheets.use_haunts_format = False  # Disable haunts for unit test
        config.sheet_document_id = ""
        
        with patch('src.worklog.sync.sheets.Credentials'):
            sync = GoogleSheetsSync(config)
            assert sync.config.sheet_document_id == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
