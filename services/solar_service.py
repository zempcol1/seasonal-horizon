from datetime import date, datetime

from config import config
from services.api_client import TTLCache, request_json

_cache = TTLCache(config.CACHE_TTL_SOLAR)


def _get_winter_solstice_date():
    """Return the most recent winter solstice."""
    today = date.today()
    solstice = date(today.year, 12, 21)
    if today < solstice:
        solstice = date(today.year - 1, 12, 21)
    return solstice


def get_daylight_delta(lat, lon):
    """
    Fetches solar dynamics: day length, change from yesterday, week, and solstice.
    """
    cache_key = f"solar_{lat:.2f}_{lon:.2f}_{date.today()}"
    cached = _cache.get(cache_key)
    if cached:
        return cached

    try:
        solstice = _get_winter_solstice_date()
        today = date.today()
        days_since_solstice = (today - solstice).days
        past_days = min(days_since_solstice, 92)
        
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["sunrise", "sunset", "daylight_duration"],
            "timezone": "auto",
            "past_days": past_days,
            "forecast_days": 1
        }
        
        data = request_json(url, params)
        if not data:
            return {}

        daily = data.get("daily", {})
        durations = daily.get("daylight_duration", [])
        sunrises = daily.get("sunrise", [])
        sunsets = daily.get("sunset", [])

        if not durations:
            return {}

        idx_today = len(durations) - 1
        today_sec = durations[idx_today]
        
        yesterday_sec = durations[idx_today - 1] if idx_today > 0 else today_sec
        delta_daily = today_sec - yesterday_sec
        
        idx_week = idx_today - 7
        last_week_sec = durations[idx_week] if idx_week >= 0 else today_sec
        delta_weekly = today_sec - last_week_sec
        
        solstice_sec = durations[0] if len(durations) > 7 else today_sec
        delta_solstice = today_sec - solstice_sec

        sunrise_str = sunrises[idx_today] if idx_today < len(sunrises) else ""
        sunset_str = sunsets[idx_today] if idx_today < len(sunsets) else ""

        fmt = "%Y-%m-%dT%H:%M"
        result = {
            "day_len_sec": today_sec,
            "delta_daily_sec": delta_daily,
            "delta_weekly_sec": delta_weekly,
            "delta_solstice_sec": delta_solstice,
            "sunrise": datetime.strptime(sunrise_str, fmt) if sunrise_str else None,
            "sunset": datetime.strptime(sunset_str, fmt) if sunset_str else None
        }
        
        _cache.set(cache_key, result)
        return result
        
    except Exception:
        return {}
