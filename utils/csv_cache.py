"""
CSV file caching utility to avoid reloading unchanged files.
Tracks file modification times and only reloads when files change.
"""
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class CSVCache:
    """Cache for CSV file modification times and data"""
    
    def __init__(self):
        self._file_timestamps: Dict[str, float] = {}
        self._cached_data: Dict[str, any] = {}
    
    def is_file_changed(self, file_path: str) -> bool:
        """
        Check if a file has been modified since last check.
        Returns True if file changed or doesn't exist in cache.
        """
        if not os.path.exists(file_path):
            return False
        
        current_mtime = os.path.getmtime(file_path)
        cached_mtime = self._file_timestamps.get(file_path)
        
        if cached_mtime is None or current_mtime > cached_mtime:
            return True
        
        return False
    
    def update_cache(self, file_path: str, data: any = None):
        """Update cache timestamp for a file, optionally store data"""
        if os.path.exists(file_path):
            self._file_timestamps[file_path] = os.path.getmtime(file_path)
            if data is not None:
                self._cached_data[file_path] = data
    
    def get_cached_data(self, file_path: str) -> Optional[any]:
        """Get cached data for a file if available and not stale"""
        if self.is_file_changed(file_path):
            return None
        return self._cached_data.get(file_path)
    
    def clear_cache(self, file_path: str = None):
        """Clear cache for a specific file or all files"""
        if file_path:
            self._file_timestamps.pop(file_path, None)
            self._cached_data.pop(file_path, None)
        else:
            self._file_timestamps.clear()
            self._cached_data.clear()

# Global cache instance
csv_cache = CSVCache()

