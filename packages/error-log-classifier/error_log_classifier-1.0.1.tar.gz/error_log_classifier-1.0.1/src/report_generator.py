"""
Report Generator Module
Generates analysis reports from clustered logs.
"""

from collections import Counter


class ReportGenerator:
    """Generates reports from clustered and analyzed logs."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.report_data = {}
    
    def generate_summary(self, clusters, stats=None):
        """
        Generate a summary report from clusters.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            stats (dict): Optional statistics dictionary
            
        Returns:
            dict: Summary report
        """
        top_clusters = self._get_top_clusters(clusters, top_n=10)
        cluster_stats = self._get_cluster_statistics(clusters)
        
        report = {
            'summary': {
                'total_clusters': len(clusters),
                'total_lines': sum(len(lines) for lines in clusters.values()),
                'average_cluster_size': cluster_stats['avg_size'],
                'largest_cluster': cluster_stats['max_size'],
                'smallest_cluster': cluster_stats['min_size'],
            },
            'top_clusters': top_clusters,
            'additional_stats': stats or {},
        }
        
        self.report_data = report
        return report
    
    def _get_top_clusters(self, clusters, top_n=10):
        """
        Get top N clusters by frequency.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            top_n (int): Number of top clusters
            
        Returns:
            list: Top clusters with details
        """
        cluster_list = []
        for signature, lines in clusters.items():
            cluster_list.append({
                'signature': signature,
                'count': len(lines),
                'sample_lines': [line for _, line in lines[:3]],
                'line_numbers': [line_num for line_num, _ in lines],
            })
        
        # Sort by count descending
        cluster_list.sort(key=lambda x: x['count'], reverse=True)
        return cluster_list[:top_n]
    
    def _get_cluster_statistics(self, clusters):
        """
        Calculate cluster statistics.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            
        Returns:
            dict: Statistics
        """
        if not clusters:
            return {
                'avg_size': 0,
                'max_size': 0,
                'min_size': 0,
            }
        
        sizes = [len(lines) for lines in clusters.values()]
        return {
            'avg_size': sum(sizes) / len(sizes),
            'max_size': max(sizes),
            'min_size': min(sizes),
        }
    
    def generate_detailed_report(self, clusters, timestamp_buckets=None):
        """
        Generate a detailed report with time analysis.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            timestamp_buckets (dict): {bucket: lines} optional
            
        Returns:
            dict: Detailed report
        """
        top_clusters = self._get_top_clusters(clusters, top_n=20)
        
        report = {
            'clusters': top_clusters,
            'time_analysis': timestamp_buckets or {},
            'error_distribution': self._get_error_distribution(clusters),
        }
        
        return report
    
    def _get_error_distribution(self, clusters):
        """
        Analyze error type distribution.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            
        Returns:
            dict: Error type distribution
        """
        error_types = Counter()
        
        for signature, lines in clusters.items():
            # Extract error type from signature
            if '|' in signature:
                error_type = signature.split('|')[0]
            else:
                error_type = signature.split()[0]
            
            error_types[error_type] += len(lines)
        
        return dict(error_types.most_common(10))
    
    def format_summary_text(self, report):
        """
        Format report as plain text.
        
        Args:
            report (dict): The report dictionary
            
        Returns:
            str: Formatted text report
        """
        lines = []
        
        lines.append("=" * 70)
        lines.append("ERROR LOG ANALYSIS REPORT")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary section
        summary = report['summary']
        lines.append("SUMMARY")
        lines.append("-" * 70)
        lines.append(f"Total Error Clusters: {summary['total_clusters']}")
        lines.append(f"Total Lines Analyzed: {summary['total_lines']}")
        lines.append(f"Average Cluster Size: {summary['average_cluster_size']:.2f}")
        lines.append(f"Largest Cluster: {summary['largest_cluster']} occurrences")
        lines.append(f"Smallest Cluster: {summary['smallest_cluster']} occurrences")
        lines.append("")
        
        # Top clusters
        lines.append("TOP OFFENDERS (10 Most Frequent)")
        lines.append("-" * 70)
        for i, cluster in enumerate(report['top_clusters'][:10], 1):
            lines.append(f"\n{i}. Signature: {cluster['signature'][:80]}")
            lines.append(f"   Occurrences: {cluster['count']}")
            lines.append(f"   Sample lines: {cluster['sample_lines'][0][:100]}")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def format_csv_rows(self, report):
        """
        Format report for CSV export.
        
        Args:
            report (dict): The report dictionary
            
        Returns:
            list: List of dictionaries suitable for CSV
        """
        rows = []
        
        for cluster in report['top_clusters']:
            rows.append({
                'rank': len(rows) + 1,
                'signature': cluster['signature'],
                'occurrence_count': cluster['count'],
                'sample_line': cluster['sample_lines'][0] if cluster['sample_lines'] else '',
                'line_numbers': ','.join(str(n) for n in cluster['line_numbers'][:10]),
            })
        
        return rows








# added: change 5
_added_marker_5 = 5


# added: change 12
_added_marker_12 = 12


# added: change 19
_added_marker_19 = 19


# added: src change 5
_added_marker_new_5 = 5


# added: src change 12
_added_marker_new_12 = 12


# added: src change 19
_added_marker_new_19 = 19

