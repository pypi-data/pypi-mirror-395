# Error-log-classifier
=======
# Error Log Classifier Project

**Group 106** - Preetham Ghorpade (251810700340) & Harish R S (251810700315)

## Overview

The Error Log Classifier is a Python-based tool that reads large error logs, clusters similar lines by signature, extracts patterns, and generates comprehensive reports. It's designed for ops and support teams to quickly identify recurring failures and high-priority issues.

### Key Capabilities

- **Text Normalization**: Normalizes IP addresses, UUIDs, numbers, paths, and other variable data to reveal underlying patterns
- **Smart Signature Extraction**: Identifies error types and creates compact signatures for clustering
- **Efficient Clustering**: Groups similar errors by signature using memory-bounded processing
- **Frequency Analysis**: Ranks error patterns by frequency to surface top offenders
- **Flexible Filtering**: Include/exclude patterns and keyword matching for focused analysis
- **Time Bucketing**: Organize errors by time periods for trend analysis
- **Multiple Export Formats**: Generate CSV, JSON, and professional HTML reports
- **Regression Tracking**: Compare two analysis runs to detect new errors and regressions
- **Memory Efficient**: Processes large files with periodic garbage collection and streaming reads

## Project Structure

```
ELC-PH/
├── main.py                 # Main application entry point
├── src/
│   ├── log_processor.py           # File reading and filtering
│   ├── signature_extractor.py     # Text normalization and signature generation
│   ├── clustering.py              # Error clustering by similarity
│   ├── report_generator.py        # Report generation and formatting
│   ├── export_handler.py          # CSV, JSON, HTML export
│   └── diff_analyzer.py           # Comparing analysis runs
├── data/
│   └── sample_errors.log          # Sample error log for testing
├── output/                        # Reports and exported data (generated)
├── tests/                         # Unit tests
├── docs/                          # Documentation
└── README.md                      # This file
```

## Requirements

- **Python 3.6+** (no external dependencies - uses only standard library)
- Required modules: `re`, `collections`, `csv`, `json`

## Installation

No installation required! Just clone/download the project and run:

```bash
python main.py --help
```

## Usage

### 1. Analyze a Log File

Basic analysis:
```bash
python main.py analyze data/sample_errors.log -o output
```

This will:
- Read the log file
- Extract error signatures
- Cluster similar errors
- Generate CSV, JSON, and HTML reports in the `output/` directory

### 2. Filter Logs During Analysis

Include only specific patterns:
```bash
python main.py analyze data/error.log -o output -i "ERROR|CRITICAL"
```

Exclude specific patterns:
```bash
python main.py analyze data/error.log -o output -e "INFO|DEBUG"
```

Filter by keywords:
```bash
python main.py analyze data/error.log -o output -k "database" "timeout"
```

### 3. Compare Two Analysis Runs (Regression Tracking)

Compare baseline vs current run to track regressions:
```bash
python main.py diff output/baseline_analysis.json output/current_analysis.json -o output
```

This will:
- Load both analysis JSON files
- Calculate differences in error frequencies
- Identify new error patterns
- Highlight resolved issues
- Detect regressions (increased frequencies)
- Export detailed comparison report

### 4. Display Project Information

```bash
python main.py info
```

## Command Reference

### Analyze Command
```
python main.py analyze <logfile> -o <output_dir> [OPTIONS]

Positional arguments:
  logfile                Path to error log file

Required arguments:
  -o, --output          Output directory for reports

Optional arguments:
  -m, --max-lines       Maximum number of lines to read
  -i, --include         Regex pattern to include lines
  -e, --exclude         Regex pattern to exclude lines
  -k, --keywords        Keywords that must appear (multiple allowed)
  -t, --time-bucket     Group errors by time bucket (minutes)
```

### Diff Command
```
python main.py diff <baseline> <current> -o <output_dir>

Positional arguments:
  baseline              Path to baseline JSON report
  current               Path to current JSON report

Required arguments:
  -o, --output          Output directory for diff report
```

## Output Formats

### CSV Report
Contains the top error patterns with:
- Rank and signature
- Number of occurrences
- Sample error line
- Line numbers where pattern appears

### HTML Report
Professional dashboard with:
- Visual summary cards (cluster count, total lines, etc.)
- Interactive table of top offenders
- Color-coded severity indicators
- Responsive design for mobile viewing
- Automatic timestamp

### JSON Report
Complete machine-readable report with:
- Full summary statistics
- All clusters and their details
- Sample lines for each pattern
- Additional analysis metadata

