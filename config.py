"""
Configuration management for Seasonal Horizon.
Uses environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Application configuration."""
    
    # Flask
    DEBUG: bool = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    # API Settings
    API_TIMEOUT: int = int(os.environ.get('API_TIMEOUT', '8'))
    API_MAX_RETRIES: int = int(os.environ.get('API_MAX_RETRIES', '3'))
    
    # Cache TTL (seconds)
    CACHE_TTL_WEATHER: int = int(os.environ.get('CACHE_TTL_WEATHER', '300'))  # 5 min
    CACHE_TTL_SOLAR: int = int(os.environ.get('CACHE_TTL_SOLAR', '300'))  # 5 min
    CACHE_TTL_GEO: int = int(os.environ.get('CACHE_TTL_GEO', '3600'))  # 1 hour
    
    # Rate Limiting (requests per minute)
    RATE_LIMIT_UPLIFT: int = int(os.environ.get('RATE_LIMIT_UPLIFT', '30'))
    RATE_LIMIT_SEARCH: int = int(os.environ.get('RATE_LIMIT_SEARCH', '60'))
    
    # Logging
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Default location (Zurich)
    DEFAULT_LAT: float = 47.37
    DEFAULT_LON: float = 8.54
    DEFAULT_CITY: str = 'Zurich'


# Singleton instance
config = Config()
