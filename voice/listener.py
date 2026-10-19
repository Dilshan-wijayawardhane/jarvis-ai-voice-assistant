"""Audio listener for JARVIS commands."""

import time
from typing import Optional
import threading
import queue

import sounddevice as sd
import numpy as np

from config import config
from utils.logger import logger

class AudioListener:
    """Low-level audio listener for command detection."""
    
    def __init__(self):
        self.sample_rate = config.sample_rate
        self.chunk_size = config.chunk_size
        self.microphone_index = config.microphone_index
        
        self.is_recording = False
        self.audio_data = []
        
        self._test_audio()
    
    def _test_audio(self) -> bool:
        """Test audio input."""
        try:
            devices = sd.query_devices()
            if devices:
                logger.info(f"Audio devices found: {len(devices)}")
                return True
            return False
        except Exception as e:
            logger.error(f"Audio test failed: {e}")
            return False
    
    def record_audio(self, duration: float = 5.0) -> Optional[np.ndarray]:
        """Record audio for the specified duration."""
        try:
            logger.debug(f"Recording audio for {duration} seconds...")
            
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.float32,
                device=self.microphone_index
            )
            
            sd.wait()
            logger.debug(f"Audio recorded: {len(audio_data)} samples")
            return audio_data
            
        except Exception as e:
            logger.error(f"Recording error: {e}")
            return None
    
    def start_recording(self) -> None:
        """Start continuous recording."""
        self.is_recording = True
        self.audio_data = []
        
        def record_thread():
            while self.is_recording:
                try:
                    data = sd.rec(
                        int(self.sample_rate * 0.1),
                        samplerate=self.sample_rate,
                        channels=1,
                        dtype=np.float32,
                        device=self.microphone_index
                    )
                    sd.wait()
                    self.audio_data.append(data)
                except Exception as e:
                    logger.error(f"Recording thread error: {e}")
                    time.sleep(0.1)
        
        thread = threading.Thread(target=record_thread, daemon=True)
        thread.start()
        logger.debug("Recording started")
    
    def stop_recording(self) -> Optional[np.ndarray]:
        """Stop recording and return audio data."""
        self.is_recording = False
        if self.audio_data:
            combined = np.concatenate(self.audio_data)
            self.audio_data = []
            return combined
        return None
    
    def is_audio_available(self) -> bool:
        """Check if audio input is available."""
        try:
            sd.query_devices(self.microphone_index)
            return True
        except:
            return False