import requests
import time
from datetime import date

# Simple in-memory cache
_cache = {}
_cache_ttl = 300  # 5 minutes

def _get_cached(key):
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < _cache_ttl:
            return data
        del _cache[key]
    return None

def _set_cached(key, data):
    _cache[key] = (data, time.time())

def fetch_daily_weather(lat, lon, days=5):
    """
    Fetches daily weather data including multi-day forecast.
    Returns structured data with today, tomorrow, and week outlook.
    """
    cache_key = f"weather_{lat:.2f}_{lon:.2f}_{date.today()}"
    cached = _get_cached(cache_key)
    if cached:
        return cached

    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["weathercode", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
            "timezone": "auto",
            "forecast_days": days
        }
        
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        
        daily = data.get("daily", {})
        codes = daily.get("weathercode", [])
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])
        
        # Structure the response
        result = {
            "daily": daily,
            "today": {
                "code": codes[0] if codes else 0,
                "temp_max": temps_max[0] if temps_max else None,
                "temp_min": temps_min[0] if temps_min else None,
                "precip": precip[0] if precip else 0
            },
            "tomorrow": {
                "code": codes[1] if len(codes) > 1 else 0,
                "temp_max": temps_max[1] if len(temps_max) > 1 else None,
                "precip": precip[1] if len(precip) > 1 else 0
            },
            "week_codes": codes[:5] if codes else [],
            "week_precip_total": sum(precip[:5]) if precip else 0,
            "week_temp_trend": _calc_temp_trend(temps_max[:5]) if temps_max else "stable"
        }
        
        _set_cached(cache_key, result)
        return result
        
    except Exception as e:
        print(f"Weather API error: {e}")
        return {}

def _calc_temp_trend(temps):
    """Calculate if temperatures are rising, falling, or stable."""
    if not temps or len(temps) < 3:
        return "stable"
    first_half = sum(temps[:len(temps)//2]) / (len(temps)//2)
    second_half = sum(temps[len(temps)//2:]) / (len(temps) - len(temps)//2)
    diff = second_half - first_half
    if diff > 3:
        return "warming"
    elif diff < -3:
        return "cooling"
    return "stable"
