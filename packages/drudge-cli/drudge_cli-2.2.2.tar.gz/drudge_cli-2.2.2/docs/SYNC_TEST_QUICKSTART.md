# 🧪 Google Sheets Sync Testing - Quick Start

## What We've Built

I've created a complete integration testing setup for your Google Sheets sync functionality:

### ✅ Files Created
1. **`test_sync_integration.py`** - Integration test script that performs real sync
2. **`test-config.yaml.example`** - Template configuration file  
3. **`docs/SYNC_TESTING.md`** - Complete setup and testing guide
4. **`.gitignore`** - Updated to protect sensitive credentials

### ✅ Files Updated
- **`ToDo.md`** - Test count updated (39 → 47)
- **`README.md`** - Test count updated (39 → 47)  
- **`CHANGELOG.md`** - Test count updated (39 → 47)

---

## 🚀 What You Need to Do

### Step 1: Create Test Google Sheet (10 minutes)

Follow the instructions in `docs/GOOGLE_SHEETS_STRUCTURE.md`:

1. **Create new Google Sheet** (name it "Drudge Test Sheet")
2. **Add Config sheet:**
   - Sheet name: `config`
   - Headers: `Calendar ID | Project Alias`
   - Add row: `primary | TestProject`

3. **Add Monthly sheets:**
   - Create sheet: `October` (current month)
   - Create sheet: `November` (next month)
   - Headers for both: `Date | Start time | Project | Activity | Details | Spent`

4. **Get Document ID:**
   - Copy from URL: `https://docs.google.com/spreadsheets/d/YOUR_DOCUMENT_ID/edit`

### Step 2: Create Service Account (15 minutes)

1. **Google Cloud Console:** https://console.cloud.google.com/
2. **Enable Google Sheets API** (APIs & Services → Library)
3. **Create Service Account:**
   - Name: `drudge-test-sync`
   - Create JSON key → Save as `test-credentials.json` in project root
4. **Share your test sheet** with service account email (Editor permission)

### Step 3: Create Config File (2 minutes)

```bash
# Copy template
cp test-config.yaml.example test-config.yaml

# Edit and replace YOUR_TEST_SHEET_DOCUMENT_ID with your actual Document ID
nano test-config.yaml  # or use your favorite editor
```

### Step 4: Run Integration Test (1 minute)

```bash
# Build Docker image (if not already built)
docker build -f Dockerfile.test -t drudge-test .

# Run integration test with mounted credentials
docker run --rm \
  -v $(pwd)/test-credentials.json:/app/test-credentials.json:ro \
  -v $(pwd)/test-config.yaml:/app/test-config.yaml:ro \
  drudge-test python test_sync_integration.py
```

### Step 5: Verify Results

The test will:
1. ✅ Create a test task
2. ✅ Sync to your Google Sheet
3. ✅ Verify data in the sheet
4. ✅ Clean up test data

**Check the output** - you should see:
```
✅ INTEGRATION TEST PASSED!
```

**Manually verify** in your test Google Sheet:
- Open the `October` sheet
- Look for test task with today's date

---

## 📚 Documentation

For detailed instructions, see:
- **`docs/SYNC_TESTING.md`** - Complete setup guide with troubleshooting
- **`docs/GOOGLE_SHEETS_STRUCTURE.md`** - Sheet structure reference

---

## 🔐 Security Reminders

- ✅ `test-credentials.json` is in `.gitignore` (don't commit!)
- ✅ `test-config.yaml` is in `.gitignore` (don't commit!)
- ✅ Use separate test sheet (never production!)
- ✅ Use separate service account (test only!)

---

## ❓ Having Issues?

Common problems and solutions:

**"Credentials not found"**
→ Make sure `test-credentials.json` exists and Docker volume mount is correct

**"Permission denied"**  
→ Share test Google Sheet with service account email (Editor permission)

**"Sheet not found: October"**
→ Create monthly sheets with current month name

**Full troubleshooting guide:** See `docs/SYNC_TESTING.md`

---

## 🎯 Next Steps After Testing

Once sync test passes:
1. ✅ Move on to test infrastructure refactoring (tests/ directory)
2. ✅ Create reusable GitHub Actions workflows  
3. ✅ Prepare v2.2.0 release with Google Sheets sync!

---

**Questions?** All detailed instructions are in `docs/SYNC_TESTING.md`
