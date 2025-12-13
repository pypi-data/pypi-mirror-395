"""
System monitoring utilities for the annotator
"""
import psutil
from typing import Dict


class SystemMonitor:
    """Monitor system resources (CPU, RAM, etc.)"""
    
    @staticmethod
    def get_cpu_usage() -> float:
        """
        Get current CPU usage percentage.
        
        Returns:
            float: CPU usage percentage (0-100)
        """
        return psutil.cpu_percent(interval=0.1)
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """
        Get current memory usage.
        
        Returns:
            dict: Dictionary with 'used_gb', 'total_gb', and 'percent'
        """
        memory = psutil.virtual_memory()
        return {
            'used_gb': memory.used / (1024 ** 3),
            'total_gb': memory.total / (1024 ** 3),
            'percent': memory.percent
        }
    
    @staticmethod
    def get_disk_usage() -> Dict[str, float]:
        """
        Get current disk usage.
        
        Returns:
            dict: Dictionary with 'used_gb', 'total_gb', and 'percent'
        """
        disk = psutil.disk_usage('/')
        return {
            'used_gb': disk.used / (1024 ** 3),
            'total_gb': disk.total / (1024 ** 3),
            'percent': disk.percent
        }
    
    @staticmethod
    def get_system_info() -> Dict[str, any]:
        """
        Get comprehensive system information.
        
        Returns:
            dict: System information including CPU, RAM, and disk
        """
        return {
            'cpu_usage': SystemMonitor.get_cpu_usage(),
            'memory': SystemMonitor.get_memory_usage(),
            'disk': SystemMonitor.get_disk_usage()
        }
