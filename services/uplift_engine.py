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
- Shrinking daylight has no signal. It is true, but it is not what this app
  is for.
- Nothing is stated that was not measured. Templates declare the facts they
  need through their placeholders, and _pick_template only offers ones whose
  every placeholder is backed.
- The message stays the same all day for one place: the date and location
  seed the choices. `variant` asks for another one.
"""

import random
import re
from dataclasses import dataclass
from datetime import date

from config import today as local_today
from services.solar_service import get_daylight_delta
from services.weather_service import FOG_CODES, SNOW_CODES, fetch_daily_weather
from services import uplift_content as content

# Above this the spring signs come late and snow plays a bigger part, so the
# mountains get their own nature content.
ALPINE_ELEVATION_M = 800

COLD_PHASES = frozenset(["darkening", "returning_light"])

TOP_N = 3  # how many of the strongest signals enter the weighted draw


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


def _when(days, lang):
    """"tomorrow" or "in 3 days"."""
    if lang == "de":
        return "morgen" if days == 1 else f"in {days} Tagen"
    return "tomorrow" if days == 1 else f"in {days} days"


def _weekday_name(index, lang):
    """Localized weekday name for a 0=Monday index."""
    return (content.WEEKDAYS.get(lang) or content.WEEKDAYS["en"])[index]


def _localized(data, lang):
    """The entry for this language, falling back to English."""
    return data.get(lang) or data.get("en") or []


_PLACEHOLDER = re.compile(r"\{(\w+)")


def _pick_template(templates, data, rng):
    """
    Choose a template whose every placeholder is backed by real data.

    Templates asking for a fact we could not measure are dropped rather than
    rendered, so the app never shows an unbacked claim or a raw "{placeholder}".
    Returns None when nothing qualifies, which means: say nothing here.
    """
    usable = [t for t in templates
              if all(k in data for k in _PLACEHOLDER.findall(t))]
    return rng.choice(usable) if usable else None


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
    analysis: dict      # what stands out in the week ahead

    @property
    def is_cold(self):
        return self.phase in COLD_PHASES


def _build_context(solar, weather, today, lang):
    return Context(
        today=today,
        lang=lang,
        region=_region(weather.get("elevation")),
        phase=_phase(today),
        solar=solar,
        weather=weather.get("today", {}),
        analysis=weather.get("analysis", {}),
    )


# ===== Signals =====

@dataclass(frozen=True)
class Signal:
    key: str
    weight: int
    data: dict


# -- light: calculated, so always there unless the sun never rises

def _turning_day(ctx):
    """The winter solstice itself."""
    if (ctx.today.month, ctx.today.day) != (12, 21):
        return None
    return Signal("turning_day", 95, {})


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


def _since_solstice(ctx):
    minutes = int(ctx.solar.get("delta_solstice_sec", 0) // 60)
    if ctx.phase != "returning_light" or minutes < 1:
        return None
    return Signal("since_solstice", 70, {"hours_gained": format_span(minutes)})


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
    })


def _sunset_milestone(ctx):
    """The next half hour the sunset crosses - exact, since it is calculated."""
    milestone = ctx.solar.get("sunset_milestone")
    if ctx.phase not in ("returning_light", "spring") or not milestone:
        return None
    days = milestone["days"]
    return Signal("sunset_milestone", 75 if ctx.phase == "returning_light" else 55, {
        "milestone_time": milestone["time"],
        "milestone_days": days,
        **_counted(days, "days", "days_dat", lang=ctx.lang),
        "sunset": _clock(ctx.solar["sunset"]),
    })


def _noon_sun(ctx):
    """The sun climbing higher at midday - it gets stronger, not just longer."""
    gain = ctx.solar.get("noon_gain_deg", 0)
    if ctx.phase != "returning_light" or gain < 2:
        return None
    return Signal("noon_sun", 50, {"noon_gain": round(gain)})


def _peak_light(ctx):
    if ctx.phase != "summer" or ctx.today.month not in (6, 7) or not ctx.solar:
        return None
    return Signal("peak_light", 45, {
        "day_length": format_duration(ctx.solar["day_len_sec"]),
        "sunset": _clock(ctx.solar["sunset"]),
    })


# -- weather: from the forecast, so absent without one

def _sun_ahead(ctx):
    """Not much sun today, but a sunny day within the next four."""
    days = ctx.analysis.get("next_sunny_in_days")
    if days is None or days > 4:
        return None
    hours = max(1, round(ctx.analysis["next_sunny_hours"]))
    return Signal("sun_ahead", 85 if ctx.is_cold else 60, {
        "sunny_day": _weekday_name(ctx.analysis["next_sunny_weekday"], ctx.lang),
        "when": _when(days, ctx.lang),
        "sun_hours": hours,
        **_counted(hours, "hours", lang=ctx.lang),
    })


def _sunny_today(ctx):
    if not ctx.weather.get("is_sunny"):
        return None
    hours = max(1, round(ctx.weather["sun_hours"]))
    return Signal("sunny_today", 75 if ctx.is_cold else 50, {
        "sun_hours": hours, **_counted(hours, "hours", lang=ctx.lang),
    })


def _some_sun(ctx):
    """A dull winter day that still has an hour or two of sun in it."""
    hours = ctx.weather.get("sun_hours")
    if not ctx.is_cold or ctx.weather.get("is_sunny") or hours is None or hours < 1:
        return None
    hours = round(hours)
    return Signal("some_sun", 55, {
        "sun_hours": hours, **_counted(hours, "hours", lang=ctx.lang),
    })


def _snow(ctx):
    if ctx.weather.get("code") not in SNOW_CODES:
        return None
    return Signal("snow", 80 if ctx.is_cold else 50, {})


def _fog(ctx):
    if ctx.weather.get("code") not in FOG_CODES:
        return None
    return Signal("fog", 70, {})


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


def _weekend_sunny(ctx):
    """Thursday and Friday, when the weekend is close enough to plan."""
    if ctx.today.weekday() not in (3, 4) or not ctx.analysis.get("weekend_sunny"):
        return None
    return Signal("weekend_sunny", 55, {})


def _season(ctx):
    """Always matches - a line about the phase of the year."""
    return Signal("season", 30, {})


SIGNALS = (
    _turning_day,           # 95
    _evenings_turned,       # 85
    _sun_ahead,             # 85 / 60
    _solstice_countdown,    # 80
    _mornings_turned,       # 80 / 50
    _snow,                  # 80 / 50
    _sunny_today,           # 75 / 50
    _sunset_milestone,      # 75 / 55
    _warming,               # 55-85
    _since_solstice,        # 70
    _fog,                   # 70
    _frost_clear,           # 70
    _sunny_streak,          # 65
    _daily_gain,            # 60 / 45
    _some_sun,              # 55
    _weekend_sunny,         # 55
    _noon_sun,              # 50
    _peak_light,            # 45
    _season,                # 30, always matches
)


def _signals(ctx):
    """Every signal that holds today, strongest first."""
    found = [s for s in (signal(ctx) for signal in SIGNALS) if s is not None]
    return sorted(found, key=lambda s: s.weight, reverse=True)


def _select(ctx, rng):
    """Draw the lead from the strongest few, by weight."""
    top = _signals(ctx)[:TOP_N]
    return rng.choices(top, weights=[s.weight for s in top])[0]


# ===== Text =====

# Leads that observe the sun without suggesting anything, so in winter the
# companion can be the one invitation: go out into it.
_SUNNY_LEADS = frozenset(["sunny_today", "frost_clear"])


def _lead(ctx, signal, rng):
    pool = content.PHASES[ctx.phase] if signal.key == "season" else content.SIGNALS[signal.key]
    template = _pick_template(_localized(pool, ctx.lang), signal.data, rng)
    return template.format(**signal.data) if template else None


def _companion_pool(ctx, lead):
    """Nature lines, or nudges outside when the winter sun is out."""
    if ctx.is_cold and lead.key in _SUNNY_LEADS:
        return _localized(content.SUN_ENJOYMENT, ctx.lang)
    spring = _localized(content.SPRING_SIGNS[ctx.region], ctx.lang)
    return spring.get(ctx.today.month) or \
        _localized(content.NATURE_SIGNS[ctx.today.month], ctx.lang)


def _compose(ctx, seed, variant):
    """
    Lead plus companion. `seed` fixes the day's choices for one place.

    The lead is drawn afresh for each variant, but the companion steps
    through its pool from a fixed start, so asking for another message
    always changes something - with few signals the draw alone often
    landed on the same text again.
    """
    rng = random.Random(f"{seed}:{variant}")
    lead = _select(ctx, rng)
    text = _lead(ctx, lead, rng) or _lead(ctx, _season(ctx), rng)

    pool = _companion_pool(ctx, lead)
    start = random.Random(seed).randrange(len(pool))
    return f"{text} {pool[(start + variant) % len(pool)]}"


# ===== Facts =====

def _format_facts(ctx):
    """The numbers shown beside the text. Unmeasured values read "--"."""
    solar = ctx.solar
    temp = ctx.weather.get("temp_max")

    def minutes(key):
        return int(solar[key] // 60)

    return {
        "sunrise": _clock(solar.get("sunrise")),
        "sunset": _clock(solar.get("sunset")),
        "day_length": format_duration(solar["day_len_sec"]) if solar else "--",
        "delta_yesterday": f"{minutes('delta_daily_sec'):+d} min" if solar else "--",
        "delta_week": f"{minutes('delta_weekly_sec'):+d} min" if solar else "--",
        "delta_solstice": format_signed_span(minutes("delta_solstice_sec")) if solar else "--",
        "weather_code": ctx.weather.get("code") or 0,
        "temp_max": f"{temp:.0f}°C" if temp is not None else "--",
    }


def generate_uplift_data(lat, lon, lang="en", variant=0):
    """Today's message and figures for one place."""
    if lang not in ("en", "de"):
        lang = "en"

    today = local_today()
    solar = get_daylight_delta(lat, lon, today)
    weather = fetch_daily_weather(lat, lon, days=7) or {}

    ctx = _build_context(solar, weather, today, lang)
    return {
        "text": _compose(ctx, f"{today}:{lat:.2f}:{lon:.2f}", variant),
        "facts": _format_facts(ctx),
    }
