"""Time and date tools for JARVIS."""

from datetime import datetime
import pytz
from typing import Dict, Any

class TimeTool:
    """Tool for handling time and date queries."""
    
    @staticmethod
    def get_time() -> Dict[str, str]:
        """Get current time."""
        now = datetime.now()
        return {
            'time': now.strftime('%I:%M %p').lstrip('0'),
            'time_24h': now.strftime('%H:%M'),
            'timestamp': now.isoformat()
        }
    
    @staticmethod
    def get_date() -> Dict[str, str]:
        """Get current date."""
        now = datetime.now()
        return {
            'date': now.strftime('%B %d, %Y'),
            'short_date': now.strftime('%m/%d/%Y'),
            'day_of_week': now.strftime('%A'),
            'timestamp': now.isoformat()
        }
    
    @staticmethod
    def get_datetime() -> Dict[str, str]:
        """Get full date and time."""
        now = datetime.now()
        return {
            'datetime': now.strftime('%B %d, %Y at %I:%M %p'),
            'timestamp': now.isoformat()
        }
    
    @staticmethod
    def format_time_response() -> str:
        """Format time for voice response."""
        time_info = TimeTool.get_time()
        return f"It's {time_info['time']}"
    
    @staticmethod
    def format_date_response() -> str:
        """Format date for voice response."""
        date_info = TimeTool.get_date()
        return f"Today is {date_info['day_of_week']}, {date_info['date']}"
    
    @staticmethod
    def format_datetime_response() -> str:
        """Format full date and time for voice response."""
        dt_info = TimeTool.get_datetime()
        return f"It's {dt_info['datetime']}"