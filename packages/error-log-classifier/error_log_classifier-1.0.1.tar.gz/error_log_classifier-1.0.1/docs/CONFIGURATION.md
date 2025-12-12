# Configuration & Customization Guide

This guide explains how to customize the Error Log Classifier for your specific needs.

## Adding Custom Normalization Patterns

Edit `src/signature_extractor.py` in the `__init__` method:

```python
self.patterns = [
    # Existing patterns...
    (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>'),
    
    # ADD YOUR CUSTOM PATTERNS HERE:
    (r'your_regex_pattern_here', '<YOUR_PLACEHOLDER>'),
]
```

### Examples

**Add your database connection string normalization:**
```python
(r'jdbc:[a-z]+://[^:]+:\d+/\w+', '<JDBC_URL>'),
```

**Add your internal service domain:**
```python
(r'\b(?:internal|staging|prod)\.company\.com\b', '<COMPANY_DOMAIN>'),
```

**Add error codes:**
```python
(r'ERR-\d{4}', '<ERR_CODE>'),
```

**Add AWS ARNs:**
```python
(r'arn:aws:[a-z0-9\-]+:\d{12}:', '<AWS_ARN>'),
```

## Customizing Error Type Detection

Edit `signature_extractor.py` `extract_error_type()` method:

```python
def extract_error_type(self, line):
    error_patterns = [
        # Your custom patterns first
        r'your_pattern',
        
        # Existing patterns...
        r'\b(Error|Exception|Warning|Critical|Fatal):\s*(\w+)',
    ]
```

## Modifying Clustering Algorithm

Edit `clustering.py` to implement custom similarity:

```python
def cluster_by_similarity(self, lines, threshold=0.7):
    """
    Implement your own clustering algorithm
    """
    clusters = {}
    
    for line_num, line in lines:
        # Your clustering logic
        best_cluster = self.find_best_cluster(line, clusters, threshold)
        if best_cluster:
            clusters[best_cluster].append((line_num, line))
        else:
            clusters[str(line_num)] = [(line_num, line)]
    
    return clusters
```

## Custom Export Formats

Add to `export_handler.py`:

```python
@staticmethod
def export_markdown(report, output_path):
    """Export report as Markdown"""
    lines = ["# Error Analysis Report\n"]
    
    for rank, cluster in enumerate(report['top_clusters'], 1):
        lines.append(f"## {rank}. {cluster['signature']}\n")
        lines.append(f"**Occurrences:** {cluster['count']}\n")
        lines.append(f"**Sample:** {cluster['sample_lines'][0]}\n\n")
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    
    return output_path
```

## Filtering Configuration

### Global Filters

Create a filter config file (e.g., `config/filters.json`):

```json
{
  "exclude_keywords": ["DEBUG", "TRACE", "INFO", "SPAM"],
  "include_only": ["ERROR", "CRITICAL", "FATAL"],
  "keyword_filters": {
    "database": ["db", "database", "sql", "connection"],
    "security": ["auth", "permission", "denied", "unauthorized"],
    "performance": ["timeout", "slow", "exceeded", "limit"]
  }
}
```

Load in `main.py`:

```python
import json

with open('config/filters.json') as f:
    config = json.load(f)

filtered_logs = log_processor.filter_logs(
    logs,
    exclude_pattern='|'.join(config['exclude_keywords']),
    keywords=config['keyword_filters']['database']
)
```

## Performance Tuning

### Adjust Chunk Size for GC

```python
# In main.py __init__
classifier = ErrorLogClassifier(chunk_size=2000)  # Increase for less GC
# or
classifier = ErrorLogClassifier(chunk_size=500)   # Decrease for low-memory systems
```

### Limit Report Size

```python
# In report_generator.py
def generate_summary(self, clusters, stats=None, top_n=20):
    top_clusters = self._get_top_clusters(clusters, top_n=top_n)
```

## Extend for Real-Time Processing

Stream processing example:

```python
from src.log_processor import LogProcessor
from src.signature_extractor import SignatureExtractor
from src.clustering import ErrorClusterer

def process_live_logs(log_stream):
    processor = LogProcessor()
    extractor = SignatureExtractor()
    clusterer = ErrorClusterer()
    
    for line in log_stream:
        signature = extractor.get_signature(line)
        # Update cluster incrementally
        # Send alert if critical pattern detected
        if 'CRITICAL' in signature:
            send_alert(signature)
```

## Integration with External Systems

### Send to Splunk

