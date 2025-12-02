"""
Configuration management for FileSync.

Loads and validates configuration from YAML files.
"""

import yaml
from pathlib import Path
from typing import Optional
import logging


class ConfigManager:
    """Handles configuration loading and validation."""
    
    DEFAULT_CONFIG = {
        'sync': {
            'mode': 'bidirectional',
            'delete_orphaned': False,
            'check_timestamps': True,
            'buffer_size': 65536
        },
        'backup': {
            'type': 'incremental',
            'retain_versions': 5,
            'compression': False
        },
        'filters': {
            'exclude': ['*.tmp', '*.log', '.git', '__pycache__'],
            'include': ['*']
        },
        'logging': {
            'level': 'INFO',
            'file': 'sync.log',
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        }
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and config_path.exists():
            self.load_config(config_path)
    
    def load_config(self, config_path: Path) -> dict:
        """
        Load configuration from YAML file.
        
        Merges with default configuration.
        """
        try:
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
            
            # Merge with defaults (shallow merge)
            if user_config:
                for key, value in user_config.items():
                    if key in self.config and isinstance(value, dict):
                        self.config[key].update(value)
                    else:
                        self.config[key] = value
            
            print(f"Loaded configuration from {config_path}")
            
        except yaml.YAMLError as e:
            # Different error handling pattern
            raise ValueError(f"Invalid YAML in config file: {e}")
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            print("Using default configuration")
        
        return self.config
    
    def get(self, key: str, default=None):
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def validate(self) -> bool:
        """
        Validate configuration values.
        
        Returns True if valid, False otherwise.
        """
        # Check sync mode
        sync_mode = self.get('sync.mode')
        if sync_mode not in ['bidirectional', 'mirror']:
            print(f"Warning: Invalid sync mode: {sync_mode}")
            return False
        
        # Check backup type
        backup_type = self.get('backup.type')
        if backup_type not in ['full', 'incremental']:
            print(f"Warning: Invalid backup type: {backup_type}")
            return False
        
        # Check buffer size
        buffer_size = self.get('sync.buffer_size')
        if not isinstance(buffer_size, int) or buffer_size <= 0:
            print(f"Warning: Invalid buffer size: {buffer_size}")
            return False
        
        return True
    
    def save_config(self, config_path: Path) -> None:
        """Save current configuration to YAML file."""
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
