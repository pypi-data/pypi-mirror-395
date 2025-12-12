# 🚀 Getting Started - Error Log Classifier

Welcome! You have a complete, production-ready error log analysis tool. Here's how to get started immediately.

## ⚡ 30-Second Start

```bash
# 1. Run analysis
python main.py analyze data/sample_errors.log -o output

# 2. Open the HTML report
start output/error_analysis_*.html
```

That's it! You're now analyzing error logs. 🎉

---

## 📊 What You Just Did

When you ran that command:

1. ✅ Read 47 error lines
2. ✅ Normalized variable data (IPs, paths, numbers)
3. ✅ Grouped similar errors (32 clusters)
4. ✅ Ranked by frequency (Database errors: #1 with 16 occurrences)
5. ✅ Generated 3 reports (CSV, JSON, HTML)

---

## 🎨 View Your Results

### Option 1: Beautiful HTML Dashboard (Recommended)
```bash
start output/error_analysis_*.html
```
Shows summary cards, top 10 errors, statistics with professional styling.

### Option 2: CSV in Excel
```bash
start output/error_analysis_*.csv
```
Import directly to spreadsheet, sort, filter, and pivot.

### Option 3: JSON for Programmatic Use
```bash
# View raw JSON
type output/error_analysis_*.json
```

---

## 📝 Next: Modify & Test

### Test 1: Add More Database Errors

```bash
# 1. Open the sample log
notepad data/sample_errors.log

# 2. Add 6 more lines like this at the end:
[2024-12-01 10:29:00.123] ERROR: Database connection timeout at server 192.168.1.116
[2024-12-01 10:29:15.456] ERROR: Database connection timeout at server 192.168.1.117
[2024-12-01 10:29:30.789] ERROR: Database connection timeout at server 192.168.1.118
[2024-12-01 10:29:45.012] ERROR: Database connection timeout at server 192.168.1.119
[2024-12-01 10:30:00.345] ERROR: Database connection timeout at server 192.168.1.120
[2024-12-01 10:30:15.678] ERROR: Database connection timeout at server 192.168.1.121

# 3. Save and close (Ctrl+S, Alt+F4)

# 4. Run analysis again
python main.py analyze data/sample_errors.log -o output

# 5. Check results - Database errors should jump from 16 to 22!
start output/error_analysis_*.html
```

**You just proved:** The tool dynamically responds to input changes. ✅

---

## 🔍 Test 2: Detect Regressions

### Step 1: Save Baseline
```bash
python main.py analyze data/sample_errors.log -o output/baseline

# Note the JSON filename for later
```

### Step 2: Remove Some Errors
```bash
# Edit data/sample_errors.log
notepad data/sample_errors.log

# Delete the last 6 lines you just added (or any category)
# Save and close
```

### Step 3: Run New Analysis
```bash
python main.py analyze data/sample_errors.log -o output/updated

# Note the new JSON filename
```

### Step 4: Compare
```bash
# Replace the filenames with what you noted above
python main.py diff output/baseline/error_analysis_20251204_*.json ^
               output/updated/error_analysis_20251204_*.json -o output/diff

# You'll see what changed!
```

**Result Example:**
```
Database errors: 22 → 16 (-27%)
NullPointerException: still 5
RESOLVED: No new errors
```

---

## 📚 Complete Usage Guide

### Basic Analysis
```bash
# Analyze a log file and get all reports
python main.py analyze <logfile> -o <output_dir>

Example:
python main.py analyze /var/log/app.log -o daily_report
```

### With Filters
```bash
# Only CRITICAL and ERROR, skip DEBUG
python main.py analyze app.log -o output -i "ERROR|CRITICAL"

# Focus on specific keywords
python main.py analyze app.log -o db_issues -k database connection timeout

# Exclude noise
python main.py analyze app.log -o clean -e "DEBUG|INFO|TRACE"
```

### Compare Two Runs
```bash
python main.py diff baseline.json current.json -o comparison
```

### Get Help
```bash
python main.py info              # Project information
python main.py analyze --help    # Analyze command help
python main.py diff --help       # Diff command help
```

---

## 📖 Documentation Quick Links

| For... | Read... | Time |
|--------|---------|------|
| **Overview** | `README.md` | 10 min |
| **Quick Start** | `QUICKSTART.md` | 5 min |
| **Examples** | `docs/EXAMPLES.md` | 15 min |
| **Testing** | `docs/DYNAMIC_TESTING.md` | 10 min |
| **Deep Dive** | `docs/ARCHITECTURE.md` | 20 min |
| **Everything** | `docs/INDEX.md` | 10 min |

---

## 🎯 Common Workflows

### Workflow 1: Daily Log Analysis

**Run Every Morning:**
```bash
python main.py analyze "logs/$(date +\%Y-\%m-\%d).log" -o daily_report
```

**Result:** Dashboard showing today's top errors

### Workflow 2: After Deployment

**Before Deployment:**
```bash
python main.py analyze logs/production.log -o /backup/pre_deploy
```

**After Deployment:**
```bash
python main.py analyze logs/production.log -o /backup/post_deploy
```

**Compare:**
```bash
python main.py diff /backup/pre_deploy/report.json \
               /backup/post_deploy/report.json -o /reports/deployment_impact
```

**Result:** See if deployment caused regressions

### Workflow 3: Investigate Database Issues

```bash
# Find only database-related errors
python main.py analyze production.log -o db_report \
  -k "database" "connection" "timeout" "pool"

# Result: CSV you can email to database team
# "Hey, we have 156 database connection timeouts"
```

---

## 💡 Key Concepts

### 1. Normalization
The tool replaces variable data with placeholders:
- `192.168.1.100` → `<IP>`
- `user_12345` → `user_<NUM>`
- `/var/log/app.log` → `<PATH>`

**Why?** Groups similar errors that differ only in data.

### 2. Clustering
Similar errors are grouped by signature:
```
All of these cluster together:
- Connection to 192.168.1.1 failed
- Connection to 192.168.1.2 failed
- Connection to 192.168.1.3 failed

Into one: "Database|connection to <IP> failed"
```

### 3. Ranking
Clusters are sorted by frequency:
```
1. Database errors: 16 occurrences (38% of all)
2. NullPointerException: 5 occurrences (12%)
3. Auth failures: 4 occurrences (9%)
...
```

### 4. Diff Analysis
Compare two runs to detect:
- **Regressions:** Errors increased (⚠️)
- **Improvements:** Errors decreased (✅)
- **New Issues:** Never seen before (🔴)
- **Resolved:** Fixed errors (🟢)

---

## 🔧 Troubleshooting

### Issue: "File not found"
**Solution:** Check the path is correct
```bash
# Make sure the file exists
dir data/sample_errors.log

# If it doesn't, create it or use correct path
python main.py analyze ./logs/error.log -o output
```

### Issue: No errors found
**Solution:** Your filter might be too strict
```bash
# Try without filters
python main.py analyze logs/error.log -o output

# Or loosen the filter
python main.py analyze logs/error.log -o output -i "ERROR|WARN|CRITICAL"
```

### Issue: "Output directory"
**Solution:** It will be created automatically, or create it manually
```bash
mkdir output
python main.py analyze logs/error.log -o output
```

---

## 🎓 Learning Exercises

### Exercise 1: Understand Normalization
1. Edit `data/sample_errors.log`
2. Change IP from `192.168.1.100` to `10.0.0.1`
3. Run analysis - notice it clusters with other IPs ✅

### Exercise 2: Test Frequency Ranking
1. Add 10 more copies of any error line
2. Run analysis
3. That error jumps higher in ranking ✅

### Exercise 3: Track Improvements
1. Save baseline with `diff` output
2. Remove one error category entirely
3. Run diff - shows you improved ✅

### Exercise 4: Filter Specific Issues
1. Run with `-k "database"` - only DB errors
2. Run with `-i "CRITICAL"` - only critical
3. Run with `-e "DEBUG"` - skip debug ✅

---

## 🚀 Advanced Usage

### Process Large File in Chunks
```bash
# Only read first 1M lines
python main.py analyze huge.log -o output -m 1000000
```

### Export Results to Team
```bash
# Generate CSV that team can import
python main.py analyze app.log -o output
# Send: output/error_analysis_*.csv to your team
```

### Automate Daily Reports
```powershell
# Save as daily_analysis.ps1
$date = Get-Date -Format "yyyy-MM-dd"
python main.py analyze "logs/$date.log" -o "reports/$date"
start "reports/$date/error_analysis_*.html"
```

### Track Weekly Trends
```bash
# Monday
python main.py analyze logs/monday.log -o monday

# Friday
python main.py analyze logs/friday.log -o friday

# Compare
python main.py diff monday/report.json friday/report.json -o weekly
# See what changed over the week!
```

---

## 💾 What Gets Generated

### Files Created
```
output/
├── error_analysis_20251204_123135.csv    # Spreadsheet format
├── error_analysis_20251204_123135.json   # Complete data
└── error_analysis_20251204_123135.html   # Dashboard
```

### What's in Each File

**CSV:**
- Rank, signature, count, sample line, line numbers
- Ready to sort, filter, and pivot in Excel

**JSON:**
- Full clustering data
- All line numbers
- Complete statistics
- Perfect for programmatic use

**HTML:**
- Professional dashboard
- Summary statistics cards
- Top 10 errors table
- Responsive design
- Print-friendly

---

## ✨ Pro Tips

### Tip 1: View HTML Reports Beautifully
The HTML files have embedded CSS and styling. Open them in any browser.

### Tip 2: Keep JSON for Diffs
Save JSON reports to compare between runs and detect regressions.

### Tip 3: Use CSV for Team Sharing
Non-technical team members can open CSV in Excel and understand the results.

### Tip 4: Filter Before Analysis
Use `-k` and `-e` flags to focus on relevant errors, cleaner results.

### Tip 5: Check Sample Lines
Each error includes actual sample lines so you can see the real errors.

---

## 🎉 You're Ready!

You now understand:
- ✅ How to run analysis
- ✅ How to view results
- ✅ How to modify and test
- ✅ How to compare runs
- ✅ How to track improvements

**Next:** Pick a workflow above and start analyzing your logs!

---

## 📞 Need More Help?

- **Quick commands** → `python main.py info`
- **Examples** → Read `docs/EXAMPLES.md`
- **Testing** → Read `docs/DYNAMIC_TESTING.md`
- **Deep dive** → Read `docs/ARCHITECTURE.md`
- **Full index** → Read `docs/INDEX.md`

---

## 🎯 Quick Command Reference

```bash
# Analyze
python main.py analyze data/sample_errors.log -o output

# View help
python main.py analyze --help

# With filters
python main.py analyze app.log -o output -k "error_type"

# Compare runs
python main.py diff report1.json report2.json -o comparison

# Project info
python main.py info
```

---

Happy analyzing! 🚀

For questions or issues, check the documentation files in `docs/` folder.

