"""
CLI commands module for the WorkLog application.

This module contains all Typer CLI command definitions and integrates
with the core WorkLog functionality through the managers package.
"""
import logging
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console

from ..managers.worklog import WorkLog
from ..config import WorkLogConfig
from .. import __version__

# Initialize Rich console and logger
console = Console()
logger = logging.getLogger(__name__)

# Create Typer application
app = typer.Typer(
    name="drudge",
    help="🚀 Drudge CLI - A comprehensive work time tracking tool with task management, time tracking, and reporting features.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=True,
    pretty_exceptions_show_locals=False
)

# Global WorkLog instance - initialized on first command
_worklog_instance: Optional[WorkLog] = None


def get_worklog() -> WorkLog:
    """
    Get or create the global WorkLog instance.
    
    Returns:
        WorkLog: Configured WorkLog instance
    """
    global _worklog_instance
    if _worklog_instance is None:
        config = WorkLogConfig.load_from_yaml()
        _worklog_instance = WorkLog(config=config)
    return _worklog_instance


# ============================================================================
# Task Management Commands
# ============================================================================

@app.command()
def start(
    task_name: Optional[str] = typer.Argument(None, help="Name of the task to start (anonymous if omitted)"),
    time: Optional[str] = typer.Option(None, "--time", "-t", help="Custom start time (HH:MM or YYYY-MM-DD HH:MM)"),
    project: Optional[str] = typer.Option(None, "--project", "-P", help="Project/category name for task organization"),
    force: bool = typer.Option(False, "--force", "-f", help="Force start by ending active tasks"),
    parallel: bool = typer.Option(False, "--parallel", "-p", help="Allow parallel tasks (don't auto-end active tasks)")
) -> None:
    """
    🚀 Start a new task or resume a paused one.
    
    By default, starting a new task ends any active tasks (single-task mode).
    Use --parallel to work on multiple tasks simultaneously.
    Omit task name to start anonymous work session.
    
    Examples:
        drudge start "Fix bug #123"
        drudge start                    # Anonymous work
        drudge start "Review PR" --time 09:30
        drudge start "Meeting" --time "2025-12-10 14:00"  # Specific date
        drudge start "Fix bug" --project "Backend API"   # With project
        drudge start "Meeting" --parallel
        drudge start "Task" --force     # End active tasks first
    """
    worklog = get_worklog()
    
    # Handle modes:
    # - parallel=True: Allow concurrent tasks (don't auto-end)
    # - parallel=False (default): Single-task mode (auto-end active tasks)
    # force parameter is respected in both modes for explicit auto-ending
    auto_end_mode = not parallel  # Single-task mode auto-ends
    success = worklog.start_task(task_name, custom_time=time, force=force or auto_end_mode, parallel=parallel, project=project)
    
    if not success:
        raise typer.Exit(1)


@app.command()
def end(
    task_name: Optional[str] = typer.Argument(None, help="Name of the task to end (omit to end all active tasks)"),
    time: Optional[str] = typer.Option(None, "--time", "-t", help="Custom end time (HH:MM or YYYY-MM-DD HH:MM)"),
    all: bool = typer.Option(False, "--all", "-a", help="End all active AND paused tasks"),
    sync: bool = typer.Option(False, "--sync", "-s", help="Automatically sync to Google Sheets after ending task(s)")
) -> None:
    """
    🏁 End an active task and record completion.
    
    Omit task name to end all active tasks.
    Use --all to also end paused tasks (converting accumulated time to entries).
    Use --sync to automatically sync completed tasks to Google Sheets.
    
    Examples:
        drudge end "Fix bug #123"
        drudge end "Meeting" --time 17:30
        drudge end "Meeting" --time "2025-12-10 17:30"    # Specific date
        drudge end                          # End all active tasks
        drudge end --all                    # End all active AND paused tasks
        drudge end "Review PR" --sync       # End task and sync to Google Sheets
    """
    worklog = get_worklog()
    
    # If --all flag is used, end all active AND paused tasks
    if all:
        worklog.end_all_tasks(custom_time=time, include_paused=True)
    # If no task name provided, end all active tasks
    elif task_name is None:
        worklog.end_all_tasks(custom_time=time, include_paused=False)
    # End specific task
    else:
        success = worklog.end_task(task_name, custom_time=time)
        if not success:
            raise typer.Exit(1)
    
    # Auto-sync if requested via --sync flag OR enabled in config
    config = worklog.config
    should_sync = sync or config.google_sheets.auto_sync
    
    if should_sync:
        # Check if sync is properly configured
        if not config.google_sheets.enabled:
            console.print("⚠️  [yellow]Google Sheets sync is not enabled - skipping sync[/yellow]")
            console.print("💡 Enable it in config.yaml: google_sheets.enabled = true", style="dim")
        elif not config.sheet_document_id:
            console.print("⚠️  [yellow]Google Sheets document ID not configured - skipping sync[/yellow]")
            console.print("💡 Set it in config.yaml: sheet_document_id = 'your-sheet-id'", style="dim")
        else:
            try:
                from ..sync.sheets import GoogleSheetsSync
                
                console.print("\n🔄 Syncing to Google Sheets...", style="dim")
                sheets_sync = GoogleSheetsSync(config)
                result = sheets_sync.sync_daily()
                console.print(f"✅ Synced {result['count']} task(s) to Google Sheets", style="green")
            except Exception as e:
                console.print(f"❌ Sync failed: {e}", style="red")
                logger.exception("Error during auto-sync")
                console.print("💡 You can sync manually later with: drudge sync", style="dim")


