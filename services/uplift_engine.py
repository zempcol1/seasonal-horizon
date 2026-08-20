"""
Uplift Engine - Narrative-driven, scenario-based daylight messaging.
Supports multiple languages (en, de).
"""

import random
import hashlib
import re
from datetime import date, datetime
from services.solar_service import get_daylight_delta
from services.weather_service import classify, fetch_daily_weather
from services import uplift_content as content


# ===== HELPER: Get localized content =====

def _get_localized(data, lang, fallback="en"):
    """Get content for specific language with fallback."""
    if isinstance(data, dict):
        if lang in data:
            return data[lang]
        return data.get(fallback, [])
    return data  # Already a list


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


def _effective_month(month, lat):
    """
    Month translated to its northern-hemisphere equivalent.

    Everything seasonal below is written from a northern point of view, so for
    southern latitudes we shift half a year and reuse it. Deliberately crude:
    no equinox dates, just the six-month flip.
    """
    if lat < 0:
        return (month + 5) % 12 + 1
    return month


def _weekday_name(index, lang):
    """Localized weekday name for a 0=Monday index."""
    if index is None:
        return ""
    names = content.WEEKDAYS.get(lang) or content.WEEKDAYS["en"]
    return names[index]


def _get_localized_nested(data, key, lang, fallback="en"):
    """Get nested content by key and language."""
    if key not in data:
        return []
    return _get_localized(data[key], lang, fallback)


# ===== SCENARIO DETECTION =====

