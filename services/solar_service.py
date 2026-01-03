from datetime import date, timedelta
import pytz

# try astral v3 style imports first, fallback to suntime
try:
	# astral v3: Observer + sun
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
	# fallback: use suntime (add to requirements)
	from suntime import Sun

	def get_sun_times(lat, lon, target_date=None):
		if target_date is None:
			target_date = date.today()
		s = Sun(lat, lon)
		# suntime returns datetimes in local timezone; convert to UTC
		sunrise_local = s.get_local_sunrise_time(target_date)
		sunset_local = s.get_local_sunset_time(target_date)
		sunrise_utc = sunrise_local.astimezone(pytz.UTC)
		sunset_utc = sunset_local.astimezone(pytz.UTC)
		return {
			"sunrise": sunrise_utc.isoformat(),
			"sunset": sunset_utc.isoformat(),
			"day_length_seconds": int((sunset_utc - sunrise_utc).total_seconds())
		}

def get_daylight_delta(lat, lon):
	today = date.today()
	today_len = get_sun_times(lat, lon, today)["day_length_seconds"]
	yesterday = today - timedelta(days=1)
	y_len = get_sun_times(lat, lon, yesterday)["day_length_seconds"]
	delta = today_len - y_len
	return {"seconds_delta": delta, "minutes_delta": delta // 60}

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