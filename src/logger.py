"""
Logging setup for FileSync.

Configures logging based on configuration settings.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(config: dict, log_file: Optional[Path] = None) -> None:
    """
    Setup logging configuration.
    
    Args:
        config: Configuration dictionary
        log_file: Optional override for log file path
    """
    log_config = config.get('logging', {})
    level = log_config.get('level', 'INFO')
    log_format = log_config.get('format', '%(asctime)s - %(levelname)s - %(message)s')
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)
    elif log_config.get('file'):
        # Use file from config
        log_file_path = Path(log_config['file'])
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
