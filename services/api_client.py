"""
Shared plumbing for calling external HTTP APIs: retries and response caching.

Both helpers here existed as near-copies in app.py, solar_service.py and
weather_service.py before being consolidated.
"""

import time

import requests

from config import config
from services.logging_service import log_event


class TTLCache:
    """Dict cache whose entries expire after `ttl` seconds."""

    def __init__(self, ttl):
        self.ttl = ttl
        self._entries = {}

    def get(self, key):
        """Return the cached value, or None if missing or expired."""
        entry = self._entries.get(key)
        if entry is None:
            return None

        value, stored_at = entry
        if time.time() - stored_at >= self.ttl:
            del self._entries[key]
            return None
        return value

    def set(self, key, value):
        self._entries[key] = (value, time.time())

    def clear(self):
        self._entries.clear()


def request_json(url, params, retries=None, timeout=None):
    """
    GET `url` and return the parsed JSON body.

    Retries with a short backoff on any request failure. Returns None if every
    attempt fails, so callers can fall back rather than handle exceptions.
    """
    retries = retries or config.API_MAX_RETRIES
    timeout = timeout or config.API_TIMEOUT

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                log_event('api_fail', f'{url}:{str(e)[:50]}')
            else:
                time.sleep(0.3 * (attempt + 1))

    return None
