# Usage Examples - Error Log Classifier

This document contains real-world usage examples.

## Example 1: Basic Analysis

Analyze a log file and generate all reports:

```bash
python main.py analyze data/application.log -o output/analysis_1
```

**Output:**
- `error_analysis_20241201_101530.csv`
- `error_analysis_20241201_101530.json`
- `error_analysis_20241201_101530.html`

**What happens:**
1. Reads the entire log file
2. Normalizes error messages
3. Groups similar errors into clusters
4. Ranks by frequency
5. Exports to three formats

---

## Example 2: Filter Critical Errors

Only analyze CRITICAL and FATAL errors, ignore everything else:

```bash
python main.py analyze data/application.log -o output/critical_analysis -i "CRITICAL|FATAL"
```

This creates focused reports showing only the most severe issues.

---

## Example 3: Exclude Noise

Analyze logs but ignore debugging output:

```bash
python main.py analyze data/application.log -o output/clean_analysis -e "DEBUG|TRACE|INFO"
```

The `-e` flag (exclude) removes lines matching the pattern, reducing noise.

---

## Example 4: Keyword Filtering

Find only database-related errors:

```bash
python main.py analyze data/application.log -o output/db_errors -k database connection sql
```

**What this does:**
- Only includes lines containing "database" OR "connection" OR "sql"
- Useful for narrowing down to specific subsystems
- Can use multiple keywords

---

## Example 5: Process Large File in Batches

For a multi-GB log file, process only the first 500,000 lines:

```bash
python main.py analyze data/huge.log -o output/first_batch -m 500000
```

This prevents memory issues and lets you analyze recent logs first.

---

## Example 6: Time-Based Bucketing

Group errors by hour for trend analysis:

```bash
python main.py analyze data/application.log -o output/time_analysis -t 60
```

Each error cluster is bucketed by the hour it occurred in, helping identify when issues happen.

---

## Example 7: Combination - Everything

Complex analysis with multiple filters:

```bash
python main.py analyze data/application.log \
  -o output/complex_analysis \
  -i "ERROR|CRITICAL" \
  -e "DEBUG|TEST" \
  -k "database" "timeout" \
  -m 1000000
```

This:
- ✓ Includes only ERROR and CRITICAL
- ✓ Excludes DEBUG and TEST lines
- ✓ Only keeps lines with "database" or "timeout"
- ✓ Processes first 1M lines only

---

## Example 8: Regression Detection - Full Workflow

Track what changed between two application versions.

### Step 1: Analyze Pre-Deployment Logs

```bash
python main.py analyze logs/v1.4.0.log -o output/v1.4.0_analysis
```

This creates: `output/v1.4.0_analysis/error_analysis_*.json`

### Step 2: Deploy New Version and Analyze

```bash
python main.py analyze logs/v1.5.0.log -o output/v1.5.0_analysis
```

This creates: `output/v1.5.0_analysis/error_analysis_*.json`

### Step 3: Compare Results

```bash
python main.py diff output/v1.4.0_analysis/error_analysis_20241201_101530.json \
               output/v1.5.0_analysis/error_analysis_20241201_102145.json \
               -o output/regression_report
```

**Output shows:**
- 🆕 **NEW PATTERNS** - Never seen before errors in v1.5.0
- 🔴 **REGRESSIONS** - Errors that happened more frequently
- ✅ **RESOLVED** - Errors from v1.4.0 that no longer appear
- 📊 **CHANGES** - Frequency changes for existing patterns

---

## Example 9: Database Connection Issues

Team needs to understand database connectivity problems:

```bash
python main.py analyze data/errors.2024-12-01.log \
  -o output/db_connectivity \
  -k "database" "connection" "timeout" "refused" "unreachable"
```

Then share the HTML report with the DBA team.

---

## Example 10: Authentication & Security

Security team investigates unauthorized access attempts:

```bash
python main.py analyze data/security.log \
  -o output/auth_issues \
  -k "auth" "permission" "denied" "invalid" "unauthorized" \
  -i "ERROR|CRITICAL"
```

The CSV export can be imported into their security dashboard.

---

## Example 11: Performance Issues

Operations team identifies slow/timeout errors:

```bash
python main.py analyze data/application.log \
  -o output/perf_issues \
  -k "timeout" "slow" "exceeded" "limit" "memory" "cpu" \
  -e "DEBUG" \
  -m 500000
```

---

## Example 12: Nightly Automated Analysis

Script for automated nightly analysis (save as `nightly_analysis.ps1`):

```powershell
# Configuration
$logFile = "C:\logs\application.$(Get-Date -Format 'yyyy-MM-dd').log"
$outputDir = "C:\reports\analysis_$(Get-Date -Format 'yyyy-MM-dd')"
$archiveDir = "C:\reports\archives\"

# Run analysis
Write-Host "Starting error analysis..."
python main.py analyze $logFile -o $outputDir -e "DEBUG|TRACE"

# Archive previous reports
if (Test-Path $outputDir) {
    Copy-Item -Path "$outputDir\*.html" -Destination $archiveDir
}

# Open latest HTML report
$htmlReport = Get-ChildItem "$outputDir\*.html" | Sort-Object LastWriteTime | Select-Object -Last 1
if ($htmlReport) {
    Invoke-Item $htmlReport.FullName
}

Write-Host "Analysis complete!"
```

Schedule this with Windows Task Scheduler to run every night at 2 AM.

---

## Example 13: Email Results

After analysis, email the CSV to stakeholders:

