"""System information tools for JARVIS."""

import psutil
import platform
import os
from typing import Dict, Any
from datetime import datetime

class SystemTool:
    """Tool for handling system information queries."""
    
    @staticmethod
    def get_cpu_usage() -> Dict[str, Any]:
        """Get CPU usage information."""
        return {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
            'frequency': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
        }
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Get memory usage information."""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free
        }
    
    @staticmethod
    def get_disk_usage() -> Dict[str, Any]:
        """Get disk usage information."""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get general system information."""
        return {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    
    @staticmethod
    def get_boot_time() -> str:
        """Get system boot time."""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        return boot_time.strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def format_cpu_response() -> str:
        """Format CPU information for voice response."""
        cpu_info = SystemTool.get_cpu_usage()
        return f"CPU usage is at {cpu_info['percent']:.0f} percent"
    
    @staticmethod
    def format_memory_response() -> str:
        """Format memory information for voice response."""
        memory_info = SystemTool.get_memory_usage()
        used_gb = memory_info['used'] / (1024**3)
        total_gb = memory_info['total'] / (1024**3)
        return f"Memory usage is at {memory_info['percent']:.0f} percent, using {used_gb:.1f} gigabytes out of {total_gb:.1f} gigabytes"
    
    @staticmethod
    def format_system_response() -> str:
        """Format system information for voice response."""
        sys_info = SystemTool.get_system_info()
        return f"You are running {sys_info['system']} version {sys_info['release']} on {sys_info['machine']}"