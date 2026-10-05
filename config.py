"""
Configuration management for Seasonal Horizon.
Uses environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

# The app is tuned for Central and Western Europe, which shares one clock.
TIMEZONE = 'Europe/Zurich'


@dataclass(frozen=True)
class Config:
    """Application configuration."""
    
    # Flask
    DEBUG: bool = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    # API Settings
    API_TIMEOUT: int = int(os.environ.get('API_TIMEOUT', '8'))
    API_MAX_RETRIES: int = int(os.environ.get('API_MAX_RETRIES', '3'))
    
    # Calls to Open-Meteo per day and process, below its free tier of ~10,000
    UPSTREAM_DAILY_LIMIT: int = int(os.environ.get('UPSTREAM_DAILY_LIMIT', '8000'))

    # Cache TTL (seconds). The message stays the same all day, so the
    # forecast does not need to be fresher than half an hour.
    CACHE_TTL_WEATHER: int = int(os.environ.get('CACHE_TTL_WEATHER', '1800'))  # 30 min
    CACHE_TTL_GEO: int = int(os.environ.get('CACHE_TTL_GEO', '3600'))  # 1 hour
    CACHE_MAX_ENTRIES: int = int(os.environ.get('CACHE_MAX_ENTRIES', '2000'))  # per cache

    # Rate Limiting (requests per minute and IP)
    RATE_LIMIT_UPLIFT: int = int(os.environ.get('RATE_LIMIT_UPLIFT', '30'))
    RATE_LIMIT_SEARCH: int = int(os.environ.get('RATE_LIMIT_SEARCH', '30'))
    
    # Logging
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Shown in the UI and its changelog
    VERSION: str = 'v0.6'

    # Default location (Zurich)
    DEFAULT_LAT: float = 47.37
    DEFAULT_LON: float = 8.54
    DEFAULT_CITY: str = 'Zurich'


# Singleton instance
config = Config()


def today() -> date:
    """Today on the local clock. The server runs on UTC, an hour behind."""
    return datetime.now(ZoneInfo(TIMEZONE)).date()
