"""Speech-to-text module for JARVIS."""

import time
import queue
import threading
from typing import Optional, Callable
import numpy as np

import sounddevice as sd
from scipy import signal
import speech_recognition as sr

from config import config
from utils.logger import logger

class SpeechToText:
    """Speech-to-text conversion using Google Speech Recognition."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone_index = config.microphone_index
        self.sample_rate = config.sample_rate
        self.chunk_size = config.chunk_size
        
        # These are the working settings from the test!
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.pause_threshold = 0.3
        self.recognizer.phrase_threshold = 0.2
        self.recognizer.non_speaking_duration = 0.3
        
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        self._test_microphone()
    
    def _test_microphone(self) -> bool:
        """Test if microphone is available."""
        try:
            devices = sd.query_devices()
            if not devices:
                logger.error("No audio devices found")
                return False
            
            # Check if the specified microphone exists
            if self.microphone_index < len(devices):
                device_info = devices[self.microphone_index]
                logger.info(f"Using microphone: {device_info['name']}")
                return True
            else:
                logger.warning(f"Microphone index {self.microphone_index} not found, using default")
                return True
                
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False
    
    def listen_for_speech(self, timeout: float = 10.0) -> Optional[str]:
        """Listen for speech and convert to text."""
        try:
            logger.debug("Listening for speech...")
            
            with sr.Microphone(device_index=self.microphone_index) as source:
                # Adjust for ambient noise (like in the test)
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                logger.debug(f"Energy threshold set to: {self.recognizer.energy_threshold}")
                
                # Listen for speech with phrase_time_limit for faster response
                try:
                    audio = self.recognizer.listen(
                        source, 
                        timeout=timeout, 
                        phrase_time_limit=5
                    )
                    logger.debug("Audio captured, recognizing...")
                    
                    # Try Google Speech Recognition
                    text = self.recognizer.recognize_google(audio)
                    
                    if text:
                        logger.info(f"Recognized: {text}")
                        return text
                    else:
                        return None
                        
                except sr.WaitTimeoutError:
                    logger.debug("Speech listening timed out")
                    return None
                except sr.UnknownValueError:
                    logger.debug("Speech not recognized")
                    return "I didn't quite catch that."
                except sr.RequestError as e:
                    logger.error(f"Google API error: {e}")
                    return "I'm having trouble with speech recognition right now."
                except Exception as e:
                    logger.error(f"Speech recognition error: {e}")
                    return None
                    
        except Exception as e:
            logger.error(f"Microphone error: {e}")
            return None
    
    def _recognize_audio(self, audio) -> Optional[str]:
        """Recognize speech from audio."""
        try:
            # Try Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                logger.warning("Google Speech Recognition failed")
            
            return None
            
        except Exception as e:
            logger.error(f"Recognition error: {e}")
            return None
    
    def listen_with_indicator(self, callback: Callable[[Optional[str]], None]) -> None:
        """Listen for speech and call callback with result."""
        def listener_thread():
            while self.is_listening:
                text = self.listen_for_speech()
                callback(text)
                time.sleep(0.1)
        
        if not self.is_listening:
            self.is_listening = True
            thread = threading.Thread(target=listener_thread, daemon=True)
            thread.start()
    
    def stop_listening(self) -> None:
        """Stop listening for speech."""
        self.is_listening = False
        logger.debug("Stopped listening")
    
    def test_microphone(self) -> bool:
        """Test microphone and speech recognition."""
        logger.info("Testing microphone...")
        print("Please speak a test phrase...")
        
        text = self.listen_for_speech(timeout=5.0)
        
        if text:
            logger.info(f"Test successful: {text}")
            print(f"Recognized: {text}")
            return True
        else:
            logger.warning("Microphone test failed")
            return False