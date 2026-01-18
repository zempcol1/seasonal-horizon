import random
from datetime import date, datetime
from services.solar_service import get_daylight_delta
from services.weather_service import fetch_daily_weather
from services import uplift_content as content

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

def _get_trend_phrases(delta_min):
    """Get appropriate trend phrases based on daily change."""
    if delta_min >= 2:
        return content.TREND_STRONG_GAIN
    elif delta_min >= 1:
        return content.TREND_MODERATE_GAIN
    elif delta_min > 0:
        return content.TREND_SLOW_GAIN
    elif delta_min == 0:
        return content.TREND_STABLE
    elif delta_min > -1:
        return content.TREND_SLOW_LOSS
    elif delta_min > -2:
        return content.TREND_MODERATE_LOSS
    else:
        return content.TREND_STRONG_LOSS

def _get_weather_category(code):
    """Convert weather code to category."""
    if code in [0, 1]:
        return "clear"
    elif code in [2, 3, 45, 48]:
        return "cloudy"
    elif code in [71, 73, 75, 77, 85, 86]:
        return "snow"
    else:
        return "rain"

def _get_sunrise_category(hour):
    """Categorize sunrise time."""
    if hour < 5:
        return "very_early"
    elif hour < 6:
        return "early"
    elif hour < 7:
        return "moderate"
    elif hour < 8:
        return "late"
    else:
        return "very_late"

def _get_sunset_category(hour, minute):
    """Categorize sunset time."""
    decimal_hour = hour + minute / 60
    if decimal_hour < 16.5:
        return "very_early"
    elif decimal_hour < 17.5:
        return "early"
    elif decimal_hour < 19:
        return "moderate"
    elif decimal_hour < 20.5:
        return "late"
    else:
        return "very_late"

def _get_solstice_category(delta_s_min, month, day):
    """Categorize progress relative to winter solstice."""
    hours = abs(delta_s_min) / 60
    
    # Check if we're past summer solstice (losing light but still ahead of winter)
    if month > 6 or (month == 6 and day > 21):
        if month < 12 or (month == 12 and day < 21):
            return "past_peak", hours
    
    # Winter solstice region
    if month == 12 and day >= 21:
        return "just_past_winter", hours
    if month == 1 and day <= 10:
        return "just_past_winter", hours
    
    # Recovery phases
    if hours < 0.5:
        return "early_recovery", hours
    elif hours < 1.5:
        return "early_recovery", hours
    elif hours < 3:
        return "mid_recovery", hours
    elif hours < 5:
        return "strong_recovery", hours
    else:
        return "near_peak", hours

def _get_weather_outlook(weather_data):
    """Analyze weather trend for the week."""
    if not weather_data:
        return "stable"
    
    temp_trend = weather_data.get("week_temp_trend", "stable")
    week_codes = weather_data.get("week_codes", [])
    
    if temp_trend == "warming":
        return "warming"
    elif temp_trend == "cooling":
        return "cooling"
    
    if len(week_codes) >= 3:
        bad_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]
        today_bad = week_codes[0] in bad_codes
        later_bad = any(c in bad_codes for c in week_codes[2:4])
        
        if today_bad and not later_bad:
            return "improving"
        elif not today_bad and later_bad:
            return "worsening"
    
    return "stable"

def _compare_tomorrow_weather(today_code, tomorrow_code):
    """Compare today and tomorrow weather."""
    good_codes = [0, 1, 2]
    today_good = today_code in good_codes
    tomorrow_good = tomorrow_code in good_codes
    
    if not today_good and tomorrow_good:
        return "better"
    elif today_good and not tomorrow_good:
        return "worse"
    return "same"

