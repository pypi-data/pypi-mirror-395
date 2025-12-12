#!/usr/bin/env python3
"""
Migration script to fix inconsistent string_cache naming in session files.

This script walks through /sphere/app/featrix_output and fixes any session files
that have 'string_cache' (singular) instead of 'strings_cache' (plural).

Usage:
    python src/migrate_string_cache_naming.py [--dry-run] [--session-dir PATH]
"""

import json
import logging
import sys
from pathlib import Path
import argparse
import fcntl

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def migrate_session_file(session_path: Path, dry_run: bool = False) -> bool:
    """
    Migrate a single session file to fix string_cache naming.
    
    Args:
        session_path: Path to the .session file
        dry_run: If True, only report what would be changed without modifying files
    
    Returns:
        True if migration was needed/applied, False otherwise
    """
    try:
        # Read the session file
        with open(session_path, 'r') as f:
            # Try to acquire a shared lock (non-blocking)
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                logger.warning(f"⚠️  Session file {session_path} is locked, skipping...")
                return False
            
            try:
                session_data = json.load(f)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        
        # Check if migration is needed
        needs_migration = False
        if 'string_cache' in session_data and 'strings_cache' not in session_data:
            needs_migration = True
            logger.info(f"📝 Found session with 'string_cache' (singular): {session_path.name}")
        
        if not needs_migration:
            return False
        
        if dry_run:
            logger.info(f"   [DRY RUN] Would rename 'string_cache' -> 'strings_cache' in {session_path.name}")
            return True
        
        # Perform migration
        logger.info(f"   Migrating: renaming 'string_cache' -> 'strings_cache'")
        session_data['strings_cache'] = session_data.pop('string_cache')
        
        # Write back to file (using atomic write pattern like save_session)
        temp_path = session_path.parent / f"{session_path.stem}.tmp"
        
        try:
            # Write to temp file
            with open(temp_path, 'w') as f:
                json.dump(session_data, f, indent=4)
            
            # Verify it's valid JSON
            with open(temp_path, 'r') as f:
                json.load(f)
            
            # Atomic rename
            temp_path.rename(session_path)
            logger.info(f"   ✅ Successfully migrated {session_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Error migrating {session_path.name}: {e}")
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()
            return False
            
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in {session_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error processing {session_path}: {e}")
        return False


def migrate_all_sessions(session_dir: Path, dry_run: bool = False):
    """
    Check session directory and migrate all session files.
    
    Args:
        session_dir: Directory containing .session files
        dry_run: If True, only report what would be changed
    """
    if not session_dir.exists():
        logger.error(f"❌ Session directory does not exist: {session_dir}")
        return
    
    if not session_dir.is_dir():
        logger.error(f"❌ Session path is not a directory: {session_dir}")
        return
    
    logger.info(f"🔍 Checking session directory: {session_dir}")
    if dry_run:
        logger.info("   [DRY RUN MODE - no files will be modified]")
    
    # List .session files directly from the directory (no recursive walking)
    try:
        session_files = [f for f in session_dir.iterdir() if f.is_file() and f.suffix == '.session']
    except PermissionError:
        logger.error(f"❌ Permission denied accessing {session_dir}")
        return
    
    logger.info(f"📊 Found {len(session_files)} session files")
    
    migrated_count = 0
    error_count = 0
    
    for session_file in session_files:
        try:
            if migrate_session_file(session_file, dry_run=dry_run):
                migrated_count += 1
        except Exception as e:
            logger.error(f"❌ Unexpected error processing {session_file}: {e}")
            error_count += 1
    
    logger.info("")
    logger.info("=" * 60)
    logger.info(f"📊 Migration Summary:")
    logger.info(f"   Total session files: {len(session_files)}")
    logger.info(f"   Migrated: {migrated_count}")
    logger.info(f"   Errors: {error_count}")
    if dry_run:
        logger.info(f"   [DRY RUN - no files were actually modified]")
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Migrate session files to fix string_cache naming inconsistency"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Only report what would be changed without modifying files'
    )
    parser.add_argument(
        '--session-dir',
        type=str,
        default=None,
        help='Path to session directory (default: /sphere/app/featrix_sessions)'
    )
    
    args = parser.parse_args()
    
    # Determine session directory
    if args.session_dir:
        session_dir = Path(args.session_dir)
    else:
        # Try to get from config
        try:
            from config import config
            session_dir = Path(config.session_dir)
        except (ImportError, AttributeError):
            # Fallback to default
            session_dir = Path("/sphere/app/featrix_sessions")
            logger.warning(f"⚠️  Could not import config, using default: {session_dir}")
    
    logger.info(f"🚀 Starting string_cache migration")
    logger.info(f"   Session directory: {session_dir}")
    
    migrate_all_sessions(session_dir, dry_run=args.dry_run)
    
    if not args.dry_run:
        logger.info("✅ Migration complete!")
    else:
        logger.info("✅ Dry run complete! Use without --dry-run to apply changes.")


if __name__ == "__main__":
    main()

