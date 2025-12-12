#!/usr/bin/env python3
"""
Google Sheets Sync Integration Test

This script performs a real end-to-end test of the Google Sheets sync functionality:
1. Creates test tasks in drudge
2. Syncs to Google Sheets using real API
3. Verifies data in the sheet
4. Cleans up test data

REQUIREMENTS:
- test-credentials.json: Service account credentials
- test-config.yaml: Test configuration with sheet Document ID
- Test Google Sheet with config and monthly sheets

USAGE:
    docker run --rm \
      -v $(pwd)/test-credentials.json:/app/test-credentials.json:ro \
      -v $(pwd)/test-config.yaml:/app/test-config.yaml:ro \
      drudge-test python test_sync_integration.py
"""

import os
import sys
import time
import yaml
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from worklog.managers.worklog import WorkLog
from worklog.sync.sheets import GoogleSheetsSync
from worklog.config import WorkLogConfig


def print_banner(text, char="="):
    """Print a banner for visual separation."""
    print(f"\n{char * 48}")
    print(text)
    print(f"{char * 48}\n")


def load_test_config():
    """Load test configuration."""
    config_path = Path("/app/test-config.yaml")
    if not config_path.exists():
        # Try local path if not in Docker
        config_path = Path(__file__).parent / "test-config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(
            "Test config not found. Create test-config.yaml with:\n"
            "  google_sheets:\n"
            "    enabled: true\n"
            "    document_id: YOUR_TEST_SHEET_ID\n"
            "    credentials_file: /app/test-credentials.json\n"
        )
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    return config


def verify_credentials(config):
    """Verify credentials file exists."""
    # Get path from config
    sheets_config = config.get("google_sheets", {})
    creds_path_str = sheets_config.get("credentials_file", "/app/credentials.json")
    creds_path = Path(creds_path_str)
    
    if not creds_path.exists():
        # Try without /app prefix if in Docker
        if creds_path_str.startswith("/app/"):
            local_name = creds_path_str.replace("/app/", "")
            creds_path = Path(__file__).parent / local_name
    
    if not creds_path.exists():
        raise FileNotFoundError(
            f"Credentials file not found: {creds_path_str}\n"
            "Make sure to mount credentials file to Docker:\n"
            f"  -v $(pwd)/credentials.json:/app/credentials.json:ro"
        )
    
    return str(creds_path)


def create_test_task(manager, project="TestProject"):
    """Create a test task."""
    task_name = "Integration Test Task"
    
    print(f"📝 Creating test task...")
    manager.start_task(task_name, project=project)
    
    print(f"   Started: {task_name} ({project})")
    
    return task_name


def end_test_task(manager, task_name):
    """End the test task."""
    print(f"\n⏳ Waiting 30 seconds (simulating work)...")
    time.sleep(30)
    
    success = manager.end_task(task_name)
    if not success:
        raise RuntimeError(f"Failed to end task: {task_name}")
    
    # Get the completed task from entries
    completed_task = None
    for entry in reversed(manager.data.entries):
        if entry.task == task_name and entry.end_time is not None:
            completed_task = entry
            break
    
    if not completed_task:
        raise RuntimeError(f"Could not find completed task: {task_name}")
    
    # Calculate duration
    start_dt = datetime.fromisoformat(completed_task.start_time)
    end_dt = datetime.fromisoformat(completed_task.end_time)
    duration_seconds = (end_dt - start_dt).total_seconds()
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    
    print(f"\n✅ Task ended: {hours}h {minutes}m")
    
    return completed_task


def sync_to_sheets(config):
    """Sync tasks to Google Sheets."""
    print(f"\n🔄 Syncing to Google Sheets...")
    
    # Get sync config
    sheets_config = config.get("google_sheets", {})
    document_id = sheets_config.get("document_id")
    credentials_file = sheets_config.get("credentials_file")
    
    if not document_id:
        raise ValueError("Document ID not found in test-config.yaml")
    
    # Create WorkLogConfig with sheets settings
    wl_config = WorkLogConfig()
    wl_config.worklog_dir = config.get("worklog_dir", "/tmp/test-worklog")
    
    # Configure Google Sheets settings
    wl_config.google_sheets.enabled = True
    wl_config.google_sheets.document_id = document_id
    wl_config.google_sheets.round_hours = sheets_config.get("round_hours", 0.25)
    
    # Create sync instance
    creds_path = Path(credentials_file) if credentials_file else None
    sync = GoogleSheetsSync(config=wl_config, credentials_path=creds_path)
    
    # Get today's tasks
    worklog_dir = config.get("worklog_dir", str(Path.home() / ".worklog"))
    wl_config = WorkLogConfig()
    wl_config.worklog_dir = worklog_dir
    manager = WorkLog(config=wl_config)
    
    # Filter completed tasks from today
    today = datetime.now().date()
    completed_tasks = []
    for entry in manager.data.entries:
        if entry.end_time is not None:
            # Parse date from start_time
            entry_date = datetime.fromisoformat(entry.start_time).date()
            if entry_date == today:
                completed_tasks.append(entry)
    
    if not completed_tasks:
        raise RuntimeError("No completed tasks to sync!")
    
    # Sync tasks
    synced_count = sync.sync_tasks(completed_tasks)
    
    print(f"✅ Sync completed: {synced_count} task(s) synced")
    
    return synced_count


