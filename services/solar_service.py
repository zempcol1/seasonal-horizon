from datetime import date, datetime

from config import config
from services.api_client import TTLCache, request_json

_cache = TTLCache(config.CACHE_TTL_SOLAR)

TIME_FORMAT = "%Y-%m-%dT%H:%M"
FORECAST_DAYS = 16  # the most Open-Meteo allows; the milestone is simply
                    # absent when it falls outside that window


def _get_darkest_solstice_date(lat):
    """
    Most recent solstice with the shortest day, for this hemisphere.

    December in the north, June in the south. Getting this wrong would make
    every "gained since the solstice" figure meaningless below the equator.
    """
    today = date.today()
    month, day = (12, 21) if lat >= 0 else (6, 21)
    solstice = date(today.year, month, day)
    if today < solstice:
        solstice = date(today.year - 1, month, day)
    return solstice


def _parse(stamp):
    return datetime.strptime(stamp, TIME_FORMAT) if stamp else None


def _next_sunset_milestone(sunsets, idx_today):
    """
    When the sunset next crosses a half-hour mark - 18:00, 18:30, and so on.

    Read off the actual forecast rather than extrapolated from today's rate,
    because a projected date could easily be a day or two out, and a wrong
    date is exactly what this app must never print. Whole hours alone were
    too rare to be useful: Open-Meteo only forecasts 16 days, and a sunset
    moving two minutes a day needs longer than that to travel a full hour.

    Returns None while the evenings are still drawing in.
    """
    today_sunset = _parse(sunsets[idx_today]) if idx_today < len(sunsets) else None
    if not today_sunset:
        return None

    minutes = today_sunset.hour * 60 + today_sunset.minute
    target = (minutes // 30 + 1) * 30       # next :00 or :30 after today
    if target >= 24 * 60:
        return None

    for offset, stamp in enumerate(sunsets[idx_today + 1:], start=1):
        sunset = _parse(stamp)
        if sunset and sunset.hour * 60 + sunset.minute >= target:
            return {"time": f"{target // 60:02d}:{target % 60:02d}", "days": offset}
    return None


def get_daylight_delta(lat, lon):
    """
    Fetches solar dynamics: day length, change from yesterday, week, and solstice.
    """
    cache_key = f"solar_{lat:.2f}_{lon:.2f}_{date.today()}"
    cached = _cache.get(cache_key)
    if cached:
        return cached

    try:
        solstice = _get_darkest_solstice_date(lat)
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
            "forecast_days": FORECAST_DAYS,
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

        # The series runs [past_days ... today ... forecast], so today sits at
        # index past_days - not at the end, now that we ask for future days.
        idx_today = min(past_days, len(durations) - 1)
        today_sec = durations[idx_today]

        yesterday_sec = durations[idx_today - 1] if idx_today > 0 else today_sec
        idx_week = idx_today - 7
        last_week_sec = durations[idx_week] if idx_week >= 0 else today_sec
        solstice_sec = durations[0] if idx_today > 7 else today_sec

        result = {
            "day_len_sec": today_sec,
            "delta_daily_sec": today_sec - yesterday_sec,
            "delta_weekly_sec": today_sec - last_week_sec,
            "delta_solstice_sec": today_sec - solstice_sec,
            "sunrise": _parse(sunrises[idx_today]) if idx_today < len(sunrises) else None,
            "sunset": _parse(sunsets[idx_today]) if idx_today < len(sunsets) else None,
            "sunset_milestone": _next_sunset_milestone(sunsets, idx_today),
        }

        _cache.set(cache_key, result)
        return result

    except Exception:
        return {}
