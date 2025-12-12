"""
Signature Extractor Module
Normalizes error log lines and extracts error signatures.
"""

import re
from collections import Counter


class SignatureExtractor:
    """Extracts and normalizes error signatures from log lines."""
    
    def __init__(self):
        """Initialize the signature extractor with common patterns."""
        # Patterns to normalize (find and replace with placeholders)
        self.patterns = [
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>'),  # IP addresses
            (r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', '<UUID>'),  # UUIDs
            (r'\b\d{10,}\b', '<NUM>'),  # Large numbers (timestamps, IDs)
            (r'(at |in )\d+', r'\1<LINE>'),  # Line numbers
            (r'0x[0-9a-f]+', '<HEX>'),  # Hex addresses
            (r'"[^"]*"', '<STR>'),  # Quoted strings
            (r"'[^']*'", '<STR>'),  # Single quoted strings
            (r'/[\w/.-]+', '<PATH>'),  # File paths (unix)
            (r'\\[\w\\.-]+', '<PATH>'),  # File paths (windows)
            (r'\b\d+\.\d+\.\d+\.\d+\b', '<VERSION>'),  # Versions
        ]
        
        # Compile patterns for performance
        self.compiled_patterns = [(re.compile(pattern, re.IGNORECASE), repl) 
                                  for pattern, repl in self.patterns]
    
    def normalize(self, line):
        """
        Normalize a log line by replacing specific patterns with placeholders.
        
        Args:
            line (str): The log line to normalize
            
        Returns:
            str: The normalized log line
        """
        normalized = line.strip()
        
        # Apply all patterns
        for pattern, replacement in self.compiled_patterns:
            normalized = pattern.sub(replacement, normalized)
        
        # Additional aggressive normalization for better clustering
        # Remove specific port numbers but keep the structure
        normalized = re.sub(r':\d{4,5}(?=\s|$)', ':<PORT>', normalized)
        
        # Reduce multiple spaces
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized.lower()
    
    def extract_error_type(self, line):
        """
        Extract the error type from a log line.
        
        Args:
            line (str): The log line
            
        Returns:
            str: The error type (Exception name, Error class, or first significant word)
        """
        # Look for common error patterns
        error_patterns = [
            r'\b(Error|Exception|Warning|Critical|Fatal):\s*(\w+)',
            r'\b(\w+Error)\b',
            r'\b(\w+Exception)\b',
            r'(?:at|in|from)\s+(\w+)',
        ]
        
        for pattern in error_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1) if len(match.groups()) == 1 else match.group(2)
        
        # Extract first capitalized word
        words = line.split()
        for word in words:
            if word[0].isupper():
                return word.lower()
        
        return 'unknown'
    
    def get_signature(self, line):
        """
        Get a compact signature for a log line.
        Combines error type with first few normalized tokens, excluding timestamps.
        
        Args:
            line (str): The log line
            
        Returns:
            str: A compact signature
        """
        error_type = self.extract_error_type(line)
        normalized = self.normalize(line)
        
        # Remove timestamps - be more aggressive
        # Removes [YYYY-MM-DD HH:MM:SS.mmm] and similar patterns
        normalized = re.sub(r'\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.?\d*\]', '', normalized)
        # Also remove loose timestamps
        normalized = re.sub(r'\d{1,2}:\d{2}:\d{2}\.?\d*\]?', '', normalized)
        # Remove error/warn/critical labels that might be duplicated
        normalized = re.sub(r'(error|warn|critical|info|debug):\s*', '', normalized, flags=re.IGNORECASE)
        
        # Get meaningful tokens
        tokens = normalized.split()
        # Filter out very short tokens and duplicates
        tokens = [t for t in tokens if len(t) > 2][:4]
        
        signature = f"{error_type}|" + " ".join(tokens)
        return signature[:90]  # Limit signature length








# added: change 6
_added_marker_6 = 6


# added: change 13
_added_marker_13 = 13


# added: change 20
_added_marker_20 = 20


# added: src change 6
_added_marker_new_6 = 6


# added: src change 13
_added_marker_new_13 = 13


# added: src change 20
_added_marker_new_20 = 20

