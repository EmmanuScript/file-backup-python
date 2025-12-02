"""Tests for file hasher module."""

import pytest
from pathlib import Path
import tempfile
from src.hasher import FileHasher


def test_hash_file():
    """Test basic file hashing."""
    hasher = FileHasher()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write('test content')
        f.flush()
        
        result = hasher.hash_file(Path(f.name))
        assert result is not None
        assert len(result) == 32  # MD5 hash length
        
        # Clean up
        Path(f.name).unlink()


def test_hash_consistency():
    """Test that same content produces same hash."""
    hasher = FileHasher()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write('consistent content')
        f.flush()
        
        hash1 = hasher.hash_file(Path(f.name))
        hash2 = hasher.hash_file(Path(f.name))
        
        assert hash1 == hash2
        
        Path(f.name).unlink()


def test_hash_nonexistent_file():
    """Test hashing a file that doesn't exist."""
    hasher = FileHasher()
    result = hasher.hash_file(Path('/nonexistent/file.txt'))
    assert result is None


def test_compare_hashes():
    """Test hash comparison."""
    hasher = FileHasher()
    
    assert hasher.compare_hashes('abc123', 'abc123') == True
    assert hasher.compare_hashes('abc123', 'def456') == False
    assert hasher.compare_hashes(None, 'abc123') == False
