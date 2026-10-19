#!/usr/bin/env python3
"""Database migration script for JARVIS."""

import sqlite3
from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from utils.logger import logger

def get_current_version():
    """Get current database version."""
    try:
        conn = sqlite3.connect(config.db_path)
        cursor = conn.cursor()
        
        # Check if version table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='db_version'")
        if not cursor.fetchone():
            conn.close()
            return 0
        
        cursor.execute("SELECT version FROM db_version ORDER BY version DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 0
        
    except Exception as e:
        logger.error(f"Failed to get database version: {e}")
        return 0

def set_version(version):
    """Set database version."""
    try:
        conn = sqlite3.connect(config.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS db_version (
                version INTEGER PRIMARY KEY,
                migrated_at TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        from datetime import datetime
        cursor.execute(
            "INSERT INTO db_version (version, migrated_at, description) VALUES (?, ?, ?)",
            (version, datetime.now().isoformat(), f"Migration to version {version}")
        )
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Failed to set database version: {e}")
        return False

def migrate_v1_to_v2():
    """Migrate from version 1 to version 2 (add settings table)."""
    logger.info("Migrating database from v1 to v2...")
    
    try:
        conn = sqlite3.connect(config.db_path)
        cursor = conn.cursor()
        
        # Add settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Add conversation metadata column if not exists
        cursor.execute("PRAGMA table_info(conversations)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'duration' not in columns:
            cursor.execute("ALTER TABLE conversations ADD COLUMN duration INTEGER")
            logger.info("Added 'duration' column to conversations")
        
        conn.commit()
        conn.close()
        
        logger.info("Migration to v2 completed")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False

def migrate():
    """Run all necessary migrations."""
    current_version = get_current_version()
    logger.info(f"Current database version: {current_version}")
    
    if current_version < 1:
        # Initial database creation
        from init_database import init_database
        if init_database():
            set_version(1)
            current_version = 1
    
    if current_version < 2:
        if migrate_v1_to_v2():
            set_version(2)
            current_version = 2
    
    logger.info(f"Database migration complete. Version: {current_version}")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("JARVIS Database Migration")
    print("=" * 50)
    print()
    
    if migrate():
        print(f"\n✓ Migration complete! Database version: {get_current_version()}")
    else:
        print("\n✗ Migration failed")
        sys.exit(1)