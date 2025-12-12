# Google Sheets Structure for Drudge Sync

This document describes the Google Sheets structure used by drudge for syncing work tasks. The structure is **haunts-compatible**, meaning if you use [haunts](https://github.com/keul/haunts), it can read this sheet and sync to Google Calendar.

## 📊 Sheet Structure

### **Document Structure**

Your Google Spreadsheet should contain:

1. **Config Sheet** (default name: `config`)
   - Maps project names to Google Calendar IDs
   - Required for haunts Calendar sync (optional for drudge)

2. **Monthly Sheets** (named by month: `October`, `November`, etc.)
   - Each month has its own sheet tab
   - Contains work task entries

---

## 📋 Config Sheet Structure

**Sheet name:** `config` (customizable via `CONTROLLER_SHEET_NAME` in haunts.ini)

### Columns:

| Column A | Column B | Column C (optional) |
|----------|----------|---------------------|
| Calendar ID | Project Alias | Linked Calendar ID |

**Example:**
```
| Calendar ID                          | Project Alias | Linked Calendar ID |
|--------------------------------------|---------------|-------------------|
| primary                              | Backend       |                   |
| frontend-cal@group.calendar.google   | Frontend      |                   |
| devops@group.calendar.google.com     | DevOps        |                   |
```

**Notes:**
- **Calendar ID**: Google Calendar ID (e.g., `primary` or `email@group.calendar.google.com`)
- **Project Alias**: Short name used in task entries (must match drudge project names)
- **Linked Calendar ID**: Optional - for calendar aliases

---

## 📅 Monthly Sheet Structure

**Sheet names:** Use full month names: `January`, `February`, `March`, `April`, `May`, `June`, `July`, `August`, `September`, `October`, `November`, `December`

### Column Headers (Row 1):

| Column | Default Name | Description | Example |
|--------|--------------|-------------|---------|
| A | `Date` | Date in DD/MM/YYYY format | `04/10/2025` |
| B | `Start time` | Start time in HH:MM format | `09:30` |
| C | `Project` | Project name (from config sheet) | `Backend` |
| D | `Activity` | Task description | `Implement login API` |
| E | `Details` | Optional task details | `Added JWT authentication` |
| F | `Spent` | Duration in decimal hours | `2.5` or `2,5` |
| G | `Event id` | Google Calendar event ID (auto-filled by haunts) | - |
| H | `Link` | Link to calendar event (auto-filled by haunts) | - |
| I | `Action` | Action for haunts (`DELETE` or empty) | - |

**Customizable column names** (via haunts.ini):
- `PROJECT_COLUMN_NAME` (default: `Project`)
- `SPENT_COLUMN_NAME` (default: `Spent`)
- `ACTIVITY_COLUMN_NAME` (default: `Activity`)
- `START_TIME_COLUMN_NAME` (default: `Start time`)
- `DETAILS_COLUMN_NAME` (default: `Details`)
- `EVENT_ID_COLUMN_NAME` (default: `Event id`)
- `LINK_COLUMN_NAME` (default: `Link`)
- `ACTION_COLUMN_NAME` (default: `Action`)

---

## 🔄 Drudge Sync Behavior

### **What Drudge Writes:**

When syncing tasks, drudge writes the following columns:

1. **Date**: Task completion date in `DD/MM/YYYY` format
2. **Start time**: Task start time in `HH:MM` format (from drudge timestamps)
3. **Project**: Project name (from `--project` flag or config)
4. **Activity**: Task name/description
5. **Details**: *(Optional)* Additional task details
6. **Spent**: Duration in decimal hours (formatted according to config)

**Columns NOT written by drudge:**
- `Event id` - Filled by haunts when creating calendar events
- `Link` - Filled by haunts with calendar event link
- `Action` - Used by haunts for sync control (`DELETE`, `IGNORE`, etc.)

### **Duration Formatting:**

Drudge formats duration based on your config:

```yaml
google_sheets:
  hours_decimal: 1      # Decimal places
  round_hours: 0.25     # Round to 15 minutes
```

**Examples:**
- Task duration: 2h 47m
- With `hours_decimal: 1`, `round_hours: 0.25` → `2.75` (2h 45m)
- With `hours_decimal: 2`, `round_hours: 0.5` → `2.50` (2h 30m)
- With `hours_decimal: 0`, `round_hours: 1.0` → `3` (3h)

**Decimal separator:** Uses comma (`,`) for European format, e.g., `2,5` hours

---

## 📝 Example Sheet Data

### **Config Sheet:**
```
| Calendar ID              | Project Alias |
|-------------------------|---------------|
| primary                 | Backend       |
| frontend@group.calendar | Frontend      |
| research@group.calendar | Research      |
```

### **October Sheet:**
```
| Date       | Start time | Project  | Activity              | Details           | Spent |
|------------|------------|----------|----------------------|-------------------|-------|
| 04/10/2025 | 09:00      | Backend  | Implement login API  | JWT auth          | 2,5   |
| 04/10/2025 | 11:30      | Frontend | Fix CSS layout       | Responsive design | 1,75  |
| 04/10/2025 | 14:00      | Backend  | Database migration   | PostgreSQL 15     | 3,0   |
```

---

## 🔗 Integration with Haunts

If you use **haunts** for Calendar sync:

1. **Drudge** writes tasks to Google Sheet (columns: Date, Start time, Project, Activity, Spent)
2. **Haunts** reads the sheet and:
   - Creates Google Calendar events
   - Fills `Event id` and `Link` columns
   - Marks `Action` as `IGNORE` (processed)

**Without haunts:**
- Drudge still writes to the sheet
- You have a time-tracking spreadsheet
- No calendar sync (unless you implement it yourself)

---

## 🛠️ Setup Instructions

### **For Haunts Users:**
1. Use your existing haunts Google Sheet
2. Drudge will auto-import `CONTROLLER_SHEET_DOCUMENT_ID` from `~/.haunts/haunts.ini`
3. Run `drudge config --setup` to configure sync

### **For Non-Haunts Users:**

1. **Create Google Spreadsheet:**
   - Create a new Google Sheet
   - Copy the Document ID from URL: `https://docs.google.com/spreadsheets/d/YOUR_DOCUMENT_ID/edit`

2. **Create Config Sheet:**
   - Create a sheet named `config`
   - Add headers: `Calendar ID` | `Project Alias`
   - Add your projects (Calendar ID can be empty if not using haunts)

3. **Create Monthly Sheets:**
   - Create sheets named: `January`, `February`, `March`, etc.
   - Add headers (Row 1): `Date | Start time | Project | Activity | Details | Spent`

4. **Configure Drudge:**
   ```bash
   drudge config --setup
   # Enter your Google Sheet Document ID
   # Configure projects to match your sheet
   ```

5. **Grant Permissions:**
   - Share the Google Sheet with your Google account
   - Enable Google Sheets API in Google Cloud Console
   - Create OAuth credentials (or use service account)

---

## 🔐 Authentication

Drudge uses **Google Sheets API** for sync. You'll need:

1. **Google Cloud Project** with Sheets API enabled
2. **OAuth 2.0 credentials** (or service account key)
3. **Credentials file** at `~/.worklog/credentials.json`

See [Google Sheets API Quickstart](https://developers.google.com/sheets/api/quickstart/python) for setup.

---

## 📚 References

- **Haunts:** https://github.com/keul/haunts
- **Google Sheets API:** https://developers.google.com/sheets/api
- **Drudge Config:** Run `drudge config --show` to see your configuration
