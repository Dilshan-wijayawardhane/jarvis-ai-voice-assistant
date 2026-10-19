"""Main assistant logic for JARVIS."""

import time
import threading
from typing import Optional, Callable

from config import config
from ai.llm import LLMClient
from voice.wake_word import WakeWordDetector
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech
from core.conversation import ConversationManager
from core.command_router import CommandRouter
from memory.database import Database
from utils.logger import logger

class Assistant:
    """Main JARVIS assistant."""
    
    def __init__(self):
        # Initialize components
        self.database = Database(config.db_path)
        self.conversation_manager = ConversationManager(self.database)
        self.command_router = CommandRouter(self.database)
        self.llm = LLMClient()
        self.wake_word_detector = WakeWordDetector()
        self.speech_to_text = SpeechToText()
        self.text_to_speech = TextToSpeech()
        
        self.is_running = False
        self.is_processing = False
        self.is_speaking = False
        self.should_shutdown = False
        
        # Status flags
        self.all_systems_online = False
    
    def start(self) -> None:
        """Start the assistant."""
        try:
            logger.info("Starting JARVIS...")
            
            # Initialize all systems
            self._initialize_systems()
            
            if not self.all_systems_online:
                logger.warning("Some systems are not online")
            
            self.is_running = True
            self.should_shutdown = False
            
            # Start main loop
            self._main_loop()
            
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
            self.shutdown()
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            self.shutdown()
    
    def _initialize_systems(self) -> bool:
        """Initialize all systems."""
        logger.info("Initializing systems...")
        
        systems_ok = True
        
        # Check database
        try:
            count = self.database.get_conversation_count()
            logger.info(f"✓ Database initialized ({count} conversations)")
        except Exception as e:
            logger.error(f"✗ Database initialization failed: {e}")
            systems_ok = False
        
        # Check LLM
        if config.is_llm_configured():
            logger.info("✓ LLM configured")
        else:
            logger.warning("✗ LLM not configured")
            systems_ok = False
        
        # Check microphone
        if self.speech_to_text._test_microphone():
            logger.info("✓ Microphone available")
        else:
            logger.error("✗ Microphone not available")
            systems_ok = False
        
        # Check TTS
        try:
            logger.info("✓ TTS available")
        except Exception as e:
            logger.warning(f"✗ TTS may not work: {e}")
        
        self.all_systems_online = systems_ok
        return systems_ok
    
    def _main_loop(self) -> None:
        """Main assistant loop."""
        # Start wake word detection
        self.wake_word_detector.detect_wake_word(self._on_wake_word_detected)
        
        # Display status
        self._display_status()
        
        if self.all_systems_online:
            self._speak("All systems online. How may I assist you?")
        
        logger.info("JARVIS is now running. Say 'Jarvis' to activate.")
        
        # Keep the main thread alive
        while self.is_running and not self.should_shutdown:
            try:
                time.sleep(0.1)
                
                # Check for keyboard activation (SPACE key)
                if self._check_keyboard_activation():
                    self._on_wake_word_detected()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                time.sleep(1)
        
        self.shutdown()
    
    def _on_wake_word_detected(self) -> None:
        """Handle wake word detection."""
        if self.is_processing or self.is_speaking:
            logger.debug("Already processing, ignoring wake word")
            return
        
        logger.info("Wake word detected! Activating...")
        self._activate_assistant()
    
    def _activate_assistant(self) -> None:
        """Activate the assistant and listen for command."""
        self.is_processing = True
        
        try:
            # Pause wake word detection
            self.wake_word_detector.stop_detection()
            
            # Acknowledge
            self._speak("Yes?")
            
            # Listen for command
            if self.voice_enabled:
                self._listen_for_command()
            
        except Exception as e:
            logger.error(f"Assistant activation error: {e}")
        finally:
            self.is_processing = False
            
            # Resume wake word detection if not shutting down
            if not self.should_shutdown:
                self.wake_word_detector.detect_wake_word(self._on_wake_word_detected)
    
    def _listen_for_command(self) -> None:
        """Listen for voice command."""
        try:
            logger.info("Listening for command...")
            
            # Listen for speech
            command = self.speech_to_text.listen_for_speech(timeout=10.0)
            
            if command:
                if command == "I didn't quite catch that.":
                    self._speak("I didn't quite catch that.")
                    return
                
                # Process command
                self._process_command(command)
            else:
                # No command detected
                if self.should_shutdown:
                    return
                self._speak("I didn't hear anything.")
                
        except Exception as e:
            logger.error(f"Command listening error: {e}")
    
    def _process_command(self, command: str) -> None:
        """Process a command."""
        try:
            logger.info(f"Processing command: {command}")
            
            # Route the command
            is_local, response = self.command_router.route_command(command)
            
            if response == "GOODBYE":
                self.should_shutdown = True
                self._speak("Goodbye! I'll be here if you need me.")
                return
            
            if is_local and response:
                # Local command handled
                self._speak(response)
                return
            
            # Not a local command, use LLM
            if self.llm.is_configured():
                # Get conversation context
                context = self.conversation_manager.get_context()
                
                # Generate response
                response = self.llm.generate_response(command, context)
                
                if response:
                    # Save conversation
                    self.conversation_manager.add_message(command, response)
                    
                    # Speak the response
                    self._speak(response)
                else:
                    self._speak("I had trouble processing your request.")
            else:
                self._speak("I'm not configured to handle that request. Please check my AI settings.")
                
        except Exception as e:
            logger.error(f"Command processing error: {e}")
            self._speak("I encountered an error while processing your command.")
    
    def _speak(self, text: str) -> None:
        """Speak text using TTS."""
        if not self.voice_enabled:
            print(f"JARVIS: {text}")
            return
        
        try:
            self.is_speaking = True
            
            # Temporarily pause wake word detection
            self.wake_word_detector.stop_detection()
            
            # Speak
            def on_speech_complete():
                self.is_speaking = False
                # Resume wake word detection if not shutting down
                if not self.should_shutdown and self.is_running:
                    self.wake_word_detector.detect_wake_word(self._on_wake_word_detected)
            
            # Show speaking status
            print(f"JARVIS: Speaking...")
            print(f"JARVIS: {text}")
            
            # Speak
            self.text_to_speech.speak(text, on_speech_complete)
            
        except Exception as e:
            logger.error(f"Speech error: {e}")
            # Fallback to text output
            print(f"JARVIS: {text}")
            self.is_speaking = False
        finally:
            # Make sure wake word detection resumes
            if not self.should_shutdown and self.is_running:
                self.wake_word_detector.detect_wake_word(self._on_wake_word_detected)
    
    def _check_keyboard_activation(self) -> bool:
        """Check if SPACE key is pressed for activation."""
        try:
            import keyboard
            if keyboard.is_pressed('space'):
                # Debounce
                time.sleep(0.1)
                return True
        except:
            pass
        return False
    
    def _display_status(self) -> None:
        """Display system status."""
        status = "=" * 50
        print(f"\n{status}")
        print(f"╔{'═'*48}╗")
        print(f"║{' '*15}J.A.R.V.I.S{' '*17}║")
        print(f"║{' '*13}Personal AI Voice Assistant{' '*10}║")
        print(f"╚{'═'*48}╝")
        print(f"{status}")
        print(f"Status   : {'ONLINE' if self.all_systems_online else 'DEGRADED'}")
        print(f"AI       : {'CONNECTED' if self.llm.is_configured() else 'NOT CONFIGURED'}")
        print(f"Voice    : {'READY' if self.voice_enabled else 'DISABLED'}")
        print(f"Wake     : '{config.wake_word}'")
        print(f"{status}\n")
    
    def shutdown(self) -> None:
        """Shutdown the assistant."""
        logger.info("Shutting down JARVIS...")
        
        self.is_running = False
        self.should_shutdown = True
        
        # Stop all components
        if self.wake_word_detector:
            self.wake_word_detector.stop_detection()
        
        if self.speech_to_text:
            self.speech_to_text.stop_listening()
        
        if self.text_to_speech:
            self.text_to_speech.stop_speaking()
        
        logger.info("JARVIS has been shut down")
        print("\nJARVIS has been shut down.")
    
    @property
    def voice_enabled(self) -> bool:
        """Check if voice is enabled."""
        return config.voice_enabled and self.all_systems_online
    
    def test_system(self) -> dict:
        """Run system tests."""
        results = {
            'database': False,
            'llm': False,
            'microphone': False,
            'tts': False,
            'wake_word': False,
            'stt': False
        }
        
        logger.info("Running system tests...")
        
        # Test database
        try:
            count = self.database.get_conversation_count()
            results['database'] = True
            logger.info(f"✓ Database: {count} conversations")
        except Exception as e:
            logger.error(f"✗ Database: {e}")
        
        # Test LLM
        if self.llm.is_configured():
            try:
                response = self.llm.test_connection()
                results['llm'] = response
                logger.info(f"✓ LLM: {'Connected' if response else 'Failed'}")
            except Exception as e:
                logger.error(f"✗ LLM: {e}")
        else:
            logger.warning("⚠ LLM not configured")
        
        # Test microphone
        try:
            results['microphone'] = self.speech_to_text._test_microphone()
            logger.info(f"✓ Microphone: {'OK' if results['microphone'] else 'Failed'}")
        except Exception as e:
            logger.error(f"✗ Microphone: {e}")
        
        # Test TTS
        try:
            results['tts'] = self.text_to_speech.test_tts()
            logger.info(f"✓ TTS: {'OK' if results['tts'] else 'Failed'}")
        except Exception as e:
            logger.error(f"✗ TTS: {e}")
        
        # Test wake word (requires user interaction)
        try:
            print("\nTesting wake word detection...")
            print(f"Please say '{config.wake_word}' within 10 seconds...")
            results['wake_word'] = self.wake_word_detector.test_wake_word()
        except Exception as e:
            logger.error(f"✗ Wake word: {e}")
        
        # Test STT
        try:
            print("\nTesting speech recognition...")
            print("Please say a short phrase within 5 seconds...")
            text = self.speech_to_text.listen_for_speech(timeout=5.0)
            results['stt'] = text is not None
            if text:
                logger.info(f"✓ STT: Recognized '{text}'")
            else:
                logger.warning("⚠ STT: No speech recognized")
        except Exception as e:
            logger.error(f"✗ STT: {e}")
        
        # Summary
        logger.info("\nTest Summary:")
        for component, result in results.items():
            status = "✓" if result else "✗"
            logger.info(f"  {status} {component}")
        
        return results