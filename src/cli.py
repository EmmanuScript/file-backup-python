"""
Command-line interface for FileSync.

Provides sync, backup, and restore commands.
"""

import click
from pathlib import Path
import sys
from .config_manager import ConfigManager
from .sync_engine import SyncEngine
from .backup_manager import BackupManager
from .logger import setup_logging
import logging


@click.group()
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """FileSync - Backup and synchronization tool."""
    ctx.ensure_object(dict)
    
    # Load configuration
    config_path = Path(config) if config else Path('config.yaml')
    config_manager = ConfigManager(config_path if config_path.exists() else None)
    
    # Override log level if verbose
    if verbose:
        config_manager.config['logging']['level'] = 'DEBUG'
    
    setup_logging(config_manager.config)
    
    ctx.obj['config'] = config_manager.config
    ctx.obj['config_manager'] = config_manager


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('destination', type=click.Path())
@click.option('--dry-run', is_flag=True, help='Show what would be done without making changes')
@click.pass_context
def sync(ctx, source, destination, dry_run):
    """
    Synchronize files between SOURCE and DESTINATION directories.
    
    Examples:
        filesync sync /path/to/source /path/to/dest
        filesync sync --dry-run /home/user/docs /backup/docs
    """
    config = ctx.obj['config']
    logger = logging.getLogger(__name__)
    
    source_path = Path(source)
    dest_path = Path(destination)
    
    if not source_path.exists():
        click.echo(f"Error: Source directory does not exist: {source}", err=True)
        sys.exit(1)
    
    # Create destination if it doesn't exist
    dest_path.mkdir(parents=True, exist_ok=True)
    
    if dry_run:
        click.echo("DRY RUN - No changes will be made")
        click.echo("Dry-run mode not fully implemented yet!")
        return
    
    try:
        engine = SyncEngine(str(source_path), str(dest_path), config)
        
        click.echo(f"Syncing {source} -> {destination}")
        stats = engine.sync()
        
        # Display results
        click.echo("\nSync completed:")
        click.echo(f"  Copied: {stats['copied']}")
        click.echo(f"  Updated: {stats['updated']}")
        click.echo(f"  Deleted: {stats['deleted']}")
        click.echo(f"  Skipped: {stats['skipped']}")
        click.echo(f"  Errors: {stats['errors']}")
        
    except KeyboardInterrupt:
        click.echo("\nSync interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('backup_dir', type=click.Path())
@click.option('--type', 'backup_type', type=click.Choice(['full', 'incremental']), 
              help='Type of backup to create')
@click.pass_context
def backup(ctx, source, backup_dir, backup_type):
    """
    Create a backup of SOURCE directory in BACKUP_DIR.
    
    Examples:
        filesync backup /home/user/docs /backups
        filesync backup --type full /data /backups/data
    """
    config = ctx.obj['config']
    
    # Override backup type if specified
    if backup_type:
        config['backup']['type'] = backup_type
    
    source_path = Path(source)
    backup_path = Path(backup_dir)
    
    if not source_path.exists():
        click.echo(f"Error: Source does not exist: {source}", err=True)
        sys.exit(1)
    
    backup_path.mkdir(parents=True, exist_ok=True)
    
    try:
        manager = BackupManager(config)
        
        click.echo(f"Creating {config['backup']['type']} backup...")
        click.echo(f"Source: {source}")
        click.echo(f"Destination: {backup_dir}")
        
        result = manager.create_backup(source_path, backup_path)
        
        click.echo("\nBackup completed:")
        click.echo(f"  Type: {result['type']}")
        click.echo(f"  Timestamp: {result['timestamp']}")
        click.echo(f"  Files copied: {result['files_copied']}")
        if 'files_skipped' in result:
            click.echo(f"  Files skipped: {result['files_skipped']}")
        click.echo(f"  Errors: {result['errors']}")
        
    except Exception as e:
        # Missing specific error handling!
        click.echo(f"Backup failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('backup_path', type=click.Path(exists=True))
@click.argument('destination', type=click.Path())
@click.pass_context
def restore(ctx, backup_path, destination):
    """
    Restore files from BACKUP_PATH to DESTINATION.
    
    Examples:
        filesync restore /backups/full_20231201_120000 /home/user/docs
    """
    config = ctx.obj['config']
    
    backup_dir = Path(backup_path)
    dest_path = Path(destination)
    
    dest_path.mkdir(parents=True, exist_ok=True)
    
    try:
        manager = BackupManager(config)
        
        click.echo(f"Restoring from {backup_path}")
        click.echo(f"Destination: {destination}")
        
        result = manager.restore(backup_dir, dest_path)
        
        click.echo("\nRestore completed:")
        click.echo(f"  Files restored: {result['restored']}")
        click.echo(f"  Errors: {result['errors']}")
        
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Restore failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.pass_context
def status(ctx, directory):
    """
    Show status and statistics for a directory.
    """
    click.echo("Status command not yet implemented!")
    click.echo(f"Directory: {directory}")


if __name__ == '__main__':
    cli(obj={})
