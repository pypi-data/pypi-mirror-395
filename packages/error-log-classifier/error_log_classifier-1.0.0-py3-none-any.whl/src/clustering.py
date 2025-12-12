"""
Clustering Module
Groups similar error log lines together.
"""

import re
from collections import defaultdict, Counter


class ErrorClusterer:
    """Clusters similar error log lines."""
    
    def __init__(self, similarity_threshold=0.7):
        """
        Initialize the clusterer.
        
        Args:
            similarity_threshold (float): Minimum similarity to group lines (0-1)
        """
        self.similarity_threshold = similarity_threshold
        self.clusters = defaultdict(list)
        self.cluster_count = 0
    
    def cluster_by_signature(self, lines_with_signatures):
        """
        Cluster lines based on signatures.
        
        Args:
            lines_with_signatures (iterable): Iterator of (line_num, line, signature) tuples
            
        Returns:
            dict: {signature: [(line_num, line), ...]}
        """
        clusters = defaultdict(list)
        
        for line_num, line, signature in lines_with_signatures:
            clusters[signature].append((line_num, line))
        
        self.clusters = clusters
        self.cluster_count = len(clusters)
        return clusters
    
    def get_top_clusters(self, clusters, top_n=10):
        """
        Get the most frequent clusters.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            top_n (int): Number of top clusters to return
            
        Returns:
            list: [(signature, count, [(line_num, line), ...]), ...]
        """
        cluster_items = [
            (sig, len(lines), lines)
            for sig, lines in clusters.items()
        ]
        
        # Sort by frequency
        cluster_items.sort(key=lambda x: x[1], reverse=True)
        
        return cluster_items[:top_n]
    
    def get_cluster_stats(self, clusters):
        """
        Calculate statistics about clusters.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            
        Returns:
            dict: Statistics about the clusters
        """
        if not clusters:
            return {
                'total_clusters': 0,
                'total_lines': 0,
                'avg_cluster_size': 0,
                'largest_cluster': 0,
                'smallest_cluster': 0,
                'median_cluster_size': 0,
            }
        
        cluster_sizes = [len(lines) for lines in clusters.values()]
        total_lines = sum(cluster_sizes)
        
        return {
            'total_clusters': len(clusters),
            'total_lines': total_lines,
            'avg_cluster_size': total_lines / len(clusters) if clusters else 0,
            'largest_cluster': max(cluster_sizes) if cluster_sizes else 0,
            'smallest_cluster': min(cluster_sizes) if cluster_sizes else 0,
            'median_cluster_size': sorted(cluster_sizes)[len(cluster_sizes)//2] if cluster_sizes else 0,
        }
    
    def find_similar_clusters(self, clusters, pattern):
        """
        Find clusters matching a pattern.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            pattern (str): Regex pattern to match
            
        Returns:
            dict: Matching clusters
        """
        regex = re.compile(pattern, re.IGNORECASE)
        matching = {}
        
        for sig, lines in clusters.items():
            if regex.search(sig) or any(regex.search(line) for _, line in lines):
                matching[sig] = lines
        
        return matching
    
    def get_frequency_counter(self, clusters):
        """
        Get a frequency counter for cluster sizes.
        
        Args:
            clusters (dict): {signature: [(line_num, line), ...]}
            
        Returns:
            Counter: Frequency distribution of cluster sizes
        """
        sizes = [len(lines) for lines in clusters.values()]
        return Counter(sizes)
    
    def memory_usage_estimate(self):
        """
        Estimate memory usage of clusters.
        
        Returns:
            dict: Estimated memory usage
        """
        total_lines = sum(len(lines) for lines in self.clusters.values())
        avg_line_size = 200  # bytes, estimate
        
        estimated_bytes = total_lines * avg_line_size
        estimated_mb = estimated_bytes / (1024 * 1024)
        
        return {
            'total_lines': total_lines,
            'clusters': len(self.clusters),
            'estimated_mb': estimated_mb,
            'estimated_gb': estimated_mb / 1024,
        }








# added: change 1
_added_marker_1 = 1


# added: change 8
_added_marker_8 = 8


# added: change 15
_added_marker_15 = 15


# added: src change 1
_added_marker_new_1 = 1


# added: src change 8
_added_marker_new_8 = 8


# added: src change 15
_added_marker_new_15 = 15