```python
import urllib.request
import json

def send_to_splunk(report, splunk_url, token):
    headers = {'Authorization': f'Splunk {token}'}
    data = json.dumps(report).encode('utf-8')
    
    req = urllib.request.Request(
        f"{splunk_url}/services/collector",
        data=data,
        headers=headers,
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        print(f"Sent to Splunk: {response.status}")
```

### Send to Elasticsearch

```python
import json
import urllib.request

def send_to_elasticsearch(report, es_url, index):
    for cluster in report['top_clusters']:
        doc = {
            'signature': cluster['signature'],
            'count': cluster['count'],
            'timestamp': datetime.now().isoformat()
        }
        
        req = urllib.request.Request(
            f"{es_url}/{index}/_doc",
            data=json.dumps(doc).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        urllib.request.urlopen(req)
```

### Post to Slack

```python
import json
import urllib.request

def post_to_slack(report, webhook_url):
    blocks = []
    
    for rank, cluster in enumerate(report['top_clusters'][:5], 1):
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{rank}. {cluster['signature']}*\nOccurrences: {cluster['count']}"
            }
        })
    
    payload = json.dumps({'blocks': blocks})
    
    req = urllib.request.Request(
        webhook_url,
        data=payload.encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    urllib.request.urlopen(req)
```

## Advanced Filtering

### Time-based Filtering

```python
from datetime import datetime, timedelta

def filter_by_time_range(logs, start_time, end_time):
    for line_num, line, timestamp in logs:
        if timestamp:
            try:
                ts = datetime.fromisoformat(timestamp)
                if start_time <= ts <= end_time:
                    yield line_num, line, timestamp
            except:
                pass
```

### Severity-based Filtering

```python
SEVERITY_LEVELS = {
    'DEBUG': 0,
    'INFO': 1,
    'WARN': 2,
    'ERROR': 3,
    'CRITICAL': 4
}

def filter_by_severity(logs, min_severity='ERROR'):
    min_level = SEVERITY_LEVELS.get(min_severity, 0)
    
    for line_num, line, timestamp in logs:
        for level, value in SEVERITY_LEVELS.items():
            if level in line.upper() and value >= min_level:
                yield line_num, line, timestamp
                break
```

## Custom Report Templates

```python
def generate_custom_report(clusters):
    """Generate your custom report format"""
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_patterns': len(clusters),
        'patterns': []
    }
    
    for sig, lines in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
        report['patterns'].append({
            'pattern': sig,
            'frequency': len(lines),
            'occurrences': len(lines),
            'impact': 'high' if len(lines) > 10 else 'medium' if len(lines) > 5 else 'low'
        })
    
    return report
```

## Automated Scheduling

### Windows Task Scheduler

Create `schedule_analysis.ps1`:

```powershell
$logFile = "C:\logs\app_$(Get-Date -Format 'yyyy-MM-dd').log"
$outputDir = "C:\reports\analysis_$(Get-Date -Format 'yyyy-MM-dd')"

python main.py analyze $logFile -o $outputDir -e "DEBUG|INFO"

# Email report
$emailParams = @{
    To = "team@company.com"
    From = "alerts@company.com"
    Subject = "Daily Error Analysis"
    Body = "Analysis complete. See attachment."
    Attachments = "$outputDir\error_analysis_*.csv"
    SmtpServer = "smtp.company.com"
}
Send-MailMessage @emailParams
```

Schedule with:
```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At 3AM
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "C:\scripts\schedule_analysis.ps1"
Register-ScheduledTask -TaskName "DailyErrorAnalysis" -Trigger $trigger -Action $action
```

### Linux/Mac Cron

Add to crontab:

```bash
# Daily analysis at 2 AM
0 2 * * * cd /opt/elc && python main.py analyze logs/errors.log -o output && mail -s "Daily Error Report" team@company.com < output/error_analysis_*.csv
```

## Monitoring and Alerts

```python
def check_for_regressions(baseline, current, threshold=0.2):
    """Alert if error frequency increased by threshold %"""
    alerts = []
    
    baseline_map = {c['signature']: c['count'] for c in baseline['top_clusters']}
    current_map = {c['signature']: c['count'] for c in current['top_clusters']}
    
    for sig in baseline_map:
        if sig in current_map:
            increase = (current_map[sig] - baseline_map[sig]) / baseline_map[sig]
            if increase > threshold:
                alerts.append({
                    'type': 'REGRESSION',
                    'signature': sig,
                    'increase_pct': increase * 100,
                    'baseline': baseline_map[sig],
                    'current': current_map[sig]
                })
    
    return alerts
```

---

## Need Help?

- See README.md for usage
- Check EXAMPLES.md for use cases
- Review ARCHITECTURE.md for design
- Run `python main.py info` for overview

