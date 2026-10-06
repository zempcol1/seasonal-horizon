"""City lookup via the Open-Meteo geocoding API."""

from datetime import datetime
from zoneinfo import ZoneInfo

from services.api_client import TTLCache, request_json
from config import TIMEZONE, config

SEARCH_URL = "https://geocoding-api.open-meteo.com/v1/search"
MIN_QUERY_LENGTH = 2
MAX_QUERY_LENGTH = 80
MAX_RESULTS = 8
# More than are shown, since places off the app's clock are dropped.
FETCH_RESULTS = 50

# A winter and a summer day, so summer time has to match as well.
_PROBE_DAYS = (datetime(2026, 1, 15), datetime(2026, 7, 15))

_cache = TTLCache(config.CACHE_TTL_GEO)


def on_our_clock(tz_name):
    """
    Whether a place keeps the app's clock all year. Sun times are shown on
    that clock, so London or Helsinki would be an hour off.
    """
    try:
        zone = ZoneInfo(tz_name)
    except Exception:  # missing or unknown zone
        return False
    home = ZoneInfo(TIMEZONE)
    return all(day.replace(tzinfo=zone).utcoffset() == day.replace(tzinfo=home).utcoffset()
               for day in _PROBE_DAYS)


def search_cities(query, lang="en"):
    """
    Look up cities by name, named in the given language. Returns [] for
    short queries and on failure.

    Failures are deliberately not cached, so a brief outage cannot blank out
    a city for the whole cache lifetime.
    """
    # No city name is longer than this; anything more is not a search.
    query = (query or "").strip()[:MAX_QUERY_LENGTH]
    if len(query) < MIN_QUERY_LENGTH:
        return []

    cache_key = (lang, query.lower())
    cached = _cache.get(cache_key)
    if cached is not None:
        return cached

    data = request_json(SEARCH_URL,
                        {"name": query, "count": FETCH_RESULTS, "language": lang})
    if not data:
        return []

    results = [r for r in data.get("results", []) if on_our_clock(r.get("timezone"))][:MAX_RESULTS]
    if lang == "de":
        # Swiss spelling, like the rest of the app: Giessen, not Gießen.
        results = [{k: v.replace("ß", "ss") if isinstance(v, str) else v for k, v in r.items()}
                   for r in results]
    _cache.set(cache_key, results)
    return results
