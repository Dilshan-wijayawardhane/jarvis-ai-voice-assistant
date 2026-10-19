#!/usr/bin/env python3
"""Simple launcher for JARVIS."""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch JARVIS with proper setup."""
    print("=" * 60)
    print("  J.A.R.V.I.S — Personal AI Voice Assistant")
    print("=" * 60)
    print()
    
    # Check for .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("   Please copy .env.example to .env and configure it.")
        print()
        if Path(".env.example").exists():
            print("   You can run:")
            print("   cp .env.example .env")
        print()
        return
    
    # Check for data directory
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir(exist_ok=True)
    
    # Run main
    try:
        import main
        main.main()
    except KeyboardInterrupt:
        print("\n\nJARVIS shutdown complete.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nCheck the logs for more details.")
        sys.exit(1)

if __name__ == "__main__":
    main()