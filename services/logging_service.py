"""
Minimal logging service for Seasonal Horizon.
Designed to be storage-efficient for shared hosting.
"""

import logging
import sys
from datetime import datetime
from config import config


# Create a minimal formatter
class CompactFormatter(logging.Formatter):
    """Compact log format to save space."""
    
    def format(self, record):
        # Format: TIME|LEVEL|MSG (no date, no module path)
        time_str = datetime.now().strftime('%H:%M:%S')
        return f"{time_str}|{record.levelname[0]}|{record.getMessage()}"


def get_logger(name: str = 'seasonal_horizon') -> logging.Logger:
    """
    Get a configured logger instance.
    
    Logs to stdout only (PythonAnywhere captures this).
    Uses compact format to minimize storage.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))
    
    # Stream handler only (PythonAnywhere captures stdout)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CompactFormatter())
    logger.addHandler(handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


# Convenience function for one-off logs
def log_event(event_type: str, details: str = ''):
    """
    Log a significant event. Use sparingly.
    
    Event types: 'startup', 'error', 'rate_limit', 'api_fail'
    """
    logger = get_logger()
    msg = f"{event_type}"
    if details:
        msg += f":{details}"
    
    if event_type == 'error':
        logger.error(msg)
    elif event_type == 'rate_limit':
        logger.warning(msg)
    else:
        logger.info(msg)
