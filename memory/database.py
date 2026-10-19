"""SQLite database for conversation storage."""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import json

from utils.logger import logger

class Database:
    """Database manager for JARVIS conversations."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Create database tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
                
                conn.commit()
                logger.info(f"Database initialized at {self.db_path}")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def save_conversation(
        self, 
        user_message: str, 
        assistant_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Save a conversation entry to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                timestamp = datetime.now().isoformat()
                metadata_json = json.dumps(metadata) if metadata else None
                
                cursor.execute('''
                    INSERT INTO conversations (timestamp, user_message, assistant_response, metadata)
                    VALUES (?, ?, ?, ?)
                ''', (timestamp, user_message, assistant_response, metadata_json))
                
                conn.commit()
                conversation_id = cursor.lastrowid
                logger.debug(f"Saved conversation {conversation_id}")
                return conversation_id
                
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
            return -1
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, timestamp, user_message, assistant_response, metadata
                    FROM conversations
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                results = []
                for row in cursor.fetchall():
                    result = dict(row)
                    if result.get('metadata'):
                        result['metadata'] = json.loads(result['metadata'])
                    results.append(result)
                
                return results
                
        except Exception as e:
            logger.error(f"Failed to get conversations: {e}")
            return []
    
    def get_conversation_history_for_context(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get conversation history formatted for LLM context."""
        conversations = self.get_recent_conversations(limit)
        
        # Reverse to get chronological order
        history = []
        for conv in reversed(conversations):
            history.append({
                'role': 'user',
                'content': conv['user_message']
            })
            history.append({
                'role': 'assistant',
                'content': conv['assistant_response']
            })
        
        return history
    
    def clear_conversation_history(self) -> bool:
        """Clear all conversation history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM conversations')
                conn.commit()
                logger.info("Cleared conversation history")
                return True
                
        except Exception as e:
            logger.error(f"Failed to clear conversation history: {e}")
            return False
    
    def get_conversation_count(self) -> int:
        """Get total number of conversations."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM conversations')
                count = cursor.fetchone()[0]
                return count
                
        except Exception as e:
            logger.error(f"Failed to get conversation count: {e}")
            return 0
    
    def delete_conversation(self, conversation_id: int) -> bool:
        """Delete a specific conversation by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Failed to delete conversation {conversation_id}: {e}")
            return False