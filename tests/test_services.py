"""Unit tests for the service modules."""

import random
import re
from datetime import date, datetime
from unittest.mock import patch

import pytest


class TestSolarService:

    def test_result_is_cached(self):
        from services import solar_service
        solar_service._cache.clear()

        with patch.object(solar_service, 'request_json') as mock_req:
            mock_req.return_value = {
                "daily": {
                    "daylight_duration": [28800, 29000, 29200],
                    "sunrise": ["2024-01-15T08:00", "2024-01-16T07:58", "2024-01-17T07:56"],
                    "sunset": ["2024-01-15T16:00", "2024-01-16T16:03", "2024-01-17T16:06"],
                }
            }
            first = solar_service.get_daylight_delta(47.37, 8.54)
            second = solar_service.get_daylight_delta(47.37, 8.54)

        assert mock_req.call_count == 1
        assert first == second

    @pytest.mark.parametrize('payload', [None, {"daily": {}}])
    def test_unusable_response_yields_nothing(self, payload):
        """No data must mean no data, never a zero-filled result."""
        from services import solar_service
        solar_service._cache.clear()

        with patch.object(solar_service, 'request_json', return_value=payload):
            assert solar_service.get_daylight_delta(47.37, 8.54) == {}


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
                    "precipitation_sum": [0, 0],
                    "precipitation_probability_max": [0, 10],
                }
            }
            weather_service.fetch_daily_weather(47.37, 8.54)
            weather_service.fetch_daily_weather(47.37, 8.54)

        assert mock_req.call_count == 1

    def test_code_classification(self):
        from services.weather_service import classify, is_good, is_bad

        assert [is_good(c) for c in (0, 1, 2)] == [True] * 3
        assert [is_good(c) for c in (3, 61)] == [False] * 2
        assert [is_bad(c) for c in (61, 95)] == [True] * 2
        assert [is_bad(c) for c in (0, 3)] == [False] * 2

        # Buckets for narrative lookup. Note 2 is "good" but not "clear".
        assert classify(0) == "clear"
        assert classify(2) == "grey"
        assert classify(75) == "snow"
        assert classify(61) == "rain"

    @pytest.mark.parametrize('temps,expected', [
        ([10, 11, 12, 15, 16, 17, 18], ("warming", "warming_strong")),
        ([18, 17, 16, 12, 11, 10, 9], ("cooling", "cooling_strong")),
        ([15, 15, 15, 15, 15, 15, 15], ("stable",)),
    ])
    def test_temperature_trend(self, temps, expected):
        from services.weather_service import _analyze_forecast

        forecast = [{"is_good": True, "is_bad": False, "date": datetime(2024, 1, 15)}
                    for _ in range(7)]
        assert _analyze_forecast(forecast, temps)["temp_trend"] in expected


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


