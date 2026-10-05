"""
The week's weather, read for what there is to look forward to.

Sunshine hours are the measure, not weather codes. A code says "overcast"
or "showers" for a day that still gets nine hours of sun, which is exactly
the kind of day this app should not talk down.

The last 30 days come along with the forecast, so a sunny day can be told
apart from the first sunny day in a week, and a mild one from the warmest
in a month.
"""

from datetime import datetime

from config import TIMEZONE, config, today
from services.api_client import TTLCache, request_json

_cache = TTLCache(config.CACHE_TTL_WEATHER)

SNOW_CODES = frozenset([71, 73, 75, 77, 85, 86])
FOG_CODES = frozenset([45, 48])

# Share of the daylight with direct sun that makes a day a sunny one.
SUNNY_SHARE = 0.5

PAST_DAYS = 30

# Hochnebel: a thick low layer with clear sky above it, over the hours when
# it matters. Above the lid the sun is out.
LID_HOURS = range(9, 16)
LID_LOW_MIN = 70        # % low cloud
LID_ABOVE_MAX = 30      # % mid and high cloud


def _sun(sunshine_sec, daylight_sec):
    """Hours of sun and whether that makes the day a sunny one."""
    if sunshine_sec is None or not daylight_sec:
        return None, False
    return sunshine_sec / 3600, sunshine_sec / daylight_sec >= SUNNY_SHARE


def fetch_daily_weather(lat, lon, days=7):
    """The coming week day by day, the past month, and what stands out."""
    cache_key = f"weather_{lat:.2f}_{lon:.2f}_{today()}"
    cached = _cache.get(cache_key)
    if cached:
        return cached

    data = request_json("https://api.open-meteo.com/v1/forecast", {
        "latitude": lat,
        "longitude": lon,
        "daily": ["weathercode", "temperature_2m_max", "temperature_2m_min",
                  "sunshine_duration", "daylight_duration", "precipitation_sum",
                  "snowfall_sum", "uv_index_max"],
        "hourly": ["cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
        "timezone": TIMEZONE,
        "past_days": PAST_DAYS,
        "forecast_days": days,
    })
    if not data:
        return {}

    try:
        rows = _rows(data.get("daily", {}))
    except (TypeError, ValueError):
        return {}   # malformed response: no weather rather than a crash

    # The series runs [past ... today ... forecast]; find today by its date.
    stamp = today().isoformat()
    idx = next((i for i, r in enumerate(rows) if r["date"] == stamp), None)
    if idx is None:
        return {}

    forecast, history = rows[idx:idx + days], rows[:idx]
    forecast[0]["low_cloud_lid"] = _low_cloud_lid(data.get("hourly", {}), stamp)

    result = {
        "forecast": forecast,
        "today": forecast[0],
        "elevation": data.get("elevation"),
        "analysis": _analyze_forecast(forecast, history),
    }
    _cache.set(cache_key, result)
    return result


def _rows(daily):
    """One dict per day, with sunshine read into hours and a sunny flag."""
    def column(name, i):
        values = daily.get(name) or []
        return values[i] if i < len(values) else None

    rows = []
    for i, stamp in enumerate(daily.get("time", [])):
        sun_hours, is_sunny = _sun(column("sunshine_duration", i),
                                   column("daylight_duration", i))
        rows.append({
            "date": stamp,
            "weekday_index": datetime.strptime(stamp, "%Y-%m-%d").weekday(),
            "code": column("weathercode", i),
            "temp_max": column("temperature_2m_max", i),
            "temp_min": column("temperature_2m_min", i),
            "precip": column("precipitation_sum", i),
            "snow_cm": column("snowfall_sum", i),
            "uv": column("uv_index_max", i),
            "sun_hours": sun_hours,
            "is_sunny": is_sunny,
        })
    return rows


def _low_cloud_lid(hourly, stamp):
    """True when today's daytime sky is a low lid with clear air above it."""
    times = hourly.get("time") or []
    hours = [i for i, t in enumerate(times)
             if t.startswith(stamp) and int(t[11:13]) in LID_HOURS]
    if not hours:
        return False

    def mean(name):
        values = [(hourly.get(name) or [None] * len(times))[i] for i in hours]
        values = [v for v in values if v is not None]
        return sum(values) / len(values) if values else None

    low = mean("cloud_cover_low")
    above = [m for m in (mean("cloud_cover_mid"), mean("cloud_cover_high")) if m is not None]
    if low is None or not above:
        return False
    return low >= LID_LOW_MIN and max(above) <= LID_ABOVE_MAX


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


def _analyze_forecast(forecast, history=()):
    """What in the week ahead, and against the month behind, is worth noticing."""
    trend, change = _temp_trend([d["temp_max"] for d in forecast])
    analysis = {
        "temp_trend": trend,
        "temp_change": change,
        "next_sunny_in_days": None,
        "next_sunny_weekday": None,
        "next_sunny_hours": None,
        "sunny_streak": 0,
        "weekend_sunny": False,
        "grey_days_before": None,
        "warmest_since": None,
        "week_sun_hours": None,
        "past_week_sun_hours": None,
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

    week = [d["sun_hours"] for d in forecast[:7]]
    past_week = [d["sun_hours"] for d in history[-7:]]
    if len(week) == 7 and None not in week:
        analysis["week_sun_hours"] = sum(week)
    if len(past_week) == 7 and None not in past_week:
        analysis["past_week_sun_hours"] = sum(past_week)

    if history:
        analysis["grey_days_before"] = _grey_days_before(history)
        analysis["warmest_since"] = _warmest_since(forecast[0], history)
    return analysis


def _grey_days_before(history):
    """How many days in a row before today had no real sun."""
    count = 0
    for day in reversed(history):
        if day["is_sunny"] or day["sun_hours"] is None:
            break
        count += 1
    return count


def _warmest_since(today_row, history):
    """
    The last date that was at least as warm as today, as "YYYY-MM-DD".

    "" when nothing in the past month was - today is the warmest in a month.
    None when today's temperature is unknown.
    """
    high = today_row["temp_max"]
    if high is None:
        return None
    for day in reversed(history):
        if day["temp_max"] is not None and day["temp_max"] >= high:
            return day["date"]
    return ""


_pollen_cache = TTLCache(config.CACHE_TTL_WEATHER)

POLLEN_TYPES = ("alder", "birch", "grass")


def fetch_pollen(lat, lon):
    """Today's peak pollen count per type, in grains per m³. Empty if unknown."""
    cache_key = f"pollen_{lat:.2f}_{lon:.2f}_{today()}"
    cached = _pollen_cache.get(cache_key)
    if cached is not None:
        return cached

    data = request_json("https://air-quality-api.open-meteo.com/v1/air-quality", {
        "latitude": lat,
        "longitude": lon,
        "hourly": [f"{kind}_pollen" for kind in POLLEN_TYPES],
        "timezone": TIMEZONE,
        "forecast_days": 1,
    })
    hourly = (data or {}).get("hourly", {})
    result = {}
    for kind in POLLEN_TYPES:
        values = [v for v in hourly.get(f"{kind}_pollen") or [] if v is not None]
        if values:
            result[kind] = max(values)

    _pollen_cache.set(cache_key, result)
    return result