def verify_in_sheet(config):
    """Verify task appears in Google Sheet."""
    print(f"\n🔍 Verifying data in Google Sheet...")
    
    sheets_config = config.get("google_sheets", {})
    document_id = sheets_config.get("document_id")
    credentials_file = sheets_config.get("credentials_file")
    
    # Create sync instance to read data
    sync = GoogleSheetsSync(
        document_id=document_id,
        credentials_file=credentials_file
    )
    
    # Get current month sheet
    month_name = datetime.now().strftime("%B")
    
    # Read data from sheet
    try:
        # Get sheet values
        result = sync.service.spreadsheets().values().get(
            spreadsheetId=document_id,
            range=f"{month_name}!A:F"
        ).execute()
        
        values = result.get('values', [])
        
        if len(values) < 2:
            raise RuntimeError("No data found in sheet (only headers)")
        
        # Last row should be our test task
        last_row = values[-1]
        
        # Parse row (Date, Start time, Project, Activity, Details, Spent)
        if len(last_row) >= 6:
            date, start_time, project, activity, details, spent = last_row[:6]
            
            print(f"✅ Task found in sheet:")
            print(f"   Date: {date}")
            print(f"   Start: {start_time}")
            print(f"   Project: {project}")
            print(f"   Activity: {activity}")
            print(f"   Duration: {spent}")
            
            # Basic validation
            today = datetime.now().strftime("%d/%m/%Y")
            if date != today:
                print(f"⚠️  Warning: Date mismatch (expected {today})")
            
            if project != "TestProject":
                print(f"⚠️  Warning: Project mismatch (expected TestProject)")
            
            if "Integration Test Task" not in activity:
                print(f"⚠️  Warning: Activity mismatch")
            
            return True
        else:
            raise RuntimeError(f"Invalid row format: {last_row}")
    
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def cleanup_test_data(config):
    """Remove test data from sheet."""
    print(f"\n🧹 Cleaning up test data...")
    
    sheets_config = config.get("google_sheets", {})
    document_id = sheets_config.get("document_id")
    credentials_file = sheets_config.get("credentials_file")
    
    sync = GoogleSheetsSync(
        document_id=document_id,
        credentials_file=credentials_file
    )
    
    month_name = datetime.now().strftime("%B")
    
    try:
        # Get current row count
        result = sync.service.spreadsheets().values().get(
            spreadsheetId=document_id,
            range=f"{month_name}!A:A"
        ).execute()
        
        row_count = len(result.get('values', []))
        
        if row_count > 1:  # More than just headers
            # Delete last row (our test data)
            delete_range = f"{month_name}!A{row_count}:F{row_count}"
            
            sync.service.spreadsheets().values().clear(
                spreadsheetId=document_id,
                range=delete_range
            ).execute()
            
            print(f"✅ Test data removed from sheet")
        
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
    
    # Also cleanup temp worklog directory
    worklog_dir = Path(config.get("worklog_dir", "/tmp/test-worklog"))
    if worklog_dir.exists():
        import shutil
        shutil.rmtree(worklog_dir)
        print(f"✅ Temp worklog removed: {worklog_dir}")


def main():
    """Run integration test."""
    try:
        print_banner("🧪 Starting Google Sheets Sync Integration Test")
        
        # Load config
        config = load_test_config()
        doc_id = config.get("google_sheets", {}).get("document_id", "")
        print(f"✅ Config loaded: Test sheet ID = {doc_id[:10]}...{doc_id[-10:]}")
        
        # Verify credentials
        creds_path = verify_credentials(config)
        print(f"✅ Credentials found: {creds_path}")
        
        # Set up worklog directory
        worklog_dir = config.get("worklog_dir", "/tmp/test-worklog")
        os.makedirs(f"{worklog_dir}/daily", exist_ok=True)
        
        # Create manager with custom config
        wl_config = WorkLogConfig()
        wl_config.worklog_dir = worklog_dir
        manager = WorkLog(config=wl_config)
        
        # Create test task
        task_name = create_test_task(manager, project="TestProject")
        
        # End test task
        task = end_test_task(manager, task_name)
        
        # Sync to sheets
        synced_count = sync_to_sheets(config)
        
        if synced_count == 0:
            raise RuntimeError("Sync returned 0 tasks!")
        
        # Verify in sheet
        verified = verify_in_sheet(config)
        
        if not verified:
            raise RuntimeError("Verification failed!")
        
        # Cleanup
        cleanup_test_data(config)
        
        print_banner("✅ INTEGRATION TEST PASSED!", "=")
        
        return 0
    
    except Exception as e:
        print_banner(f"❌ INTEGRATION TEST FAILED!", "=")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
