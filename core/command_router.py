"""Command router for JARVIS."""

import re
from typing import Optional, Tuple, Callable, Dict, Any
import threading
import time

from tools.time_tool import TimeTool
from tools.system_tool import SystemTool
from tools.help_tool import HelpTool
from memory.database import Database
from utils.logger import logger

class CommandRouter:
    """Route commands to appropriate handlers."""
    
    def __init__(self, database: Database):
        self.database = database
        
        # Register local command handlers
        self.local_commands: Dict[str, Callable] = {
            'time': self._handle_time,
            'date': self._handle_date,
            'datetime': self._handle_datetime,
            'cpu': self._handle_cpu,
            'memory': self._handle_memory,
            'system': self._handle_system,
            'help': self._handle_help,
            'clear': self._handle_clear,
            'shutdown': self._handle_shutdown,
            'exit': self._handle_shutdown,
            'goodbye': self._handle_shutdown
        }
        
        # Command patterns
        self.patterns = {
            'time': r'(what(\s+is)?\s+)?(the\s+)?time',
            'date': r'(what(\s+is)?\s+)?(today\'s\s+)?(the\s+)?date',
            'datetime': r'(what(\s+is)?\s+)?(the\s+)?date\s+and\s+time',
            'cpu': r'(cpu|processor|processing)\s+(usage|use|load)',
            'memory': r'(memory|ram)\s+(usage|use|load)',
            'system': r'(operating\s+system|os|system\s+info)',
            'help': r'(help|what\s+can\s+you\s+do|capabilities)',
            'clear': r'(clear|delete|reset)\s+(conversation\s+)?history',
            'shutdown': r'(goodbye|shutdown|exit|quit|stop)'
        }
    
    def route_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """Route command to appropriate handler."""
        if not command or not command.strip():
            return False, None
        
        command = command.lower().strip()
        logger.debug(f"Routing command: {command}")
        
        # Check for local commands
        for cmd_name, pattern in self.patterns.items():
            if re.search(pattern, command):
                logger.info(f"Local command detected: {cmd_name}")
                handler = self.local_commands.get(cmd_name)
                if handler:
                    return True, handler(command)
                break
        
        # Not a local command
        return False, None
    
    def _handle_time(self, command: str) -> str:
        """Handle time command."""
        return TimeTool.format_time_response()
    
    def _handle_date(self, command: str) -> str:
        """Handle date command."""
        return TimeTool.format_date_response()
    
    def _handle_datetime(self, command: str) -> str:
        """Handle date and time command."""
        return TimeTool.format_datetime_response()
    
    def _handle_cpu(self, command: str) -> str:
        """Handle CPU usage command."""
        return SystemTool.format_cpu_response()
    
    def _handle_memory(self, command: str) -> str:
        """Handle memory usage command."""
        return SystemTool.format_memory_response()
    
    def _handle_system(self, command: str) -> str:
        """Handle system information command."""
        return SystemTool.format_system_response()
    
    def _handle_help(self, command: str) -> str:
        """Handle help command."""
        return HelpTool.format_help_response()
    
    def _handle_clear(self, command: str) -> str:
        """Handle clear history command."""
        count = self.database.get_conversation_count()
        if count == 0:
            return "Your conversation history is already empty."
        
        success = self.database.clear_conversation_history()
        if success:
            return f"Conversation history cleared. {count} conversations removed."
        else:
            return "I had trouble clearing the conversation history."
    
    def _handle_shutdown(self, command: str) -> str:
        """Handle shutdown command."""
        # This will be handled by the main application
        return "GOODBYE"