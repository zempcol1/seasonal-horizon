"""
Uplift Engine - Narrative-driven, scenario-based daylight messaging.
Supports multiple languages (en, de).

Two things are worth knowing before reading on:

- Scenarios live in RULES as one function each, returning a Scenario with its
  weight or None. The weights sit next to the condition that earns them, so
  they can be compared and tuned without reading the whole file.
- Nothing is stated that was not measured. Templates declare the facts they
  need through their own placeholders, and _pick_template only offers ones
  whose every placeholder is backed. A fact we could not fetch is absent from
  the data dict, which silently removes every template that depended on it.
"""

import random
import re
from dataclasses import dataclass
from datetime import date

from services.solar_service import get_daylight_delta
from services.weather_service import classify, fetch_daily_weather
from services import uplift_content as content

COLD_MONTHS = frozenset([11, 12, 1, 2, 3])


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


# ===== Localized content =====

def _get_localized(data, lang, fallback="en"):
    """Get content for specific language with fallback."""
    if isinstance(data, dict):
        if lang in data:
            return data[lang]
        return data.get(fallback, [])
    return data  # Already a list


def _get_localized_nested(data, key, lang, fallback="en"):
    """Get nested content by key and language."""
    if key not in data:
        return []
    return _get_localized(data[key], lang, fallback)


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


def _weekday_name(index, lang):
    """Localized weekday name for a 0=Monday index."""
    if index is None:
        return ""
    names = content.WEEKDAYS.get(lang) or content.WEEKDAYS["en"]
    return names[index]


# ===== Season =====

def _effective_month(month, lat):
    """
    Month translated to its northern-hemisphere equivalent.

    Everything seasonal here is written from a northern point of view, so for
    southern latitudes we shift half a year and reuse it. Deliberately crude:
    no equinox dates, just the six-month flip.
    """
    if lat < 0:
        return (month + 5) % 12 + 1
    return month


def _get_seasonal_phase(month, day, lat=0.0):
    """Determine seasonal phase based on date and hemisphere."""
    month = _effective_month(month, lat)
    if (month == 12 and day >= 21) or month == 1:
        return "deep_winter"
    elif month == 2 or (month == 3 and day < 20):
        return "late_winter"
    elif (month == 3 and day >= 20) or month == 4:
        return "early_spring"
    elif month == 5 or (month == 6 and day < 21):
        return "late_spring"
    elif (month == 6 and day >= 21) or month == 7:
        return "peak_summer"
    elif month == 8 or (month == 9 and day < 22):
        return "late_summer"
    elif (month == 9 and day >= 22) or month == 10:
        return "early_autumn"
    else:
        return "late_autumn"


def _days_to_date(from_date, to_date):
    """Calculate days until a target date, handling year wrapping."""
    if to_date < from_date:
        to_date = to_date.replace(year=from_date.year + 1)
    return (to_date - from_date).days


# ===== Context =====

@dataclass(frozen=True)
class Context:
    """
    Everything derived once from a solar + weather fetch.

    Values that could not be measured are None rather than zero, so a template
    depending on them is dropped instead of stating a confident nothing.
    """
    today: date
    lat: float
    lang: str

    has_solar: bool
    day_len_sec: int
    delta_daily_sec: int
    delta_daily_min: int        # absolute
    delta_weekly_min: int
    delta_solstice_min: int
    day_length: str
    hours_gained: str
    sunrise: str
    sunset: str

    has_weather: bool
    weather_code: int
    weather_category: str
    today_weather: dict
    analysis: dict
    temps: list

    season_month: int
    is_cold_season: bool


