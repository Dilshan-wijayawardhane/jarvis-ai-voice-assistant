"""Conversation management for JARVIS."""

from typing import List, Dict, Optional
from memory.database import Database
from config import config
from utils.logger import logger

class ConversationManager:
    """Manage conversation context and history."""
    
    def __init__(self, database: Database):
        self.database = database
        self.current_conversation: List[Dict[str, str]] = []
        self.max_history = config.max_conversation_history
    
    def add_message(self, user_message: str, assistant_response: str) -> None:
        """Add a message to the current conversation."""
        self.current_conversation.append({
            'role': 'user',
            'content': user_message
        })
        self.current_conversation.append({
            'role': 'assistant',
            'content': assistant_response
        })
        
        # Keep conversation within limits
        if len(self.current_conversation) > self.max_history * 2:
            # Remove oldest messages
            self.current_conversation = self.current_conversation[
                -(self.max_history * 2):
            ]
        
        # Save to database
        self.database.save_conversation(user_message, assistant_response)
    
    def get_context(self) -> List[Dict[str, str]]:
        """Get current conversation context."""
        return self.current_conversation.copy()
    
    def clear_conversation(self) -> None:
        """Clear current conversation context."""
        self.current_conversation = []
        logger.debug("Conversation context cleared")
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history from database."""
        if limit is None:
            limit = self.max_history
        return self.database.get_conversation_history_for_context(limit)
    
    def format_conversation(self) -> str:
        """Format conversation for display."""
        messages = self.get_context()
        if not messages:
            return "No conversation history"
        
        formatted = []
        for msg in messages:
            role = "You" if msg['role'] == 'user' else "JARVIS"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)