"""
Unit tests for Error Log Classifier modules
"""

import unittest
import tempfile
import json
from pathlib import Path

from src.signature_extractor import SignatureExtractor
from src.clustering import ErrorClusterer
from src.log_processor import LogProcessor
from src.report_generator import ReportGenerator


class TestSignatureExtractor(unittest.TestCase):
    """Test signature extraction functionality."""
    
    def setUp(self):
        self.extractor = SignatureExtractor()
    
    def test_normalize_ip_address(self):
        """Test IP address normalization."""
        line = "Connection failed to 192.168.1.100"
        normalized = self.extractor.normalize(line)
        self.assertIn('<ip>', normalized.lower())
        self.assertNotIn('192.168.1.100', normalized)
    
    def test_normalize_paths(self):
        """Test file path normalization."""
        line = "Error in /var/log/app.log file"
        normalized = self.extractor.normalize(line)
        self.assertIn('<path>', normalized.lower())
    
    def test_extract_error_type(self):
        """Test error type extraction."""
        line = "DatabaseException: Connection timeout"
        error_type = self.extractor.extract_error_type(line)
        self.assertIn('exception', error_type.lower())
    
    def test_get_signature(self):
        """Test signature generation."""
        line = "Connection to 192.168.1.100 failed at line 45"
        sig = self.extractor.get_signature(line)
        self.assertIsInstance(sig, str)
        self.assertGreater(len(sig), 0)


class TestClustering(unittest.TestCase):
    """Test clustering functionality."""
    
    def setUp(self):
        self.clusterer = ErrorClusterer()
    
    def test_cluster_by_signature(self):
        """Test clustering by signature."""
        lines_with_sigs = [
            (0, "line1", "sig1"),
            (1, "line2", "sig1"),
            (2, "line3", "sig2"),
        ]
        clusters = self.clusterer.cluster_by_signature(lines_with_sigs)
        
        self.assertEqual(len(clusters), 2)
        self.assertEqual(len(clusters["sig1"]), 2)
        self.assertEqual(len(clusters["sig2"]), 1)
    
    def test_get_top_clusters(self):
        """Test getting top clusters."""
        clusters = {
            "sig1": [(0, "line1"), (1, "line2"), (2, "line3")],
            "sig2": [(3, "line4")],
        }
        top = self.clusterer.get_top_clusters(clusters, top_n=1)
        
        self.assertEqual(len(top), 1)
        self.assertEqual(top[0][0], "sig1")
        self.assertEqual(top[0][1], 3)
    
    def test_cluster_stats(self):
        """Test cluster statistics."""
        clusters = {
            "sig1": [(0, "line1"), (1, "line2")],
            "sig2": [(3, "line4"), (4, "line5"), (5, "line6")],
        }
        stats = self.clusterer.get_cluster_stats(clusters)
        
        self.assertEqual(stats['total_clusters'], 2)
        self.assertEqual(stats['total_lines'], 5)
        self.assertEqual(stats['largest_cluster'], 3)


class TestReportGenerator(unittest.TestCase):
    """Test report generation."""
    
    def setUp(self):
        self.report_gen = ReportGenerator()
    
    def test_generate_summary(self):
        """Test summary report generation."""
        clusters = {
            "sig1": [(0, "line1"), (1, "line2")],
            "sig2": [(3, "line4")],
        }
        report = self.report_gen.generate_summary(clusters)
        
        self.assertIn('summary', report)
        self.assertIn('top_clusters', report)
        self.assertEqual(report['summary']['total_clusters'], 2)
        self.assertEqual(report['summary']['total_lines'], 3)
    
    def test_format_summary_text(self):
        """Test text formatting."""
        clusters = {
            "sig1": [(0, "line1"), (1, "line2")],
        }
        report = self.report_gen.generate_summary(clusters)
        text = self.report_gen.format_summary_text(report)
        
        self.assertIn('ERROR LOG ANALYSIS REPORT', text)
        self.assertIn('SUMMARY', text)


class TestLogProcessor(unittest.TestCase):
    """Test log processing functionality."""
    
    def setUp(self):
        self.processor = LogProcessor()
        
        # Create temporary test log file
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', 
            delete=False, 
            suffix='.log'
        )
        self.temp_path = self.temp_file.name
        
        # Write test data
        self.temp_file.write("[2024-12-01 10:00:00] ERROR: Test error 1\n")
        self.temp_file.write("[2024-12-01 10:00:01] ERROR: Test error 2\n")
        self.temp_file.write("[2024-12-01 10:00:02] WARN: Test warning\n")
        self.temp_file.close()
    
    def tearDown(self):
        Path(self.temp_path).unlink()
    
    def test_read_logs(self):
        """Test reading logs from file."""
        logs = list(self.processor.read_logs(self.temp_path))
        
        self.assertEqual(len(logs), 3)
        self.assertEqual(logs[0][0], 0)  # line number
        self.assertIn("Test error 1", logs[0][1])  # line content
    
    def test_filter_logs_by_pattern(self):
        """Test filtering logs by pattern."""
        logs = self.processor.read_logs(self.temp_path)
        filtered = list(self.processor.filter_logs(logs, pattern='ERROR'))
        
        self.assertEqual(len(filtered), 2)
    
    def test_filter_logs_exclude(self):
        """Test excluding logs by pattern."""
        logs = self.processor.read_logs(self.temp_path)
        filtered = list(self.processor.filter_logs(logs, exclude_pattern='WARN'))
        
        self.assertEqual(len(filtered), 2)


if __name__ == '__main__':
    unittest.main()

