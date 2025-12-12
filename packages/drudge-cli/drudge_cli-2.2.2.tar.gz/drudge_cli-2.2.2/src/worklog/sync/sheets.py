"""Google Sheets sync functionality for haunts-compatible format."""

import math
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Optional

import gspread
from google.auth.exceptions import DefaultCredentialsError
from google.oauth2.service_account import Credentials

from ..config import WorkLogConfig
from ..models import TaskEntry

# Optional haunts import
try:
    from haunts import spreadsheet as haunts_spreadsheet
    HAUNTS_AVAILABLE = True
except ImportError:
    HAUNTS_AVAILABLE = False


def round_hours(hours: float, increment: float) -> float:
    """
    Round hours to the nearest increment.
    
    Args:
        hours: The hours value to round
        increment: The rounding increment (0.25 for 15min, 0.5 for 30min, 1.0 for hour)
    
    Returns:
        Rounded hours value
    
    Examples:
        >>> round_hours(2.2, 0.25)  # 2h 12m → 2.25 (2h 15m)
        2.25
        >>> round_hours(2.6, 0.5)   # 2h 36m → 2.5 (2h 30m)
        2.5
        >>> round_hours(2.4, 1.0)   # 2h 24m → 2.0 (2h 0m)
        2.0
    """
    return round(hours / increment) * increment


def format_hours(hours: float, round_increment: float) -> str:
    """
    Format hours with rounding, using comma as decimal separator.
    
    Decimal places are automatically determined based on the rounding increment:
    - 1.0 (hour) → 0 decimals
    - 0.5 (30min) → 1 decimal
    - 0.25 (15min) → 2 decimals
    
    Args:
        hours: The hours value to format
        round_increment: Rounding increment (0.25, 0.5, or 1.0)
    
    Returns:
        Formatted hours string with comma separator (European format)
    
    Examples:
        >>> format_hours(2.2, 0.25)  # 2h 12m → "2,25"
        '2,25'
        >>> format_hours(2.6, 0.5)   # 2h 36m → "2,5"
        '2,5'
        >>> format_hours(2.4, 1.0)   # 2h 24m → "2"
        '2'
    """
    rounded = round_hours(hours, round_increment)
    
    # Determine decimal places based on increment
    if round_increment >= 1.0:
        decimal_places = 0
    elif round_increment >= 0.5:
        decimal_places = 1
    else:  # 0.25 or smaller
        decimal_places = 2
    
    if decimal_places == 0:
        return str(int(rounded))
    
    # Format with calculated decimal places
    format_str = f"{{:.{decimal_places}f}}"
    formatted = format_str.format(rounded)
    
    # Replace dot with comma for European format
    return formatted.replace(".", ",")


