"""Tests for configuration manager."""

import pytest
from pathlib import Path
import tempfile
from src.config_manager import ConfigManager


def test_default_config():
    """Test that default configuration is loaded."""
    manager = ConfigManager()
    
    assert manager.config is not None
    assert 'sync' in manager.config
    assert 'backup' in manager.config
    assert 'filters' in manager.config


def test_get_config_value():
    """Test getting nested configuration values."""
    manager = ConfigManager()
    
    sync_mode = manager.get('sync.mode')
    assert sync_mode == 'bidirectional'
    
    buffer_size = manager.get('sync.buffer_size')
    assert buffer_size == 65536


def test_validate_config():
    """Test configuration validation."""
    manager = ConfigManager()
    
    # Default config should be valid
    assert manager.validate() == True
    
    # Test with invalid sync mode
    manager.config['sync']['mode'] = 'invalid_mode'
    assert manager.validate() == False
