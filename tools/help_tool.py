"""Help tool for JARVIS."""

from typing import Dict, List, Any

class HelpTool:
    """Tool for providing help information."""
    
    @staticmethod
    def get_help() -> Dict[str, Any]:
        """Get help information."""
        return {
            'name': 'JARVIS V1',
            'description': 'Personal AI Voice Assistant',
            'features': {
                'voice': [
                    'Wake word detection ("Jarvis")',
                    'Voice command recognition',
                    'Natural voice responses'
                ],
                'system': [
                    'Time and date queries',
                    'System information (CPU, memory, OS)',
                    'Conversation history storage'
                ],
                'other': [
                    'Keyboard activation (SPACE key)',
                    'Text input mode for testing',
                    'Test mode for debugging'
                ]
            },
            'commands': {
                'time': 'What time is it?',
                'date': 'What is today\'s date?',
                'system': 'What is my CPU usage?',
                'memory': 'How much RAM am I using?',
                'os': 'What operating system am I running?',
                'clear': 'Clear conversation history',
                'help': 'What can you do?',
                'shutdown': 'Goodbye Jarvis'
            }
        }
    
    @staticmethod
    def format_help_response() -> str:
        """Format help information for voice response."""
        help_info = HelpTool.get_help()
        
        response = (
            f"I am {help_info['name']}, a {help_info['description']}. "
            "I can help you with:\n\n"
            "Voice Commands:\n"
            f"  - Time: {help_info['commands']['time']}\n"
            f"  - Date: {help_info['commands']['date']}\n"
            f"  - System Info: {help_info['commands']['system']}\n"
            f"  - Memory Usage: {help_info['commands']['memory']}\n"
            f"  - Operating System: {help_info['commands']['os']}\n"
            f"  - Clear History: {help_info['commands']['clear']}\n"
            f"  - Help: {help_info['commands']['help']}\n"
            f"  - Shutdown: {help_info['commands']['shutdown']}\n\n"
            "You can activate me by saying 'Jarvis' or pressing the SPACE key. "
            "For any other questions, just ask and I'll do my best to help."
        )
        
        return response