#!/usr/bin/env python3
"""Quick test to verify HOME environment changes work correctly."""

import os
import tempfile
from pathlib import Path

# Test 1: Check current HOME
print(f"1. Current HOME: {os.environ.get('HOME')}")
print(f"2. Path.home(): {Path.home()}")

# Test 2: Change HOME
test_dir = tempfile.mkdtemp()
print(f"\n3. Created temp dir: {test_dir}")

os.environ['HOME'] = test_dir
print(f"4. Set HOME to: {os.environ.get('HOME')}")
print(f"5. Path.home() after change: {Path.home()}")

# Test 3: Create .worklog structure
worklog_dir = Path(test_dir) / '.worklog'
worklog_dir.mkdir(parents=True, exist_ok=True)
(worklog_dir / 'daily').mkdir(parents=True, exist_ok=True)

print(f"\n6. Created: {worklog_dir}")
print(f"7. Exists: {worklog_dir.exists()}")
print(f"8. Daily dir exists: {(worklog_dir / 'daily').exists()}")

# Test 4: Now test with actual CLI
print("\n9. Testing with actual CLI import...")
from src.worklog.cli.commands import app
from typer.testing import CliRunner

runner = CliRunner()
result = runner.invoke(app, ["start", "Test"])
print(f"10. Exit code: {result.exit_code}")
print(f"11. Output: {result.stdout[:200]}")
if result.exit_code != 0:
    print(f"12. Error output: {result.stderr if hasattr(result, 'stderr') else 'N/A'}")
