"""
Uplift Engine - what is good about today, in one short message.
Supports multiple languages (en, de).

Every message has the same shape: a lead from the strongest signal of the
day, then a companion line from nature - or, on a sunny winter day, a
suggestion for using the sun.

- A signal is one true, good thing about today: the light gaining, sun in
  the forecast, fresh snow. Each is a function in SIGNALS returning a Signal
  with its weight, or None. The weights sit next to the condition that earns
  them, so they can be compared and tuned in one place.
- A signal names the pool its text comes from. Most use their own key; some
  pick a variant ("daily_gain.fast", "snow.alpine") so the wording follows
  how strong the signal is and where the reader is.
- Shrinking daylight has no signal. It is true, but it is not what this app
  is for.
- Nothing is stated that was not measured. Templates declare the facts they
  need through their placeholders, and only templates whose every
  placeholder is backed are offered.
- The message stays the same all day for one place, and each pool steps
  through its lines day by day, so a line comes back only once the pool is
  used up. `variant` asks for another message.
"""

import random
import re
from dataclasses import dataclass, field
from datetime import date, timedelta

from config import today as local_today
from services.solar_service import get_daylight_delta
from services.weather_service import (FOG_CODES, SNOW_CODES, fetch_daily_weather,
                                      fetch_pollen)
from services import uplift_content as content

# Above this the spring signs come late and snow plays a bigger part, so the
# mountains get their own nature content.
ALPINE_ELEVATION_M = 800

COLD_PHASES = frozenset(["darkening", "returning_light"])

TOP_N = 3  # how many of the strongest signals enter the weighted draw

# A signal this strong is the day's news - the solstice, the equinox,
# Sechseläuten. It leads today's message instead of entering the draw;
# "another thought" can still bring up the rest.
EVENT_WEIGHT = 90

# Pollen is real evidence of spring, and bad news for anyone with hay fever.
# So it is only ever considered on one day in this many, per place - rare on
# purpose. Keep it rare.
POLLEN_EVERY_DAYS = 7
POLLEN_BY_MONTH = {2: "alder", 3: "alder", 4: "birch", 5: "grass", 6: "grass"}
POLLEN_NOTICEABLE = 20   # grains per m³

# Customs are a local special for the Zurich and Aargau area. A box, not the
# real borders: it takes in a strip of the neighbours, which is close enough.
CUSTOMS_LAT = (47.13, 47.70)
CUSTOMS_LON = (7.70, 9.00)


# ===== Formatting =====

def format_duration(seconds):
    """Seconds as "14h 3m"."""
    return f"{int(seconds // 3600)}h {int((seconds % 3600) // 60)}m"


def format_span(minutes):
    """Unsigned minutes as "1h 13m", or "22m" below the hour."""
    hours, mins = abs(minutes) // 60, abs(minutes) % 60
    return f"{hours}h {mins}m" if hours else f"{mins}m"


def format_signed_span(minutes):
    """Signed minutes as "-1h 13m", or "+22 min" below the hour."""
    if abs(minutes) < 60:
        return f"{minutes:+d} min"
    return f"{'+' if minutes >= 0 else '-'}{format_span(minutes)}"


def _clock(moment):
    return moment.strftime("%H:%M") if moment else "--:--"


def _format_date(day, lang):
    """ "28 October" / "28. Oktober" """
    month = (content.MONTHS.get(lang) or content.MONTHS["en"])[day.month - 1]
    return f"{day.day}. {month}" if lang == "de" else f"{day.day} {month}"


# Nouns that follow a number. Templates take the word as a placeholder so a
# count of one does not read as "1 minutes".
_NOUNS = {
    "en": {"minutes": ("minute", "minutes"),
           "hours": ("hour", "hours"),
           "days": ("day", "days"),
           "days_dat": ("day", "days")},
    "de": {"minutes": ("Minute", "Minuten"),
           "hours": ("Stunde", "Stunden"),
           "days": ("Tag", "Tage"),
           "days_dat": ("Tag", "Tagen")},   # "in 1 Tag" / "in 3 Tagen"
}


