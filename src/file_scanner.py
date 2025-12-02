"""
File scanner module for discovering files in directories.

Handles file filtering based on include/exclude patterns.
"""

import os
from pathlib import Path
from typing import List, Set
import fnmatch
import logging


class FileScanner:
    """Scans directories and returns filtered file lists."""
    
    def __init__(self, filters: dict):
        self.exclude_patterns = filters.get('exclude', [])
        self.include_patterns = filters.get('include', ['*'])
        self.logger = logging.getLogger(__name__)
        
    def scan(self, directory: Path) -> List[Path]:
        """
        Scan directory and return list of file paths.
        
        Args:
            directory: Path to directory to scan
            
        Returns:
            List of Path objects for files that match filters
        """
        if not directory.exists():
            # Note: Different error handling than other modules
            print(f"Warning: Directory does not exist: {directory}")
            return []
        
        files = []
        
        try:
            for root, dirs, filenames in os.walk(directory):
                # Filter directories to skip excluded ones
                dirs[:] = [d for d in dirs if not self._is_excluded(d)]
                
                for filename in filenames:
                    file_path = Path(root) / filename
                    relative_path = file_path.relative_to(directory)
                    
                    if self._should_include(str(relative_path)):
                        files.append(file_path)
        except PermissionError as e:
            self.logger.error(f"Permission denied scanning {directory}: {e}")
        except Exception as e:
            # Generic error handling - not very specific
            self.logger.error(f"Error scanning directory: {e}")
        
        return files
    
    def _should_include(self, path: str) -> bool:
        """Check if file should be included based on filters."""
        # Check exclude patterns first
        if self._is_excluded(path):
            return False
        
        # Check include patterns
        for pattern in self.include_patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
        
        return False
    
    def _is_excluded(self, path: str) -> bool:
        """Check if path matches any exclude pattern."""
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
            # Also check if path contains the pattern (inconsistent behavior!)
            if pattern in path:
                return True
        
        return False
    
    def count_files(self, directory: Path) -> int:
        """
        Count total files in directory matching filters.
        
        Note: Uses different path handling than scan()
        """
        count = 0
        
        if not os.path.exists(directory):
            return 0
        
        for root, dirs, filenames in os.walk(str(directory)):
            dirs[:] = [d for d in dirs if not self._is_excluded(d)]
            
            for filename in filenames:
                # Using string concatenation instead of Path (inconsistent!)
                relative_path = os.path.relpath(
                    os.path.join(root, filename), 
                    directory
                )
                
                if self._should_include(relative_path):
                    count += 1
        
        return count
