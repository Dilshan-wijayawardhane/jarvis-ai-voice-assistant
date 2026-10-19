"""Configuration management for JARVIS."""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

class Config:
    """Central configuration manager for JARVIS."""
    
    def __init__(self):
        # Load environment variables
        env_path = Path(__file__).parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        else:
            load_dotenv()
        
        # LLM Configuration
        self.llm_api_key: str = os.getenv('LLM_API_KEY', '')
        self.llm_base_url: str = os.getenv('LLM_BASE_URL', 'https://api.openai.com/v1')
        self.llm_model: str = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
        
        # JARVIS Configuration
        self.wake_word: str = os.getenv('WAKE_WORD', 'jarvis').lower()
        self.tts_voice: str = os.getenv('TTS_VOICE', 'en-US-JennyNeural')
        self.max_conversation_history: int = int(os.getenv('MAX_CONVERSATION_HISTORY', '10'))
        self.voice_enabled: bool = os.getenv('VOICE_ENABLED', 'true').lower() == 'true'
        self.wake_word_enabled: bool = os.getenv('WAKE_WORD_ENABLED', 'true').lower() == 'true'
        
        # Audio Configuration
        self.microphone_index: int = int(os.getenv('MICROPHONE_INDEX', '0'))
        self.sample_rate: int = int(os.getenv('SAMPLE_RATE', '16000'))
        self.chunk_size: int = int(os.getenv('CHUNK_SIZE', '1024'))
        
        # Paths
        self.base_dir: Path = Path(__file__).parent
        self.data_dir: Path = self.base_dir / 'data'
        self.db_path: Path = self.data_dir / 'jarvis.db'
        
        # Validate configuration
        self._validate()
    
    def _validate(self) -> None:
        """Validate configuration settings."""
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)
        
        # Check for API key
        if not self.llm_api_key:
            import logging
            logging.warning("LLM_API_KEY not set. AI features will not work.")
    
    def is_llm_configured(self) -> bool:
        """Check if LLM is properly configured."""
        return bool(self.llm_api_key)
    
    def is_voice_enabled(self) -> bool:
        """Check if voice features are enabled."""
        return self.voice_enabled

# Global configuration instance
config = Config()