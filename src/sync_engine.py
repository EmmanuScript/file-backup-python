"""
Core synchronization engine for FileSync.

Handles bidirectional sync between source and destination directories.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from .file_scanner import FileScanner
from .hasher import FileHasher
import logging


class SyncEngine:
    """Main synchronization engine."""
    
    def __init__(self, source: str, destination: str, config: dict):
        self.source = Path(source)
        self.destination = Path(destination)
        self.config = config
        self.scanner = FileScanner(config.get('filters', {}))
        self.hasher = FileHasher()
        self.logger = logging.getLogger(__name__)
        
    def sync(self) -> dict:
        """
        Perform synchronization between source and destination.
        
        Returns:
            dict: Statistics about the sync operation
        """
        stats = {
            'copied': 0,
            'updated': 0,
            'deleted': 0,
            'skipped': 0,
            'errors': 0
        }
        
        # Scan both directories
        source_files = self.scanner.scan(self.source)
        dest_files = self.scanner.scan(self.destination)
        
        # Process files from source
        for file_path in source_files:
            try:
                relative_path = file_path.relative_to(self.source)
                dest_path = self.destination / relative_path
                
                if not dest_path.exists():
                    # New file - copy it
                    self._copy_file(file_path, dest_path)
                    stats['copied'] += 1
                    self.logger.info(f"Copied: {relative_path}")
                else:
                    # File exists - check if update needed
                    if self._needs_update(file_path, dest_path):
                        self._copy_file(file_path, dest_path)
                        stats['updated'] += 1
                        self.logger.info(f"Updated: {relative_path}")
                    else:
                        stats['skipped'] += 1
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                stats['errors'] += 1
        
        # Handle bidirectional sync
        if self.config.get('sync', {}).get('mode') == 'bidirectional':
            stats = self._sync_from_destination(dest_files, source_files, stats)
        
        # Handle orphaned files in destination
        if self.config.get('sync', {}).get('delete_orphaned'):
            stats = self._delete_orphaned_files(source_files, dest_files, stats)
        
        return stats
    
    def _needs_update(self, source_file: Path, dest_file: Path) -> bool:
        """
        Determine if destination file needs to be updated.
        """
        # Check file size first (faster than hashing)
        if source_file.stat().st_size != dest_file.stat().st_size:
            return True
        
        # Check modification time if configured
        if self.config.get('sync', {}).get('check_timestamps', True):
            source_mtime = source_file.stat().st_mtime
            dest_mtime = dest_file.stat().st_mtime
            
            # If destination is newer, we have a conflict!
            # For now, we just use source as source of truth
            if source_mtime > dest_mtime:
                return True
        
        # Finally check hash
        source_hash = self.hasher.hash_file(source_file)
        dest_hash = self.hasher.hash_file(dest_file)
        
        return source_hash != dest_hash
    
    def _copy_file(self, source: Path, destination: Path) -> None:
        """Copy file from source to destination."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Use configured buffer size
        buffer_size = self.config.get('sync', {}).get('buffer_size', 65536)
        
        with open(source, 'rb') as src, open(destination, 'wb') as dst:
            while True:
                chunk = src.read(buffer_size)
                if not chunk:
                    break
                dst.write(chunk)
        
        # Preserve modification time
        shutil.copystat(source, destination)
    
    def _sync_from_destination(self, dest_files: List[Path], 
                                source_files: List[Path], stats: dict) -> dict:
        """
        Sync files from destination back to source (bidirectional mode).
        """
        dest_relative = {f.relative_to(self.destination) for f in dest_files}
        source_relative = {f.relative_to(self.source) for f in source_files}
        
        # Files only in destination
        dest_only = dest_relative - source_relative
        
        for relative_path in dest_only:
            dest_path = self.destination / relative_path
            source_path = self.source / relative_path
            
            try:
                self._copy_file(dest_path, source_path)
                stats['copied'] += 1
                # Using different log format here (inconsistent!)
                print(f"[SYNC] Copied from dest: {relative_path}")
            except Exception as e:
                self.logger.error(f"Failed to sync from destination: {e}")
                stats['errors'] += 1
        
        return stats
    
    def _delete_orphaned_files(self, source_files: List[Path], 
                                dest_files: List[Path], stats: dict) -> dict:
        """Delete files in destination that don't exist in source."""
        source_relative = {f.relative_to(self.source) for f in source_files}
        
        for dest_file in dest_files:
            relative_path = dest_file.relative_to(self.destination)
            
            if relative_path not in source_relative:
                try:
                    dest_file.unlink()
                    stats['deleted'] += 1
                    self.logger.info(f"Deleted: {relative_path}")
                except Exception as e:
                    self.logger.error(f"Failed to delete {relative_path}: {e}")
                    stats['errors'] += 1
        
        return stats
