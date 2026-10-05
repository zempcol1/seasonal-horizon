"""Unit tests for the service modules."""

import random
import re
from datetime import date, datetime
from unittest.mock import patch

import pytest


class TestSolarService:

    def test_matches_the_published_times(self):
        """Zurich, 5 Oct 2026 - Open-Meteo gives 07:30 and 18:57."""
        from services.solar_service import get_daylight_delta

        r = get_daylight_delta(47.37, 8.54, date(2026, 10, 5))
        assert r["sunrise"].strftime("%H:%M") == "07:30"
        assert r["sunset"].strftime("%H:%M") == "18:57"

    def test_spring_gain_counts_all_the_way_from_december(self):
        """Fetching used to stop 92 days back, which undercounted from March."""
        from services.solar_service import get_daylight_delta

        r = get_daylight_delta(47.37, 8.54, date(2026, 5, 1))
        assert r["delta_solstice_sec"] > 6 * 3600

    def test_sunset_milestone_only_while_evenings_lengthen(self):
        from services.solar_service import get_daylight_delta

        assert get_daylight_delta(47.37, 8.54, date(2026, 1, 10))["sunset_milestone"] ==             {"time": "17:00", "days": 4}
        assert get_daylight_delta(47.37, 8.54, date(2026, 10, 5))["sunset_milestone"] is None

    def test_evenings_turn_before_the_solstice_and_mornings_after(self):
        from services.solar_service import get_daylight_delta

        december = get_daylight_delta(47.37, 8.54, date(2025, 12, 14))
        assert december["delta_daily_sec"] < 0 < december["sunset_shift_sec"]
        assert get_daylight_delta(47.37, 8.54, date(2026, 1, 10))["sunrise_shift_sec"] < 0

    def test_polar_night_yields_nothing(self):
        """No sunrise at all must mean no data, never a zero-filled result."""
        from services.solar_service import get_daylight_delta

        assert get_daylight_delta(89.0, 0.0, date(2026, 1, 10)) == {}


class TestWeatherService:

    def test_result_is_cached(self):
        from services import weather_service
        weather_service._cache.clear()

        with patch.object(weather_service, 'request_json') as mock_req:
            mock_req.return_value = {
                "daily": {
                    "time": ["2024-01-15", "2024-01-16"],
                    "weathercode": [0, 3],
                    "temperature_2m_max": [10, 12],
                    "temperature_2m_min": [2, 4],
                    "sunshine_duration": [20000, 0],
                    "daylight_duration": [30000, 30000],
                }
            }
            weather_service.fetch_daily_weather(47.37, 8.54)
            weather_service.fetch_daily_weather(47.37, 8.54)

        assert mock_req.call_count == 1

    def test_sunshine_not_the_code_makes_a_sunny_day(self):
        """An "overcast" code with nine hours of sun is a sunny day."""
        from services.weather_service import _sun

        assert _sun(9 * 3600, 10 * 3600) == (9, True)
        assert _sun(1 * 3600, 10 * 3600) == (1, False)
        assert _sun(None, 10 * 3600) == (None, False)

    def test_analysis_finds_what_to_look_forward_to(self):
        from services.weather_service import _analyze_forecast

        def day(weekday, sunny):
            return {"weekday_index": weekday, "is_sunny": sunny,
                    "sun_hours": 6 if sunny else 0, "temp_max": 5}

        grey_then_sun = [day(0, False), day(1, False), day(2, True)]
        assert _analyze_forecast(grey_then_sun)["next_sunny_in_days"] == 2

        # Thursday, sun all the way through the weekend.
        sunny_week = [day(d % 7, True) for d in range(3, 10)]
        analysis = _analyze_forecast(sunny_week)
        assert analysis["sunny_streak"] == 7
        assert analysis["next_sunny_in_days"] is None
        assert analysis["weekend_sunny"] is True

    @pytest.mark.parametrize('temps,expected', [
        ([10, 11, 12, 15, 16, 17, 18], ("warming", "warming_strong")),
        ([18, 17, 16, 12, 11, 10, 9], ("stable",)),     # cooling is not a signal
        ([15, 15, 15, 15, 15, 15, 15], ("stable",)),
    ])
    def test_temperature_trend(self, temps, expected):
        from services.weather_service import _temp_trend

        assert _temp_trend(temps)[0] in expected


