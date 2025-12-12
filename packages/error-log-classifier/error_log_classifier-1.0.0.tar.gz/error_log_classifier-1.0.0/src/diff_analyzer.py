"""
Diff Analyzer Module
Compares two analysis runs to identify regressions and changes.
"""

import json
from datetime import datetime


class DiffAnalyzer:
    """Analyzes differences between two analysis runs."""
    
    def __init__(self):
        """Initialize the diff analyzer."""
        self.baseline_report = None
        self.current_report = None
    
    def load_baseline(self, report_dict):
        """
        Load baseline report for comparison.
        
        Args:
            report_dict (dict): The baseline report
        """
        self.baseline_report = report_dict
    
    def load_current(self, report_dict):
        """
        Load current report for comparison.
        
        Args:
            report_dict (dict): The current report
        """
        self.current_report = report_dict
    
    def compare(self):
        """
        Compare baseline and current reports.
        
        Returns:
            dict: Comparison results
        """
        if not self.baseline_report or not self.current_report:
            raise ValueError("Both baseline and current reports must be loaded")
        
        diff = {
            'timestamp': datetime.now().isoformat(),
            'summary_changes': self._compare_summaries(),
            'new_patterns': self._find_new_patterns(),
            'resolved_patterns': self._find_resolved_patterns(),
            'changed_frequencies': self._find_frequency_changes(),
            'regressions': self._find_regressions(),
        }
        
        return diff
    
    def _compare_summaries(self):
        """
        Compare summary statistics.
        
        Returns:
            dict: Changes in summary
        """
        baseline_summary = self.baseline_report.get('summary', {})
        current_summary = self.current_report.get('summary', {})
        
        changes = {}
        for key in baseline_summary:
            if key in current_summary:
                baseline_val = baseline_summary[key]
                current_val = current_summary[key]
                
                if isinstance(baseline_val, (int, float)):
                    change = current_val - baseline_val
                    pct_change = (change / baseline_val * 100) if baseline_val != 0 else 0
                    
                    changes[key] = {
                        'baseline': baseline_val,
                        'current': current_val,
                        'absolute_change': change,
                        'percent_change': pct_change,
                    }
        
        return changes
    
    def _find_new_patterns(self):
        """
        Find patterns that appeared in current but not in baseline.
        
        Returns:
            list: New patterns
        """
        baseline_sigs = {c['signature'] for c in self.baseline_report.get('top_clusters', [])}
        current_clusters = self.current_report.get('top_clusters', [])
        
        new_patterns = []
        for cluster in current_clusters:
            if cluster['signature'] not in baseline_sigs:
                new_patterns.append({
                    'signature': cluster['signature'],
                    'count': cluster['count'],
                    'sample': cluster['sample_lines'][0] if cluster['sample_lines'] else '',
                })
        
        # Sort by frequency
        new_patterns.sort(key=lambda x: x['count'], reverse=True)
        return new_patterns
    
    def _find_resolved_patterns(self):
        """
        Find patterns that were in baseline but not in current.
        
        Returns:
            list: Resolved patterns
        """
        baseline_clusters = self.baseline_report.get('top_clusters', [])
        current_sigs = {c['signature'] for c in self.current_report.get('top_clusters', [])}
        
        resolved_patterns = []
        for cluster in baseline_clusters:
            if cluster['signature'] not in current_sigs:
                resolved_patterns.append({
                    'signature': cluster['signature'],
                    'previous_count': cluster['count'],
                    'sample': cluster['sample_lines'][0] if cluster['sample_lines'] else '',
                })
        
        return resolved_patterns
    
    def _find_frequency_changes(self):
        """
        Find patterns with significant frequency changes.
        
        Returns:
            list: Patterns with changed frequencies
        """
        baseline_map = {
            c['signature']: c['count']
            for c in self.baseline_report.get('top_clusters', [])
        }
        current_map = {
            c['signature']: c['count']
            for c in self.current_report.get('top_clusters', [])
        }
        
        changes = []
        for signature in baseline_map:
            if signature in current_map:
                baseline_count = baseline_map[signature]
                current_count = current_map[signature]
                
                if baseline_count != current_count:
                    change = current_count - baseline_count
                    pct_change = (change / baseline_count * 100) if baseline_count > 0 else 0
                    
                    changes.append({
                        'signature': signature,
                        'baseline_count': baseline_count,
                        'current_count': current_count,
                        'absolute_change': change,
                        'percent_change': pct_change,
                    })
        
        # Sort by absolute change
        changes.sort(key=lambda x: abs(x['absolute_change']), reverse=True)
        return changes
    
    def _find_regressions(self):
        """
        Find regressions (increased error frequencies).
        
        Returns:
            list: Regression patterns
        """
        changes = self._find_frequency_changes()
        
        # Regressions are increases in frequency
        regressions = [c for c in changes if c['absolute_change'] > 0]
        regressions.sort(key=lambda x: x['percent_change'], reverse=True)
        
        return regressions
    
    def format_diff_report(self, diff):
        """
        Format diff as readable text.
        
        Args:
            diff (dict): The diff dictionary
            
        Returns:
            str: Formatted text report
        """
        lines = []
        
        lines.append("=" * 70)
        lines.append("ERROR LOG ANALYSIS - REGRESSION REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {diff['timestamp']}")
        lines.append("")
        
        # Summary changes
        lines.append("SUMMARY CHANGES")
        lines.append("-" * 70)
        for key, changes in diff['summary_changes'].items():
            if changes['absolute_change'] != 0:
                direction = "↑" if changes['absolute_change'] > 0 else "↓"
                lines.append(
                    f"{key}: {changes['baseline']} → {changes['current']} "
                    f"({direction} {changes['percent_change']:.1f}%)"
                )
        lines.append("")
        
        # Regressions
        if diff['regressions']:
            lines.append("🔴 REGRESSIONS (Increased Errors)")
            lines.append("-" * 70)
            for i, reg in enumerate(diff['regressions'][:5], 1):
                lines.append(
                    f"{i}. {reg['signature'][:70]}\n"
                    f"   {reg['baseline_count']} → {reg['current_count']} "
                    f"(+{reg['percent_change']:.1f}%)"
                )
        lines.append("")
        
        # New patterns
        if diff['new_patterns']:
            lines.append("🆕 NEW PATTERNS")
            lines.append("-" * 70)
            for i, pattern in enumerate(diff['new_patterns'][:5], 1):
                lines.append(f"{i}. {pattern['signature'][:70]}")
                lines.append(f"   Count: {pattern['count']}")
        lines.append("")
        
        # Resolved patterns
        if diff['resolved_patterns']:
            lines.append("✅ RESOLVED PATTERNS")
            lines.append("-" * 70)
            for i, pattern in enumerate(diff['resolved_patterns'][:5], 1):
                lines.append(f"{i}. {pattern['signature'][:70]}")
                lines.append(f"   Previous count: {pattern['previous_count']}")
        lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def export_diff_json(self, diff, output_path):
        """
        Export diff analysis to JSON.
        
        Args:
            diff (dict): The diff dictionary
            output_path (str): Path to output file
            
        Returns:
            str: Path to created file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(diff, f, indent=2)
            return output_path
        except Exception as e:
            print(f"Error writing diff JSON: {e}")
            return None








# added: change 2
_added_marker_2 = 2


# added: change 9
_added_marker_9 = 9


# added: change 16
_added_marker_16 = 16


# added: src change 2
_added_marker_new_2 = 2


# added: src change 9
_added_marker_new_9 = 9


# added: src change 16
_added_marker_new_16 = 16

