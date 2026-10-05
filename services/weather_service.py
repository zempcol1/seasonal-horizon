"""
The week's weather, read for what there is to look forward to.

Sunshine hours are the measure, not weather codes. A code says "overcast"
or "showers" for a day that still gets nine hours of sun, which is exactly
the kind of day this app should not talk down.
"""

from datetime import datetime

from config import TIMEZONE, config, today
from services.api_client import TTLCache, request_json

_cache = TTLCache(config.CACHE_TTL_WEATHER)

SNOW_CODES = frozenset([71, 73, 75, 77, 85, 86])
FOG_CODES = frozenset([45, 48])

# Share of the daylight with direct sun that makes a day a sunny one.
SUNNY_SHARE = 0.5


def _sun(sunshine_sec, daylight_sec):
    """Hours of sun and whether that makes the day a sunny one."""
    if sunshine_sec is None or not daylight_sec:
        return None, False
    return sunshine_sec / 3600, sunshine_sec / daylight_sec >= SUNNY_SHARE


def fetch_daily_weather(lat, lon, days=7):
    """The coming week, day by day, plus what stands out in it."""
    cache_key = f"weather_{lat:.2f}_{lon:.2f}_{today()}"
    cached = _cache.get(cache_key)
    if cached:
        return cached

    data = request_json("https://api.open-meteo.com/v1/forecast", {
        "latitude": lat,
        "longitude": lon,
        "daily": ["weathercode", "temperature_2m_max", "temperature_2m_min",
                  "sunshine_duration", "daylight_duration"],
        "timezone": TIMEZONE,
        "forecast_days": days,
    })
    if not data:
        return {}

    daily = data.get("daily", {})

    def column(name, i):
        values = daily.get(name) or []
        return values[i] if i < len(values) else None

    forecast = []
    try:
        for i, stamp in enumerate(daily.get("time", [])[:days]):
            sun_hours, is_sunny = _sun(column("sunshine_duration", i),
                                       column("daylight_duration", i))
            forecast.append({
                "weekday_index": datetime.strptime(stamp, "%Y-%m-%d").weekday(),
                "code": column("weathercode", i),
                "temp_max": column("temperature_2m_max", i),
                "temp_min": column("temperature_2m_min", i),
                "sun_hours": sun_hours,
                "is_sunny": is_sunny,
            })
    except (TypeError, ValueError):
        return {}   # malformed response: no weather rather than a crash
    if not forecast:
        return {}

    result = {
        "forecast": forecast,
        "today": forecast[0],
        "elevation": data.get("elevation"),
        "analysis": _analyze_forecast(forecast),
    }
    _cache.set(cache_key, result)
    return result


def _temp_trend(temps):
    """Compare the first three days with the next three."""
    temps = [t for t in temps if t is not None]
    if len(temps) < 6:
        return "stable", 0
    diff = round(sum(temps[3:6]) / 3 - sum(temps[:3]) / 3, 1)
    if diff > 4:
        return "warming_strong", diff
    if diff > 2:
        return "warming", diff
    return "stable", diff


def _analyze_forecast(forecast):
    """What in the week ahead is worth looking forward to."""
    trend, change = _temp_trend([d["temp_max"] for d in forecast])
    analysis = {
        "temp_trend": trend,
        "temp_change": change,
        "next_sunny_in_days": None,
        "next_sunny_weekday": None,
        "next_sunny_hours": None,
        "sunny_streak": 0,
        "weekend_sunny": False,
    }

    if forecast[0]["is_sunny"]:
        streak = 0
        for day in forecast:
            if not day["is_sunny"]:
                break
            streak += 1
        analysis["sunny_streak"] = streak
    else:
        for offset, day in enumerate(forecast[1:], start=1):
            if day["is_sunny"]:
                analysis["next_sunny_in_days"] = offset
                analysis["next_sunny_weekday"] = day["weekday_index"]
                analysis["next_sunny_hours"] = day["sun_hours"]
                break

    weekend = [d for d in forecast[1:] if d["weekday_index"] in (5, 6)]
    analysis["weekend_sunny"] = len(weekend) == 2 and all(d["is_sunny"] for d in weekend)
    return analysis