class TestUpliftEngine:

    def _solar(self):
        return {
            "day_len_sec": 36000,
            "delta_daily_sec": 120,
            "delta_weekly_sec": 840,
            "delta_solstice_sec": 3600,
            "sunrise": datetime(2024, 1, 15, 8, 0),
            "sunset": datetime(2024, 1, 15, 18, 0),
        }

    def test_detect_scenario_picks_a_known_scenario(self):
        from services.uplift_engine import detect_scenario

        weather = {
            "forecast": [{"is_good": False, "is_bad": True}],
            "today": {"is_good": False, "is_bad": True},
            "analysis": {"next_good_weekday": 2, "next_good_in_days": 2,
                         "temp_trend": "stable", "bad_streak_length": 2},
        }
        scenario, _ = detect_scenario(weather, self._solar(), date(2024, 2, 15))
        assert scenario in ("rain_clearing_soon", "light_fighter",
                            "post_solstice_grind", "stable_focus_light")

    def test_every_rule_can_fire(self):
        """
        Each rule gets a context built to satisfy exactly its own condition.

        A rule that silently stopped matching - a renamed analysis key, a
        flipped comparison - would otherwise just quietly never be chosen.
        """
        from services.uplift_engine import RULES, _build_context

        def ctx(solar, weather, today=date(2024, 2, 15), lat=47.4):
            return _build_context(solar, weather, today, "en", lat)

        def w(today_weather, analysis=None):
            return {"today": today_weather, "analysis": analysis or {},
                    "forecast": [{"temp_max": 10}]}

        s = {"day_len_sec": 36000, "delta_daily_sec": 180,
             "delta_solstice_sec": 3600, "delta_weekly_sec": 900}

        probes = {
            "_carpe_diem": ctx(s, w({"is_good": True},
                                    {"next_bad_weekday": 3, "next_bad_in_days": 2})),
            "_rain_clearing_soon": ctx(s, w({"is_bad": True},
                                            {"next_good_weekday": 2, "next_good_in_days": 2})),
            "_light_fighter": ctx(s, w({"is_bad": True})),
            "_post_solstice_grind": ctx(s, w({}), date(2024, 1, 20)),
            "_warming_trend": ctx(s, w({}, {"temp_trend": "warming_strong", "temp_change": 5})),
            "_spring_acceleration": ctx(s, w({}), date(2024, 3, 10)),
            "_breakthrough_day": ctx(s, w({"is_good": True})),
            "_peak_light": ctx({**s, "day_len_sec": 55000}, w({}), date(2024, 6, 30)),
            "_cooling_trend": ctx(s, w({}, {"temp_trend": "cooling_strong", "temp_change": -5})),
            "_good_streak": ctx(s, w({}, {"good_streak_length": 5})),
            "_solstice_approaching": ctx(s, w({}), date(2024, 6, 15)),
            "_weekend_outlook": ctx(s, w({}, {"weekend_outlook": "good"})),
            "_grey_stretch": ctx(s, w({}, {"bad_streak_length": 4})),
            "_stable_focus_light": ctx(s, w({})),
        }

        assert {rule.__name__ for rule in RULES} == set(probes), "probe list out of sync"
        for rule in RULES:
            assert rule(probes[rule.__name__]) is not None, f"{rule.__name__} never fires"

    def test_southern_hemisphere_flips_the_solstice_rule(self):
        """The June solstice is the peak up north and the low point down south."""
        from services.uplift_engine import _solstice_approaching, _build_context

        june = date(2024, 6, 15)
        north = _solstice_approaching(_build_context({}, {}, june, "en", 47.4))
        south = _solstice_approaching(_build_context({}, {}, june, "en", -33.9))
        assert north.data["peak_or_min"] == "peak"
        assert south.data["peak_or_min"] == "minimum"

    @pytest.mark.parametrize('lang', ['en', 'de', 'fr'])
    def test_generates_text_in_any_language(self, lang):
        from services.uplift_engine import generate_uplift_data

        with patch('services.uplift_engine.get_daylight_delta', return_value=self._solar()), \
             patch('services.uplift_engine.fetch_daily_weather') as mock_weather:
            mock_weather.return_value = {
                "forecast": [{"code": 0, "temp_max": 10, "is_good": True, "is_bad": False}],
                "today": {"code": 0, "is_good": True, "is_bad": False},
                "analysis": {"temp_trend": "stable"},
            }
            result = generate_uplift_data(47.37, 8.54, lang=lang)

        assert result["text"]
        assert set(result) == {"text", "facts"}

    def test_extreme_latitude(self):
        """Polar summer: 24h of daylight and no sunrise time at all."""
        from services.uplift_engine import generate_uplift_data

        with patch('services.uplift_engine.get_daylight_delta') as mock_solar, \
             patch('services.uplift_engine.fetch_daily_weather', return_value={}):
            mock_solar.return_value = {
                "day_len_sec": 86400, "delta_daily_sec": 0, "delta_weekly_sec": 0,
                "delta_solstice_sec": 0, "sunrise": None, "sunset": None,
            }
            assert generate_uplift_data(70.0, 25.0)["text"]


class TestNeverClaimsUnbackedFacts:
    """The app must never state something it did not measure."""

    def test_southern_hemisphere_seasons_are_flipped(self):
        from services.uplift_engine import _get_seasonal_phase

        assert _get_seasonal_phase(1, 15, lat=47.4) == "deep_winter"
        assert _get_seasonal_phase(1, 15, lat=-33.9) == "peak_summer"
        assert _get_seasonal_phase(7, 15, lat=-33.9) == "deep_winter"

    def test_darkest_solstice_follows_hemisphere(self):
        from services.solar_service import _get_darkest_solstice_date

        assert _get_darkest_solstice_date(47.4).month == 12
        assert _get_darkest_solstice_date(-33.9).month == 6

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
