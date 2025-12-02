"""
Backup management module.

Handles full and incremental backup operations.
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from .file_scanner import FileScanner
from .hasher import FileHasher
import logging


class BackupManager:
    """Manages backup and restore operations."""
    
    def __init__(self, config: dict):
        self.config = config
        self.scanner = FileScanner(config.get('filters', {}))
        self.hasher = FileHasher()
        self.logger = logging.getLogger(__name__)
        
    def create_backup(self, source: Path, backup_dir: Path) -> dict:
        """
        Create a backup of source directory.
        
        Args:
            source: Source directory to backup
            backup_dir: Destination for backup
            
        Returns:
            Dictionary with backup metadata
        """
        backup_type = self.config.get('backup', {}).get('type', 'full')
        
        if backup_type == 'full':
            return self._full_backup(source, backup_dir)
        elif backup_type == 'incremental':
            return self._incremental_backup(source, backup_dir)
        else:
            raise ValueError(f"Unknown backup type: {backup_type}")
    
    def _full_backup(self, source: Path, backup_dir: Path) -> dict:
        """
        Create a full backup.
        
        Copies all files from source to a timestamped backup directory.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f"full_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)
        
        files = self.scanner.scan(source)
        copied = 0
        errors = 0
        
        for file_path in files:
            try:
                relative_path = file_path.relative_to(source)
                dest_path = backup_path / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(file_path, dest_path)
                copied += 1
            except Exception as e:
                # Different logging style than other modules
                print(f"ERROR: Failed to backup {file_path}: {e}")
                errors += 1
        
        # Save metadata
        metadata = {
            'type': 'full',
            'timestamp': timestamp,
            'source': str(source),
            'files_copied': copied,
            'errors': errors
        }
        
        self._save_metadata(backup_path, metadata)
        
        # Clean old backups
        self._cleanup_old_backups(backup_dir)
        
        return metadata
    
    def _incremental_backup(self, source: Path, backup_dir: Path) -> dict:
        """
        Create an incremental backup.
        
        Only backs up files that have changed since last backup.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f"incr_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Find last backup to compare against
        last_backup = self._find_last_backup(backup_dir)
        last_hashes = {}
        
        if last_backup:
            last_hashes = self._load_hashes(last_backup)
        
        files = self.scanner.scan(source)
        copied = 0
        skipped = 0
        errors = 0
        current_hashes = {}
        
        for file_path in files:
            try:
                relative_path = file_path.relative_to(source)
                file_hash = self.hasher.hash_file(file_path)
                current_hashes[str(relative_path)] = file_hash
                
                # Check if file changed
                if str(relative_path) in last_hashes:
                    if last_hashes[str(relative_path)] == file_hash:
                        skipped += 1
                        continue
                
                # Copy changed or new file
                dest_path = backup_path / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_path)
                copied += 1
                
            except Exception as e:
                self.logger.error(f"Backup error for {file_path}: {e}")
                errors += 1
        
        # Save hashes for next incremental backup
        self._save_hashes(backup_path, current_hashes)
        
        metadata = {
            'type': 'incremental',
            'timestamp': timestamp,
            'source': str(source),
            'files_copied': copied,
            'files_skipped': skipped,
            'errors': errors,
            'base_backup': str(last_backup) if last_backup else None
        }
        
        self._save_metadata(backup_path, metadata)
        self._cleanup_old_backups(backup_dir)
        
        return metadata
    
    def restore(self, backup_path: Path, destination: Path) -> dict:
        """
        Restore files from backup to destination.
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")
        
        metadata = self._load_metadata(backup_path)
        
        if metadata.get('type') == 'incremental':
            # For incremental, need to restore base backup first
            # This is incomplete! Should chain through all incrementals
            pass
        
        restored = 0
        errors = 0
        
        for file_path in backup_path.rglob('*'):
            if file_path.is_file() and file_path.name not in ['metadata.json', 'hashes.json']:
                try:
                    relative_path = file_path.relative_to(backup_path)
                    dest_path = destination / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    shutil.copy2(file_path, dest_path)
                    restored += 1
                except Exception as e:
                    self.logger.error(f"Restore error: {e}")
                    errors += 1
        
        return {'restored': restored, 'errors': errors}
    
    def _find_last_backup(self, backup_dir: Path) -> Optional[Path]:
        """Find the most recent backup directory."""
        if not backup_dir.exists():
            return None
        
        backups = [d for d in backup_dir.iterdir() if d.is_dir()]
        if not backups:
            return None
        
        # Sort by name (timestamp based)
        backups.sort(reverse=True)
        return backups[0]
    
    def _save_metadata(self, backup_path: Path, metadata: dict) -> None:
        """Save backup metadata to JSON file."""
        metadata_file = backup_path / 'metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _load_metadata(self, backup_path: Path) -> dict:
        """Load backup metadata from JSON file."""
        metadata_file = backup_path / 'metadata.json'
        if not metadata_file.exists():
            return {}
        
        with open(metadata_file, 'r') as f:
            return json.load(f)
    
    def _save_hashes(self, backup_path: Path, hashes: dict) -> None:
        """Save file hashes for incremental backup."""
        hash_file = backup_path / 'hashes.json'
        with open(hash_file, 'w') as f:
            json.dump(hashes, f, indent=2)
    
    def _load_hashes(self, backup_path: Path) -> dict:
        """Load file hashes from backup."""
        hash_file = backup_path / 'hashes.json'
        if not hash_file.exists():
            return {}
        
        with open(hash_file, 'r') as f:
            return json.load(f)
    
    def _cleanup_old_backups(self, backup_dir: Path) -> None:
        """
        Remove old backups beyond retention limit.
        """
        retain_versions = self.config.get('backup', {}).get('retain_versions', 5)
        
        if not backup_dir.exists():
            return
        
        backups = sorted([d for d in backup_dir.iterdir() if d.is_dir()], 
                        reverse=True)
        
        # Keep only the newest retain_versions
        for old_backup in backups[retain_versions:]:
            try:
                shutil.rmtree(old_backup)
                # Inconsistent logging again!
                print(f"Cleaned up old backup: {old_backup.name}")
            except Exception as e:
                self.logger.error(f"Failed to cleanup {old_backup}: {e}")
