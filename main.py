#!/usr/bin/env python3
"""JARVIS V1 - Personal AI Voice Assistant"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.assistant import Assistant
from config import config
from utils.logger import logger

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='JARVIS Personal AI Voice Assistant')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--text', action='store_true', help='Run in text input mode')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("\n" + "="*50)
    print("╔" + "═"*48 + "╗")
    print("║" + " "*15 + "J.A.R.V.I.S" + " "*17 + "║")
    print("║" + " "*13 + "Personal AI Voice Assistant" + " "*10 + "║")
    print("╚" + "═"*48 + "╝")
    print("="*50 + "\n")
    
    if args.test:
        print("🔧 TEST MODE")
        print("-" * 50)
        print("Running system tests...\n")
        
        assistant = Assistant()
        results = assistant.test_system()
        
        print("\nTest Results:")
        for component, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {component:12} : {status}")
        
        print("\nTest complete.")
        return
    
    if args.text:
        print("⌨️ TEXT INPUT MODE")
        print("-" * 50)
        print("Type your commands (type 'exit' or 'quit' to quit)\n")
        
        assistant = Assistant()
        
        # Initialize basic systems
        assistant.voice_enabled = False
        
        print("JARVIS: Text input mode activated. How may I assist you?")
        
        while True:
            try:
                command = input("\nYou: ").strip()
                if command.lower() in ['exit', 'quit', 'goodbye']:
                    print("JARVIS: Goodbye!")
                    break
                if command:
                    assistant._process_command(command)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        return
    
    # Normal voice mode
    try:
        assistant = Assistant()
        assistant.start()
    except KeyboardInterrupt:
        print("\n\nShutting down JARVIS...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nFatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()