@app.command()
def pause(
    task_name: str = typer.Argument(..., help="Name of the task to pause"),
    time: Optional[str] = typer.Option(None, "--time", "-t", help="Custom pause time (HH:MM or YYYY-MM-DD HH:MM)")
) -> None:
    """
    ⏸️ Pause an active task for later resumption.
    
    Examples:
        worklog pause "Fix bug #123"
        worklog pause "Review PR" --time 12:00
        worklog pause "Review PR" --time "2025-12-10 12:00"
    """
    worklog = get_worklog()
    success = worklog.pause_task(task_name, custom_time=time)
    
    if not success:
        raise typer.Exit(1)


@app.command()
def resume(
    task_name: str = typer.Argument(..., help="Name of the task to resume"),
    time: Optional[str] = typer.Option(None, "--time", "-t", help="Custom resume time (HH:MM or YYYY-MM-DD HH:MM)")
) -> None:
    """
    ▶️ Resume a paused task.
    
    Examples:
        worklog resume "Fix bug #123"
        worklog resume "Review PR" --time 13:00
        worklog resume "Review PR" --time "2025-12-10 13:00"
    """
    worklog = get_worklog()
    success = worklog.resume_task(task_name, custom_time=time)
    
    if not success:
        raise typer.Exit(1)


# ============================================================================
# Status and Information Commands
# ============================================================================

@app.command()
def recent(
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Limit number of tasks shown")
) -> None:
    """
    📝 List recent tasks for quick reference.
    
    Example:
        worklog recent --limit 10
    """
    worklog = get_worklog()
    worklog.list_recent_tasks(limit=limit)


@app.command()
def list(
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Filter by date (YYYY-MM-DD)"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Limit number of entries"),
    task: Optional[str] = typer.Option(None, "--task", "-t", help="Filter by task name"),
    project: Optional[str] = typer.Option(None, "--project", "-P", help="Filter by project name")
) -> None:
    """
    📋 Show work status: active tasks, paused tasks, and completed entries.
    
    Without filters: Shows current status (active/paused tasks + today's count)
    With filters: Shows filtered completed entries
    
    Examples:
        drudge list                      # Show current status
        drudge list --date 2025-01-15    # Show tasks from specific date
        drudge list --task "bug" --limit 5
        drudge list --project "Backend API"  # Filter by project
    """
    worklog = get_worklog()
    worklog.list_entries(date=date, limit=limit, task_filter=task, project_filter=project)


@app.command()
def daily(
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Date for summary (YYYY-MM-DD)"),
    sync: bool = typer.Option(False, "--sync", "-s", help="Sync today's tasks to Google Sheets after showing summary")
) -> None:
    """
    📅 Show daily work summary with time totals.
    
    Use --sync to automatically sync today's tasks to Google Sheets after showing the summary.
    
    Examples:
        drudge daily
        drudge daily --date 2025-01-15
        drudge daily --sync              # Show summary and sync to Google Sheets
    """
    worklog = get_worklog()
    worklog.show_daily_summary(date=date)
    
    # Auto-sync today's tasks if requested
    if sync:
        from ..sync.sheets import GoogleSheetsSync
        
        config = worklog.config
        
        # Check if sync is properly configured
        if not config.google_sheets.enabled:
            console.print("\n⚠️  [yellow]Google Sheets sync is not enabled - skipping sync[/yellow]")
            console.print("💡 Enable it in config.yaml: google_sheets.enabled = true", style="dim")
        elif not config.sheet_document_id:
            console.print("\n⚠️  [yellow]Google Sheets document ID not configured - skipping sync[/yellow]")
            console.print("💡 Set it in config.yaml: sheet_document_id = 'your-sheet-id'", style="dim")
        else:
            try:
                console.print("\n🔄 Syncing today's tasks to Google Sheets...", style="dim")
                sheets_sync = GoogleSheetsSync(config)
                result = sheets_sync.sync_daily()
                console.print(f"✅ Synced {result['count']} task(s) to Google Sheets", style="green")
            except Exception as e:
                console.print(f"\n❌ Sync failed: {e}", style="red")
                logger.exception("Error during daily sync")
                console.print("💡 You can sync manually with: drudge sync --daily", style="dim")


