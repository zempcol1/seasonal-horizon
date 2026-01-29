import requests
from datetime import date, timedelta, datetime
import pytz
import time

from config import config

# Simple in-memory cache
_cache = {}


def _get_cached(key):
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < config.CACHE_TTL_SOLAR:
            return data
        del _cache[key]
    return None


def _set_cached(key, data):
    _cache[key] = (data, time.time())


def _request_with_retry(url, params, max_retries=None, timeout=None):
    """Make HTTP request with retry logic."""
    max_retries = max_retries or config.API_MAX_RETRIES
    timeout = timeout or config.API_TIMEOUT
    last_error = None
    
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            last_error = "timeout"
            time.sleep(0.5 * (attempt + 1))
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            time.sleep(0.3 * (attempt + 1))
    return None


# try astral v3 style imports first, fallback to suntime
try:
	from astral import Observer
	from astral.sun import sun as astral_sun
	_ASTRAL = True
except Exception:
	_ASTRAL = False

if _ASTRAL:
	def get_sun_times(lat, lon, target_date=None):
		if target_date is None:
			target_date = date.today()
		observer = Observer(latitude=lat, longitude=lon, elevation=0)
		s = astral_sun(observer=observer, date=target_date, tzinfo=pytz.UTC)
		return {
			"sunrise": s["sunrise"].isoformat(),
			"sunset": s["sunset"].isoformat(),
			"day_length_seconds": int((s["sunset"] - s["sunrise"]).total_seconds())
		}
else:
	from suntime import Sun

	def get_sun_times(lat, lon, target_date=None):
		if target_date is None:
			target_date = date.today()
		s = Sun(lat, lon)
		sunrise_local = s.get_local_sunrise_time(target_date)
		sunset_local = s.get_local_sunset_time(target_date)
		sunrise_utc = sunrise_local.astimezone(pytz.UTC)
		sunset_utc = sunset_local.astimezone(pytz.UTC)
		return {
			"sunrise": sunrise_utc.isoformat(),
			"sunset": sunset_utc.isoformat(),
			"day_length_seconds": int((sunset_utc - sunrise_utc).total_seconds())
		}


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
    cached = _get_cached(cache_key)
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
        
        data = _request_with_retry(url, params)
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
        
        _set_cached(cache_key, result)
        return result
        
    except Exception:
        return {}


def get_daylight_stats(lat, lon):
	"""
	Return dict with:
	 - day_length_seconds (today)
	 - delta_since_yesterday_minutes
	 - delta_since_winter_solstice_minutes
	"""
	today = date.today()
	yesterday = today - timedelta(days=1)
	# most recent Dec 21 before today
	solstice = date(today.year, 12, 21)
	if today < solstice:
		solstice = date(today.year - 1, 12, 21)

	today_len = get_sun_times(lat, lon, today)["day_length_seconds"]
	y_len = get_sun_times(lat, lon, yesterday)["day_length_seconds"]
	s_len = get_sun_times(lat, lon, solstice)["day_length_seconds"]

	delta_y = today_len - y_len
	delta_s = today_len - s_len
	return {
		"day_length_seconds": int(today_len),
		"delta_since_yesterday_minutes": int(round(delta_y / 60.0)),
		"delta_since_solstice_minutes": int(round(delta_s / 60.0))
	}