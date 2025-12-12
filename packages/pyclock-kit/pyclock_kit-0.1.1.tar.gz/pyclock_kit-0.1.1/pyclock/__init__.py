"""PyClockKit - A simple time utility package for PyPI demonstration."""

from datetime import datetime
from typing import Optional

__version__ = "0.1.0"
__author__ = "Stanislaw Kurzyp"
__email__ = "kurzyp.st@gmail.com"


def get_time(format: Optional[str] = None) -> str:
    """
    Get the current time as a formatted string.
    
    Args:
        format: Optional format string for datetime.strftime().
                If None, returns ISO format (YYYY-MM-DD HH:MM:SS).
    
    Returns:
        Current time as a formatted string.
        
    Examples:
        >>> get_time()
        '2025-12-03 22:48:59'
        
        >>> get_time("%H:%M:%S")
        '22:48:59'
        
        >>> get_time("%Y-%m-%d")
        '2025-12-03'
    """
    now = datetime.now()
    
    if format is None:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    return now.strftime(format)


def get_timestamp() -> float:
    """
    Get the current Unix timestamp.
    
    Returns:
        Current time as Unix timestamp (seconds since epoch).
        
    Example:
        >>> get_timestamp()
        1701637739.123456
    """
    return datetime.now().timestamp()


def get_utc_time(format: Optional[str] = None) -> str:
    """
    Get the current UTC time as a formatted string.
    
    Args:
        format: Optional format string for datetime.strftime().
                If None, returns ISO format (YYYY-MM-DD HH:MM:SS).
    
    Returns:
        Current UTC time as a formatted string.
        
    Example:
        >>> get_utc_time()
        '2025-12-03 21:48:59'
    """
    now = datetime.utcnow()
    
    if format is None:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    return now.strftime(format)


# Export public API
__all__ = ["get_time", "get_timestamp", "get_utc_time"]