def _noun(count, kind, lang):
    """The right form of a counted noun - "1 Minute" but "4 Minuten"."""
    forms = _NOUNS.get(lang, _NOUNS["en"])[kind]
    return forms[0] if abs(count) == 1 else forms[1]


def _counted(count, *kinds, lang):
    """A count's nouns, ready to drop into a template."""
    return {kind: _noun(count, kind, lang) for kind in kinds}


def _countdown(key, days, lang):
    """
    A count of days, plus "tomorrow" / "in 3 days" as {when}.

    At one day the count itself is left out, which drops the templates that
    would read "count 1 day" and leaves those saying "tomorrow".
    """
    data = {"when": _when(days, lang), **_counted(days, "days", "days_dat", lang=lang)}
    if days != 1:
        data[key] = days
    return data


def _when(days, lang):
    """ "today", "tomorrow" or "in 3 days" """
    if lang == "de":
        return {0: "heute", 1: "morgen"}.get(days, f"in {days} Tagen")
    return {0: "today", 1: "tomorrow"}.get(days, f"in {days} days")


def _weekday_name(index, lang):
    """Localized weekday name for a 0=Monday index."""
    return (content.WEEKDAYS.get(lang) or content.WEEKDAYS["en"])[index]


def _localized(data, lang):
    """The entry for this language, falling back to English."""
    return data.get(lang) or data.get("en") or []


_PLACEHOLDER = re.compile(r"\{(\w+)")


def _backed(templates, data):
    """
    The templates whose every placeholder is backed by real data.

    Templates asking for a fact we could not measure are dropped rather than
    rendered, so the app never shows an unbacked claim or a raw "{placeholder}".
    """
    return [t for t in templates if all(k in data for k in _PLACEHOLDER.findall(t))]


@dataclass(frozen=True)
class Picker:
    """
    Chooses lines so that one place sees something new each day.

    Each pool steps through its lines one day at a time, from a starting
    point that depends on the place, so a line comes back only after the
    whole pool has been used; random drawing repeated far sooner. `variant`
    moves every pool one step further, so asking for another message always
    changes it.
    """
    place: str
    day: date
    variant: int = 0

    def pick(self, pool, name):
        if not pool:
            return None
        start = random.Random(f"{self.place}:{name}").randrange(len(pool))
        return pool[(start + self.day.toordinal() + self.variant) % len(pool)]

    def rng(self):
        """For the weighted draw of the lead."""
        return random.Random(f"{self.place}:{self.day}:{self.variant}")

    def every(self, days, name):
        """True on one day in `days` for this place - for things kept rare."""
        start = random.Random(f"{self.place}:{name}").randrange(days)
        return (self.day.toordinal() + start) % days == 0


# ===== Where and when =====

def _region(elevation):
    """
    Lowland or alpine, used to pick nature observations that fit.

    The app is tuned for one climate band - Switzerland, Germany, Austria,
    the Benelux, northern France and Italy - so height is what separates
    one place from another. Unknown elevation counts as lowland.
    """
    if elevation is not None and elevation >= ALPINE_ELEVATION_M:
        return "alpine"
    return "lowland"


def _in_customs_area(lat, lon):
    return CUSTOMS_LAT[0] <= lat <= CUSTOMS_LAT[1] and CUSTOMS_LON[0] <= lon <= CUSTOMS_LON[1]


def _phase(day):
    """Where the year stands. The dates are the ones in the README."""
    month_day = (day.month, day.day)
    if month_day >= (12, 21) or month_day < (3, 20):
        return "returning_light"
    if month_day < (6, 21):
        return "spring"
    if month_day < (9, 22):
        return "summer"
    if month_day < (11, 1):
        return "autumn"
    return "darkening"


