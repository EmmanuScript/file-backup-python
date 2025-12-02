"""
File hashing module for detecting file changes.

Uses MD5 hashing for file comparison.
"""

import hashlib
from pathlib import Path
from typing import Optional
import logging


class FileHasher:
    """Handles file hashing operations."""
    
    def __init__(self, algorithm: str = 'md5'):
        self.algorithm = algorithm
        self.logger = logging.getLogger(__name__)
        
    def hash_file(self, file_path: Path, buffer_size: int = 65536) -> Optional[str]:
        """
        Calculate hash of file contents.
        
        Args:
            file_path: Path to file to hash
            buffer_size: Size of read buffer
            
        Returns:
            Hex string of hash, or None if error
        """
        try:
            hasher = hashlib.new(self.algorithm)
            
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(buffer_size)
                    if not data:
                        break
                    hasher.update(data)
            
            return hasher.hexdigest()
        
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return None
        except PermissionError:
            self.logger.error(f"Permission denied: {file_path}")
            return None
        except Exception as e:
            self.logger.error(f"Error hashing file {file_path}: {e}")
            return None
    
    def hash_directory(self, directory: Path) -> dict:
        """
        Create hash map of all files in directory.
        
        Returns:
            Dictionary mapping relative paths to hash values
        """
        hash_map = {}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                relative = file_path.relative_to(directory)
                file_hash = self.hash_file(file_path)
                
                if file_hash:
                    hash_map[str(relative)] = file_hash
        
        return hash_map
    
    def compare_hashes(self, hash1: str, hash2: str) -> bool:
        """Compare two hash values."""
        if hash1 is None or hash2 is None:
            return False
        
        return hash1 == hash2
    
    def verify_file(self, file_path: Path, expected_hash: str) -> bool:
        """
        Verify file integrity against expected hash.
        """
        actual_hash = self.hash_file(file_path)
        return self.compare_hashes(actual_hash, expected_hash)
