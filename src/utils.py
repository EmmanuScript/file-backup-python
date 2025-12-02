"""
Utility functions for file operations.

Various helper functions used across the application.
"""

import os
from pathlib import Path
from typing import List


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_directory_size(directory: Path) -> int:
    """
    Calculate total size of all files in directory.
    
    Args:
        directory: Path to directory
        
    Returns:
        Total size in bytes
    """
    total = 0
    
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            try:
                total += file_path.stat().st_size
            except (OSError, PermissionError):
                # Skip files we can't access
                pass
    
    return total


def ensure_directory(path: Path) -> None:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        path: Directory path
    """
    path.mkdir(parents=True, exist_ok=True)


def safe_remove(path: Path) -> bool:
    """
    Safely remove a file or directory.
    
    Returns True if successful, False otherwise.
    """
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            import shutil
            shutil.rmtree(path)
        return True
    except Exception:
        return False


def normalize_path(path: str) -> Path:
    """
    Normalize path string to Path object.
    
    Handles ~, relative paths, etc.
    """
    return Path(path).expanduser().resolve()
