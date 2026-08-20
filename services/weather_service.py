from datetime import date, datetime

from config import config
from services.api_client import TTLCache, request_json

_cache = TTLCache(config.CACHE_TTL_WEATHER)

# Open-Meteo weather codes, grouped for narrative lookup.
CLEAR_CODES = frozenset([0, 1])
GOOD_CODES = frozenset([0, 1, 2])  # clear, mainly clear, partly cloudy
SNOW_CODES = frozenset([71, 73, 75, 77, 85, 86])
RAIN_CODES = frozenset([51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99])


def classify(code):
    """Bucket a code as clear / snow / rain / grey for narrative lookup."""
    if code in CLEAR_CODES:
        return "clear"
    if code in SNOW_CODES:
        return "snow"
    if code in RAIN_CODES:
        return "rain"
    return "grey"


def is_good(code):
    """Clear enough to be worth going outside."""
    return code in GOOD_CODES


def is_bad(code):
    """Rain or storms."""
    return code in RAIN_CODES


def fetch_daily_weather(lat, lon, days=7):
    """
    Fetches 7-day weather data with detailed analysis for narrative generation.
    """
    cache_key = f"weather_{lat:.2f}_{lon:.2f}_{date.today()}"
    cached = _cache.get(cache_key)
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
        
        data = request_json(url, params)
        if not data:
            return {}

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
            code = codes[i]
            forecast.append({
                "date": day_date,
                "weekday_index": day_date.weekday() if day_date else None,
                "code": code,
                "temp_max": temps_max[i] if i < len(temps_max) else None,
                "temp_min": temps_min[i] if i < len(temps_min) else None,
                "precip": precip[i] if i < len(precip) else 0,
                "precip_prob": precip_prob[i] if i < len(precip_prob) else 0,
                "is_good": is_good(code),
                "is_bad": is_bad(code),
            })

        result = {
            "forecast": forecast,
            "today": forecast[0] if forecast else {},
            "analysis": _analyze_forecast(forecast, temps_max)
        }
        
        _cache.set(cache_key, result)
        return result
        
    except Exception:
        return {}


def _analyze_forecast(forecast, temps_max):
    """Analyze the 7-day forecast for narrative patterns."""
    if not forecast:
        return {}
    
    analysis = {
        "temp_trend": "stable",
        "temp_change": 0,
        "next_good_weekday": None,
        "next_good_in_days": -1,
        "next_bad_weekday": None,
        "next_bad_in_days": -1,
        "good_streak_length": 0,
        "bad_streak_length": 0,
        "weekend_outlook": "mixed",
    }
    
    # Temperature trend analysis
    if temps_max and len(temps_max) >= 3:
        today_temp = temps_max[0] if temps_max[0] else 0
        
        # Count how many of next days are warmer
        warmer_count = sum(1 for t in temps_max[1:5] if t and t > today_temp + 1)

        # Calculate trend from first half to second half
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
        # Also check if consistently warming day-over-day
        elif warmer_count >= 3:
            analysis["temp_trend"] = "warming"
    
    if forecast[0].get("is_bad", False):
        for i, day in enumerate(forecast[1:], 1):
            if day.get("is_good", False):
                analysis["next_good_weekday"] = day.get("weekday_index")
                analysis["next_good_in_days"] = i
                break
    
    if forecast[0].get("is_good", False):
        for i, day in enumerate(forecast[1:], 1):
            if day.get("is_bad", False):
                analysis["next_bad_weekday"] = day.get("weekday_index")
                analysis["next_bad_in_days"] = i
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

    return analysis