def generate_uplift_data(lat, lon, city=None):
    solar = get_daylight_delta(lat, lon) or {}
    weather = fetch_daily_weather(lat, lon) or {}
    
    # Parse solar data
    day_sec = solar.get("day_len_sec", 0)
    delta_daily = solar.get("delta_daily_sec", 0)
    delta_weekly = solar.get("delta_weekly_sec", 0)
    delta_solstice = solar.get("delta_solstice_sec", 0)
    sunrise = solar.get("sunrise")
    sunset = solar.get("sunset")
    
    # Format values
    hours = int(day_sec // 3600)
    mins = int((day_sec % 3600) // 60)
    day_len_str = f"{hours}h {mins}m"
    sunrise_str = sunrise.strftime("%H:%M") if sunrise else "--:--"
    sunset_str = sunset.strftime("%H:%M") if sunset else "--:--"
    
    # Calculate deltas
    delta_d_min = int(delta_daily // 60)
    delta_w_min = int(delta_weekly // 60)
    delta_s_min = int(delta_solstice // 60)
    
    # Get weather info
    today_weather = weather.get("today", {})
    tomorrow_weather = weather.get("tomorrow", {})
    weather_code = today_weather.get("code", 0)
    tomorrow_code = tomorrow_weather.get("code", 0)
    weather_cat = _get_weather_category(weather_code)
    temps = weather.get("daily", {}).get("temperature_2m_max", [10])
    
    # Deterministic randomness for today's date + location + random element
    today = date.today()
    # Add some true randomness to vary output
    random_seed = f"{today}|{lat:.2f}|{lon:.2f}|{random.randint(0, 999)}"
    rng = random.Random(random_seed)
    
    # Build text components
    text_parts = []
    
    # 1. Core daylight fact (always included)
    daylight_intros = [
        f"Today brings {day_len_str} of daylight, from {sunrise_str} to {sunset_str}.",
        f"You have {day_len_str} of light today, spanning {sunrise_str} to {sunset_str}.",
        f"Daylight runs {day_len_str} today, with sunrise at {sunrise_str} and sunset at {sunset_str}.",
        f"The day offers {day_len_str} of natural light, {sunrise_str} to {sunset_str}.",
        f"Between {sunrise_str} and {sunset_str}, you have {day_len_str} of daylight.",
    ]
    text_parts.append(rng.choice(daylight_intros))
    
    # 2. Trend observation
    if delta_d_min != 0:
        trend_phrases = _get_trend_phrases(delta_d_min)
        trend_text = rng.choice(trend_phrases)
        if "{delta}" in trend_text:
            trend_text = trend_text.format(delta=abs(delta_d_min))
        text_parts.append(trend_text)
    
    # 3. Seasonal phase context
    phase = _get_seasonal_phase(today.month, today.day)
    phase_text = rng.choice(content.SEASONAL_PHASE[phase])
    text_parts.append(phase_text)
    
    # 4. Weather observation (high probability)
    if rng.random() > 0.25:
        weather_phrases = content.WEATHER_TODAY.get(weather_cat, content.WEATHER_TODAY["cloudy"])
        text_parts.append(rng.choice(weather_phrases))
    
    # 5. Tomorrow comparison or week outlook (medium probability)
    if rng.random() > 0.5:
        tomorrow_compare = _compare_tomorrow_weather(weather_code, tomorrow_code)
        if tomorrow_compare != "same":
            tomorrow_phrases = content.WEATHER_TOMORROW.get(tomorrow_compare, [])
            if tomorrow_phrases:
                text_parts.append(rng.choice(tomorrow_phrases))
        else:
            outlook = _get_weather_outlook(weather)
            if outlook != "stable":
                outlook_phrases = content.WEATHER_WEEK_OUTLOOK.get(outlook, [])
                if outlook_phrases:
                    text_parts.append(rng.choice(outlook_phrases))
    
    # 6. Nature observation (high probability - this was missing!)
    if rng.random() > 0.2:
        nature_obs = content.NATURE_OBSERVATIONS.get(today.month, [])
        if nature_obs:
            text_parts.append(rng.choice(nature_obs))
    
    # 7. Practical sunrise/sunset note (lower probability)
    if rng.random() > 0.7 and sunrise and sunset:
        sunrise_hour = int(sunrise_str.split(":")[0])
        sunset_parts = sunset_str.split(":")
        sunset_hour = int(sunset_parts[0])
        sunset_min = int(sunset_parts[1])
        
        sunrise_cat = _get_sunrise_category(sunrise_hour)
        sunset_cat = _get_sunset_category(sunset_hour, sunset_min)
        
        # Pick either sunrise or sunset observation
        if rng.random() > 0.5:
            phrases = content.PRACTICAL_SUNRISE.get(sunrise_cat, [])
            if phrases:
                text_parts.append(rng.choice(phrases).format(time=sunrise_str))
        else:
            phrases = content.PRACTICAL_SUNSET.get(sunset_cat, [])
            if phrases:
                text_parts.append(rng.choice(phrases).format(time=sunset_str))
    
    # Combine text - aim for 3-5 sentences
    final_parts = text_parts[:5]  # Limit to 5 components max
    if len(final_parts) < 3 and len(text_parts) > len(final_parts):
        final_parts = text_parts[:3]  # Ensure at least 3 if available
    
    text = " ".join(final_parts)
    
    # Format deltas for display
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
    
    return {"text": text, "facts": facts}