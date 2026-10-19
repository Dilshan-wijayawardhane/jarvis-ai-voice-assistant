#!/usr/bin/env python3
"""Initialize the JARVIS database."""

import sqlite3
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from utils.logger import logger

def init_database():
    """Create the database and tables if they don't exist."""
    try:
        db_path = config.db_path
        
        # Ensure data directory exists
        config.data_dir.mkdir(exist_ok=True)
        
        # Connect to database (creates file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_message TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        # Create index for timestamp
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON conversations(timestamp DESC)
        ''')
        
        # Create index for user messages (for faster search)
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_message 
            ON conversations(user_message)
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database initialized successfully at {db_path}")
        print(f"✓ Database created: {db_path}")
        print("✓ Tables: conversations")
        print("✓ Indexes: timestamp, user_message")
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        print(f"✗ Database initialization failed: {e}")
        return False

def verify_database():
    """Verify the database structure."""
    try:
        db_path = config.db_path
        
        if not db_path.exists():
            print(f"✗ Database not found at {db_path}")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
        if not cursor.fetchone():
            print("✗ Table 'conversations' not found")
            conn.close()
            return False
        
        # Check schema
        cursor.execute("PRAGMA table_info(conversations)")
        columns = cursor.fetchall()
        expected_columns = ['id', 'timestamp', 'user_message', 'assistant_response', 'metadata']
        
        actual_columns = [col[1] for col in columns]
        
        print(f"✓ Table 'conversations' found with columns: {actual_columns}")
        
        # Get row count
        cursor.execute("SELECT COUNT(*) FROM conversations")
        count = cursor.fetchone()[0]
        print(f"✓ {count} conversations in database")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("JARVIS Database Initialization")
    print("=" * 50)
    print()
    
    # Initialize database
    if init_database():
        print("\nDatabase structure:")
        verify_database()
        print("\n✓ Database is ready for use!")
    else:
        print("\n✗ Database initialization failed")
        sys.exit(1)