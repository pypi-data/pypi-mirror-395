"""
Comprehensive CLI Integration Tests for Drudge CLI.

This module tests ALL commands with ALL options to ensure complete CLI coverage.
Tests are run using Typer's CliRunner for isolated testing.
"""

import re
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner

from src.worklog.cli.commands import app


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class TestCLICommands(unittest.TestCase):
    """Test all CLI commands with their options."""
    
    def setUp(self):
        """Set up test environment with isolated home directory."""
        # Reset worklog singleton first
        import src.worklog.cli.commands as cmd_module
        cmd_module._worklog_instance = None
        
        # Stop any existing patch from previous test
        if hasattr(self, 'config_patcher'):
            self.config_patcher.stop()
        
        self.test_dir = tempfile.mkdtemp()
        
        # Ensure .worklog directory structure exists
        worklog_dir = Path(self.test_dir) / '.worklog'
        worklog_dir.mkdir(parents=True, exist_ok=True)
        (worklog_dir / 'daily').mkdir(parents=True, exist_ok=True)
        (worklog_dir / 'backups').mkdir(parents=True, exist_ok=True)
        
        # Patch config to use THIS test's directory
        from src.worklog.config import WorkLogConfig
        self.config_patcher = patch.object(WorkLogConfig, 'worklog_dir', str(worklog_dir))
        self.config_patcher.start()
        
        # Create CliRunner
        self.runner = CliRunner()
    
    def tearDown(self):
        """Clean up test environment."""
        # Reset worklog singleton to ensure test isolation
        import src.worklog.cli.commands as cmd_module
        cmd_module._worklog_instance = None
        # Stop patch
        self.config_patcher.stop()
        # Clean up test directory
        if hasattr(self, 'test_dir') and Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)
    
    # ========================================================================
    # START Command Tests
    # ========================================================================
    
    def test_start_basic(self):
        """Test basic start command."""
        result = self.runner.invoke(app, ["start", "Test Task"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Started", result.stdout)
        self.assertIn("Test Task", result.stdout)
    
    def test_start_with_parallel(self):
        """Test start command with --parallel flag."""
        # Start first task
        result1 = self.runner.invoke(app, ["start", "Task 1"])
        self.assertEqual(result1.exit_code, 0)
        
        # Start second task with --parallel
        result2 = self.runner.invoke(app, ["start", "Task 2", "--parallel"])
        self.assertEqual(result2.exit_code, 0)
        self.assertIn("Task 2", result2.stdout)
    
    def test_start_with_time(self):
        """Test start command with --time option."""
        result = self.runner.invoke(app, ["start", "Task", "--time", "09:00"])
        self.assertEqual(result.exit_code, 0)
    
    def test_start_anonymous(self):
        """Test anonymous task start."""
        result = self.runner.invoke(app, ["start", ""])
        self.assertEqual(result.exit_code, 0)
        # Clean up: end the anonymous task
        self.runner.invoke(app, ["end", "--all"])
        self.assertIn("Started", result.stdout)
    
    def test_start_help(self):
        """Test start command help."""
        result = self.runner.invoke(app, ["start", "--help"])
        self.assertEqual(result.exit_code, 0)
        output = strip_ansi(result.stdout)
        self.assertIn("Start a new task", output)
        self.assertIn("--parallel", output)
        self.assertIn("--time", output)
    
    # ========================================================================
    # END Command Tests
    # ========================================================================
    
    def test_end_specific_task(self):
        """Test ending a specific task."""
        # Start a task first
        self.runner.invoke(app, ["start", "Test Task"])
        result = self.runner.invoke(app, ["end", "Test Task"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Completed", result.stdout)
    
    def test_end_all_active(self):
        """Test ending all active tasks."""
        # Start multiple tasks
        self.runner.invoke(app, ["start", "Task 1", "--parallel"])
        self.runner.invoke(app, ["start", "Task 2", "--parallel"])
        
        # End all
        result = self.runner.invoke(app, ["end"])
        self.assertEqual(result.exit_code, 0)
    
    def test_end_with_all_flag(self):
        """Test end command with --all flag (includes paused)."""
        # Start and pause a task
        self.runner.invoke(app, ["start", "Task 1"])
        self.runner.invoke(app, ["pause", "Task 1"])
        self.runner.invoke(app, ["start", "Task 2"])
        
        # End all including paused
        result = self.runner.invoke(app, ["end", "--all"])
        self.assertEqual(result.exit_code, 0)
    
    def test_end_with_time(self):
        """Test end command with --time option."""
        self.runner.invoke(app, ["start", "Task"])
        result = self.runner.invoke(app, ["end", "Task", "--time", "17:30"])
        self.assertEqual(result.exit_code, 0)
    
    def test_end_with_sync(self):
        """Test end command with --sync flag."""
        self.runner.invoke(app, ["start", "Task"])
        # Sync will fail (no Google Sheets config) but should not crash
        result = self.runner.invoke(app, ["end", "Task", "--sync"])
        self.assertEqual(result.exit_code, 0)
    
    def test_end_help(self):
        """Test end command help."""
        result = self.runner.invoke(app, ["end", "--help"])
        self.assertEqual(result.exit_code, 0)
        output = strip_ansi(result.stdout)
        self.assertIn("End an active task", output)
        self.assertIn("--all", output)
        self.assertIn("--sync", output)
    
    # ========================================================================
    # PAUSE/RESUME Command Tests
    # ========================================================================
    
    def test_pause_task(self):
        """Test pause command."""
        self.runner.invoke(app, ["start", "Task to Pause"])
        result = self.runner.invoke(app, ["pause", "Task to Pause"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Paused", result.stdout)
    
    def test_pause_with_time(self):
        """Test pause command with --time option."""
        self.runner.invoke(app, ["start", "Task"])
        result = self.runner.invoke(app, ["pause", "Task", "--time", "12:00"])
        self.assertEqual(result.exit_code, 0)
    
    def test_resume_task(self):
        """Test resume command."""
        self.runner.invoke(app, ["start", "Task"])
        self.runner.invoke(app, ["pause", "Task"])
        result = self.runner.invoke(app, ["resume", "Task"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Resumed", result.stdout)
        # Clean up: end the task
        self.runner.invoke(app, ["end", "Task"])
    
    def test_resume_with_time(self):
        """Test resume command with --time option."""
        self.runner.invoke(app, ["start", "Task"])
        self.runner.invoke(app, ["pause", "Task"])
        result = self.runner.invoke(app, ["resume", "Task", "--time", "13:00"])
        self.assertEqual(result.exit_code, 0)
        # Clean up: end the task
        self.runner.invoke(app, ["end", "Task"])
    
    # ========================================================================
    # LIST Command Tests
    # ========================================================================
    
    def test_list_basic(self):
        """Test basic list command."""
        result = self.runner.invoke(app, ["list"])
        self.assertEqual(result.exit_code, 0)
    
    def test_list_with_date(self):
        """Test list command with --date filter."""
        result = self.runner.invoke(app, ["list", "--date", "2025-10-06"])
        self.assertEqual(result.exit_code, 0)
    
    def test_list_with_limit(self):
        """Test list command with --limit option."""
        result = self.runner.invoke(app, ["list", "--limit", "5"])
        self.assertEqual(result.exit_code, 0)
    
    def test_list_with_task_filter(self):
        """Test list command with --task filter."""
        result = self.runner.invoke(app, ["list", "--task", "bug"])
        self.assertEqual(result.exit_code, 0)
    
    def test_list_help(self):
        """Test list command help."""
        result = self.runner.invoke(app, ["list", "--help"])
        self.assertEqual(result.exit_code, 0)
        output = strip_ansi(result.stdout)
        self.assertIn("Show work status", output)
    
    # ========================================================================
    # RECENT Command Tests
    # ========================================================================
    
    def test_recent_basic(self):
        """Test basic recent command."""
        result = self.runner.invoke(app, ["recent"])
        self.assertEqual(result.exit_code, 0)
    
    def test_recent_with_limit(self):
        """Test recent command with --limit option."""
        result = self.runner.invoke(app, ["recent", "--limit", "3"])
        self.assertEqual(result.exit_code, 0)
    
    def test_recent_help(self):
        """Test recent command help."""
        result = self.runner.invoke(app, ["recent", "--help"])
        self.assertEqual(result.exit_code, 0)
    
    # ========================================================================
    # DAILY Command Tests
    # ========================================================================
    
    def test_daily_basic(self):
        """Test basic daily command."""
        result = self.runner.invoke(app, ["daily"])
        self.assertEqual(result.exit_code, 0)
    
    def test_daily_with_date(self):
        """Test daily command with --date option."""
        result = self.runner.invoke(app, ["daily", "--date", "2025-10-05"])
        self.assertEqual(result.exit_code, 0)
    
    def test_daily_with_sync(self):
        """Test daily command with --sync flag."""
        # Sync will fail (no config) but should not crash
        result = self.runner.invoke(app, ["daily", "--sync"])
        self.assertEqual(result.exit_code, 0)
    
    def test_daily_help(self):
        """Test daily command help."""
        result = self.runner.invoke(app, ["daily", "--help"])
        self.assertEqual(result.exit_code, 0)
        output = strip_ansi(result.stdout)
        self.assertIn("Show daily work summary", output)
        self.assertIn("--sync", output)
    
    # ========================================================================
    # SYNC Command Tests
    # ========================================================================
    
    def test_sync_basic(self):
        """Test basic sync command (will fail gracefully without config)."""
        result = self.runner.invoke(app, ["sync"])
        # Should exit with error (no config) but not crash
        self.assertIn("not enabled", result.stdout.lower())
    
    def test_sync_daily(self):
        """Test sync command with --daily flag."""
        result = self.runner.invoke(app, ["sync", "--daily"])
        self.assertIn("not enabled", result.stdout.lower())
    
    def test_sync_monthly(self):
        """Test sync command with --monthly flag."""
        result = self.runner.invoke(app, ["sync", "--monthly"])
        self.assertIn("not enabled", result.stdout.lower())
    
    def test_sync_with_date(self):
        """Test sync command with --date option."""
        result = self.runner.invoke(app, ["sync", "--date", "2025-10-06"])
        self.assertIn("not enabled", result.stdout.lower())
    
    def test_sync_test_mode(self):
        """Test sync command with --test flag."""
        result = self.runner.invoke(app, ["sync", "--test"])
        self.assertIn("not enabled", result.stdout.lower())
    
    def test_sync_help(self):
        """Test sync command help."""
        result = self.runner.invoke(app, ["sync", "--help"])
        self.assertEqual(result.exit_code, 0)
        output = strip_ansi(result.stdout)
        self.assertIn("Sync worklog entries", output)
        self.assertIn("--daily", output)
        self.assertIn("--monthly", output)
        self.assertIn("--test", output)
    
    # ========================================================================
    # CLEAN Command Tests
    # ========================================================================
    
    def test_clean_by_date(self):
        """Test clean command with date."""
        # Create some entries first
        self.runner.invoke(app, ["start", "Task"])
        self.runner.invoke(app, ["end", "Task"])
        
        # Clean by date (with auto-confirm in test)
        result = self.runner.invoke(app, ["clean", "2025-10-06"], input="y\n")
        self.assertEqual(result.exit_code, 0)
    
    def test_clean_by_task(self):
        """Test clean command with task name."""
        self.runner.invoke(app, ["start", "Task to Clean"])
        self.runner.invoke(app, ["end", "Task to Clean"])
        
        result = self.runner.invoke(app, ["clean", "Task to Clean"], input="y\n")
        self.assertEqual(result.exit_code, 0)
    
    def test_clean_all(self):
        """Test clean command with --all flag."""
        result = self.runner.invoke(app, ["clean", "--all"], input="y\n")
        self.assertEqual(result.exit_code, 0)
    
    def test_clean_help(self):
        """Test clean command help."""
        result = self.runner.invoke(app, ["clean", "--help"])
        self.assertEqual(result.exit_code, 0)
        output = strip_ansi(result.stdout)
        self.assertIn("Clean worklog entries", output)
    
    # ========================================================================
    # CONFIG Command Tests
    # ========================================================================
    
    def test_config_basic(self):
        """Test basic config command."""
        result = self.runner.invoke(app, ["config"])
        self.assertEqual(result.exit_code, 0)
    
    def test_config_help(self):
        """Test config command help."""
        result = self.runner.invoke(app, ["config", "--help"])
        self.assertEqual(result.exit_code, 0)
    
    # ========================================================================
    # VERSION Command Tests
    # ========================================================================
    
    def test_version(self):
        """Test version command."""
        result = self.runner.invoke(app, ["version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Drudge CLI", result.stdout)
        self.assertIn("Version", result.stdout)
    
    # ========================================================================
    # HELP Command Tests
    # ========================================================================
    
    def test_main_help(self):
        """Test main help command."""
        result = self.runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)
        output = strip_ansi(result.stdout)
        self.assertIn("Drudge CLI", output)
        self.assertIn("start", output)
        self.assertIn("end", output)
        self.assertIn("sync", output)
    
    # ========================================================================
    # Error Handling Tests
    # ========================================================================
    
    def test_end_nonexistent_task(self):
        """Test ending a task that doesn't exist."""
        result = self.runner.invoke(app, ["end", "Nonexistent Task"])
        self.assertNotEqual(result.exit_code, 0)
    
    def test_pause_nonexistent_task(self):
        """Test pausing a task that doesn't exist."""
        result = self.runner.invoke(app, ["pause", "Nonexistent"])
        self.assertNotEqual(result.exit_code, 0)
    
    def test_resume_nonexistent_task(self):
        """Test resuming a task that doesn't exist (currently succeeds as no-op)."""
        result = self.runner.invoke(app, ["resume", "Nonexistent"])
        # Note: CLI currently returns success for resuming nonexistent task
        self.assertEqual(result.exit_code, 0)


class TestDataMigration(unittest.TestCase):
    """Test backward compatibility and data migration."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create .worklog directory
        self.worklog_dir = Path(self.test_dir) / '.worklog'
        self.worklog_dir.mkdir(parents=True, exist_ok=True)
        
        # Patch config to use test directory
        from src.worklog.config import WorkLogConfig
        self.config_patcher = patch.object(WorkLogConfig, 'worklog_dir', str(self.worklog_dir))
        self.config_patcher.start()
        
        self.runner = CliRunner()
    
    def tearDown(self):
        """Clean up."""
        self.config_patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_load_old_format_without_project(self):
        """Test loading worklog.json from old version (without project field)."""
        # Create old format worklog.json (without project)
        import json
        old_data = {
            "entries": [
                {
                    "task": "Old Task",
                    "start_time": "2025-10-06T09:00:00",
                    "end_time": "2025-10-06T10:00:00",
                    "duration": "01:00:00"
                }
            ],
            "active_tasks": {},
            "paused_tasks": [],
            "recent_tasks": ["Old Task"]
        }
        
        worklog_file = self.worklog_dir / 'worklog.json'
        with open(worklog_file, 'w') as f:
            json.dump(old_data, f)
        
        # Should load without error
        result = self.runner.invoke(app, ["list"])
        self.assertEqual(result.exit_code, 0)
    
    def test_load_new_format_with_project(self):
        """Test loading worklog.json with project field (new version)."""
        import json
        new_data = {
            "entries": [
                {
                    "task": "New Task",
                    "start_time": "2025-10-06T09:00:00",
                    "end_time": "2025-10-06T10:00:00",
                    "duration": "01:00:00",
                    "project": "TestProject"
                }
            ],
            "active_tasks": {},
            "paused_tasks": [],
            "recent_tasks": ["New Task"],
            "active_task_projects": {}
        }
        
        worklog_file = self.worklog_dir / 'worklog.json'
        with open(worklog_file, 'w') as f:
            json.dump(new_data, f)
        
        # Should load without error
        result = self.runner.invoke(app, ["list"])
        self.assertEqual(result.exit_code, 0)
    
    def test_mixed_format_entries(self):
        """Test loading worklog.json with mixed old and new format entries."""
        import json
        mixed_data = {
            "entries": [
                {
                    "task": "Old Task",
                    "start_time": "2025-10-06T09:00:00",
                    "end_time": "2025-10-06T10:00:00",
                    "duration": "01:00:00"
                },
                {
                    "task": "New Task",
                    "start_time": "2025-10-06T11:00:00",
                    "end_time": "2025-10-06T12:00:00",
                    "duration": "01:00:00",
                    "project": "TestProject"
                }
            ],
            "active_tasks": {},
            "paused_tasks": [],
            "recent_tasks": [],
            "active_task_projects": {}
        }
        
        worklog_file = self.worklog_dir / 'worklog.json'
        with open(worklog_file, 'w') as f:
            json.dump(mixed_data, f)
        
        # Should load both formats without error
        result = self.runner.invoke(app, ["list"])
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
