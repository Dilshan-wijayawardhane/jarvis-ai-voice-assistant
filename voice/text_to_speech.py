"""Text-to-speech module for JARVIS."""

import asyncio
import threading
import edge_tts
import pyttsx3
from typing import Optional, Callable
from pathlib import Path

from config import config
from utils.logger import logger

class TextToSpeech:
    """Text-to-speech using edge-tts with fallback to pyttsx3."""
    
    def __init__(self):
        self.voice = config.tts_voice
        self.is_speaking = False
        self._use_edge_tts = True
        
        # Initialize fallback TTS
        try:
            self.fallback_engine = pyttsx3.init()
            self.fallback_engine.setProperty('rate', 180)
            self.fallback_engine.setProperty('volume', 0.9)
        except Exception as e:
            logger.warning(f"Fallback TTS initialization failed: {e}")
            self.fallback_engine = None
    
    def speak(self, text: str, callback: Optional[Callable] = None) -> bool:
        """Speak the given text."""
        if not text or not text.strip():
            return False
        
        try:
            self.is_speaking = True
            logger.info(f"Speaking: {text[:100]}...")
            
            # Try edge-tts first
            if self._use_edge_tts:
                try:
                    self._speak_edge_tts(text)
                except Exception as e:
                    logger.warning(f"Edge-TTS failed: {e}, using fallback")
                    self._use_edge_tts = False
                    self._speak_fallback(text)
            else:
                self._speak_fallback(text)
            
            self.is_speaking = False
            
            if callback:
                callback()
            
            return True
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            self.is_speaking = False
            return False
    
    def _speak_edge_tts(self, text: str) -> None:
        """Speak using edge-tts."""
        async def _speak():
            try:
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save('temp_tts.mp3')
                
                # Play the audio
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load('temp_tts.mp3')
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
                
                pygame.mixer.quit()
                
                # Clean up
                Path('temp_tts.mp3').unlink(missing_ok=True)
                
            except Exception as e:
                logger.error(f"Edge-TTS playback error: {e}")
                raise
        
        # Run async in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_speak())
        finally:
            loop.close()
    
    def _speak_fallback(self, text: str) -> None:
        """Speak using fallback TTS engine."""
        if self.fallback_engine:
            self.fallback_engine.say(text)
            self.fallback_engine.runAndWait()
        else:
            logger.error("No TTS engine available")
            # Print to console as fallback
            print(f"\nJARVIS: {text}\n")
    
    def is_playing(self) -> bool:
        """Check if TTS is currently playing."""
        return self.is_speaking
    
    def stop_speaking(self) -> None:
        """Stop current speech."""
        self.is_speaking = False
        if self.fallback_engine:
            self.fallback_engine.stop()
        logger.debug("Stopped TTS")
    
    def test_tts(self) -> bool:
        """Test TTS functionality."""
        try:
            logger.info("Testing TTS...")
            self.speak("Hello, this is a test of the text to speech system.")
            return True
        except Exception as e:
            logger.error(f"TTS test failed: {e}")
            return False