class TestRateLimiter:

    def test_allows_under_limit_then_blocks(self):
        from services.rate_limiter import RateLimiter

        limiter = RateLimiter()
        for _ in range(5):
            assert limiter.is_allowed("1.2.3.4", 5) is True
        assert limiter.is_allowed("1.2.3.4", 5) is False

    def test_limits_are_per_ip(self):
        from services.rate_limiter import RateLimiter

        limiter = RateLimiter()
        for _ in range(5):
            limiter.is_allowed("ip1", 5)
        assert limiter.is_allowed("ip2", 5) is True


JANUARY = date(2026, 1, 20)

SOLAR = {
    "day_len_sec": 32640, "delta_daily_sec": 150, "delta_weekly_sec": 1000,
    "delta_solstice_sec": 1900,
    "sunrise": datetime(2026, 1, 20, 8, 5), "sunset": datetime(2026, 1, 20, 17, 9),
    "sunset_milestone": {"time": "17:30", "days": 9},
    "sunrise_shift_sec": -50, "sunset_shift_sec": 87, "noon_gain_deg": 3.4,
}


def _ctx(day=JANUARY, solar=SOLAR, today=None, analysis=None, elevation=None, lang="en"):
    from services.uplift_engine import _build_context
    weather = {"today": today or {}, "analysis": analysis or {}, "elevation": elevation}
    return _build_context(solar, weather, day, lang)


# One context per signal, built to satisfy exactly its own condition.
PROBES = {
    "_turning_day": lambda: _ctx(date(2025, 12, 21)),
    "_evenings_turned": lambda: _ctx(date(2025, 12, 14), {**SOLAR, "sunset_shift_sec": 9}),
    "_sun_ahead": lambda: _ctx(analysis={"next_sunny_in_days": 2, "next_sunny_weekday": 3,
                                         "next_sunny_hours": 5.6}),
    "_solstice_countdown": lambda: _ctx(date(2025, 12, 10)),
    "_mornings_turned": lambda: _ctx(),
    "_snow": lambda: _ctx(today={"code": 73}),
    "_sunny_today": lambda: _ctx(today={"is_sunny": True, "sun_hours": 6.2}),
    "_sunset_milestone": lambda: _ctx(),
    "_warming": lambda: _ctx(analysis={"temp_trend": "warming", "temp_change": 3.1}),
    "_since_solstice": lambda: _ctx(),
    "_fog": lambda: _ctx(today={"code": 45}),
    "_frost_clear": lambda: _ctx(today={"is_sunny": True, "sun_hours": 6, "temp_min": -4}),
    "_sunny_streak": lambda: _ctx(analysis={"sunny_streak": 4}),
    "_daily_gain": lambda: _ctx(),
    "_some_sun": lambda: _ctx(today={"is_sunny": False, "sun_hours": 2.4}),
    "_weekend_sunny": lambda: _ctx(date(2026, 1, 22), analysis={"weekend_sunny": True}),
    "_noon_sun": lambda: _ctx(),
    "_peak_light": lambda: _ctx(date(2026, 6, 25)),
    "_season": lambda: _ctx(),
}