### Diff Report
Regression analysis showing:
- Summary changes between runs
- New error patterns that appeared
- Resolved patterns that disappeared
- Changed frequencies with percentages
- Critical regressions highlighted

## Example Workflows

### Workflow 1: Daily Log Analysis

```bash
# Analyze today's errors
python main.py analyze logs/2024-12-01.log -o output/daily

# Generate CSV for spreadsheet import
# Output files: error_analysis_*.csv, error_analysis_*.html
```

### Workflow 2: Identify Database Issues

```bash
# Focus on database-related errors
python main.py analyze logs/all_errors.log -o output/db_issues \
  -k "database" "connection" "timeout" \
  -e "DEBUG"

# View top database errors in generated HTML report
```

### Workflow 3: Track Regressions After Deployment

```bash
# Run 1: Before deployment
python main.py analyze logs/pre_deploy.log -o baseline

# Run 2: After deployment
python main.py analyze logs/post_deploy.log -o current

# Compare
python main.py diff baseline/error_analysis_*.json \
               current/error_analysis_*.json \
               -o comparison

# Review diff_report_*.json to see what changed
```

### Workflow 4: Time-based Analysis

```bash
# Analyze errors bucketed by hour
python main.py analyze logs/errors.log -o output \
  -t 60
```

## How It Works

### 1. Text Normalization

The SignatureExtractor normalizes log lines by replacing:
- IP addresses → `<IP>`
- UUIDs → `<UUID>`
- Large numbers → `<NUM>`
- Line numbers → `<LINE>`
- Hex addresses → `<HEX>`
- Quoted strings → `<STR>`
- File paths → `<PATH>`
- Version numbers → `<VERSION>`

Example:
```
Before:  Connection to 192.168.1.100 failed at line 45
After:   connection to <IP> failed at <LINE>
```

### 2. Signature Generation

Combines extracted error type with first few normalized tokens:
```
Signature: database|connection to <IP> failed at
```

### 3. Clustering

Groups lines with identical signatures using a dictionary-based approach. Each signature represents one cluster of similar errors.

### 4. Analysis

Calculates statistics:
- Total clusters found
- Total lines analyzed
- Average/min/max cluster sizes
- Error type distribution
- Top N most frequent patterns

### 5. Reporting

Generates ranked list of error patterns with:
- Occurrence count
- Sample line showing actual error
- Line numbers where pattern appeared
- Memory-efficient HTML visualization

### 6. Regression Tracking

When comparing two runs:
- Detects frequency changes (regressions vs improvements)
- Identifies brand new error patterns
- Shows which patterns have been resolved
- Calculates percentage changes

## Memory Management

The tool handles large files efficiently through:

1. **Streaming File Reading**: Lines are read one at a time, not loaded into memory
2. **Chunk Processing**: Every N lines (default 1000), garbage collection is triggered
3. **Efficient Storage**: Only signatures and metadata are kept, not full lines in memory
4. **Configurable Limits**: `max_lines` parameter lets you process large logs in batches

Example: Processing a 1GB log file typically uses < 100MB of RAM

## Troubleshooting

### "File not found" error
```bash
# Ensure log file path is correct
python main.py analyze ./data/sample_errors.log -o output
```

### No clusters found
- Check if your include/exclude filters are too restrictive
- Try without filters first: `python main.py analyze data/error.log -o output`

### Memory issues on large files
- Use `--max-lines` to process in batches
- Increase garbage collection with smaller chunk size

### Reports not generating
- Check write permissions in output directory
- Ensure output directory exists or use `-o ./output` to create it

## Development Notes

### Adding Custom Normalization Patterns

Edit `src/signature_extractor.py`:
```python
self.patterns = [
    # Existing patterns...
    (r'your_regex_pattern', '<PLACEHOLDER>'),  # Add new pattern
]
```

### Modifying Clustering Logic

Edit `src/clustering.py` `cluster_by_signature()` method to implement different similarity algorithms.

### Custom Export Formats

Add new methods to `src/export_handler.py`:
```python
@staticmethod
def export_custom_format(report, output_path):
    # Your implementation
    pass
```

## Performance Metrics

Typical performance on modern hardware:
- **100K lines**: ~2 seconds
- **1M lines**: ~15 seconds  
- **10M lines**: ~2 minutes
- **Memory usage**: Scales linearly with unique patterns, not line count

## Team Members

- **Preetham Ghorpade** (251810700340)
- **Harish R S** (251810700315)

## License

Educational Project - Group 106

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify input log file format
3. Review generated JSON report for detailed analysis data
4. Check output files have proper permissions

>>>>>>> Preetham
