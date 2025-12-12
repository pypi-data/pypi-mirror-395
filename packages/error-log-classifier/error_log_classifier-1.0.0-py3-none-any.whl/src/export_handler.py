"""
Export Handler Module
Exports analysis results to CSV and HTML formats.
"""

import csv
import json
from datetime import datetime
from html import escape


class ExportHandler:
    """Handles exporting reports to various formats."""
    
    @staticmethod
    def export_csv(report, output_path):
        """
        Export report to CSV format.
        
        Args:
            report (dict): The report dictionary
            output_path (str): Path to output CSV file
            
        Returns:
            str: Path to created file
        """
        rows = []
        
        # Extract top clusters data
        for rank, cluster in enumerate(report['top_clusters'], 1):
            rows.append({
                'rank': rank,
                'signature': cluster['signature'],
                'occurrence_count': cluster['count'],
                'sample_line': cluster['sample_lines'][0] if cluster['sample_lines'] else '',
                'first_10_line_numbers': ','.join(str(n) for n in cluster['line_numbers'][:10]),
                'total_line_count': len(cluster['line_numbers']),
            })
        
        if not rows:
            return None
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'rank',
                    'signature',
                    'occurrence_count',
                    'sample_line',
                    'first_10_line_numbers',
                    'total_line_count',
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(rows)
            
            return output_path
        except Exception as e:
            print(f"Error writing CSV file: {e}")
            return None
    
    @staticmethod
    def export_json(report, output_path):
        """
        Export report to JSON format.
        
        Args:
            report (dict): The report dictionary
            output_path (str): Path to output JSON file
            
        Returns:
            str: Path to created file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(report, jsonfile, indent=2)
            return output_path
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return None
    
    @staticmethod
    def export_html(report, output_path, title="Error Log Analysis Report"):
        """
        Export report to HTML format.
        
        Args:
            report (dict): The report dictionary
            output_path (str): Path to output HTML file
            title (str): Report title
            
        Returns:
            str: Path to created file
        """
        try:
            html_content = ExportHandler._generate_html(report, title)
            
            with open(output_path, 'w', encoding='utf-8') as htmlfile:
                htmlfile.write(html_content)
            
            return output_path
        except Exception as e:
            print(f"Error writing HTML file: {e}")
            return None
    
    @staticmethod
    def _generate_html(report, title):
        """
        Generate HTML content from report.
        
        Args:
            report (dict): The report dictionary
            title (str): Report title
            
        Returns:
            str: HTML content
        """
        summary = report['summary']
        top_clusters = report['top_clusters']
        
        # Build HTML
        html_parts = []
        
        html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error Log Analysis</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .timestamp {
            opacity: 0.9;
            font-size: 0.9em;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .summary-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
        }
        
        .summary-card h3 {
            color: #667eea;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        
        .summary-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }
        
        .section {
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        th {
            background-color: #f9f9f9;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #667eea;
            border-bottom: 2px solid #e0e0e0;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        tr:hover {
            background-color: #f9f9f9;
        }
        
        .rank {
            font-weight: bold;
            color: #667eea;
        }
        
        .occurrence {
            background-color: #ffe8e8;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            color: #d63031;
        }
        
        .signature {
            max-width: 500px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        .sample-line {
            background-color: #f0f0f0;
            padding: 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            max-width: 100%;
            overflow-x: auto;
            color: #555;
        }
        
        .error-badge {
            display: inline-block;
            background-color: #667eea;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            margin-right: 5px;
        }
        
        .error-badge.critical {
            background-color: #d63031;
        }
        
        .error-badge.warning {
            background-color: #fdcb6e;
            color: #333;
        }
        
        footer {
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 0.9em;
        }
        
        .stats-row {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            flex: 1;
            min-width: 150px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        
        .stat-label {
            font-size: 0.85em;
            color: #999;
            text-transform: uppercase;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
""")
        
        # Header
        html_parts.append(f"""        <header>
            <h1>{escape(title)}</h1>
            <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </header>
""")
        
        # Summary cards
        html_parts.append("        <div class=\"summary-grid\">")
        html_parts.append(f"""            <div class="summary-card">
                <h3>Total Clusters</h3>
                <div class="value">{summary['total_clusters']}</div>
            </div>""")
        html_parts.append(f"""            <div class="summary-card">
                <h3>Lines Analyzed</h3>
                <div class="value">{summary['total_lines']:,}</div>
            </div>""")
        html_parts.append(f"""            <div class="summary-card">
                <h3>Avg Cluster Size</h3>
                <div class="value">{summary['average_cluster_size']:.2f}</div>
            </div>""")
        html_parts.append(f"""            <div class="summary-card">
                <h3>Largest Cluster</h3>
                <div class="value">{summary['largest_cluster']:,}</div>
            </div>""")
        html_parts.append("        </div>")
        
        # Top offenders table
        html_parts.append("""        <div class="section">
            <h2>Top Offenders - Most Frequent Error Patterns</h2>
            <table>
                <thead>
                    <tr>
                        <th style="width: 5%;">Rank</th>
                        <th style="width: 40%;">Error Signature</th>
                        <th style="width: 12%;">Occurrences</th>
                        <th style="width: 43%;">Sample Line</th>
                    </tr>
                </thead>
                <tbody>
""")
        
        for rank, cluster in enumerate(top_clusters, 1):
            sample = escape(cluster['sample_lines'][0][:100]) if cluster['sample_lines'] else 'N/A'
            signature = escape(cluster['signature'][:80])
            
            html_parts.append(f"""                    <tr>
                        <td class="rank">#{rank}</td>
                        <td class="signature" title="{escape(cluster['signature'])}">{signature}</td>
                        <td><span class="occurrence">{cluster['count']}</span></td>
                        <td><div class="sample-line">{sample}...</div></td>
                    </tr>
""")
        
        html_parts.append("""                </tbody>
            </table>
        </div>
""")
        
        # Additional statistics
        html_parts.append("""        <div class="section">
            <h2>Analysis Statistics</h2>
            <div class="stats-row">
                <div class="stat-item">
                    <div class="stat-label">Smallest Cluster</div>
                    <div class="stat-value">""")
        html_parts.append(str(summary['smallest_cluster']))
        html_parts.append("""</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Average per Cluster</div>
                    <div class="stat-value">""")
        html_parts.append(f"{summary['average_cluster_size']:.1f}")
        html_parts.append("""</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Coverage by Top 10</div>
                    <div class="stat-value">""")
        
        total_lines = summary['total_lines']
        top_10_count = sum(cluster['count'] for cluster in top_clusters[:10])
        coverage = (top_10_count / total_lines * 100) if total_lines > 0 else 0
        html_parts.append(f"{coverage:.1f}%")
        html_parts.append("""</div>
                </div>
            </div>
        </div>
""")
        
        # Footer
        html_parts.append("""        <footer>
            <p>Error Log Classifier - Automated Analysis Report</p>
        </footer>
    </div>
</body>
</html>
""")
        
        return "\n".join(html_parts)








# added: change 3
_added_marker_3 = 3


# added: change 10
_added_marker_10 = 10


# added: change 17
_added_marker_17 = 17


# added: src change 3
_added_marker_new_3 = 3


# added: src change 10
_added_marker_new_10 = 10


# added: src change 17
_added_marker_new_17 = 17

