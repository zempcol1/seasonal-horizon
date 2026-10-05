"""Shared plumbing for calling external HTTP APIs: retries, caching and a daily budget."""

import time

import requests

from config import config, today
from services.logging_service import log_event

# Open-Meteo's free tier allows about 10,000 calls a day. Someone asking for
# thousands of different places could spend that alone and leave everyone
# else without weather, so past this many calls a day we stop asking. The
# light is calculated, so the app carries on without the forecast until
# midnight. Counted per process, which is fine for a handful of workers.
UPSTREAM_DAILY_LIMIT = config.UPSTREAM_DAILY_LIMIT

_budget = {"day": None, "used": 0}


class TTLCache:
    """
    Dict cache whose entries expire after `ttl` seconds.

    Holds at most `max_size` entries, dropping the oldest first, so a flood
    of different coordinates cannot grow it without end.
    """

    def __init__(self, ttl, max_size=None):
        self.ttl = ttl
        self.max_size = max_size or config.CACHE_MAX_ENTRIES
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
        self._entries.pop(key, None)
        if len(self._entries) >= self.max_size:
            # Dicts keep insertion order, so the first key is the oldest.
            del self._entries[next(iter(self._entries))]
        self._entries[key] = (value, time.time())

    def clear(self):
        self._entries.clear()


def _spend_budget():
    """Count one upstream call against today's budget; False once it is used up."""
    day = today()
    if _budget["day"] != day:
        _budget["day"], _budget["used"] = day, 0
    if _budget["used"] >= UPSTREAM_DAILY_LIMIT:
        return False
    _budget["used"] += 1
    if _budget["used"] == UPSTREAM_DAILY_LIMIT:
        log_event('api_budget', 'daily limit reached, no upstream calls until midnight')
    return True


def request_json(url, params, retries=None, timeout=None):
    """
    GET `url` and return the parsed JSON body.

    Retries with a short backoff on any request failure. Returns None if every
    attempt fails or the day's budget is spent, so callers can fall back
    rather than handle exceptions.
    """
    if not _spend_budget():
        return None

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