```powershell
# Run analysis
python main.py analyze data/application.log -o output/daily

# Get the latest CSV file
$csvFile = Get-ChildItem "output/daily/*.csv" | Sort-Object LastWriteTime | Select-Object -Last 1

# Email it (requires email configuration)
# $EmailParams = @{
#     To = "team@company.com"
#     From = "reports@company.com"
#     Subject = "Daily Error Analysis - $(Get-Date -Format 'yyyy-MM-dd')"
#     Body = "See attached error report"
#     Attachments = $csvFile.FullName
#     SmtpServer = "smtp.company.com"
# }
# Send-MailMessage @EmailParams
```

---

## Example 14: Compare Multiple Days

Track error trends across a week:

```bash
# Monday
python main.py analyze logs/monday.log -o output/monday

# Tuesday
python main.py analyze logs/tuesday.log -o output/tuesday

# Wednesday
python main.py analyze logs/wednesday.log -o output/wednesday

# Compare Mon vs Tue
python main.py diff output/monday/error_analysis_*.json \
               output/tuesday/error_analysis_*.json \
               -o output/mon_vs_tue

# Compare Tue vs Wed
python main.py diff output/tuesday/error_analysis_*.json \
               output/wednesday/error_analysis_*.json \
               -o output/tue_vs_wed
```

Create a spreadsheet summarizing the diffs to see trends.

---

## Example 15: Parse Specific Log Format

If your logs have custom format, use regex filtering:

```bash
# Only logs from specific service
python main.py analyze data/all.log \
  -o output/payment_service \
  -i "PaymentService|payment_service" \
  -e "DEBUG"

# Only logs from specific host
python main.py analyze data/all.log \
  -o output/host_server05 \
  -i "host=server05|server05:"

# Only logs between certain times
python main.py analyze data/all.log \
  -o output/peak_hours \
  -i "10:[0-5][0-9]|11:|12:|13:|14:" \
  -e "DEBUG"
```

---

## Performance Tips

### Tip 1: Process Recent Logs First
```bash
# Get last 1M lines of a large file, analyze recent data
tail -n 1000000 huge.log > recent.log
python main.py analyze recent.log -o output/recent
```

### Tip 2: Pre-filter with System Tools
```bash
# Filter with grep before passing to classifier
grep "ERROR\|CRITICAL" application.log > errors_only.log
python main.py analyze errors_only.log -o output/errors
```

### Tip 3: Split and Parallelize
```bash
# Split file into parts
split -n l/5 application.log part_

# Analyze each part separately
python main.py analyze part_aa -o output/part1
python main.py analyze part_ab -o output/part2
# ... etc
```

---

## Reading the Reports

### HTML Report Guide
1. **Summary Cards** - High-level statistics at the top
2. **Top Offenders Table** - Most frequent errors, click for details
3. **Sample Line** - Shows actual error message (truncated)
4. **Line Numbers** - Where to find this error in the log

### CSV Report Usage
1. Open in Excel
2. Sort by `occurrence_count` (descending) to see worst offenders
3. Use Filter to search for specific patterns
4. Create pivot tables for analysis
5. Share with team members

### JSON Report Usage
1. Import into dashboard systems
2. Parse programmatically for alerts
3. Archive for historical analysis
4. Use for diff comparisons

### Diff Report Guide
1. Look for 🔴 **REGRESSIONS** first
2. Check 🆕 **NEW PATTERNS** for unexpected errors
3. Verify ✅ **RESOLVED** patterns are actually fixed
4. Review percentage changes for significant differences

---

## Troubleshooting Examples

### Not Finding Expected Errors
```bash
# First, verify the errors exist in the file
grep -i "your_error_keyword" data/application.log | wc -l

# Then analyze without filters to see everything
python main.py analyze data/application.log -o output/debug

# Check if the keyword is there
grep -i "your_error_keyword" output/debug/error_analysis_*.json
```

### Report Takes Too Long
```bash
# Reduce data volume
python main.py analyze data/huge.log -o output -m 100000

# Filter to specific patterns only
python main.py analyze data/huge.log -o output -i "ERROR|CRITICAL"
```

### CSV is Empty
```bash
# Check if any clusters were found
python main.py analyze data/application.log -o output

# Verify JSON file has top_clusters
cat output/error_analysis_*.json | grep "top_clusters"
```

---

## Integration Examples

### Grafana Dashboard Integration

```python
import json

# Load analysis JSON
with open('analysis.json') as f:
    data = json.load(f)

# Extract metrics for Grafana
metrics = {
    'total_errors': data['summary']['total_lines'],
    'unique_patterns': data['summary']['total_clusters'],
    'top_error': data['top_clusters'][0]['signature'],
    'top_error_count': data['top_clusters'][0]['count'],
}

print(json.dumps(metrics))
```

### Splunk Integration

```bash
# Export results and upload to Splunk
python main.py analyze app.log -o output
cat output/*.json | curl -X POST https://splunk:8088/services/collector \
  -H "Authorization: Splunk $TOKEN" \
  -d @-
```

### Slack Notification

```python
import json
import requests

# Load report
with open('analysis.json') as f:
    report = json.load(f)

# Create Slack message
message = f"""
📊 Error Analysis Complete
• Total Clusters: {report['summary']['total_clusters']}
• Total Errors: {report['summary']['total_lines']:,}
• Top Issue: {report['top_clusters'][0]['signature']}
  Occurred {report['top_clusters'][0]['count']} times
"""

# Send to Slack
requests.post('https://hooks.slack.com/...', json={'text': message})
```

---

## More Help

- See **README.md** for complete reference
- Run `python main.py info` for project info
- Run `python main.py analyze --help` for command options