@app.command()
def sync(
    daily: bool = typer.Option(False, "--daily", "-d", help="Sync only today's tasks"),
    monthly: bool = typer.Option(False, "--monthly", "-m", help="Sync current month's tasks"),
    date: Optional[str] = typer.Option(None, "--date", help="Sync tasks from specific date (YYYY-MM-DD)"),
    test: bool = typer.Option(False, "--test", "-t", help="Test sync without writing (dry-run)")
) -> None:
    """
    🔄 Sync worklog entries to Google Sheets.
    
    By default, syncs all completed tasks.
    Use flags to filter which tasks to sync.
    
    Examples:
        drudge sync                  # Sync all tasks
        drudge sync --daily          # Sync only today's tasks
        drudge sync --monthly        # Sync current month's tasks
        drudge sync --date 2025-10-03  # Sync tasks from specific date
        drudge sync --test           # Test sync without writing to sheet
    """
    from ..sync.sheets import GoogleSheetsSync
    
    worklog = get_worklog()
    config = worklog.config
    
    # Check if Google Sheets sync is enabled
    if not config.google_sheets.enabled:
        console.print("❌ Google Sheets sync is not enabled in configuration", style="red")
        console.print("💡 Enable it in config.yaml: google_sheets.enabled = true", style="dim")
        raise typer.Exit(1)
    
    # Check if sheet document ID is configured
    if not config.sheet_document_id:
        console.print("❌ Google Sheets document ID is not configured", style="red")
        console.print("💡 Set it in config.yaml: sheet_document_id = 'your-sheet-id'", style="dim")
        raise typer.Exit(1)
    
    # Validate conflicting options
    option_count = sum([daily, monthly, date is not None])
    if option_count > 1:
        console.print("❌ Cannot use --daily, --monthly, and --date together", style="red")
        console.print("💡 Choose only one filtering option", style="dim")
        raise typer.Exit(1)
    
    try:
        # Initialize Google Sheets sync
        sheets_sync = GoogleSheetsSync(config)
        
        # Determine sync mode
        if test:
            console.print("🧪 [yellow]TEST MODE: No data will be written to Google Sheets[/yellow]\n")
        
        if daily:
            console.print("📅 Syncing today's tasks to Google Sheets...")
            result = sheets_sync.sync_daily(dry_run=test)
        elif monthly:
            console.print("📆 Syncing current month's tasks to Google Sheets...")
            result = sheets_sync.sync_monthly(dry_run=test)
        elif date:
            console.print(f"📅 Syncing tasks from {date} to Google Sheets...")
            result = sheets_sync.sync_date(date, dry_run=test)
        else:
            console.print("🔄 Syncing all tasks to Google Sheets...")
            result = sheets_sync.sync_all(dry_run=test)
        
        # Display results
        if test:
            console.print(f"\n✅ [green]Test completed:[/green] Would sync {result['count']} tasks", style="bold")
        else:
            console.print(f"\n✅ [green]Successfully synced {result['count']} tasks to Google Sheets[/green]", style="bold")
        
        if result.get('sheets_updated'):
            console.print(f"📊 Updated sheets: {', '.join(result['sheets_updated'])}", style="dim")
        
    except FileNotFoundError as e:
        console.print(f"❌ Credentials file not found: {e}", style="red")
        console.print("💡 Place your Google Sheets credentials JSON file in the expected location", style="dim")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Sync failed: {e}", style="red")
        logger.exception("Error during Google Sheets sync")
        raise typer.Exit(1)


