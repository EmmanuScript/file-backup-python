"""Tests for sync engine."""

import pytest
from pathlib import Path
import tempfile
from src.sync_engine import SyncEngine
from src.config_manager import ConfigManager


def test_sync_new_files():
    """Test syncing new files from source to destination."""
    config = ConfigManager().config
    
    with tempfile.TemporaryDirectory() as source_dir, \
         tempfile.TemporaryDirectory() as dest_dir:
        
        # Create files in source
        source_path = Path(source_dir)
        (source_path / 'file1.txt').write_text('content1')
        (source_path / 'file2.txt').write_text('content2')
        
        # Sync
        engine = SyncEngine(source_dir, dest_dir, config)
        stats = engine.sync()
        
        assert stats['copied'] == 2
        assert stats['updated'] == 0
        
        # Verify files exist in destination
        dest_path = Path(dest_dir)
        assert (dest_path / 'file1.txt').exists()
        assert (dest_path / 'file2.txt').exists()


def test_sync_modified_files():
    """Test syncing modified files."""
    config = ConfigManager().config
    
    with tempfile.TemporaryDirectory() as source_dir, \
         tempfile.TemporaryDirectory() as dest_dir:
        
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)
        
        # Create identical files
        (source_path / 'file.txt').write_text('original')
        (dest_path / 'file.txt').write_text('original')
        
        # Modify source
        (source_path / 'file.txt').write_text('modified content')
        
        # Sync
        engine = SyncEngine(source_dir, dest_dir, config)
        stats = engine.sync()
        
        assert stats['updated'] >= 1
        assert (dest_path / 'file.txt').read_text() == 'modified content'
