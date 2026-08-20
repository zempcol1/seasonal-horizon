"""City lookup via the Open-Meteo geocoding API."""

from services.api_client import TTLCache, request_json
from config import config

SEARCH_URL = "https://geocoding-api.open-meteo.com/v1/search"
MIN_QUERY_LENGTH = 2
MAX_RESULTS = 8

_cache = TTLCache(config.CACHE_TTL_GEO)


def search_cities(query):
    """
    Look up cities by name. Returns [] for short queries and on failure.

    Failures are deliberately not cached, so a brief outage cannot blank out
    a city for the whole cache lifetime.
    """
    query = (query or "").strip()
    if len(query) < MIN_QUERY_LENGTH:
        return []

    cache_key = query.lower()
    cached = _cache.get(cache_key)
    if cached is not None:
        return cached

    data = request_json(SEARCH_URL,
                        {"name": query, "count": MAX_RESULTS, "language": "en"})
    if not data:
        return []

    results = data.get("results", [])
    _cache.set(cache_key, results)
    return results
