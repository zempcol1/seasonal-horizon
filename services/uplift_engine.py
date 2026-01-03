from services.solar_service import get_daylight_delta
from services.weather_service import fetch_daily_temperature
from datetime import date
import hashlib, random, statistics

def _seed_from(lat, lon, d=None):
	if d is None:
		d = date.today().isoformat()
	key = f"{d}|{lat:.6f}|{lon:.6f}"
	h = hashlib.sha256(key.encode("utf-8")).digest()
	return int.from_bytes(h[:8], "big")

def _forecast_stats(lat, lon, days=7):
	"""
	Return average temperature across forecast and simple trend:
	{'avg': float, 'trend': float} where trend = last_day_avg - first_day_avg
	"""
	try:
		j = fetch_daily_temperature(lat, lon, days=days)
		d = j.get("daily", {})
		maxs = d.get("temperature_2m_max") or []
		mins = d.get("temperature_2m_min") or []
		if not maxs or not mins or len(maxs) != len(mins):
			return None
		avgs = [ (mx + mn) / 2.0 for mx, mn in zip(maxs, mins) ]
		avg_all = statistics.mean(avgs)
		trend = avgs[-1] - avgs[0] if len(avgs) >= 2 else 0.0
		return {"avg": avg_all, "trend": trend, "days": len(avgs)}
	except Exception:
		return None

def generate_uplift(lat=None, lon=None):
	# deterministic per day+coords for repeatable variance
	seed = _seed_from(lat or 0.0, lon or 0.0)
	r = random.Random(seed)

	# daylight delta in minutes
	try:
		dd = get_daylight_delta(lat, lon)
		mins = dd.get("minutes_delta", 0)
	except Exception:
		mins = None

	# weather forecast stats (7 days)
	fstats = _forecast_stats(lat, lon, days=7)

	# season by month
	month = date.today().month
	if month in (12,1,2):
		season = "winter"
	elif month in (3,4,5):
		season = "spring"
	elif month in (6,7,8):
		season = "summer"
	else:
		season = "autumn"

	# base openers and tails
	openers = [
		"Here's your seasonal note for today:",
		"A short, grounded update:",
		"Nature update for today:"
	]

	# choose tone based on forecast and season
	paragraphs = []

	# If we have forecast data, incorporate it
	if fstats:
		avg = fstats["avg"]
		trend = fstats["trend"]
		# cold & stable / colder
		if avg < 2.5 and trend <= 0.5:
			paragraphs = [
				"The coming week stays on the cool side with an average around {:.1f}°C. Winter still holds its ground—take small comforts like warm drinks and bright indoor moments.".format(avg),
				"Temperatures are low and not trending up quickly. Even short outdoor moments can provide a helpful reset: wrap up and seek whatever light you can."
			]
		# cold but warming
		elif avg < 5.0 and trend > 0.5:
			paragraphs = [
				"Average temperatures near {:.1f}°C but trending slightly warmer over the week. The small upward shift can feel meaningful — try to catch a bit more daylight when you can.".format(avg),
				"Signs of gradual warming appear in the forecast. A short walk on a milder afternoon may reveal early, subtle signs of seasonal change."
			]
		# mild / clear spring-like
		elif avg >= 5.0 and trend > 0.5:
			paragraphs = [
				"Forecasts show milder days ahead (avg ~{:.1f}°C) and a warming trend. Use the extra light as a gentle prompt for a short outdoor routine.".format(avg),
				"The week looks milder, with a clear warming trend — small outdoor rituals can help you notice the season unfolding."
			]
		else:
			# neutral fallback when forecast present
			paragraphs = [
				"The forecast suggests average temperatures near {:.1f}°C for the next days. Notice small changes in light and routine — they accumulate.".format(avg),
				"Weather is mixed but predictable this week. Taking a brief outdoor break can help mark the passing of days and the slow seasonal turn."
			]
	else:
		# no forecast -> season-aware generic phrasing
		if season == "winter":
			paragraphs = [
				"Winter still dominates. Even short outdoor moments—wrapped up warm—can help you sense subtle changes in light.",
				"Days are short and cool; small rituals around light and movement can make a difference."
			]
		elif season == "spring":
			paragraphs = [
				"Spring is on its way; look for the first subtle signs—early blooms or birds returning to morning routines.",
				"Longer days are arriving; try to notice a small shift in light during your daily routine."
			]
		elif season == "summer":
			paragraphs = [
				"Summer brings long light; use a brief outdoor pause to refill energy.",
				"Sunlit moments are plentiful — a short ritual outdoors helps mark the day."
			]
		else:
			paragraphs = [
				"Autumn is shaping the light and air; notice textures and colors shifting in short outdoor checks.",
				"Cooler air and softer light invite quiet observations in nature."
			]

	# choose opener, paragraph, and hint deterministically
	opener = r.choice(openers)
	para = r.choice(paragraphs)

	hints = [
		"Tip: a 10-minute outdoor break can reveal subtle seasonal shifts.",
		"Tip: check trees and shrubs for early buds or late leaves depending on the season.",
		"Tip: listen for changes in bird activity around sunrise."
	]
	hint = r.choice(hints)

	# assemble and optionally include daylight delta
	delta_text = ""
	if mins is not None:
		if mins > 0:
			delta_text = " You've gained {} minute{} of daylight since yesterday.".format(abs(mins), "s" if abs(mins) != 1 else "")
		elif mins < 0:
			delta_text = " You lost {} minute{} of daylight since yesterday.".format(abs(mins), "s" if abs(mins) != 1 else "")
	# final assembly
	return "{} {}{} {}".format(opener, para, delta_text, hint)