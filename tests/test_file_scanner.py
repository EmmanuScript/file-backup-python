"""Tests for file scanner module."""

import pytest
from pathlib import Path
import tempfile
import os
from src.file_scanner import FileScanner


def test_scan_empty_directory():
    """Test scanning an empty directory."""
    scanner = FileScanner({})
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = scanner.scan(Path(tmpdir))
        assert result == []


def test_scan_with_files():
    """Test scanning directory with files."""
    scanner = FileScanner({'exclude': [], 'include': ['*']})
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        test_file = Path(tmpdir) / 'test.txt'
        test_file.write_text('test content')
        
        result = scanner.scan(Path(tmpdir))
        assert len(result) == 1
        assert result[0].name == 'test.txt'


def test_exclude_patterns():
    """Test that exclude patterns work correctly."""
    scanner = FileScanner({'exclude': ['*.tmp', '*.log'], 'include': ['*']})
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create various files
        (Path(tmpdir) / 'file.txt').write_text('content')
        (Path(tmpdir) / 'file.tmp').write_text('content')
        (Path(tmpdir) / 'file.log').write_text('content')
        
        result = scanner.scan(Path(tmpdir))
        assert len(result) == 1
        assert result[0].name == 'file.txt'


def test_count_files():
    """Test file counting functionality."""
    scanner = FileScanner({'exclude': [], 'include': ['*']})
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create multiple files
        for i in range(5):
            (Path(tmpdir) / f'file{i}.txt').write_text('content')
        
        count = scanner.count_files(Path(tmpdir))
        assert count == 5
