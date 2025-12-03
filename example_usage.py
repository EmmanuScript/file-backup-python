# Example usage script for FileSync
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config_manager import ConfigManager
from sync_engine import SyncEngine
from logger import setup_logging

def main():
    """Example of using FileSync programmatically."""
    
    # Load configuration
    config_manager = ConfigManager(Path('config.yaml'))
    config = config_manager.config
    
    # Setup logging
    setup_logging(config)
    
    # Create sync engine
    source = Path.home() / 'Documents'
    destination = Path.home() / 'Backup' / 'Documents'
    
    engine = SyncEngine(str(source), str(destination), config)
    
    # Perform sync
    print(f"Syncing {source} to {destination}...")
    stats = engine.sync()
    
    print(f"\nSync completed:")
    print(f"  Copied: {stats['copied']}")
    print(f"  Updated: {stats['updated']}")
    print(f"  Errors: {stats['errors']}")

if __name__ == '__main__':
    main()
