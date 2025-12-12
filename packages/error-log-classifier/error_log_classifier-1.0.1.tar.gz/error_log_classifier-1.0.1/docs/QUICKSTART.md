# Quick Start Guide - Error Log Classifier

## 5-Minute Setup

### 1. Download/Clone Project
```
Already in: c:\Users\Asus\ELC-PH
```

### 2. Test Installation
```powershell
python main.py info
```

You should see the project information displayed.

### 3. Run Sample Analysis
```powershell
python main.py analyze data/sample_errors.log -o output
```

This will create:
- `output/error_analysis_[timestamp].csv` - Spreadsheet-friendly format
- `output/error_analysis_[timestamp].json` - Machine-readable format
- `output/error_analysis_[timestamp].html` - Beautiful dashboard report

### 4. View Results

**HTML Report** (Recommended for visualization):
```powershell
# On Windows, open the HTML file
start output/error_analysis_*.html
```

**CSV Report** (Open in Excel):
```powershell
# Open the CSV file
start output/error_analysis_*.csv
```

## Common Use Cases

### Use Case 1: Find Database Connection Issues

```powershell
python main.py analyze data/error.log -o output -k "database" "connection" "timeout"
```

**What you'll get:**
- Top 10 database connection error patterns
- How many times each pattern occurred
- Sample lines showing the actual error
- HTML report with visualization

### Use Case 2: Focus on Critical Errors Only

```powershell
python main.py analyze data/error.log -o output -i "CRITICAL|FATAL"
```

### Use Case 3: Ignore INFO/DEBUG Messages

```powershell
python main.py analyze data/error.log -o output -e "DEBUG|INFO|TRACE"
```

### Use Case 4: Check Latest Issues (First 100k lines)

```powershell
python main.py analyze data/error.log -o output -m 100000
```

### Use Case 5: Compare Before/After (Regression Detection)

```powershell
# Step 1: First analysis (before deployment)
python main.py analyze logs/before.log -o output/before

# Step 2: Second analysis (after deployment)
python main.py analyze logs/after.log -o output/after

# Step 3: Compare them
python main.py diff output/before/error_analysis_*.json output/after/error_analysis_*.json -o output/comparison
```

This will show:
- ✅ What improved (fixed bugs)
- 🔴 What got worse (regressions)
- 🆕 New errors that appeared

## Understanding the Output

### HTML Report Sections

1. **Summary Cards** (Top)
   - Total Clusters: How many unique error patterns
   - Lines Analyzed: Total error lines processed
   - Avg Cluster Size: Average times each pattern appears
   - Largest Cluster: Most frequent error

2. **Top Offenders Table**
   - Shows the 10 most frequent error patterns
   - Click any signature to see the full text
   - Sample line shows an actual example

### CSV Report Columns

| Column | Meaning |
|--------|---------|
| rank | Position in frequency ranking (1=most common) |
| signature | Normalized error pattern |
| occurrence_count | How many times this error appeared |
| sample_line | Example of the actual error |
| first_10_line_numbers | Line numbers where this pattern appears |
| total_line_count | Total occurrences of this pattern |

### JSON Report Structure

```json
{
  "summary": {
    "total_clusters": 25,
    "total_lines": 5000,
    "average_cluster_size": 200.0
  },
  "top_clusters": [
    {
      "signature": "database|connection to <IP> failed",
      "count": 850,
      "sample_lines": ["Connection failed..."],
      "line_numbers": [1, 2, 3, ...]
    }
  ]
}
```

## Tips & Tricks

### Tip 1: Process Large Files in Batches

If you have a 10GB log file:
```powershell
# Process first 1 million lines
python main.py analyze data/huge.log -o output/batch1 -m 1000000

# Then next million
# (manually edit file or use head/tail on command line)
```

### Tip 2: Export CSV Directly to Excel

```powershell
# The CSV will open in Excel automatically
start output/error_analysis_*.csv
```

Then you can:
- Sort by occurrence_count
- Filter by signature
- Create pivot tables
- Share with team

### Tip 3: Automate Daily Analysis

Create a batch script `daily_analysis.ps1`:
```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd"
python main.py analyze "logs/$timestamp.log" -o "output/$timestamp" -e "DEBUG|TRACE"
Write-Host "Analysis complete. Opening report..."
start "output/$timestamp/error_analysis_*.html"
```

Then schedule it daily with Windows Task Scheduler.

### Tip 4: Find Specific Issues

```powershell
# All database-related errors
python main.py analyze data/error.log -o db_analysis -k "database"

# All authentication failures
python main.py analyze data/error.log -o auth_analysis -k "auth" "permission" "denied"

# All timeout issues
python main.py analyze data/error.log -o timeout_analysis -k "timeout"
```

### Tip 5: Track Improvements

```powershell
# Keep a baseline from Monday
python main.py analyze "logs/monday.log" -o baseline

# Compare against Friday
python main.py diff baseline/error_analysis_*.json \
               output/friday_analysis.json \
               -o weekly_comparison

# The report shows what improved vs what regressed
```

## Troubleshooting

### Problem: "No clusters found"
**Solution:** Your include/exclude filters might be too strict
```powershell
# Try without filters
python main.py analyze data/error.log -o output
```

### Problem: "File not found"
**Solution:** Check the path is correct
```powershell
# Use full path
python main.py analyze "C:\path\to\error.log" -o output
```

### Problem: HTML report looks plain
**Solution:** That's normal! The CSS is embedded. Open in Chrome/Firefox for best view.

### Problem: Output files not created
**Solution:** Check permissions and that output folder exists
```powershell
# Create output folder first
mkdir output

# Run again
python main.py analyze data/sample_errors.log -o output
```

## Performance Expectations

| File Size | Time | Memory |
|-----------|------|--------|
| 10MB | <1 sec | 20MB |
| 100MB | 5 sec | 50MB |
| 1GB | 40 sec | 100MB |
| 10GB | 7 min | 150MB |

Times are approximate on modern hardware (2020+).

## Next Steps

1. ✅ Run the sample analysis
2. 📊 View the HTML report in your browser
3. 📋 Open the CSV in Excel
4. 🔍 Try filtering with `-k` for your domain-specific errors
5. 📈 Set up daily automated analysis
6. 🔄 Compare runs to track regressions

## Need Help?

1. See README.md for detailed command reference
2. Run `python main.py info` for project overview
3. Run tests: `python -m pytest tests/` (if pytest installed)
4. Check generated JSON report for detailed data

---

Happy error hunting! 🎯