class HauntsAdapter:
    """
    Adapter to use haunts-style formatting and optionally haunts credentials.
    
    Can use either:
    1. Existing haunts OAuth credentials (~/.config/haunts/)
    2. Service account credentials (credentials_path parameter)
    """
    
    def __init__(self, config: WorkLogConfig, credentials_path: Optional[Path] = None):
        """
        Initialize the HauntsAdapter.
        
        Priority order:
        1. If credentials_path provided → Use OAuth token or Service Account from file
        2. If no credentials_path AND haunts installed → Try ~/.config/haunts/ OAuth
        3. Otherwise → Raise clear error
        
        Args:
            config: WorkLog configuration
            credentials_path: Path to credentials file (OAuth token JSON or Service Account JSON).
                            If None, will try haunts OAuth from ~/.config/haunts/
        
        Raises:
            ImportError: If haunts library needed but not installed
            ValueError: If Google Sheets is not enabled in config
            FileNotFoundError: If no valid credentials found
        """
        if not config.google_sheets.enabled:
            raise ValueError("Google Sheets sync is not enabled in configuration")
        
        self.config = config
        self.credentials_path = credentials_path
        self._use_haunts_oauth = False
        
        # CASE 1: credentials_path provided → Use it (OAuth token or Service Account)
        if credentials_path:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"Credentials file not found: {credentials_path}\n"
                    f"Expected: OAuth token JSON or Service Account JSON"
                )
            self._init_with_service_account(credentials_path)
            return
        
        # CASE 2: No credentials_path → Try haunts OAuth if available
        if HAUNTS_AVAILABLE:
            try:
                self._init_with_haunts_oauth()
                self._use_haunts_oauth = True
                return
            except FileNotFoundError:
                # Haunts not configured, continue to error
                pass
        
        # CASE 3: No valid credentials found
        raise FileNotFoundError(
            "No credentials found. Choose one:\n"
            "  1. Provide credentials_path with OAuth token or Service Account JSON\n"
            "  2. Install haunts: pip install 'drudge-cli[sheets]'\n"
            "  3. Set up haunts OAuth: run 'haunts' command to configure ~/.config/haunts/"
        )
    
    def _init_with_haunts_oauth(self):
        """Initialize using haunts OAuth credentials and config."""
        if not HAUNTS_AVAILABLE:
            raise ImportError("haunts library is not installed")
        
        from pathlib import Path as PathlibPath
        from haunts.credentials import get_credentials
        from haunts.ini import init as haunts_init, get as haunts_get
        from googleapiclient.discovery import build
        
        # Check if haunts config exists
        haunts_config_dir = PathlibPath.home() / ".config" / "haunts"
        haunts_config_file = haunts_config_dir / "config.ini"
        
        if not haunts_config_file.exists():
            raise FileNotFoundError("Haunts config not found at ~/.config/haunts/config.ini")
        
        # Initialize haunts config
        haunts_init(haunts_config_file)
        
        # Get sheet document ID from haunts config
        haunts_sheet_id = haunts_get("CONTROLLER_SHEET_DOCUMENT_ID")
        
        # Override our config with haunts sheet ID if not already set
        if not self.config.sheet_document_id:
            self.config.sheet_document_id = haunts_sheet_id
        
        # Get OAuth credentials using haunts
        creds = get_credentials(
            haunts_config_dir,
            ["https://www.googleapis.com/auth/spreadsheets"],
            "sheets-token.json"
        )
        
        service = build("sheets", "v4", credentials=creds)
        self._sheet = service.spreadsheets()
    
    def _init_with_service_account(self, credentials_path: Path):
        """
        Initialize using credentials file.
        
        Supports two formats:
        1. Service account JSON (has "client_email" field)
        2. OAuth token JSON from haunts (has "token", "refresh_token" fields)
        """
        import json
        from google.oauth2.service_account import Credentials as ServiceAccountCredentials
        from google.oauth2.credentials import Credentials as OAuthCredentials
        from googleapiclient.discovery import build
        
        # Load and check credential type
        with open(credentials_path, 'r') as f:
            cred_data = json.load(f)
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        
        if "client_email" in cred_data:
            # Service account format
            creds = ServiceAccountCredentials.from_service_account_file(
                str(credentials_path),
                scopes=scopes
            )
        elif "refresh_token" in cred_data:
            # OAuth token format (haunts style)
            creds = OAuthCredentials(
                token=cred_data.get("token"),
                refresh_token=cred_data.get("refresh_token"),
                token_uri=cred_data.get("token_uri"),
                client_id=cred_data.get("client_id"),
                client_secret=cred_data.get("client_secret"),
                scopes=cred_data.get("scopes", scopes)
            )
        else:
            raise ValueError(
                f"Invalid credentials file format. Expected either:\n"
                f"- Service account JSON (with 'client_email')\n"
                f"- OAuth token JSON (with 'refresh_token')"
            )
        
        service = build("sheets", "v4", credentials=creds)
        self._sheet = service.spreadsheets()
    
    def _convert_task_to_haunts_format(self, task: TaskEntry) -> dict:
        """
        Convert TaskEntry to haunts-compatible format.
        
        Args:
            task: The task entry to convert
        
        Returns:
            Dictionary with haunts-compatible fields
        
        Raises:
            ValueError: If task is missing required fields
        """
        if not task.end_time:
            raise ValueError("Task must have end_time")
        
        if not task.start_time:
            raise ValueError("Task must have start_time")
        
        # Parse timestamps to datetime objects
        start_dt = datetime.fromisoformat(task.start_time)
        end_dt = datetime.fromisoformat(task.end_time)
        
        # Calculate duration as timedelta
        duration = end_dt - start_dt
        
        # Extract date (using end_time date)
        task_date = end_dt.date()
        
        return {
            'date': task_date,
            'start_time': start_dt,
            'project': task.project or "",
            'activity': task.task,  # Use task.task for activity
            'details': "",  # TaskEntry doesn't have description field
            'duration': duration
        }
    
    def _ensure_worksheet_exists(self, month_name: str) -> None:
        """
        Ensure the monthly worksheet exists with proper headers.
        
        Args:
            month_name: Name of the worksheet (e.g., "October")
        """
        try:
            # Try to get the worksheet
            self._sheet.values().get(
                spreadsheetId=self.config.sheet_document_id,
                range=f"{month_name}!A1:A1"
            ).execute()
        except Exception:
            # Worksheet doesn't exist, create it
            requests = [{
                'addSheet': {
                    'properties': {
                        'title': month_name,
                        'gridProperties': {
                            'rowCount': 100,
                            'columnCount': 10  # Updated from 9 to 10 columns
                        }
                    }
                }
            }]
            
            self._sheet.batchUpdate(
                spreadsheetId=self.config.sheet_document_id,
                body={'requests': requests}
            ).execute()
            
            # Add header row - Order: Date, Start time, Spent, Project, Activity, Details, Custom, Event id, Link, Action
            headers = [
                ["Date", "Start time", "Spent", "Project", "Activity", 
                 "Details", "Custom", "Event id", "Link", "Action"]
            ]
            
            self._sheet.values().update(
                spreadsheetId=self.config.sheet_document_id,
                range=f'{month_name}!A1:J1',  # Updated from I1 to J1
                valueInputOption='USER_ENTERED',
                body={'values': headers}
            ).execute()
    
    def sync_task(self, task: TaskEntry) -> None:
        """
        Sync a single task to Google Sheets using haunts-style formatting.
        
        Args:
            task: The task entry to sync
        
        Raises:
            ValueError: If task is not completed or missing required fields
        """
        # Convert task to haunts format
        haunts_data = self._convert_task_to_haunts_format(task)
        
        # Get month name for the sheet
        end_dt = datetime.fromisoformat(task.end_time)
        sheet_date_str = end_dt.strftime("%Y-%m-%d")
        month_name = self.config.get_sheet_name_for_date(sheet_date_str)
        
        # Ensure worksheet exists
        self._ensure_worksheet_exists(month_name)
        
        # Use haunts-style append logic (adapted from haunts.spreadsheet.append_line)
        # Get the first empty line
        next_line = self._get_first_empty_line(month_name)
        
        # Format data in haunts style
        formatted_time = haunts_data['start_time'].strftime("%H:%M")
        formatted_duration = self._format_duration_haunts(haunts_data['duration'])
        formatted_date = haunts_data['date'].strftime("%d/%m/%Y")
        
        # Build the row data matching haunts format
        # Order: Date, Start time, Spent, Project, Activity, Details, Custom, Event id, Link, Action
        row_data = [
            formatted_date,      # A: Date
            formatted_time,      # B: Start time
            formatted_duration,  # C: Spent (duration)
            haunts_data['project'],   # D: Project
            haunts_data['activity'],  # E: Activity
            haunts_data['details'],   # F: Details
            "",                  # G: Custom (empty)
            "",                  # H: Event id (filled by haunts sync)
            "",                  # I: Link (filled by haunts sync)
            ""                   # J: Action (used by haunts sync)
        ]
        
        # Write to sheet (A:J = 10 columns)
        range_name = f"{month_name}!A{next_line}:J{next_line}"
        self._sheet.values().update(
            spreadsheetId=self.config.sheet_document_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body={'values': [row_data]}
        ).execute()
    
    def _get_first_empty_line(self, month_name: str) -> int:
        """
        Find the first empty line in the worksheet.
        
        Args:
            month_name: Name of the worksheet
        
        Returns:
            Line number (1-indexed) of first empty row
        """
        try:
            result = self._sheet.values().get(
                spreadsheetId=self.config.sheet_document_id,
                range=f"{month_name}!A:A"
            ).execute()
            values = result.get('values', [])
            # First empty line is after all existing rows (skip header)
            return len(values) + 1
        except Exception:
            # If error, assume starting at line 2 (after header)
            return 2
    
    def _format_duration_haunts(self, duration: timedelta) -> str:
        """
        Format duration in haunts style (hours with comma separator).
        
        Args:
            duration: timedelta object
        
        Returns:
            Formatted duration string (e.g., "2,5" for 2.5 hours)
        """
        total_seconds = duration.total_seconds()
        hours = total_seconds / 3600
        # Round to 2 decimal places and format with comma
        rounded = round(hours, 2)
        return str(rounded).replace('.', ',')
    
    def sync_tasks(self, tasks: List[TaskEntry], filter_date: Optional[date] = None) -> int:
        """
        Sync multiple tasks to Google Sheets using haunts.
        
        Args:
            tasks: List of task entries to sync
            filter_date: If provided, only sync tasks from this date
        
        Returns:
            Number of tasks synced
        """
        synced_count = 0
        
        for task in tasks:
            if not task.end_time:
                continue  # Skip incomplete tasks
            
            # Filter by date if specified
            if filter_date:
                end_dt = datetime.fromisoformat(task.end_time)
                if end_dt.date() != filter_date:
                    continue
            
            try:
                self.sync_task(task)
                synced_count += 1
            except Exception as e:
                # Log error but continue with other tasks
                print(f"Error syncing task: {e}")
                continue
        
        return synced_count
    
    def test_connection(self) -> bool:
        """
        Test the connection to Google Sheets.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to get spreadsheet properties
            result = self._sheet.get(
                spreadsheetId=self.config.sheet_document_id
            ).execute()
            return True
        except Exception:
            return False


class GoogleSheetsSync:
    """
    Handles syncing work tasks to Google Sheets in haunts-compatible format.
    
    The sheet structure follows the haunts convention:
    - Monthly sheets named by full month name (e.g., "October", "November")
    - Columns: Date, Start time, Project, Activity, Details, Spent
    - Date format: DD/MM/YYYY
    - Time format: HH:MM
    - Duration: decimal hours with comma separator
    
    Uses HauntsAdapter backend if available, falls back to gspread.
    """
    
    def __init__(self, config: WorkLogConfig, credentials_path: Optional[Path] = None):
        """
        Initialize the Google Sheets sync.
        
        Args:
            config: WorkLog configuration (reads google_sheets.use_haunts_format)
            credentials_path: Path to credentials file (OAuth token or Service Account JSON).
                            If None and haunts library available, tries ~/.config/haunts/
        
        Raises:
            ValueError: If Google Sheets is not enabled in config
            FileNotFoundError: If credentials file doesn't exist and haunts config not found
        """
        if not config.google_sheets.enabled:
            raise ValueError("Google Sheets sync is not enabled in configuration")
        
        self.config = config
        self.credentials_path = credentials_path
        self._adapter: Optional[HauntsAdapter] = None
        self._client: Optional[gspread.Client] = None
        self._spreadsheet: Optional[gspread.Spreadsheet] = None
        
        # Use HauntsAdapter if use_haunts_format is enabled
        if config.google_sheets.use_haunts_format:
            try:
                self._adapter = HauntsAdapter(config, credentials_path)
            except (ImportError, FileNotFoundError, ValueError) as e:
                # Clear error message if haunts format requested but failed
                raise ValueError(
                    f"Cannot initialize haunts format sync: {e}\n"
                    f"Solutions:\n"
                    f"  1. Provide valid credentials_path (OAuth token or Service Account JSON)\n"
                    f"  2. Install haunts library: pip install 'drudge-cli[sheets]'\n"
                    f"  3. Set up haunts OAuth: run 'haunts' command first\n"
                    f"  4. Set google_sheets.use_haunts_format=false in config to use legacy gspread"
                ) from e
        # Otherwise use legacy gspread backend (will be initialized lazily)
    
    def _get_client(self) -> gspread.Client:
        """Get or create the gspread client."""
        if self._client is None:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file'
            ]
            
            if self.credentials_path:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}"
                    )
                creds = Credentials.from_service_account_file(
                    str(self.credentials_path),
                    scopes=scopes
                )
                self._client = gspread.authorize(creds)
            else:
                # Try default credentials (OAuth or service account)
                try:
                    self._client = gspread.oauth()
                except Exception as e:
                    raise DefaultCredentialsError(
                        "Failed to authenticate with Google Sheets. "
                        "Please provide credentials_path or set up OAuth. "
                        f"Error: {e}"
                    )
        
        return self._client
    
    def _get_spreadsheet(self) -> gspread.Spreadsheet:
        """Get or open the configured spreadsheet."""
        if self._spreadsheet is None:
            client = self._get_client()
            try:
                self._spreadsheet = client.open_by_key(self.config.sheet_document_id)
            except gspread.exceptions.SpreadsheetNotFound:
                raise ValueError(
                    f"Spreadsheet not found with ID: {self.config.sheet_document_id}. "
                    "Please check your sheet_document_id in config."
                )
        
        return self._spreadsheet
    
    def _get_or_create_sheet(self, sheet_name: str) -> gspread.Worksheet:
        """
        Get or create a worksheet by name.
        
        Args:
            sheet_name: Name of the worksheet (e.g., "October")
        
        Returns:
            The worksheet object
        """
        spreadsheet = self._get_spreadsheet()
        
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            # Create new worksheet with headers
            worksheet = spreadsheet.add_worksheet(
                title=sheet_name,
                rows=100,
                cols=9
            )
            # Add header row
            headers = [
                "Date", "Start time", "Project", "Activity", 
                "Details", "Spent", "Event id", "Link", "Action"
            ]
            worksheet.update('A1:I1', [headers])
        
        return worksheet
    
    def _format_date(self, timestamp_str: str) -> str:
        """Format ISO timestamp string to DD/MM/YYYY."""
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%d/%m/%Y")
    
    def _format_time(self, timestamp_str: str) -> str:
        """Format ISO timestamp string to HH:MM."""
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%H:%M")
    
    def _calculate_hours(self, task: TaskEntry) -> float:
        """Calculate task duration in hours from ISO timestamp strings."""
        if task.end_time and task.start_time:
            start_dt = datetime.fromisoformat(task.start_time)
            end_dt = datetime.fromisoformat(task.end_time)
            duration_seconds = (end_dt - start_dt).total_seconds()
            return duration_seconds / 3600
        return 0.0
    
    def sync_task(self, task: TaskEntry) -> None:
        """
        Sync a single task to Google Sheets.
        
        Args:
            task: The task entry to sync
        
        Raises:
            ValueError: If task is not completed (no end_time)
        """
        if not task.end_time:
            raise ValueError("Cannot sync task without end_time")
        
        # Use HauntsAdapter if available
        if self._adapter:
            self._adapter.sync_task(task)
            return
        
        # Fall back to gspread backend
        # Parse end_time to get the date for sheet selection
        end_dt = datetime.fromisoformat(task.end_time)
        sheet_date = end_dt.strftime("%Y-%m-%d")
        
        # Get the appropriate monthly sheet
        sheet_name = self.config.get_sheet_name_for_date(sheet_date)
        worksheet = self._get_or_create_sheet(sheet_name)
        
        # Calculate and format hours
        hours = self._calculate_hours(task)
        formatted_hours = format_hours(
            hours,
            self.config.google_sheets.round_hours
        )
        
        # Prepare row data
        row_data = [
            self._format_date(task.end_time),
            self._format_time(task.start_time),
            task.project or "",
            task.task,  # Use task.task for the task name
            task.description or "",
            formatted_hours,
            "",  # Event id (filled by haunts)
            "",  # Link (filled by haunts)
            ""   # Action (used by haunts)
        ]
        
        # Append to worksheet
        worksheet.append_row(row_data, value_input_option='USER_ENTERED')
    
    def sync_tasks(self, tasks: List[TaskEntry], filter_date: Optional[date] = None) -> int:
        """
        Sync multiple tasks to Google Sheets.
        
        Args:
            tasks: List of task entries to sync
            filter_date: If provided, only sync tasks from this date
        
        Returns:
            Number of tasks synced
        
        Raises:
            ValueError: If any task is not completed
        """
        synced_count = 0
        
        for task in tasks:
            if not task.end_time:
                continue  # Skip incomplete tasks
            
            # Filter by date if specified
            if filter_date:
                end_dt = datetime.fromisoformat(task.end_time)
                if end_dt.date() != filter_date:
                    continue
            
            self.sync_task(task)
            synced_count += 1
        
        return synced_count
    
    def test_connection(self) -> bool:
        """
        Test the connection to Google Sheets.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Use HauntsAdapter if available
            if self._adapter:
                return self._adapter.test_connection()
            
            # Fall back to gspread backend
            spreadsheet = self._get_spreadsheet()
            # Try to access spreadsheet title to verify access
            _ = spreadsheet.title
            return True
        except Exception:
            return False
    
    def sync_daily(self, dry_run: bool = False) -> dict:
        """
        Sync today's completed tasks to Google Sheets.
        
        Args:
            dry_run: If True, simulate sync without writing to sheets
        
        Returns:
            Dictionary with sync results (count, sheets_updated)
        """
        from ..managers.worklog import WorkLog
        
        worklog = WorkLog(config=self.config)
        today = datetime.now().date()
        
        # Filter completed tasks from today
        completed_tasks = [
            task for task in worklog.data.entries
            if task.end_time and datetime.fromisoformat(task.end_time).date() == today
        ]
        
        if dry_run:
            return {
                'count': len(completed_tasks),
                'sheets_updated': [self.config.get_sheet_name_for_date(today.strftime("%Y-%m-%d"))]
            }
        
        synced = self.sync_tasks(completed_tasks, filter_date=today)
        return {
            'count': synced,
            'sheets_updated': [self.config.get_sheet_name_for_date(today.strftime("%Y-%m-%d"))]
        }
    
    def sync_monthly(self, dry_run: bool = False) -> dict:
        """
        Sync current month's completed tasks to Google Sheets.
        
        Args:
            dry_run: If True, simulate sync without writing to sheets
        
        Returns:
            Dictionary with sync results (count, sheets_updated)
        """
        from ..managers.worklog import WorkLog
        
        worklog = WorkLog(config=self.config)
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        # Filter completed tasks from current month
        completed_tasks = [
            task for task in worklog.data.entries
            if task.end_time and 
            datetime.fromisoformat(task.end_time).month == current_month and
            datetime.fromisoformat(task.end_time).year == current_year
        ]
        
        if dry_run:
            sheet_name = self.config.get_sheet_name_for_date(now.strftime("%Y-%m-%d"))
            return {
                'count': len(completed_tasks),
                'sheets_updated': [sheet_name]
            }
        
        synced = self.sync_tasks(completed_tasks)
        sheet_name = self.config.get_sheet_name_for_date(now.strftime("%Y-%m-%d"))
        return {
            'count': synced,
            'sheets_updated': [sheet_name]
        }
    
    def sync_date(self, date_str: str, dry_run: bool = False) -> dict:
        """
        Sync tasks from a specific date to Google Sheets.
        
        Args:
            date_str: Date in YYYY-MM-DD format
            dry_run: If True, simulate sync without writing to sheets
        
        Returns:
            Dictionary with sync results (count, sheets_updated)
        
        Raises:
            ValueError: If date format is invalid
        """
        from ..managers.worklog import WorkLog
        
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format. Use YYYY-MM-DD: {e}")
        
        worklog = WorkLog(config=self.config)
        
        # Filter completed tasks from target date
        completed_tasks = [
            task for task in worklog.data.entries
            if task.end_time and datetime.fromisoformat(task.end_time).date() == target_date
        ]
        
        if dry_run:
            return {
                'count': len(completed_tasks),
                'sheets_updated': [self.config.get_sheet_name_for_date(date_str)]
            }
        
        synced = self.sync_tasks(completed_tasks, filter_date=target_date)
        return {
            'count': synced,
            'sheets_updated': [self.config.get_sheet_name_for_date(date_str)]
        }
    
    def sync_all(self, dry_run: bool = False) -> dict:
        """
        Sync all completed tasks to Google Sheets.
        
        Args:
            dry_run: If True, simulate sync without writing to sheets
        
        Returns:
            Dictionary with sync results (count, sheets_updated)
        """
        from ..managers.worklog import WorkLog
        
        worklog = WorkLog(config=self.config)
        
        # Get all completed tasks
        completed_tasks = [
            task for task in worklog.data.entries
            if task.end_time
        ]
        
        if dry_run:
            # Get unique months from completed tasks
            sheets_updated = list(set(
                self.config.get_sheet_name_for_date(
                    datetime.fromisoformat(task.end_time).strftime("%Y-%m-%d")
                )
                for task in completed_tasks
            ))
            return {
                'count': len(completed_tasks),
                'sheets_updated': sorted(sheets_updated)
            }
        
        synced = self.sync_tasks(completed_tasks)
        
        # Get unique months from synced tasks
        sheets_updated = list(set(
            self.config.get_sheet_name_for_date(
                datetime.fromisoformat(task.end_time).strftime("%Y-%m-%d")
            )
            for task in completed_tasks
        ))
        
        return {
            'count': synced,
            'sheets_updated': sorted(sheets_updated)
        }