class TestUpliftEngine:

    def test_every_signal_can_fire(self):
        """
        A signal that silently stopped matching - a renamed analysis key, a
        flipped comparison - would otherwise just quietly never be chosen.
        """
        from services.uplift_engine import SIGNALS

        assert {signal.__name__ for signal in SIGNALS} == set(PROBES), "probe list out of sync"
        for signal in SIGNALS:
            assert signal(PROBES[signal.__name__]()) is not None, f"{signal.__name__} never fires"

    @pytest.mark.parametrize('day,phase', [
        (date(2026, 10, 31), "autumn"),
        (date(2026, 11, 1), "darkening"),
        (date(2026, 12, 20), "darkening"),
        (date(2026, 12, 21), "returning_light"),
        (date(2026, 3, 19), "returning_light"),
        (date(2026, 3, 20), "spring"),
        (date(2026, 6, 21), "summer"),
        (date(2026, 9, 22), "autumn"),
    ])
    def test_phases(self, day, phase):
        from services.uplift_engine import _phase

        assert _phase(day) == phase

    def test_shrinking_days_say_nothing_about_the_light(self):
        """In autumn the light is losing, so only the season line may speak for it."""
        from services.solar_service import get_daylight_delta
        from services.uplift_engine import _signals

        october = date(2026, 10, 5)
        found = _signals(_ctx(october, get_daylight_delta(47.37, 8.54, october)))
        assert [s.key for s in found] == ["season"]

    def test_countdown_waits_for_the_last_fortnight(self):
        from services.uplift_engine import _solstice_countdown

        assert _solstice_countdown(_ctx(date(2025, 11, 20))) is None
        assert _solstice_countdown(_ctx(date(2025, 12, 7))).data["days_to_solstice"] == 14

    def test_same_message_all_day_and_another_on_request(self):
        from services.uplift_engine import generate_uplift_data

        first = generate_uplift_data(47.37, 8.54)["text"]
        assert generate_uplift_data(47.37, 8.54)["text"] == first

        texts = [generate_uplift_data(47.37, 8.54, variant=v)["text"] for v in range(10)]
        assert all(a != b for a, b in zip(texts, texts[1:])), "the button must change something"

    @pytest.mark.parametrize('elevation,region', [
        (408, "lowland"),       # Zurich
        (1560, "alpine"),       # Davos
        (None, "lowland"),      # not reported
    ])
    def test_region_follows_elevation(self, elevation, region):
        assert _ctx(elevation=elevation).region == region

    def test_companion_comes_from_the_region(self):
        from services import uplift_content as content
        from services.uplift_engine import _companion_pool, _season

        ctx = _ctx(date(2026, 2, 10), elevation=1500)
        assert _companion_pool(ctx, _season(ctx)) == content.SPRING_SIGNS["alpine"]["en"][2]

    @pytest.mark.parametrize('lang', ['en', 'de', 'fr'])
    def test_generates_text_in_any_language(self, lang):
        from services.uplift_engine import generate_uplift_data

        result = generate_uplift_data(47.37, 8.54, lang=lang)
        assert result["text"]
        assert set(result) == {"text", "facts"}

    def test_polar_night_still_gets_a_message(self):
        from services.uplift_engine import generate_uplift_data

        assert generate_uplift_data(89.0, 0.0)["text"]


class TestNeverClaimsUnbackedFacts:
    """The app must never state something it did not measure."""

    @pytest.mark.parametrize('today,expected', [
        (date(2025, 1, 10), date(2024, 12, 21)),
        (date(2025, 6, 20), date(2024, 12, 21)),
        (date(2025, 11, 15), date(2025, 6, 21)),    # no "gain" in November
        (date(2025, 12, 21), date(2025, 12, 21)),
    ])
    def test_solstice_delta_counts_from_the_last_solstice(self, today, expected):
        from services.solar_service import _last_solstice

        assert _last_solstice(today) == expected

    def test_every_template_is_backed_by_its_signal(self):
        """A pool may only use what its signal provides, in every language."""
        from services import uplift_content as content
        from services.uplift_engine import SIGNALS, _PLACEHOLDER

        for signal in SIGNALS:
            fired = signal(PROBES[signal.__name__]())
            if fired.key == "season":
                continue
            for lang, templates in content.SIGNALS[fired.key].items():
                for template in templates:
                    missing = set(_PLACEHOLDER.findall(template)) - set(fired.data)
                    assert not missing, f"{fired.key}/{lang}: {template}"

        for phase in content.PHASES.values():
            for templates in phase.values():
                assert not any("{" in t for t in templates), "phase lines take no figures"

    def test_template_needing_a_missing_fact_is_not_used(self):
        from services.uplift_engine import _pick_template

        templates = ["Backed {day_length}.", "Unbacked {bad_days}."]
        rng = random.Random(0)
        assert _pick_template(templates, {"day_length": "8h"}, rng) == "Backed {day_length}."
        assert _pick_template(templates, {}, rng) is None

    def test_no_invented_numbers_when_apis_return_nothing(self):
        from services.uplift_engine import generate_uplift_data

        with patch('services.uplift_engine.get_daylight_delta', return_value={}), \
             patch('services.uplift_engine.fetch_daily_weather', return_value={}):
            result = generate_uplift_data(47.37, 8.54, lang="en")

        assert result["facts"]["day_length"] == "--"
        assert result["facts"]["delta_yesterday"] == "--"
        assert "0h 0m" not in result["text"]
        assert not re.search(r'\{\w+\}', result["text"]), "raw placeholder leaked"

    def test_formatters_match_the_arithmetic_they_replaced(self):
        from services.uplift_engine import format_duration, format_span, format_signed_span

        assert format_duration(50580) == "14h 3m"
        assert format_duration(0) == "0h 0m"
        assert format_span(73) == "1h 13m"
        assert format_span(22) == "22m"
        assert format_signed_span(22) == "+22 min"
        assert format_signed_span(-73) == "-1h 13m"
