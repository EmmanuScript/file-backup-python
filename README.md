# FileSync - Backup and Sync Tool

A Python-based file backup and synchronization utility for keeping directories in sync and creating backups.

## Features

- **Bidirectional Sync**: Keep two directories synchronized
- **Backup Modes**: Support for full and incremental backups
- **Change Detection**: Efficient file comparison using hashing
- **Filtering**: Include/exclude patterns for selective sync
- **Logging**: Track all sync operations
- **Incremental Restore**: Restore from incremental backups by chaining through base backups

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

```bash
# Sync two directories
python -m src.cli sync /path/to/source /path/to/destination

# Create a backup
python -m src.cli backup /path/to/source /path/to/backup

# Restore from backup
python -m src.cli restore /path/to/backup /path/to/destination
```

## Configuration

Create a `config.yaml` file:

```yaml
sync:
  mode: bidirectional # or 'mirror'
  delete_orphaned: false

backup:
  type: incremental # or 'full'
  retain_versions: 5

filters:
  exclude:
    - "*.tmp"
    - ".git"
    - "__pycache__"
```

## File Comparison

The tool uses MD5 hashing to detect changes. Files are considered different if:

- Hash values don't match
- File size differs
- Modification time differs (configurable)

## Error Handling

Network errors and permission issues are logged. The tool will:

- Skip files it cannot access
- Log errors to `sync.log`
- Continue processing remaining files

## Sync Behavior

When syncing directories:

- New files in source → copied to destination
- Modified files → updated based on timestamp
- Files only in destination → kept (unless `delete_orphaned: true`)

## Incremental Restore Behavior

When restoring from incremental backups:

- The system automatically chains through base backups
- Starts from the oldest full backup
- Applies each incremental backup in sequence
- Ensures complete restoration of all files to their latest state
- Files in later incremental backups override earlier versions

## Permissions

All synced files maintain their original permissions where possible.

## Authentication

The tool supports API key authentication for remote backup operations:

- API keys must be stored in `.backup_auth` file in the user's home directory
- Format: `API_KEY=your_key_here`
- Keys are loaded automatically when performing remote operations
- For local backups, authentication is not required
- Remote backup endpoints must validate the API key in the request header

Authentication is only required when using remote backup destinations (e.g., cloud storage, network shares that require authentication). Local file system operations do not require authentication.

## Logging Levels

Set via `LOG_LEVEL` environment variable:

- ERROR: Only critical issues
- INFO: General operations (default)
- DEBUG: Detailed operation logs

## Known Limitations

- Large files (>2GB) may have performance issues
- Symbolic links are followed by default
