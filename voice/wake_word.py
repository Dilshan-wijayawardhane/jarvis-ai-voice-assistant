"""Wake word detection for JARVIS."""

import time
import threading
from typing import Optional, Callable
import speech_recognition as sr
import re

from config import config
from utils.logger import logger

class WakeWordDetector:
    """Wake word detection using speech recognition."""
    
    def __init__(self):
        self.wake_word = config.wake_word.lower()
        self.is_listening = False
        self.is_detected = False
        self.recognizer = sr.Recognizer()
        self.microphone_index = config.microphone_index
        
        # Configure recognizer
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5
        
        self._test_microphone()
    
    def _test_microphone(self) -> bool:
        """Test if microphone is available."""
        try:
            sr.Microphone(device_index=self.microphone_index)
            return True
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False
    
    def detect_wake_word(self, callback: Callable[[], None]) -> None:
        """Continuously listen for wake word and call callback when detected."""
        def listener_thread():
            logger.info(f"Wake word detection started: '{self.wake_word}'")
            
            while self.is_listening:
                try:
                    with sr.Microphone(device_index=self.microphone_index) as source:
                        logger.debug("Listening for wake word...")
                        
                        # Adjust for ambient noise
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        
                        try:
                            # Listen for short audio
                            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                            
                            try:
                                # Try to recognize speech
                                text = self.recognizer.recognize_google(audio).lower()
                                logger.debug(f"Heard: {text}")
                                
                                # Check for wake word
                                if self._contains_wake_word(text):
                                    logger.info(f"Wake word detected: {text}")
                                    self.is_detected = True
                                    callback()
                                    self.is_detected = False
                                    
                            except sr.UnknownValueError:
                                # No speech recognized, continue
                                pass
                            except sr.RequestError as e:
                                logger.warning(f"Speech recognition service error: {e}")
                                # Short delay before retry
                                time.sleep(0.5)
                                
                        except sr.WaitTimeoutError:
                            # No speech detected, continue
                            pass
                        
                except Exception as e:
                    logger.error(f"Wake word detection error: {e}")
                    time.sleep(1)  # Wait before retry
            
            logger.info("Wake word detection stopped")
        
        if not self.is_listening:
            self.is_listening = True
            thread = threading.Thread(target=listener_thread, daemon=True)
            thread.start()
    
    def _contains_wake_word(self, text: str) -> bool:
        """Check if text contains the wake word."""
        if not text:
            return False
        
        # Simple pattern matching
        words = re.findall(r'\b\w+\b', text.lower())
        return self.wake_word in words
    
    def stop_detection(self) -> None:
        """Stop wake word detection."""
        self.is_listening = False
        logger.debug("Wake word detection stopped")
    
    def simulate_wake_word(self) -> None:
        """Simulate wake word detection (for testing)."""
        logger.info("Wake word simulated")
        self.is_detected = True
    
    def test_wake_word(self) -> bool:
        """Test wake word detection."""
        logger.info("Testing wake word detection...")
        print(f"Please say '{self.wake_word}' to test...")
        
        start_time = time.time()
        while time.time() - start_time < 10:  # 10 second timeout
            try:
                with sr.Microphone(device_index=self.microphone_index) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    
                    try:
                        text = self.recognizer.recognize_google(audio).lower()
                        if self._contains_wake_word(text):
                            logger.info(f"Wake word test successful: {text}")
                            print(f"✓ Wake word detected: {text}")
                            return True
                    except:
                        pass
            except:
                pass
            
            time.sleep(0.1)
        
        logger.warning("Wake word test failed")
        print("✗ Wake word not detected")
        return False