@app.command()
def clean(
    target: Optional[str] = typer.Argument(None, help="Date (YYYY-MM-DD) or task name to clean"),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Filter by date when cleaning a task"),
    all: bool = typer.Option(False, "--all", "-a", help="Clean all worklog entries")
) -> None:
    """
    🗑️ Clean worklog entries by date, task, or all.
    
    Creates a backup before cleaning for safety.
    
    Examples:
        drudge clean 2025-10-03              # Clean all entries for a date
        drudge clean "Bug fix"               # Clean all entries for a task
        drudge clean "Meeting" --date 2025-10-03  # Clean task entries for specific date
        drudge clean --all                   # Clean all worklog entries
    """
    worklog = get_worklog()
    
    # Clean all entries
    if all:
        if target is not None:
            console.print("❌ Cannot specify a target when using --all", style="red")
            raise typer.Exit(1)
        
        # Confirm before cleaning all
        console.print("⚠️  [yellow]This will clean ALL worklog entries![/yellow]")
        confirm = typer.confirm("Are you sure you want to continue?")
        if not confirm:
            console.print("❌ Operation cancelled", style="dim")
            raise typer.Exit(0)
        
        worklog.clean_all()
        return
    
    # No target specified
    if target is None:
        console.print("❌ Please specify a date, task name, or use --all", style="red")
        raise typer.Exit(1)
    
    # Check if target is a date (YYYY-MM-DD format)
    import re
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    if re.match(date_pattern, target):
        # Clean by date
        if date is not None:
            console.print("❌ Cannot use --date when target is already a date", style="red")
            raise typer.Exit(1)
        worklog.clean_by_date(target)
    else:
        # Clean by task name
        worklog.clean_by_task(target, date=date)


# ============================================================================
# Configuration and Utility Commands
# ============================================================================

@app.command()
def config(
    show: bool = typer.Option(False, "--show", "-s", help="Show full config.yaml content"),
) -> None:
    """
    ⚙️ Show current configuration settings.
    
    By default shows a summary. Use --show to display the full config.yaml file.
    
    Examples:
        drudge config           # Show config summary
        drudge config --show    # Show full config.yaml content
    """
    from ..config import get_default_config_path, ensure_config_exists
    
    config_path = get_default_config_path()
    
    # Ensure config exists (creates from template if needed)
    ensure_config_exists(config_path)
    
    if show:
        # Show full config file content
        console.print(f"📄 Config file: [cyan]{config_path}[/cyan]\n", style="bold")
        content = config_path.read_text()
        from rich.syntax import Syntax
        syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
        console.print(syntax)
    else:
        # Show summary
        worklog = get_worklog()
        console.print("⚙️ Drudge CLI Configuration:", style="bold")
        console.print(f"� Config file: [cyan]{config_path}[/cyan]")
        console.print(f"�📁 Data directory: {worklog.worklog_dir}")
        console.print(f"� Data file: {worklog.worklog_file}")
        console.print(f"🕐 Display format: {worklog.config.display_time_format}")
        console.print(f"📋 Max recent tasks: {worklog.config.max_recent_tasks}")
        console.print(f"💾 Max backups: {worklog.config.max_backups}")
        console.print(f"📊 Google Sheets: {'enabled' if worklog.config.google_sheets.enabled else 'disabled'}")
        if worklog.config.sheet_document_id:
            console.print(f"📑 Sheet ID: {worklog.config.sheet_document_id[:20]}...")
        console.print(f"\n💡 Use [cyan]drudge config --show[/cyan] to see full config.yaml")


@app.command()
def version() -> None:
    """
    📦 Show Drudge CLI version information.
    """
    console.print("🚀 Drudge CLI", style="bold blue")
    console.print(f"Version: {__version__} (Enhanced CLI)")
    console.print("A comprehensive work time tracking and task management tool")


# ============================================================================
# Error Handling and Main Entry
# ============================================================================

def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration for the CLI.
    
    Args:
        verbose: Enable debug logging if True
    """
    # Ensure worklog directory exists
    log_dir = Path.home() / '.worklog'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'worklog.log'),
            logging.StreamHandler() if verbose else logging.NullHandler()
        ]
    )


def main() -> None:
    """
    Main entry point for the CLI application.
    
    Handles global exception catching and logging setup.
    """
    try:
        # Setup basic logging
        setup_logging()
        
        # Run the Typer app
        app()
        
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="yellow")
        raise typer.Exit(0)
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="red")
        logger.exception("Unexpected error in CLI")
        raise typer.Exit(1)


if __name__ == "__main__":
    main()