def detect_scenario(weather_data, solar_data, today, lang="en", lat=0.0):
    """
    Analyze weather and solar data to identify the primary narrative scenario.
    Returns a tuple: (scenario_key, scenario_data)
    """
    scenarios = []
    
    forecast = weather_data.get("forecast", [])
    analysis = weather_data.get("analysis", {})
    today_weather = weather_data.get("today", {})
    
    has_solar = bool(solar_data)

    delta_daily = solar_data.get("delta_daily_sec", 0)
    delta_daily_min = abs(int(delta_daily // 60))
    delta_solstice = solar_data.get("delta_solstice_sec", 0)
    delta_solstice_min = int(delta_solstice // 60)
    day_len_sec = solar_data.get("day_len_sec", 0)

    hours = int(day_len_sec // 3600)
    mins = int((day_len_sec % 3600) // 60)
    day_length = f"{hours}h {mins}m" if has_solar else None

    solstice_hours = abs(delta_solstice_min) // 60
    solstice_mins = abs(delta_solstice_min) % 60
    hours_gained = f"{solstice_hours}h {solstice_mins}m" if solstice_hours > 0 else f"{solstice_mins}m"
    if not has_solar:
        hours_gained = None

    # Seasonal tests below are written for the north; south gets the same
    # phases half a year offset.
    season_month = _effective_month(today.month, lat)

    # Warmer temps are extra motivating in winter/early spring
    is_cold_season = season_month in [11, 12, 1, 2, 3]
    
    # 1. Rain clearing soon
    if today_weather.get("is_bad", False) and analysis.get("next_good_weekday") is not None:
        days_until = analysis.get("next_good_in_days", 0)
        if 1 <= days_until <= 4:
            scenarios.append((
                "rain_clearing_soon",
                {"clear_day": _weekday_name(analysis["next_good_weekday"], lang),
                 "days_until": days_until},
                85 if days_until <= 2 else 70
            ))
    
    # 2. Carpe Diem
    if today_weather.get("is_good", False) and analysis.get("next_bad_weekday") is not None:
        days_until = analysis.get("next_bad_in_days", 0)
        if 1 <= days_until <= 3:
            scenarios.append((
                "carpe_diem",
                {"rain_day": _weekday_name(analysis["next_bad_weekday"], lang),
                 "days_until": days_until},
                90
            ))
    
    # 3. Warming trend - especially motivating in cold season
    if analysis.get("temp_trend") in ["warming", "warming_strong"]:
        temp_change = abs(analysis.get("temp_change", 0))
        base_weight = 75 if analysis["temp_trend"] == "warming_strong" else 55
        # Boost weight in winter/spring when warmth is extra welcome
        if is_cold_season:
            base_weight += 15
        scenarios.append(("warming_trend", {"temp_change": f"+{temp_change:.0f}"}, base_weight))
    
    # 4. Cooling trend
    if analysis.get("temp_trend") in ["cooling", "cooling_strong"]:
        temp_change = abs(analysis.get("temp_change", 0))
        weight = 65 if analysis["temp_trend"] == "cooling_strong" else 45
        scenarios.append(("cooling_trend", {"temp_change": f"{temp_change:.0f}"}, weight))
    
    # 5. Light Fighter
    if today_weather.get("is_bad", False) and delta_daily > 60:
        scenarios.append((
            "light_fighter",
            {"delta_min": delta_daily_min, "day_length": day_length},
            80
        ))
    
    # 6. Good streak
    good_streak = analysis.get("good_streak_length", 0)
    if good_streak >= 3:
        scenarios.append(("good_streak", {"streak_days": good_streak}, 60))
    
    # 7. Grey stretch
    bad_streak = analysis.get("bad_streak_length", 0)
    if bad_streak >= 3:
        scenarios.append(("grey_stretch", {"streak_days": bad_streak}, 50))
    
    # 8. Breakthrough day
    if today_weather.get("is_good", False) and analysis.get("next_good_weekday") is None:
        scenarios.append(("breakthrough_day", {}, 70))
    
    # 9. Peak light
    if season_month in [6, 7] and day_len_sec > 50000:
        scenarios.append(("peak_light", {"day_length": day_length}, 65))
    
    # 10. Post-solstice grind
    if season_month in [1, 2] and delta_solstice_min > 10:
        scenarios.append(("post_solstice_grind", {"hours_gained": hours_gained}, 75))
    
    # 11. Weekend outlook
    if today.weekday() in [3, 4, 5]:
        weekend_outlook = analysis.get("weekend_outlook", "mixed")
        if weekend_outlook == "good":
            scenarios.append(("weekend_good", {}, 55))
        elif weekend_outlook == "bad":
            scenarios.append(("weekend_bad", {}, 45))
    
    # 12. Spring acceleration
    if season_month in [2, 3, 4] and delta_daily_min >= 2:
        scenarios.append(("spring_acceleration", {"delta_min": delta_daily_min}, 70))
    
    # 13. Solstice approaching
    peak_month = 6 if lat >= 0 else 12
    dark_month = 12 if lat >= 0 else 6
    days_to_summer = _days_to_date(today, date(today.year, peak_month, 21))
    days_to_winter = _days_to_date(today, date(today.year, dark_month, 21))

    if 0 < days_to_summer <= 14:
        scenarios.append((
            "solstice_approaching",
            {"days_to_solstice": days_to_summer, "peak_or_min": "peak"},
            60
        ))
    elif 0 < days_to_winter <= 14:
        scenarios.append((
            "solstice_approaching",
            {"days_to_solstice": days_to_winter, "peak_or_min": "minimum"},
            60
        ))
    
    # 14. Default
    scenarios.append((
        "stable_focus_light",
        {"day_length": day_length,
         "delta_min": delta_daily_min if has_solar else None},
        30
    ))
    
    scenarios.sort(key=lambda x: x[2], reverse=True)
    top_scenarios = scenarios[:3]
    total_weight = sum(s[2] for s in top_scenarios)
    
    rng = random.Random(f"{today}|{len(forecast)}|{random.randint(0, 9999)}")
    roll = rng.random() * total_weight
    
    cumulative = 0
    chosen = scenarios[0]
    for scenario in top_scenarios:
        cumulative += scenario[2]
        if roll <= cumulative:
            chosen = scenario
            break

    key, data = chosen[0], chosen[1]
    return key, {k: v for k, v in data.items() if v is not None}


def _days_to_date(from_date, to_date):
    """Calculate days until a target date, handling year wrapping."""
    if to_date < from_date:
        to_date = to_date.replace(year=from_date.year + 1)
    return (to_date - from_date).days


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


def _get_visit_hash(lat, lon):
    """Generate a hash that changes periodically for variety."""
    time_bucket = datetime.now().hour // 6
    key = f"{lat:.2f}|{lon:.2f}|{date.today()}|{time_bucket}"
    return int(hashlib.md5(key.encode()).hexdigest()[:8], 16)


def generate_uplift_data(lat, lon, city=None, lang="en"):
    """
    Generate narrative-driven uplift text based on location and language.
    """
    # Validate language
    if lang not in ["en", "de"]:
        lang = "en"
    
    solar = get_daylight_delta(lat, lon) or {}
    weather = fetch_daily_weather(lat, lon, days=7) or {}
    
    today = date.today()
    
    day_sec = solar.get("day_len_sec", 0)
    delta_daily = solar.get("delta_daily_sec", 0)
    delta_weekly = solar.get("delta_weekly_sec", 0)
    delta_solstice = solar.get("delta_solstice_sec", 0)
    sunrise = solar.get("sunrise")
    sunset = solar.get("sunset")
    
    has_solar = bool(solar)
    season_month = _effective_month(today.month, lat)
    hours = int(day_sec // 3600)
    mins = int((day_sec % 3600) // 60)
    day_len_str = f"{hours}h {mins}m" if has_solar else "--"
    sunrise_str = sunrise.strftime("%H:%M") if sunrise else "--:--"
    sunset_str = sunset.strftime("%H:%M") if sunset else "--:--"
    
    delta_d_min = int(delta_daily // 60)
    delta_w_min = int(delta_weekly // 60)
    delta_s_min = int(delta_solstice // 60)
    
    has_weather = bool(weather)
    today_weather = weather.get("today", {})
    weather_code = today_weather.get("code", 0)
    weather_category = classify(weather_code) if has_weather else None
    analysis = weather.get("analysis", {})
    
    temps = []
    if weather.get("forecast"):
        temps = [d.get("temp_max") for d in weather["forecast"] if d.get("temp_max") is not None]
    
    visit_hash = _get_visit_hash(lat, lon)
    random_factor = random.randint(0, 99999)
    seed = f"{today}|{lat:.2f}|{lon:.2f}|{weather_code}|{visit_hash}|{random_factor}"
    rng = random.Random(seed)
    
    scenario_key, scenario_data = detect_scenario(weather, solar, today, lang, lat)
    
    text_parts = []
    used_topics = set()
    
    # 1. Primary scenario narrative (localized)
    narrative_templates = _get_localized_nested(content.FORECAST_NARRATIVES, scenario_key, lang)
    template = _pick_template(narrative_templates, scenario_data, rng)
    if template:
        text_parts.append(template.format(**scenario_data))
        
        if scenario_key in ["warming_trend", "cooling_trend"]:
            used_topics.add("temperature")
        if scenario_key in ["light_fighter", "spring_acceleration", "post_solstice_grind"]:
            used_topics.add("delta_daily")
        if scenario_key in ["peak_light", "stable_focus_light"]:
            used_topics.add("day_length")
    
    # 2. Daylight fact (localized) - skip if day_length already mentioned
    if has_solar and rng.random() > 0.3 and "day_length" not in used_topics:
        facts_data = {"day_length": day_len_str, "sunrise": sunrise_str,
                      "sunset": sunset_str}
        template = _pick_template(_get_localized(content.DAYLIGHT_FACTS, lang),
                                  facts_data, rng)
        if template:
            text_parts.append(template.format(**facts_data))
            used_topics.add("day_length")
    
    # 3. Change from yesterday (localized) - skip if delta already mentioned
    if has_solar and abs(delta_d_min) >= 1 and rng.random() > 0.4 \
            and "delta_daily" not in used_topics:
        if delta_d_min > 0:
            delta_templates = _get_localized(content.DELTA_PHRASES["gaining"], lang)
        else:
            delta_templates = _get_localized(content.DELTA_PHRASES["losing"], lang)
        
        delta_data = {"delta": abs(delta_d_min)}
        template = _pick_template(delta_templates, delta_data, rng)
        if template:
            text_parts.append(template.format(**delta_data))
            used_topics.add("delta_daily")
    
    # 4. Seasonal context (localized)
    if rng.random() > 0.5:
        phase = _get_seasonal_phase(today.month, today.day, lat)
        phase_texts = _get_localized_nested(content.SEASONAL_PHASE, phase, lang)
        if phase_texts:
            text_parts.append(rng.choice(phase_texts))
    
    # 5. Temperature outlook - add if warming and not already covered
    is_cold_season = season_month in [11, 12, 1, 2, 3]
    temp_trend = analysis.get("temp_trend", "stable")
    if is_cold_season and temp_trend in ["warming", "warming_strong"] and "temperature" not in used_topics:
        if rng.random() > 0.4:
            if scenario_key != "warming_trend":
                narrative_templates = _get_localized_nested(content.FORECAST_NARRATIVES, "warming_trend", lang)
                temp_change = abs(analysis.get("temp_change", 0))
                temp_data = {"temp_change": f"+{temp_change:.0f}"}
                template = _pick_template(narrative_templates, temp_data, rng)
                if template:
                    text_parts.append(template.format(**temp_data))
                    used_topics.add("temperature")
    
    # 6. Weather-dependent nature observation
    if rng.random() > 0.35:
        weather_nature = _get_localized(
            content.NATURE_WEATHER.get(weather_category, {}), lang) if has_weather else []
        month_signs = _get_localized(content.NATURE_SIGNS.get(season_month, {}), lang)
        observations = weather_nature or month_signs
        if observations:
            text_parts.append(rng.choice(observations))
    
    # Ensure minimum parts
    if len(text_parts) < 3:
        phase = _get_seasonal_phase(today.month, today.day, lat)
        phase_texts = _get_localized_nested(content.SEASONAL_PHASE, phase, lang)
        if phase_texts and len(text_parts) < 3:
            addition = rng.choice(phase_texts)
            if addition not in text_parts:
                text_parts.append(addition)
        
        month_signs = content.NATURE_SIGNS.get(season_month, {})
        nature_texts = _get_localized(month_signs, lang)
        if nature_texts and len(text_parts) < 3:
            addition = rng.choice(nature_texts)
            if addition not in text_parts:
                text_parts.append(addition)
    
    final_parts = text_parts[:6]
    text = " ".join(final_parts)
    
    while "  " in text:
        text = text.replace("  ", " ")
    
    # Format delta values
    if abs(delta_s_min) >= 60:
        s_hours = abs(delta_s_min) // 60
        s_mins = abs(delta_s_min) % 60
        sign = "+" if delta_s_min >= 0 else "-"
        delta_s_str = f"{sign}{s_hours}h {s_mins}m"
    else:
        delta_s_str = f"{delta_s_min:+d} min"
    
    facts = {
        "sunrise": sunrise_str,
        "sunset": sunset_str,
        "day_length": day_len_str,
        "delta_yesterday": f"{delta_d_min:+d} min" if has_solar else "--",
        "delta_week": f"{delta_w_min:+d} min" if has_solar else "--",
        "delta_solstice": delta_s_str if has_solar else "--",
        "weather_code": weather_code,
        "temp_max": f"{temps[0]:.0f}°C" if temps else "--"
    }
    
    # No more highlights
    return {"text": text, "facts": facts, "highlights": []}