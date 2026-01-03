import requests
from config import Config
from datetime import date, timedelta

def fetch_daily_temperature(lat, lon, days=7):
	end = date.today()
	start = end - timedelta(days=days-1)
	params = {
		"latitude": lat,
		"longitude": lon,
		"daily": "temperature_2m_max,temperature_2m_min",
		"timezone": "UTC",
		"start_date": start.isoformat(),
		"end_date": end.isoformat()
	}
	resp = requests.get(Config.OPEN_METEO_BASE, params=params, timeout=10)
	resp.raise_for_status()
	return resp.json()