@dataclass(frozen=True)
class Context:
    """
    Everything the signals read, gathered once.

    `solar` is empty where the sun neither rises nor sets, and `weather` is
    empty without a forecast; signals that need them then stay silent.
    """
    today: date
    lang: str
    region: str
    phase: str
    solar: dict
    weather: dict       # today's row of the forecast
    analysis: dict      # what stands out in the week ahead and the month behind
    customs: bool = False
    pollen: dict = field(default_factory=dict)

    @property
    def is_cold(self):
        return self.phase in COLD_PHASES


def _build_context(solar, weather, today, lang, customs=False, pollen=None):
    return Context(
        today=today,
        lang=lang,
        region=_region(weather.get("elevation")),
        phase=_phase(today),
        solar=solar,
        weather=weather.get("today", {}),
        analysis=weather.get("analysis", {}),
        customs=customs,
        pollen=pollen or {},
    )


# ===== Signals =====

@dataclass(frozen=True)
class Signal:
    key: str
    weight: int
    data: dict
    pool: str = None    # content pool, when not the key itself


# -- light: calculated, so always there unless the sun never rises

def _turning_day(ctx):
    """The winter solstice itself."""
    if (ctx.today.month, ctx.today.day) != (12, 21):
        return None
    return Signal("turning_day", 95, {})


def _equinox_day(ctx):
    """20 March: day and night equal, and the bright half begins."""
    if (ctx.today.month, ctx.today.day) != (3, 20):
        return None
    return Signal("equinox_day", 90, {})


