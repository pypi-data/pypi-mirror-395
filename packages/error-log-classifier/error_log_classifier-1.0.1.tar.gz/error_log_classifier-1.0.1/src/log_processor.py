"""
Log Processor Module
Reads and processes large error log files with memory bounds.
"""

import re
from datetime import datetime
from collections import defaultdict


class LogProcessor:
    """Processes error logs with memory-conscious streaming."""
    
    def __init__(self, chunk_size=1000):
        """
        Initialize the log processor.
        
        Args:
            chunk_size (int): Number of lines to process before gc cleanup
        """
        self.chunk_size = chunk_size
        self.time_pattern = re.compile(
            r'(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})'
            r'[\s_]'
            r'(\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?(?::\d{2})?)'
        )
    
    def read_logs(self, filepath, encoding='utf-8', max_lines=None):
        """
        Read logs from a file with memory efficiency.
        
        Args:
            filepath (str): Path to the log file
            encoding (str): File encoding
            max_lines (int): Maximum number of lines to read (None for all)
            
        Yields:
            tuple: (line_number, line_content, timestamp)
        """
        line_num = 0
        try:
            with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                for raw_line in f:
                    if max_lines and line_num >= max_lines:
                        break
                    
                    line = raw_line.rstrip('\n\r')
                    if line.strip():  # Skip empty lines
                        timestamp = self._extract_timestamp(line)
                        yield line_num, line, timestamp
                        line_num += 1
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
    
    def _extract_timestamp(self, line):
        """
        Extract timestamp from a log line.
        
        Args:
            line (str): The log line
            
        Returns:
            str: The timestamp or None if not found
        """
        match = self.time_pattern.search(line)
        return match.group(0) if match else None
    
    def filter_logs(self, logs, pattern=None, exclude_pattern=None, error_keywords=None):
        """
        Filter logs based on patterns and keywords.
        
        Args:
            logs (iterable): Iterator of (line_num, line, timestamp) tuples
            pattern (str): Regex pattern to match (inclusive)
            exclude_pattern (str): Regex pattern to exclude
            error_keywords (list): Keywords that must appear in the line
            
        Yields:
            tuple: Filtered (line_num, line, timestamp)
        """
        include_re = re.compile(pattern, re.IGNORECASE) if pattern else None
        exclude_re = re.compile(exclude_pattern, re.IGNORECASE) if exclude_pattern else None
        keywords = set(kw.lower() for kw in error_keywords) if error_keywords else set()
        
        for line_num, line, timestamp in logs:
            # Check exclusion pattern
            if exclude_re and exclude_re.search(line):
                continue
            
            # Check inclusion pattern
            if include_re and not include_re.search(line):
                continue
            
            # Check keywords
            line_lower = line.lower()
            if keywords and not any(kw in line_lower for kw in keywords):
                continue
            
            yield line_num, line, timestamp
    
    def bucket_by_time(self, logs, bucket_minutes=60):
        """
        Group logs into time buckets.
        
        Args:
            logs (iterable): Iterator of (line_num, line, timestamp) tuples
            bucket_minutes (int): Minutes per bucket
            
        Returns:
            dict: {bucket_key: [(line_num, line, timestamp), ...]}
        """
        buckets = defaultdict(list)
        
        for line_num, line, timestamp in logs:
            if timestamp:
                try:
                    # Try to parse and bucket the timestamp
                    bucket_key = self._get_bucket_key(timestamp, bucket_minutes)
                    buckets[bucket_key].append((line_num, line, timestamp))
                except:
                    # If parsing fails, put in 'unknown' bucket
                    buckets['unknown'].append((line_num, line, timestamp))
            else:
                buckets['unknown'].append((line_num, line, timestamp))
        
        return buckets
    
    def _get_bucket_key(self, timestamp, bucket_minutes):
        """
        Generate a bucket key from a timestamp.
        
        Args:
            timestamp (str): The timestamp string
            bucket_minutes (int): Minutes per bucket
            
        Returns:
            str: A bucket key
        """
        # Simple bucketing: extract date and hour
        # More sophisticated parsing could be added
        parts = timestamp.split()
        if len(parts) >= 2:
            date_part = parts[0]
            time_part = parts[1]
            hour = time_part.split(':')[0]
            bucket_key = f"{date_part}_{hour}:00"
            return bucket_key
        return "unknown"
    
    def get_stats(self, logs):
        """
        Calculate statistics from logs.
        
        Args:
            logs (iterable): Iterator of (line_num, line, timestamp) tuples
            
        Returns:
            dict: Statistics dictionary
        """
        stats = {
            'total_lines': 0,
            'with_timestamp': 0,
            'avg_line_length': 0,
            'min_line_length': float('inf'),
            'max_line_length': 0,
        }
        
        total_length = 0
        for line_num, line, timestamp in logs:
            stats['total_lines'] += 1
            if timestamp:
                stats['with_timestamp'] += 1
            
            line_len = len(line)
            total_length += line_len
            stats['min_line_length'] = min(stats['min_line_length'], line_len)
            stats['max_line_length'] = max(stats['max_line_length'], line_len)
        
        if stats['total_lines'] > 0:
            stats['avg_line_length'] = total_length / stats['total_lines']
            if stats['min_line_length'] == float('inf'):
                stats['min_line_length'] = 0
        
        return stats








# added: change 4
_added_marker_4 = 4


# added: change 11
_added_marker_11 = 11


# added: change 18
_added_marker_18 = 18


# added: src change 4
_added_marker_new_4 = 4


# added: src change 11
_added_marker_new_11 = 11


# added: src change 18
_added_marker_new_18 = 18

