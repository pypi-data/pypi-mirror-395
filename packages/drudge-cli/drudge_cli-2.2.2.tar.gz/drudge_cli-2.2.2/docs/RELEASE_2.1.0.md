# Release Notes - Drudge CLI v2.1.0

**Release Date:** October 4, 2025

## 🎉 What's New in v2.1.0

This release focuses on improved usability, better help system integration, and powerful cleanup capabilities.

### 1. Native Help System Integration ✨

**Removed custom help command** - Now using Typer's built-in `--help` functionality for better consistency and native shell integration.

**Before (v2.0.x):**
```bash
drudge help              # Custom help command
```

**Now (v2.1.0):**
```bash
drudge --help            # Native Typer help
drudge COMMAND --help    # Command-specific help
```

**Benefits:**
- Better shell integration
- Consistent with standard CLI conventions
- Automatic help generation for all commands
- Reduced code maintenance burden

### 2. Enhanced End Command with --all Flag 🏁

The `end` command now has more granular control over which tasks to end.

**Default Behavior (unchanged):**
```bash
drudge end               # Ends only ACTIVE tasks
```

**New --all Option:**
```bash
drudge end --all         # Ends ALL tasks (active + paused)
```

**How it works:**
- `drudge end` (no args) → Ends only active tasks, paused tasks remain untouched
- `drudge end --all` → Resumes all paused tasks first, then ends everything

**Example Workflow:**
```bash
$ drudge list
🔥 ACTIVE TASKS:
  • Active Task (Running: 01:30:00)

⏸️  PAUSED TASKS:
  • Paused Task

$ drudge end
✅ Ended 1 task(s) successfully  # Only Active Task ended

$ drudge list
⏸️  PAUSED TASKS:
  • Paused Task                  # Paused task remains

$ drudge end --all
▶️ Resumed 'Paused Task'
🏁 Completed 'Paused Task'
✅ Ended 1 task(s) successfully  # Paused task resumed and ended
```

### 3. Powerful Clean Command 🗑️

New `clean` command to erase worklog entries with automatic backup and safety features.

**Clean by Date:**
```bash
drudge clean 2025-10-03
# Removes all entries for that date
# Deletes the daily file (2025-10-03.txt)
```

**Clean by Task (all dates):**
```bash
drudge clean "Bug fix #123"
# Removes all "Bug fix #123" entries across all dates
# Rebuilds affected daily files without those entries
```

**Clean by Task + Date:**
```bash
drudge clean "Meeting" --date 2025-10-03
# Removes only "Meeting" entries from 2025-10-03
# Keeps other tasks from that date
# Rebuilds 2025-10-03.txt without "Meeting"
```

**Clean Everything:**
```bash
drudge clean --all
⚠️  This will clean ALL worklog entries!
Are you sure you want to continue? [y/N]: y
✅ Cleaned 50 entries and 10 daily files
💾 Backup created for safety
```

**Safety Features:**
- ✅ **Automatic backups** before any deletion
- ✅ **Confirmation prompt** for `--all` option
- ✅ **Smart daily file rebuild** when partially cleaning
- ✅ **Backup location**: `~/.worklog/daily/` directory

**Use Cases:**
- Remove test/debug entries
- Clean up accidental entries
- Reset worklog for new project/period
- Remove sensitive task names from history

## 📊 Technical Improvements

### Code Quality
- All 39 test cases passing ✅
- Clean separation of concerns (clean methods in WorkLog manager)
- Proper error handling with user-friendly messages
- Type-safe implementation with full type hints

### Performance
- Efficient daily file rebuilding (only affected dates)
- Optimized entry filtering
- Minimal I/O operations

### Maintainability
- Well-documented clean methods in `worklog.py`
- Reusable backup creation through `BackupManager`
- Consistent CLI patterns using Typer decorators

## 🔄 Migration Guide

### From v2.0.x to v2.1.0

**No breaking changes!** All existing commands work exactly as before.

**Optional Changes:**
1. **Help Command**: Replace `drudge help` with `drudge --help` in scripts
2. **End All**: Use `drudge end --all` when you want to end paused tasks too

**New Features Available:**
- Use `drudge clean` to manage worklog entries
- Use `drudge end --all` for comprehensive cleanup
- Use `drudge COMMAND --help` for command-specific help

## 📚 Updated Documentation

- Updated README.md with new command reference
- Created CHANGELOG.md for version tracking
- Added this release notes document (RELEASE_2.1.0.md)

## 🐛 Bug Fixes

- Fixed `DailyFileManager.format_entry()` signature in clean operations
- Improved daily file rebuild logic for partial cleaning
- Better error messages for clean command validation

## 🙏 Acknowledgments

Thanks to all users who provided feedback and feature requests that shaped this release!

## 📝 Full Changelog

See [CHANGELOG.md](../CHANGELOG.md) for detailed version history.

---

**Installation:**
```bash
pip install drudge-cli==2.1.0
```

**Upgrade:**
```bash
pip install --upgrade drudge-cli
```

**Verify:**
```bash
drudge version
# Output: Version: 2.1.0 (Enhanced CLI)
```