def _lichtmess(ctx):
    """
    2 February. The old saying - "an Lichtmess ist der Tag eine Stunde
    länger" - checked against the actual gain before it is repeated.
    Kept low-key on purpose: one candidate among others on its one day,
    not an event that always leads.
    """
    minutes = int(ctx.solar.get("delta_solstice_sec", 0) // 60)
    if (ctx.today.month, ctx.today.day) != (2, 2) or minutes < 60:
        return None
    return Signal("lichtmess", 65, {"hours_gained": format_span(minutes)})


def _solstice_countdown(ctx):
    """The last fortnight before the shortest day; earlier it is too far off."""
    if ctx.phase != "darkening":
        return None
    days = (date(ctx.today.year, 12, 21) - ctx.today).days
    if days > 14:
        return None
    return Signal("solstice_countdown", 80, {
        "days_to_solstice": days, **_counted(days, "days", "days_dat", lang=ctx.lang),
    })


def _equinox_countdown(ctx):
    """The last ten days before day and night are equal."""
    if ctx.phase != "returning_light" or ctx.today.month != 3:
        return None
    days = (date(ctx.today.year, 3, 20) - ctx.today).days
    if not 1 <= days <= 10:
        return None
    return Signal("equinox_countdown", 65, {
        "days_to_equinox": days, **_counted(days, "days", "days_dat", lang=ctx.lang),
    })


def _evenings_turned(ctx):
    """Mid-December: sunsets get later again while the day is still shrinking."""
    if ctx.phase != "darkening" or ctx.solar.get("sunset_shift_sec", 0) <= 0:
        return None
    return Signal("evenings_turned", 85, {"sunset": _clock(ctx.solar["sunset"])})


def _mornings_turned(ctx):
    """From early January the sunrise comes earlier again - news for a month."""
    if ctx.phase != "returning_light" or ctx.solar.get("sunrise_shift_sec", 0) >= 0:
        return None
    return Signal("mornings_turned", 80 if ctx.today.month == 1 else 50,
                  {"sunrise": _clock(ctx.solar["sunrise"])})


def _hour_mark(ctx):
    """The day passing a whole hour - today, or soon."""
    mark = ctx.solar.get("hour_mark")
    if ctx.phase not in ("returning_light", "spring") or not mark:
        return None
    days = mark["days"]
    return Signal("hour_mark", 80 if days == 0 else 60, {
        "hours_mark": mark["hours"], **_countdown("days_until", days, ctx.lang),
    }, pool="hour_mark.today" if days == 0 else "hour_mark")


def _since_solstice(ctx):
    minutes = int(ctx.solar.get("delta_solstice_sec", 0) // 60)
    if ctx.phase != "returning_light" or minutes < 1:
        return None
    return Signal("since_solstice", 70, {"hours_gained": format_span(minutes)})


def _autumn_twin(ctx):
    """The day is back to the length it had on a date people remember."""
    twin = ctx.solar.get("autumn_twin")
    if ctx.phase != "returning_light" or not twin:
        return None
    return Signal("autumn_twin", 60, {"twin_date": _format_date(twin, ctx.lang)})


def _daily_gain(ctx):
    delta = int(ctx.solar.get("delta_daily_sec", 0) // 60)
    if ctx.phase not in ("returning_light", "spring") or delta < 1:
        return None
    return Signal("daily_gain", 60 if ctx.phase == "returning_light" else 45, {
        "delta": delta,
        **_counted(delta, "minutes", lang=ctx.lang),
        "day_length": format_duration(ctx.solar["day_len_sec"]),
        "sunrise": _clock(ctx.solar["sunrise"]),
        "sunset": _clock(ctx.solar["sunset"]),
    }, pool="daily_gain.fast" if delta >= 3 else "daily_gain")


def _sunset_milestone(ctx):
    """The next half hour the sunset crosses - exact, since it is calculated."""
    milestone = ctx.solar.get("sunset_milestone")
    if ctx.phase not in ("returning_light", "spring") or not milestone:
        return None
    return Signal("sunset_milestone", 75 if ctx.phase == "returning_light" else 55, {
        "milestone_time": milestone["time"],
        **_countdown("milestone_days", milestone["days"], ctx.lang),
        "sunset": _clock(ctx.solar["sunset"]),
    })


def _sunrise_milestone(ctx):
    """The mornings' counterpart: sunrise before the next half hour."""
    milestone = ctx.solar.get("sunrise_milestone")
    if ctx.phase not in ("returning_light", "spring") or not milestone:
        return None
    return Signal("sunrise_milestone", 65 if ctx.phase == "returning_light" else 45, {
        "milestone_time": milestone["time"],
        **_countdown("milestone_days", milestone["days"], ctx.lang),
        "sunrise": _clock(ctx.solar["sunrise"]),
    })


def _noon_sun(ctx):
    """The sun climbing higher at midday - it gets stronger, not just longer."""
    gain = ctx.solar.get("noon_gain_deg", 0)
    if ctx.phase != "returning_light" or gain < 2:
        return None
    return Signal("noon_sun", 50, {"noon_gain": round(gain)})


def _dusk_light(ctx):
    """Usable light lasts well past sunset - civil dusk, not the sunset, ends the day."""
    dusk = ctx.solar.get("dusk")
    if ctx.phase not in COLD_PHASES or not dusk:
        return None
    return Signal("dusk_light", 45, {"dusk": _clock(dusk), "sunset": _clock(ctx.solar["sunset"])})


def _peak_light(ctx):
    if ctx.phase != "summer" or ctx.today.month not in (6, 7) or not ctx.solar:
        return None
    return Signal("peak_light", 45, {
        "day_length": format_duration(ctx.solar["day_len_sec"]),
        "sunset": _clock(ctx.solar["sunset"]),
    })


# -- weather: from the forecast and the month behind it, so absent without one

def _sun_hours_data(hours, lang):
    hours = max(1, round(hours))
    return {"sun_hours": hours, **_counted(hours, "hours", lang=lang)}


def _first_sun(ctx):
    """Sun after a run of grey days - the day people notice most."""
    grey = ctx.analysis.get("grey_days_before") or 0
    if not ctx.weather.get("is_sunny") or grey < 4:
        return None
    return Signal("first_sun", 88 if ctx.is_cold else 70, {
        "grey_days": grey,
        **_counted(grey, "days", "days_dat", lang=ctx.lang),
        **_sun_hours_data(ctx.weather["sun_hours"], ctx.lang),
    })


def _sun_ahead(ctx):
    """Not much sun today, but a sunny day within the next four."""
    days = ctx.analysis.get("next_sunny_in_days")
    if days is None or days > 4:
        return None
    return Signal("sun_ahead", 85 if ctx.is_cold else 60, {
        "sunny_day": _weekday_name(ctx.analysis["next_sunny_weekday"], ctx.lang),
        "when": _when(days, ctx.lang),
        **_sun_hours_data(ctx.analysis["next_sunny_hours"], ctx.lang),
    })


def _hochnebel(ctx):
    """
    A low lid of cloud with clear sky above it - the plateau's winter grey,
    with sun a few hundred metres up. Read from the cloud layers, so it is
    measured, not guessed. Only below the lid, and not once the sun is out.
    """
    if ctx.region != "lowland" or not ctx.weather.get("low_cloud_lid") \
            or ctx.weather.get("is_sunny") or ctx.phase == "summer":
        return None
    return Signal("hochnebel", 78, {})


def _snow(ctx):
    snow_cm = ctx.weather.get("snow_cm") or 0
    if ctx.weather.get("code") not in SNOW_CODES and snow_cm < 1:
        return None
    if ctx.region == "alpine":
        pool = "snow.alpine"
    else:
        pool = "snow.fresh" if snow_cm >= 2 else "snow"
    return Signal("snow", 80 if ctx.is_cold else 50, {"snow_cm": round(snow_cm)}, pool=pool)


def _sunny_today(ctx):
    if not ctx.weather.get("is_sunny"):
        return None
    return Signal("sunny_today", 75 if ctx.is_cold else 50,
                  _sun_hours_data(ctx.weather["sun_hours"], ctx.lang),
                  pool="sunny_today.winter" if ctx.is_cold else "sunny_today")


def _warmest_since(ctx):
    """The warmest day in weeks - in the cold half that is news, in summer it is heat."""
    since = ctx.analysis.get("warmest_since")
    high = ctx.weather.get("temp_max")
    if since is None or high is None or ctx.phase == "summer":
        return None
    if since == "":
        since_day, pool = ctx.today - timedelta(days=30), "warmest_since.month"
    else:
        since_day, pool = date.fromisoformat(since), "warmest_since"
        if (ctx.today - since_day).days < 14:
            return None
    return Signal("warmest_since", 70 if ctx.is_cold else 55, {
        "temp_high": f"{round(high)}°C",
        "since_date": _format_date(since_day, ctx.lang),
    }, pool=pool)


def _uv_strength(ctx):
    """Late winter: the UV index says the sun has real strength again."""
    uv = ctx.weather.get("uv")
    if ctx.phase != "returning_light" or uv is None or uv < 3:
        return None
    return Signal("uv_strength", 60, {"uv": round(uv)})


def _sunny_week(ctx):
    """A week ahead with clearly more sun than the week behind."""
    ahead = ctx.analysis.get("week_sun_hours")
    behind = ctx.analysis.get("past_week_sun_hours")
    if ahead is None or behind is None or ahead < 15 or ahead < behind * 1.5:
        return None
    return Signal("sunny_week", 55, {
        "week_hours": round(ahead), "past_week_hours": round(behind),
    })


def _fog(ctx):
    if ctx.weather.get("code") not in FOG_CODES:
        return None
    return Signal("fog", 70, {}, pool="fog.alpine" if ctx.region == "alpine" else "fog")


def _frost_clear(ctx):
    """A freezing night followed by a sunny day - the best kind of winter day."""
    low = ctx.weather.get("temp_min")
    if not ctx.is_cold or low is None or low > 0 or not ctx.weather.get("is_sunny"):
        return None
    return Signal("frost_clear", 70, {"temp_low": f"{round(low)}°C"})


def _warming(ctx):
    """Milder days ahead - worth most in the cold months, not needed in summer."""
    trend = ctx.analysis.get("temp_trend")
    if ctx.phase == "summer" or trend not in ("warming", "warming_strong"):
        return None
    weight = (75 if trend == "warming_strong" else 55) + (10 if ctx.is_cold else 0)
    return Signal("warming", weight,
                  {"temp_change": f"{abs(ctx.analysis.get('temp_change', 0)):.0f}"})


def _sunny_streak(ctx):
    streak = ctx.analysis.get("sunny_streak", 0)
    if streak < 3:
        return None
    return Signal("sunny_streak", 65, {
        "streak_days": streak, **_counted(streak, "days", lang=ctx.lang),
    })


def _some_sun(ctx):
    """A dull winter day that still has an hour or two of sun in it."""
    hours = ctx.weather.get("sun_hours")
    if not ctx.is_cold or ctx.weather.get("is_sunny") or hours is None or hours < 1:
        return None
    return Signal("some_sun", 55, _sun_hours_data(hours, ctx.lang))


def _weekend_sunny(ctx):
    """Thursday and Friday, when the weekend is close enough to plan."""
    if ctx.today.weekday() not in (3, 4) or not ctx.analysis.get("weekend_sunny"):
        return None
    return Signal("weekend_sunny", 55, {})


# -- nature, tied to what was measured

def _bees(ctx):
    """Late winter warmth: above about ten degrees, in sun, the bees fly."""
    high = ctx.weather.get("temp_max")
    if ctx.today.month not in (2, 3) or high is None or high < 10 \
            or (ctx.weather.get("sun_hours") or 0) < 3:
        return None
    return Signal("bees", 62, {"temp_high": f"{round(high)}°C"})


def _toads(ctx):
    """Mild, wet nights in early spring send the toads to their ponds."""
    low, wet = ctx.weather.get("temp_min"), ctx.weather.get("precip") or 0
    if ctx.today.month not in (2, 3, 4) or ctx.region != "lowland" \
            or low is None or low < 5 or wet < 1:
        return None
    return Signal("toads", 66, {})


def _pollen(ctx):
    """Kept rare on purpose - see POLLEN_EVERY_DAYS."""
    kind = POLLEN_BY_MONTH.get(ctx.today.month)
    if not kind or ctx.pollen.get(kind, 0) < POLLEN_NOTICEABLE:
        return None
    return Signal("pollen", 70, {}, pool=f"pollen.{kind}")


# -- customs, a local special for Zurich and Aargau

def _easter(year):
    """Easter Sunday (Gregorian), after Meeus/Jones/Butcher."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return date(year, month, day + 1)


def _nth_weekday(year, month, weekday, n):
    """The n-th given weekday (0=Monday) of a month."""
    first = date(year, month, 1)
    return first + timedelta(days=(weekday - first.weekday()) % 7 + 7 * (n - 1))


def _sechselaeuten(year):
    """
    Third Monday in April - moved a week later when that is Easter Monday,
    a week earlier when it falls in Holy Week. Checked against 2019 (8 Apr),
    2022 (25 Apr), 2024 (15 Apr) and 2025 (28 Apr).
    """
    day = _nth_weekday(year, 4, 0, 3)
    easter = _easter(year)
    if day == easter + timedelta(days=1):
        return day + timedelta(days=7)
    if easter - timedelta(days=7) < day < easter:
        return day - timedelta(days=7)
    return day


def _first_advent(year):
    """The fourth Sunday before Christmas."""
    christmas = date(year, 12, 25)
    fourth = christmas - timedelta(days=(christmas.weekday() + 1) % 7 or 7)
    return fourth - timedelta(days=21)


def _customs(year):
    """(pool, first day, last day, weight) - when each custom's lines hold."""
    sechselaeuten = _sechselaeuten(year)
    knabenschiessen = _nth_weekday(year, 9, 5, 2)      # second Saturday of September
    return [
        ("custom.sechselaeuten_soon", sechselaeuten - timedelta(days=7),
         sechselaeuten - timedelta(days=1), 80),
        ("custom.sechselaeuten", sechselaeuten, sechselaeuten, EVENT_WEIGHT),
        ("custom.knabenschiessen", knabenschiessen, knabenschiessen + timedelta(days=2),
         EVENT_WEIGHT),
        ("custom.samichlaus", date(year, 12, 6), date(year, 12, 6), EVENT_WEIGHT),
        ("custom.christmas_markets", _first_advent(year), date(year, 12, 23), 55),
    ]


def _custom(ctx):
    """Today's custom, if any - the strongest, where two overlap."""
    current = [c for c in _customs(ctx.today.year) if c[1] <= ctx.today <= c[2]]
    if not ctx.customs or not current:
        return None
    pool, _, last, weight = max(current, key=lambda c: c[3])
    days = (last - ctx.today).days + 1 if pool.endswith("_soon") else 0
    return Signal("custom", weight, _countdown("days_until", days, ctx.lang), pool=pool)


def _season(ctx):
    """Always matches - a line about the phase of the year."""
    return Signal("season", 30, {})


SIGNALS = (
    _turning_day,           # 95, event
    _equinox_day,           # 90, event
    _custom,                # 90 event / 80 soon / 55 season
    _first_sun,             # 88 / 70
    _evenings_turned,       # 85
    _sun_ahead,             # 85 / 60
    _solstice_countdown,    # 80
    _mornings_turned,       # 80 / 50
    _hour_mark,             # 80 / 60
    _snow,                  # 80 / 50
    _hochnebel,             # 78
    _sunny_today,           # 75 / 50
    _sunset_milestone,      # 75 / 55
    _warming,               # 55-85
    _since_solstice,        # 70
    _warmest_since,         # 70 / 55
    _pollen,                # 70, on rare days only
    _fog,                   # 70
    _frost_clear,           # 70
    _toads,                 # 66
    _equinox_countdown,     # 65
    _lichtmess,             # 65, low-key on purpose
    _sunrise_milestone,     # 65 / 45
    _sunny_streak,          # 65
    _bees,                  # 62
    _daily_gain,            # 60 / 45
    _autumn_twin,           # 60
    _uv_strength,           # 60
    _some_sun,              # 55
    _sunny_week,            # 55
    _weekend_sunny,         # 55
    _noon_sun,              # 50
    _dusk_light,            # 45
    _peak_light,            # 45
    _season,                # 30, always matches
)


def _signals(ctx):
    """Every signal that holds today, strongest first."""
    found = [s for s in (signal(ctx) for signal in SIGNALS) if s is not None]
    return sorted(found, key=lambda s: s.weight, reverse=True)


def _select(ctx, picker):
    """The day's event if there is one, otherwise a draw from the strongest few."""
    top = _signals(ctx)[:TOP_N]
    if top[0].weight >= EVENT_WEIGHT and picker.variant == 0:
        return top[0]
    return picker.rng().choices(top, weights=[s.weight for s in top])[0]


# ===== Text =====

# Leads that observe the sun without suggesting anything, so in winter the
# companion can be the one invitation: go out into it.
_SUNNY_LEADS = frozenset(["sunny_today", "frost_clear", "first_sun"])


def _conditions(weather):
    """Which of the nature lines' weather tags hold today."""
    if not weather:
        return set()
    sun, low, high = weather.get("sun_hours"), weather.get("temp_min"), weather.get("temp_max")
    checks = {
        "sunny": weather.get("is_sunny"),
        "grey": sun is not None and sun < 1,
        "wet": (weather.get("precip") or 0) >= 2,
        "frost": low is not None and low <= 0,
        "snow": weather.get("code") in SNOW_CODES or (weather.get("snow_cm") or 0) > 0,
        "warm": high is not None and high >= 15,
        "cold": high is not None and high <= 3,
    }
    return {name for name, holds in checks.items() if holds}


def _lead(ctx, signal, picker):
    name = f"phase.{ctx.phase}" if signal.key == "season" else (signal.pool or signal.key)
    pool = content.PHASES[ctx.phase] if signal.key == "season" else content.SIGNALS[name]
    template = picker.pick(_backed(_localized(pool, ctx.lang), signal.data), name)
    return template.format(**signal.data) if template else None


def _companion(ctx, lead, picker):
    """
    One line from nature, or a nudge outside when the winter sun is out.

    Nature lines carry weather tags; a tagged line is only offered when its
    weather holds, so frost is mentioned on frosty days and not on warm ones.
    """
    if ctx.is_cold and lead.key in _SUNNY_LEADS:
        return picker.pick(_localized(content.SUN_ENJOYMENT, ctx.lang), "sun_enjoyment")

    month = content.NATURE[ctx.region][ctx.today.month]
    holds = {"any"} | _conditions(ctx.weather)
    pool = [line for tag, lines in month.items() if tag in holds
            for line in _localized(lines, ctx.lang)]
    return picker.pick(pool, f"nature.{ctx.region}.{ctx.today.month}")


def _compose(ctx, picker):
    lead = _select(ctx, picker)
    text = _lead(ctx, lead, picker) or _lead(ctx, _season(ctx), picker)
    return f"{text} {_companion(ctx, lead, picker)}"


# ===== Facts =====

def _sky(weather):
    """
    Today's sky in one word, read from the measured sun like the message is.
    Codes only decide snow and fog; an "overcast" code with nine hours of
    sun is a sunny day here too.
    """
    if not weather:
        return None
    if weather.get("code") in SNOW_CODES or (weather.get("snow_cm") or 0) >= 1:
        return "snow"
    if weather.get("code") in FOG_CODES:
        return "fog"
    if weather.get("is_sunny"):
        return "sunny"
    if (weather.get("sun_hours") or 0) >= 1:
        return "mixed"
    return "rain" if (weather.get("precip") or 0) >= 1 else "grey"


def _format_facts(ctx):
    """
    The numbers shown beside the text. Unmeasured values read "--".

    The changes against yesterday, last week and the solstice are only shown
    while they are gains - in the returning light. The rest of the year they
    would mostly count losses, which is not what this app is for.
    """
    solar = ctx.solar
    temp = ctx.weather.get("temp_max")
    sun_hours = ctx.weather.get("sun_hours")

    def minutes(key):
        return int(solar[key] // 60)

    return {
        "sunrise": _clock(solar.get("sunrise")),
        "sunset": _clock(solar.get("sunset")),
        "day_length": format_duration(solar["day_len_sec"]) if solar else "--",
        "gains": ctx.phase == "returning_light",
        "delta_yesterday": f"{minutes('delta_daily_sec'):+d} min" if solar else "--",
        "delta_week": f"{minutes('delta_weekly_sec'):+d} min" if solar else "--",
        "delta_solstice": format_signed_span(minutes("delta_solstice_sec")) if solar else "--",
        "sky": _sky(ctx.weather),
        "sun_hours": round(sun_hours) if sun_hours is not None else None,
        "temp_max": f"{temp:.0f}°C" if temp is not None else "--",
    }


def generate_uplift_data(lat, lon, lang="en", variant=0):
    """Today's message and figures for one place."""
    if lang not in ("en", "de"):
        lang = "en"

    today = local_today()
    picker = Picker(f"{lat:.2f}:{lon:.2f}", today, variant)
    solar = get_daylight_delta(lat, lon, today)
    weather = fetch_daily_weather(lat, lon, days=7) or {}

    # Only asked for on the rare days pollen may be mentioned at all.
    pollen = {}
    if today.month in POLLEN_BY_MONTH and picker.every(POLLEN_EVERY_DAYS, "pollen"):
        pollen = fetch_pollen(lat, lon)

    ctx = _build_context(solar, weather, today, lang,
                         customs=_in_customs_area(lat, lon), pollen=pollen)
    return {
        "text": _compose(ctx, picker),
        "facts": _format_facts(ctx),
    }
