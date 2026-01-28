"""
Uplift Engine - Narrative-driven, scenario-based daylight messaging.
Analyzes 7-day forecast and solar data to identify the "hero" story.
"""

import random
import hashlib
import re
from datetime import date, datetime, timedelta
from services.solar_service import get_daylight_delta
from services.weather_service import fetch_daily_weather
from services import uplift_content as content


# ===== SCENARIO DETECTION =====

def detect_scenario(weather_data, solar_data, today):
    """
    Analyze weather and solar data to identify the primary narrative scenario.
    Returns a tuple: (scenario_key, scenario_data)
    """
    scenarios = []
    
    forecast = weather_data.get("forecast", [])
    analysis = weather_data.get("analysis", {})
    today_weather = weather_data.get("today", {})
    
    delta_daily = solar_data.get("delta_daily_sec", 0)
    delta_daily_min = abs(int(delta_daily // 60))
    delta_solstice = solar_data.get("delta_solstice_sec", 0)
    delta_solstice_min = int(delta_solstice // 60)
    day_len_sec = solar_data.get("day_len_sec", 0)
    
    hours = int(day_len_sec // 3600)
    mins = int((day_len_sec % 3600) // 60)
    day_length = f"{hours}h {mins}m"
    
    solstice_hours = abs(delta_solstice_min) // 60
    solstice_mins = abs(delta_solstice_min) % 60
    hours_gained = f"{solstice_hours}h {solstice_mins}m" if solstice_hours > 0 else f"{solstice_mins}m"
    
    # 1. Rain clearing soon (The Tunnel)
    if today_weather.get("is_bad", False) and analysis.get("next_good_day"):
        days_until = analysis.get("next_good_day_index", 0)
        if 1 <= days_until <= 4:
            scenarios.append((
                "rain_clearing_soon",
                {"clear_day": analysis["next_good_day"], "days_until": days_until},
                85 if days_until <= 2 else 70
            ))
    
    # 2. Carpe Diem
    if today_weather.get("is_good", False) and analysis.get("next_bad_day"):
        days_until = analysis.get("next_bad_day_index", 0)
        if 1 <= days_until <= 3:
            scenarios.append((
                "carpe_diem",
                {"rain_day": analysis["next_bad_day"], "days_until": days_until},
                90
            ))
    
    # 3. Warming trend
    if analysis.get("temp_trend") in ["warming", "warming_strong"]:
        temp_change = abs(analysis.get("temp_change", 0))
        weight = 75 if analysis["temp_trend"] == "warming_strong" else 55
        scenarios.append(("warming_trend", {"temp_change": f"+{temp_change:.0f}"}, weight))
    
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
    if today_weather.get("is_good", False) and not analysis.get("next_good_day"):
        scenarios.append(("breakthrough_day", {"bad_days": 3}, 70))
    
    # 9. Peak light
    if today.month in [6, 7] and day_len_sec > 50000:
        scenarios.append(("peak_light", {"day_length": day_length}, 65))
    
    # 10. Post-solstice grind
    if today.month in [1, 2] and delta_solstice_min > 10:
        scenarios.append(("post_solstice_grind", {"hours_gained": hours_gained}, 75))
    
    # 11. Weekend outlook
    if today.weekday() in [3, 4, 5]:
        weekend_outlook = analysis.get("weekend_outlook", "mixed")
        if weekend_outlook == "good":
            scenarios.append(("weekend_good", {}, 55))
        elif weekend_outlook == "bad":
            scenarios.append(("weekend_bad", {}, 45))
    
    # 12. Spring acceleration
    if today.month in [2, 3, 4] and delta_daily_min >= 2:
        scenarios.append(("spring_acceleration", {"delta_min": delta_daily_min}, 70))
    
    # 13. Solstice approaching
    days_to_summer = _days_to_date(today, date(today.year, 6, 21))
    days_to_winter = _days_to_date(today, date(today.year, 12, 21))
    
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
        {"day_length": day_length, "delta_min": delta_daily_min if delta_daily > 0 else abs(delta_daily_min)},
        30
    ))
    
    if not scenarios:
        return "stable_focus_light", {"day_length": day_length, "delta_min": 0}
    
    scenarios.sort(key=lambda x: x[2], reverse=True)
    top_scenarios = scenarios[:3]
    total_weight = sum(s[2] for s in top_scenarios)
    
    # More random seed for variety
    rng = random.Random(f"{today}|{len(forecast)}|{random.randint(0, 9999)}")
    roll = rng.random() * total_weight
    
    cumulative = 0
    for scenario_key, scenario_data, weight in top_scenarios:
        cumulative += weight
        if roll <= cumulative:
            return scenario_key, scenario_data
    
    return scenarios[0][0], scenarios[0][1]


def _days_to_date(from_date, to_date):
    """Calculate days until a target date, handling year wrapping."""
    if to_date < from_date:
        to_date = to_date.replace(year=from_date.year + 1)
    return (to_date - from_date).days


def _get_seasonal_phase(month, day):
    """Determine seasonal phase based on date."""
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


def _get_weather_category(code):
    """Convert weather code to category for nature observations."""
    if code in [0, 1]:
        return "clear"
    elif code in [71, 73, 75, 77, 85, 86]:
        return "snow"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]:
        return "rain"
    else:
        return "grey"


def _get_visit_hash(lat, lon):
    """Generate a hash that changes periodically for variety."""
    # Changes every ~6 hours for same location
    time_bucket = datetime.now().hour // 6
    key = f"{lat:.2f}|{lon:.2f}|{date.today()}|{time_bucket}"
    return int(hashlib.md5(key.encode()).hexdigest()[:8], 16)


def _extract_highlights(text, scenario_key, scenario_data, day_len_str, delta_d_min):
    """
    Extract 2-3 key phrases to highlight in the text.
    Returns list of phrases (max 6 words total across all highlights).
    """
    highlights = []
    
    # Priority 1: Key numbers/facts
    if day_len_str and day_len_str in text:
        highlights.append(day_len_str)
    
    # Priority 2: Scenario-specific highlights
    if scenario_key == "rain_clearing_soon" and scenario_data.get("clear_day"):
        day = scenario_data["clear_day"]
        if day in text:
            highlights.append(day)
    
    elif scenario_key == "carpe_diem" and scenario_data.get("rain_day"):
        day = scenario_data["rain_day"]
        if day in text:
            highlights.append(day)
    
    elif scenario_key == "light_fighter":
        delta = scenario_data.get("delta_min", 0)
        patterns = [f"+{delta} minutes", f"{delta} minutes", f"{delta} more minutes"]
        for p in patterns:
            if p in text:
                highlights.append(p)
                break
    
    elif scenario_key == "post_solstice_grind":
        gained = scenario_data.get("hours_gained", "")
        if gained and gained in text:
            highlights.append(gained)
    
    elif scenario_key == "warming_trend":
        change = scenario_data.get("temp_change", "")
        if change:
            patterns = [f"{change}°C", f"{change} °C"]
            for p in patterns:
                if p in text:
                    highlights.append(p)
                    break
    
    # Priority 3: Delta from yesterday
    if delta_d_min != 0 and len(highlights) < 2:
        patterns = [
            f"+{abs(delta_d_min)} minutes",
            f"{abs(delta_d_min)} minutes more",
            f"{abs(delta_d_min)} minutes less",
        ]
        for p in patterns:
            if p in text and p not in highlights:
                highlights.append(p)
                break
    
    # Priority 4: Key action words
    action_phrases = [
        "Get outside", "Make today count", "Plan accordingly",
        "the sun is back", "the light is gaining", "turning point"
    ]
    if len(highlights) < 2:
        for phrase in action_phrases:
            if phrase.lower() in text.lower() and len(highlights) < 3:
                # Find exact case in text
                match = re.search(re.escape(phrase), text, re.IGNORECASE)
                if match:
                    highlights.append(match.group(0))
                    break
    
    # Limit to 3 highlights max
    return highlights[:3]


def generate_uplift_data(lat, lon, city=None):
    """
    Generate narrative-driven uplift text based on location.
    Returns cohesive paragraph and factual data for UI.
    """
    solar = get_daylight_delta(lat, lon) or {}
    weather = fetch_daily_weather(lat, lon, days=7) or {}
    
    today = date.today()
    
    day_sec = solar.get("day_len_sec", 0)
    delta_daily = solar.get("delta_daily_sec", 0)
    delta_weekly = solar.get("delta_weekly_sec", 0)
    delta_solstice = solar.get("delta_solstice_sec", 0)
    sunrise = solar.get("sunrise")
    sunset = solar.get("sunset")
    
    hours = int(day_sec // 3600)
    mins = int((day_sec % 3600) // 60)
    day_len_str = f"{hours}h {mins}m"
    sunrise_str = sunrise.strftime("%H:%M") if sunrise else "--:--"
    sunset_str = sunset.strftime("%H:%M") if sunset else "--:--"
    
    delta_d_min = int(delta_daily // 60)
    delta_w_min = int(delta_weekly // 60)
    delta_s_min = int(delta_solstice // 60)
    
    today_weather = weather.get("today", {})
    weather_code = today_weather.get("code", 0)
    weather_cat = _get_weather_category(weather_code)
    
    temps = []
    if weather.get("forecast"):
        temps = [d.get("temp_max") for d in weather["forecast"] if d.get("temp_max") is not None]
    
    visit_hash = _get_visit_hash(lat, lon)
    random_factor = random.randint(0, 99999)
    seed = f"{today}|{lat:.2f}|{lon:.2f}|{weather_code}|{visit_hash}|{random_factor}"
    rng = random.Random(seed)
    
    scenario_key, scenario_data = detect_scenario(weather, solar, today)
    
    text_parts = []
    
    # 1. Primary scenario narrative
    narrative_templates = content.FORECAST_NARRATIVES.get(scenario_key, [])
    if narrative_templates:
        template = rng.choice(narrative_templates)
        try:
            narrative = template.format(**scenario_data)
        except KeyError:
            narrative = template
        text_parts.append(narrative)
    
    # 2. Daylight fact (high probability for grounding)
    if rng.random() > 0.3:  # 70% chance
        daylight_facts = [
            f"Today you have {day_len_str} of daylight, running from {sunrise_str} to {sunset_str}.",
            f"The day runs {day_len_str}, with sunrise at {sunrise_str} and sunset at {sunset_str}.",
            f"Daylight today: {day_len_str}. The sun is up from {sunrise_str} to {sunset_str}.",
            f"You're working with {day_len_str} of light today, {sunrise_str} to {sunset_str}.",
            f"Today's daylight window: {day_len_str}, from {sunrise_str} sunrise to {sunset_str} sunset.",
        ]
        text_parts.append(rng.choice(daylight_facts))
    
    # 3. Change from yesterday (if significant)
    if abs(delta_d_min) >= 1 and rng.random() > 0.4:  # 60% chance
        if delta_d_min > 0:
            delta_phrases = [
                f"That's {delta_d_min} minutes more than yesterday.",
                f"You gained {delta_d_min} minutes compared to yesterday.",
                f"+{delta_d_min} minutes versus yesterday.",
                f"The day is {delta_d_min} minutes longer than it was yesterday.",
            ]
        else:
            delta_phrases = [
                f"That's {abs(delta_d_min)} minutes less than yesterday.",
                f"You lost {abs(delta_d_min)} minutes compared to yesterday.",
                f"{delta_d_min} minutes versus yesterday.",
                f"The day is {abs(delta_d_min)} minutes shorter than yesterday.",
            ]
        text_parts.append(rng.choice(delta_phrases))
    
    # 4. Seasonal context (medium probability)
    if rng.random() > 0.5:  # 50% chance
        phase = _get_seasonal_phase(today.month, today.day)
        phase_texts = content.SEASONAL_PHASE.get(phase, [])
        if phase_texts:
            text_parts.append(rng.choice(phase_texts))
    
    # 5. Nature observation - HIGH PROBABILITY (this is what you wanted more of)
    if rng.random() > 0.2:  # 80% chance
        month_signs = content.NATURE_SIGNS.get(today.month, {})
        if isinstance(month_signs, dict):
            # Try weather-specific first
            weather_obs = month_signs.get(weather_cat, [])
            general_obs = month_signs.get("general", [])
            
            # Combine options
            all_obs = weather_obs + general_obs
            if all_obs:
                text_parts.append(rng.choice(all_obs))
        
        # Maybe add a second nature observation for more content
        if rng.random() > 0.6 and isinstance(month_signs, dict):  # 40% chance of second
            general_obs = month_signs.get("general", [])
            if general_obs:
                second_obs = rng.choice(general_obs)
                if second_obs not in text_parts:
                    text_parts.append(second_obs)
    
    # 6. General nature fact (lower probability, for variety)
    if rng.random() > 0.7:  # 30% chance
        text_parts.append(rng.choice(content.NATURE_FACTS_GENERAL))
    
    # 7. Closing (low probability)
    if rng.random() > 0.8:  # 20% chance
        closing_type = rng.choice(list(content.CLOSINGS.keys()))
        text_parts.append(rng.choice(content.CLOSINGS[closing_type]))
    
    # Ensure we have at least 3 parts for longer text
    if len(text_parts) < 3:
        # Add more content
        phase = _get_seasonal_phase(today.month, today.day)
        phase_texts = content.SEASONAL_PHASE.get(phase, [])
        if phase_texts and len(text_parts) < 3:
            addition = rng.choice(phase_texts)
            if addition not in text_parts:
                text_parts.append(addition)
        
        month_signs = content.NATURE_SIGNS.get(today.month, {})
        if isinstance(month_signs, dict) and len(text_parts) < 3:
            general_obs = month_signs.get("general", [])
            if general_obs:
                addition = rng.choice(general_obs)
                if addition not in text_parts:
                    text_parts.append(addition)
    
    # Limit to 5-6 parts for readability but aim for at least 4
    final_parts = text_parts[:6]
    text = " ".join(final_parts)
    
    while "  " in text:
        text = text.replace("  ", " ")
    
    # Extract highlights
    highlights = _extract_highlights(text, scenario_key, scenario_data, day_len_str, delta_d_min)
    
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
        "delta_yesterday": f"{delta_d_min:+d} min",
        "delta_week": f"{delta_w_min:+d} min",
        "delta_solstice": delta_s_str,
        "weather_code": weather_code,
        "temp_max": f"{temps[0]:.0f}°C" if temps else "--"
    }
    
    return {"text": text, "facts": facts, "highlights": highlights}