def _build_context(solar, weather, today, lang, lat):
    """Derive every value the rules and the composer need, exactly once."""
    has_solar = bool(solar)
    has_weather = bool(weather)

    day_len_sec = solar.get("day_len_sec", 0)
    delta_daily_sec = solar.get("delta_daily_sec", 0)
    delta_solstice_min = int(solar.get("delta_solstice_sec", 0) // 60)
    sunrise = solar.get("sunrise")
    sunset = solar.get("sunset")

    weather_code = weather.get("today", {}).get("code", 0)
    forecast = weather.get("forecast") or []
    season_month = _effective_month(today.month, lat)

    return Context(
        today=today,
        lat=lat,
        lang=lang,
        has_solar=has_solar,
        day_len_sec=day_len_sec,
        delta_daily_sec=delta_daily_sec,
        delta_daily_min=abs(int(delta_daily_sec // 60)),
        delta_weekly_min=int(solar.get("delta_weekly_sec", 0) // 60),
        delta_solstice_min=delta_solstice_min,
        day_length=format_duration(day_len_sec) if has_solar else None,
        hours_gained=format_span(delta_solstice_min) if has_solar else None,
        sunrise=sunrise.strftime("%H:%M") if sunrise else "--:--",
        sunset=sunset.strftime("%H:%M") if sunset else "--:--",
        has_weather=has_weather,
        weather_code=weather_code,
        # Without a forecast the code defaults to 0, which reads as "clear" -
        # so the category has to stay unknown rather than promise blue sky.
        weather_category=classify(weather_code) if has_weather else None,
        today_weather=weather.get("today", {}),
        analysis=weather.get("analysis", {}),
        temps=[d.get("temp_max") for d in forecast if d.get("temp_max") is not None],
        season_month=season_month,
        is_cold_season=season_month in COLD_MONTHS,
    )


# ===== Scenario rules =====

@dataclass(frozen=True)
class Scenario:
    key: str
    data: dict
    weight: int


def _carpe_diem(ctx):
    """Good today, rain coming - go outside while it lasts."""
    if not ctx.today_weather.get("is_good") or ctx.analysis.get("next_bad_weekday") is None:
        return None
    days = ctx.analysis.get("next_bad_in_days", 0)
    if not 1 <= days <= 3:
        return None
    return Scenario("carpe_diem", {
        "rain_day": _weekday_name(ctx.analysis["next_bad_weekday"], ctx.lang),
        "days_until": days,
    }, 90)


def _rain_clearing_soon(ctx):
    """Grey today, but a better day is already in the forecast."""
    if not ctx.today_weather.get("is_bad") or ctx.analysis.get("next_good_weekday") is None:
        return None
    days = ctx.analysis.get("next_good_in_days", 0)
    if not 1 <= days <= 4:
        return None
    return Scenario("rain_clearing_soon", {
        "clear_day": _weekday_name(ctx.analysis["next_good_weekday"], ctx.lang),
        "days_until": days,
    }, 85 if days <= 2 else 70)


def _light_fighter(ctx):
    """Grey outside, yet the day is measurably longer than yesterday."""
    if not ctx.today_weather.get("is_bad") or ctx.delta_daily_sec <= 60:
        return None
    return Scenario("light_fighter", {
        "delta_min": ctx.delta_daily_min,
        "day_length": ctx.day_length,
    }, 80)


def _post_solstice_grind(ctx):
    """January/February: the gain is real but still feels slow."""
    if ctx.season_month not in (1, 2) or ctx.delta_solstice_min <= 10:
        return None
    return Scenario("post_solstice_grind", {"hours_gained": ctx.hours_gained}, 75)


def _warming_trend(ctx):
    """Temperatures climbing - worth more in the cold half of the year."""
    trend = ctx.analysis.get("temp_trend")
    if trend not in ("warming", "warming_strong"):
        return None
    weight = 75 if trend == "warming_strong" else 55
    if ctx.is_cold_season:
        weight += 15
    change = abs(ctx.analysis.get("temp_change", 0))
    return Scenario("warming_trend", {"temp_change": f"+{change:.0f}"}, weight)


def _spring_acceleration(ctx):
    """Late winter into spring, gaining two minutes a day or more."""
    if ctx.season_month not in (2, 3, 4) or ctx.delta_daily_min < 2:
        return None
    return Scenario("spring_acceleration", {"delta_min": ctx.delta_daily_min}, 70)


def _breakthrough_day(ctx):
    """
    Clear today with no other good day in the forecast.

    Deliberately carries no data: the forecast starts today, so how long the
    preceding grey stretch ran is not knowable from here.
    """
    if not ctx.today_weather.get("is_good") or ctx.analysis.get("next_good_weekday") is not None:
        return None
    return Scenario("breakthrough_day", {}, 70)


def _peak_light(ctx):
    """High summer, past about fourteen hours of daylight."""
    if ctx.season_month not in (6, 7) or ctx.day_len_sec <= 50000:
        return None
    return Scenario("peak_light", {"day_length": ctx.day_length}, 65)


def _cooling_trend(ctx):
    trend = ctx.analysis.get("temp_trend")
    if trend not in ("cooling", "cooling_strong"):
        return None
    change = abs(ctx.analysis.get("temp_change", 0))
    return Scenario("cooling_trend", {"temp_change": f"{change:.0f}"},
                    65 if trend == "cooling_strong" else 45)


def _good_streak(ctx):
    streak = ctx.analysis.get("good_streak_length", 0)
    if streak < 3:
        return None
    return Scenario("good_streak", {"streak_days": streak}, 60)


def _solstice_approaching(ctx):
    """Within a fortnight of either solstice; they swap below the equator."""
    peak_month, dark_month = (6, 12) if ctx.lat >= 0 else (12, 6)
    to_peak = _days_to_date(ctx.today, date(ctx.today.year, peak_month, 21))
    to_dark = _days_to_date(ctx.today, date(ctx.today.year, dark_month, 21))

    if 0 < to_peak <= 14:
        days, which = to_peak, "peak"
    elif 0 < to_dark <= 14:
        days, which = to_dark, "minimum"
    else:
        return None
    return Scenario("solstice_approaching",
                    {"days_to_solstice": days, "peak_or_min": which}, 60)


def _weekend_outlook(ctx):
    """Thursday to Saturday, when the weekend forecast starts to matter."""
    if ctx.today.weekday() not in (3, 4, 5):
        return None
    outlook = ctx.analysis.get("weekend_outlook", "mixed")
    if outlook == "good":
        return Scenario("weekend_good", {}, 55)
    if outlook == "bad":
        return Scenario("weekend_bad", {}, 45)
    return None


def _grey_stretch(ctx):
    streak = ctx.analysis.get("bad_streak_length", 0)
    if streak < 3:
        return None
    return Scenario("grey_stretch", {"streak_days": streak}, 50)


def _stable_focus_light(ctx):
    """Always matches - the fallback when nothing else stands out."""
    return Scenario("stable_focus_light", {
        "day_length": ctx.day_length,
        "delta_min": ctx.delta_daily_min if ctx.has_solar else None,
    }, 30)


RULES = (
    _carpe_diem,            # 90
    _rain_clearing_soon,    # 85 / 70
    _light_fighter,         # 80
    _post_solstice_grind,   # 75
    _warming_trend,         # 55-90
    _spring_acceleration,   # 70
    _breakthrough_day,      # 70
    _peak_light,            # 65
    _cooling_trend,         # 45 / 65
    _good_streak,           # 60
    _solstice_approaching,  # 60
    _weekend_outlook,       # 55 / 45
    _grey_stretch,          # 50
    _stable_focus_light,    # 30, always matches
)

TOP_N = 3  # how many of the strongest scenarios enter the weighted draw


def _select_scenario(ctx, rng):
    """Score every rule, then draw from the strongest few by weight."""
    matches = [s for s in (rule(ctx) for rule in RULES) if s is not None]
    matches.sort(key=lambda s: s.weight, reverse=True)

    top = matches[:TOP_N]
    roll = rng.random() * sum(s.weight for s in top)

    chosen, cumulative = top[0], 0
    for scenario in top:
        cumulative += scenario.weight
        if roll <= cumulative:
            chosen = scenario
            break

    # Unmeasured values drop out here, taking their templates with them.
    return chosen.key, {k: v for k, v in chosen.data.items() if v is not None}


def detect_scenario(weather_data, solar_data, today, lang="en", lat=0.0):
    """
    Analyze weather and solar data to identify the primary narrative scenario.
    Returns a tuple: (scenario_key, scenario_data)
    """
    ctx = _build_context(solar_data, weather_data, today, lang, lat)
    return _select_scenario(ctx, random.Random())


# ===== Text composition =====

# Topics a scenario already covers, so a later segment does not repeat it.
_SCENARIO_TOPICS = {
    "warming_trend": "temperature",
    "cooling_trend": "temperature",
    "light_fighter": "delta_daily",
    "spring_acceleration": "delta_daily",
    "post_solstice_grind": "delta_daily",
    "peak_light": "day_length",
    "stable_focus_light": "day_length",
}

MAX_PARTS = 6
MIN_PARTS = 3


def _seasonal_texts(ctx):
    phase = _get_seasonal_phase(ctx.today.month, ctx.today.day, ctx.lat)
    return _get_localized_nested(content.SEASONAL_PHASE, phase, ctx.lang)


def _month_texts(ctx):
    return _get_localized(content.NATURE_SIGNS.get(ctx.season_month, {}), ctx.lang)


def _weather_texts(ctx):
    if not ctx.has_weather:
        return []
    return _get_localized(content.NATURE_WEATHER.get(ctx.weather_category, {}), ctx.lang)


def _compose_text(ctx, scenario_key, scenario_data, rng):
    """Assemble the message from the scenario plus optional extra segments."""
    parts = []
    used = set()

    # 1. The scenario narrative itself.
    templates = _get_localized_nested(content.FORECAST_NARRATIVES, scenario_key, ctx.lang)
    template = _pick_template(templates, scenario_data, rng)
    if template:
        parts.append(template.format(**scenario_data))
        topic = _SCENARIO_TOPICS.get(scenario_key)
        if topic:
            used.add(topic)

    # 2. Sunrise/sunset/day length, unless the scenario covered it already.
    if ctx.has_solar and rng.random() > 0.3 and "day_length" not in used:
        data = {"day_length": ctx.day_length, "sunrise": ctx.sunrise, "sunset": ctx.sunset}
        template = _pick_template(_get_localized(content.DAYLIGHT_FACTS, ctx.lang), data, rng)
        if template:
            parts.append(template.format(**data))
            used.add("day_length")

    # 3. Change against yesterday.
    delta_min = int(ctx.delta_daily_sec // 60)
    if ctx.has_solar and abs(delta_min) >= 1 and rng.random() > 0.4 \
            and "delta_daily" not in used:
        pool = content.DELTA_PHRASES["gaining" if delta_min > 0 else "losing"]
        data = {"delta": abs(delta_min)}
        template = _pick_template(_get_localized(pool, ctx.lang), data, rng)
        if template:
            parts.append(template.format(**data))
            used.add("delta_daily")

    # 4. Where we are in the year.
    if rng.random() > 0.5:
        phase_texts = _seasonal_texts(ctx)
        if phase_texts:
            parts.append(rng.choice(phase_texts))

    # 5. Warmth ahead earns its own line in the cold months.
    if ctx.is_cold_season and "temperature" not in used \
            and ctx.analysis.get("temp_trend") in ("warming", "warming_strong") \
            and scenario_key != "warming_trend" and rng.random() > 0.4:
        data = {"temp_change": f"+{abs(ctx.analysis.get('temp_change', 0)):.0f}"}
        templates = _get_localized_nested(content.FORECAST_NARRATIVES, "warming_trend", ctx.lang)
        template = _pick_template(templates, data, rng)
        if template:
            parts.append(template.format(**data))
            used.add("temperature")

    # 6. A nature observation: tied to the weather when we have it, otherwise
    #    to the month. Selected on what exists, not on a second dice roll.
    if rng.random() > 0.35:
        observations = _weather_texts(ctx) or _month_texts(ctx)
        if observations:
            parts.append(rng.choice(observations))

    # Very short messages read as broken, so top up from the date-derived
    # pools - those hold regardless of what the APIs returned.
    for pool in (_seasonal_texts(ctx), _month_texts(ctx)):
        if len(parts) >= MIN_PARTS:
            break
        if pool:
            addition = rng.choice(pool)
            if addition not in parts:
                parts.append(addition)

    text = " ".join(parts[:MAX_PARTS])
    while "  " in text:
        text = text.replace("  ", " ")
    return text


# ===== Facts =====

def _format_facts(ctx):
    """The numbers shown beside the text. Unmeasured values read "--"."""
    return {
        "sunrise": ctx.sunrise,
        "sunset": ctx.sunset,
        "day_length": ctx.day_length if ctx.has_solar else "--",
        "delta_yesterday": f"{int(ctx.delta_daily_sec // 60):+d} min" if ctx.has_solar else "--",
        "delta_week": f"{ctx.delta_weekly_min:+d} min" if ctx.has_solar else "--",
        "delta_solstice": format_signed_span(ctx.delta_solstice_min) if ctx.has_solar else "--",
        "weather_code": ctx.weather_code,
        "temp_max": f"{ctx.temps[0]:.0f}°C" if ctx.temps else "--",
    }


def generate_uplift_data(lat, lon, lang="en"):
    """Generate narrative-driven uplift text based on location and language."""
    if lang not in ("en", "de"):
        lang = "en"

    solar = get_daylight_delta(lat, lon) or {}
    weather = fetch_daily_weather(lat, lon, days=7) or {}

    ctx = _build_context(solar, weather, date.today(), lang, lat)
    rng = random.Random()

    scenario_key, scenario_data = _select_scenario(ctx, rng)
    return {
        "text": _compose_text(ctx, scenario_key, scenario_data, rng),
        "facts": _format_facts(ctx),
    }
