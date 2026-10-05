"""
Daylight, calculated rather than fetched.

Sunrise and sunset are astronomy, exact for any date, so there is no API to
wait for and no forecast window to run out of. That matters for milestones:
a sunset date weeks ahead is as certain as today's.
"""

from datetime import date, timedelta
from zoneinfo import ZoneInfo

from astral import Observer
from astral.sun import elevation, sun

from config import TIMEZONE

_TZ = ZoneInfo(TIMEZONE)

MILESTONE_HORIZON_DAYS = 60  # near the solstice a half hour takes ~4 weeks


def _last_solstice(today):
    """
    The most recent solstice, June or December.

    Against December the change is a gain; against June it is a loss, which
    keeps "gained since the solstice" from turning true in November.
    """
    for candidate in (date(today.year, 12, 21), date(today.year, 6, 21)):
        if candidate <= today:
            return candidate
    return date(today.year - 1, 12, 21)


def _sun(observer, day):
    """Sunrise and sunset for one day, local time."""
    times = sun(observer, date=day, tzinfo=_TZ)
    return times["sunrise"], times["sunset"]


def _noon_height(observer, day):
    """How high the sun stands at midday, in degrees."""
    return elevation(observer, sun(observer, date=day, tzinfo=_TZ)["noon"])


def _clock_seconds(moment):
    return moment.hour * 3600 + moment.minute * 60 + moment.second


def _day_length(observer, day):
    sunrise, sunset = _sun(observer, day)
    return (sunset - sunrise).total_seconds()


def _next_sunset_milestone(observer, today, today_sunset):
    """
    When the sunset next crosses a half-hour mark - 17:00, 17:30, and so on.

    Returns None while the evenings are still drawing in.
    """
    minutes = today_sunset.hour * 60 + today_sunset.minute
    target = (minutes // 30 + 1) * 30       # next :00 or :30 after today

    for offset in range(1, MILESTONE_HORIZON_DAYS + 1):
        _, sunset = _sun(observer, today + timedelta(days=offset))
        if sunset.hour * 60 + sunset.minute >= target:
            return {"time": f"{target // 60:02d}:{target % 60:02d}", "days": offset}
        if sunset.hour * 60 + sunset.minute < minutes:
            return None                     # heading the other way
    return None


def get_daylight_delta(lat, lon, today):
    """
    Day length, sunrise and sunset, and how the day has changed since
    yesterday, last week and the last solstice.

    Empty where the sun does not rise or set at all - polar day or night,
    far outside the region this app is made for.
    """
    observer = Observer(lat, lon)
    solstice = _last_solstice(today)
    try:
        sunrise, sunset = _sun(observer, today)
        sunrise_before, sunset_before = _sun(observer, today - timedelta(days=1))
        today_sec = (sunset - sunrise).total_seconds()
        last_week_sec = _day_length(observer, today - timedelta(days=7))
        solstice_sec = _day_length(observer, solstice)
    except ValueError:
        return {}

    return {
        "day_len_sec": today_sec,
        "delta_daily_sec": today_sec - (sunset_before - sunrise_before).total_seconds(),
        "delta_weekly_sec": today_sec - last_week_sec,
        "delta_solstice_sec": today_sec - solstice_sec,
        "sunrise": sunrise,
        "sunset": sunset,
        "sunset_milestone": _next_sunset_milestone(observer, today, sunset),
        # On the clock, against yesterday: negative means earlier. Sunsets
        # start getting later about ten days before the solstice, sunrises
        # earlier about ten days after it.
        "sunrise_shift_sec": _clock_seconds(sunrise) - _clock_seconds(sunrise_before),
        "sunset_shift_sec": _clock_seconds(sunset) - _clock_seconds(sunset_before),
        "noon_gain_deg": _noon_height(observer, today) - _noon_height(observer, solstice),
    }
