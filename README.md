# J.A.R.V.I.S V1 — Personal AI Voice Assistant

A voice-first personal AI assistant for Windows, inspired by the Marvel JARVIS.

## Features

- **Voice Activation**: Say "Jarvis" to activate
- **Speech Recognition**: Natural voice commands
- **AI Responses**: Powered by cloud-based LLM API
- **Text-to-Speech**: Natural voice responses
- **Local Commands**: Time, date, system information
- **Conversation History**: Local SQLite storage
- **Keyboard Fallback**: Press SPACE to activate
- **Text Input Mode**: For testing without microphone
- **Test Mode**: Component testing

## Architecture
ARVIS Core
├── Voice Layer (Wake Word, STT, TTS)
├── AI Layer (LLM Client)
├── Command Router (Local/Cloud)
├── Memory (SQLite)
└── Tools (Time, System, Help)


## Requirements

- **OS**: Windows 10/11
- **Python**: 3.11+
- **Internet**: Required for LLM API
- **Microphone**: Required for voice features

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/jarvis.git
cd jarvis

2. Create Virtual Environment
bash

python -m venv venv
venv\Scripts\activate

3. Install Dependencies
bash

pip install -r requirements.txt

4. Configure Environment
bash

cp .env.example .env

Edit .env with your API key:
text

LLM_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-3.5-turbo

5. Test Microphone
bash

python main.py --test

Usage
Voice Mode (Default)
bash

python main.py

    Say "Jarvis" to activate

    JARVIS responds "Yes?"

    Speak your command

    JARVIS responds

Keyboard Activation

    Press SPACE to activate without wake word

Text Input Mode
bash

python main.py --text

Type commands directly for testing.
Test Mode
bash

python main.py --test

Test individual components.
Commands
Voice Commands

    "Jarvis" - Activate assistant

    "What time is it?" - Current time

    "What's today's date?" - Current date

    "What's my CPU usage?" - CPU information

    "How much RAM am I using?" - Memory usage

    "What operating system am I running?" - OS info

    "What can you do?" - Help

    "Clear my conversation history." - Clear history

    "Goodbye Jarvis." - Shutdown

Any Other Question

JARVIS will use the cloud LLM to respond.
Configuration

Edit .env to configure:
env

# LLM Settings
LLM_API_KEY=your_key
LLM_MODEL=gpt-3.5-turbo

# JARVIS Settings
WAKE_WORD=jarvis
TTS_VOICE=en-US-JennyNeural
MAX_CONVERSATION_HISTORY=10
VOICE_ENABLED=true
WAKE_WORD_ENABLED=true

Troubleshooting
Microphone Not Working

    Check microphone connection

    Verify microphone is selected in Windows settings

    Test with: python main.py --test

Wake Word Not Detected

    Speak clearly

    Reduce background noise

    Use SPACE key as fallback

    Adjust microphone sensitivity

LLM API Errors

    Verify API key in .env

    Check internet connection

    Verify API credits/settings

Speech Recognition Issues

    Speak clearly

    Reduce background noise

    Use text input mode for testing

Security

    API keys stored in .env (never hardcoded)

    No automatic shell command execution

    Limited system information access

    Safe, controlled operations

Roadmap
V1 (Current)

    ✅ Voice activation

    ✅ Wake word detection

    ✅ Speech-to-text

    ✅ Cloud LLM integration

    ✅ Text-to-speech

    ✅ Conversation history

    ✅ Local commands

    ✅ Keyboard fallback

V2 (Future)

    Web search

    Weather information

    Calculator

    Application launching

    More system tools

V3 (Future)

    Screenshot understanding

    Computer vision

    Mouse/keyboard control

    Application automation

V4 (Future)

    Long-term memory

    Personal knowledge base

    RAG

    User preferences

V5 (Future)

    Tool calling

    Multi-step planning

    Autonomous task execution

    Agent architecture

License

MIT License
Support

For issues, please open a GitHub issue or contact the developer.

J.A.R.V.I.S V1 — Building the future, one voice command at a time.
text


## Summary

This implementation provides a complete, working JARVIS V1 with:

1. ✅ **Voice-first interaction** with wake word "Jarvis"
2. ✅ **Cloud LLM integration** via OpenAI-compatible API
3. ✅ **Speech-to-text** using Google Speech Recognition
4. ✅ **Text-to-speech** using Edge TTS with fallback
5. ✅ **SQLite memory** for conversation history
6. ✅ **Local commands** (time, date, system info)
7. ✅ **Command router** for local vs cloud routing
8. ✅ **Keyboard fallback** (SPACE key)
9. ✅ **Text input mode** for testing
10. ✅ **Test mode** for component testing
11. ✅ **Robust error handling** throughout
12. ✅ **Clean architecture** with modular components
13. ✅ **Security** with .env configuration
14. ✅ **Self-activation prevention** during TTS

The assistant is designed to be runnable, reliable, and maintainable, with future compatibility for advanced features.