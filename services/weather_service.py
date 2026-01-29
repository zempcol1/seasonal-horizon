import requests
import time
from datetime import date, datetime

from config import config

# Simple in-memory cache
_cache = {}


def _get_cached(key):
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < config.CACHE_TTL_WEATHER:
            return data
        del _cache[key]
    return None


def _set_cached(key, data):
    _cache[key] = (data, time.time())


def fetch_daily_weather(lat, lon, days=7):
    """
    Fetches 7-day weather data with detailed analysis for narrative generation.
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
            "daily": ["weathercode", "temperature_2m_max", "temperature_2m_min", 
                      "precipitation_sum", "precipitation_probability_max"],
            "timezone": "auto",
            "forecast_days": days
        }
        
        resp = requests.get(url, params=params, timeout=config.API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        codes = daily.get("weathercode", [])
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])
        precip_prob = daily.get("precipitation_probability_max", [])
        
        forecast = []
        for i in range(min(7, len(codes))):
            day_date = datetime.strptime(dates[i], "%Y-%m-%d") if i < len(dates) else None
            forecast.append({
                "date": day_date,
                "weekday": day_date.strftime("%A") if day_date else f"Day {i+1}",
                "weekday_short": day_date.strftime("%a") if day_date else f"D{i+1}",
                "code": codes[i] if i < len(codes) else 0,
                "temp_max": temps_max[i] if i < len(temps_max) else None,
                "temp_min": temps_min[i] if i < len(temps_min) else None,
                "precip": precip[i] if i < len(precip) else 0,
                "precip_prob": precip_prob[i] if i < len(precip_prob) else 0,
                "is_good": _is_good_weather(codes[i] if i < len(codes) else 0),
                "is_bad": _is_bad_weather(codes[i] if i < len(codes) else 0),
            })
        
        result = {
            "forecast": forecast,
            "today": forecast[0] if forecast else {},
            "tomorrow": forecast[1] if len(forecast) > 1 else {},
            "analysis": _analyze_forecast(forecast, temps_max)
        }
        
        _set_cached(cache_key, result)
        return result
        
    except Exception:
        return {}


def _is_good_weather(code):
    """Check if weather code indicates good weather."""
    return code in [0, 1, 2]  # Clear, mainly clear, partly cloudy

def _is_bad_weather(code):
    """Check if weather code indicates bad/rainy weather."""
    return code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]  # Rain/storms

def _is_snow(code):
    """Check if weather code indicates snow."""
    return code in [71, 73, 75, 77, 85, 86]

def _analyze_forecast(forecast, temps_max):
    """Analyze the 7-day forecast for narrative patterns."""
    if not forecast:
        return {}
    
    analysis = {
        "temp_trend": "stable",
        "temp_change": 0,
        "next_good_day": None,
        "next_good_day_index": -1,
        "next_bad_day": None,
        "next_bad_day_index": -1,
        "good_streak_length": 0,
        "bad_streak_length": 0,
        "weekend_outlook": "mixed",
        "week_character": "mixed",
    }
    
    if temps_max and len(temps_max) >= 3:
        first_half = sum(t for t in temps_max[:3] if t) / max(1, len([t for t in temps_max[:3] if t]))
        second_half = sum(t for t in temps_max[3:6] if t) / max(1, len([t for t in temps_max[3:6] if t]))
        diff = second_half - first_half
        analysis["temp_change"] = round(diff, 1)
        if diff > 4:
            analysis["temp_trend"] = "warming_strong"
        elif diff > 2:
            analysis["temp_trend"] = "warming"
        elif diff < -4:
            analysis["temp_trend"] = "cooling_strong"
        elif diff < -2:
            analysis["temp_trend"] = "cooling"
    
    if forecast[0].get("is_bad", False):
        for i, day in enumerate(forecast[1:], 1):
            if day.get("is_good", False):
                analysis["next_good_day"] = day.get("weekday", f"Day {i+1}")
                analysis["next_good_day_index"] = i
                break
    
    if forecast[0].get("is_good", False):
        for i, day in enumerate(forecast[1:], 1):
            if day.get("is_bad", False):
                analysis["next_bad_day"] = day.get("weekday", f"Day {i+1}")
                analysis["next_bad_day_index"] = i
                break
    
    today_good = forecast[0].get("is_good", False)
    streak = 1
    for day in forecast[1:]:
        if day.get("is_good", False) == today_good:
            streak += 1
        else:
            break
    
    if today_good:
        analysis["good_streak_length"] = streak
    else:
        analysis["bad_streak_length"] = streak
    
    today_date = forecast[0].get("date")
    if today_date:
        days_until_saturday = (5 - today_date.weekday()) % 7
        days_until_sunday = (6 - today_date.weekday()) % 7
        
        sat_good = sun_good = False
        if days_until_saturday < len(forecast):
            sat_good = forecast[days_until_saturday].get("is_good", False)
        if days_until_sunday < len(forecast):
            sun_good = forecast[days_until_sunday].get("is_good", False)
        
        if sat_good and sun_good:
            analysis["weekend_outlook"] = "good"
        elif not sat_good and not sun_good:
            analysis["weekend_outlook"] = "bad"
        else:
            analysis["weekend_outlook"] = "mixed"
    
    good_days = sum(1 for d in forecast if d.get("is_good", False))
    bad_days = sum(1 for d in forecast if d.get("is_bad", False))
    
    if good_days >= 5:
        analysis["week_character"] = "mostly_good"
    elif bad_days >= 5:
        analysis["week_character"] = "mostly_bad"
    elif good_days >= 3 and bad_days <= 2:
        analysis["week_character"] = "good_stretch"
    elif bad_days >= 3 and good_days <= 2:
        analysis["week_character"] = "grey_stretch"
    
    return analysis
