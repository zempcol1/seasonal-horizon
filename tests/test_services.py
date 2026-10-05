"""Unit tests for the service modules."""

import re
from datetime import date, datetime, timedelta
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

    def test_milestones_only_while_the_light_grows(self):
        from services.solar_service import get_daylight_delta

        january = get_daylight_delta(47.37, 8.54, date(2026, 1, 10))
        october = get_daylight_delta(47.37, 8.54, date(2026, 10, 5))
        assert january["sunset_milestone"] == {"time": "17:00", "days": 4}
        assert january["sunrise_milestone"]["time"] == "08:00"
        for key in ("sunset_milestone", "sunrise_milestone", "hour_mark", "autumn_twin"):
            assert october[key] is None, key

    def test_evenings_turn_before_the_solstice_and_mornings_after(self):
        from services.solar_service import get_daylight_delta

        december = get_daylight_delta(47.37, 8.54, date(2025, 12, 14))
        assert december["delta_daily_sec"] < 0 < december["sunset_shift_sec"]
        assert get_daylight_delta(47.37, 8.54, date(2026, 1, 10))["sunrise_shift_sec"] < 0

    def test_autumn_twin_is_as_long_as_today(self):
        """12 February has about the light of late October."""
        from services.solar_service import get_daylight_delta

        twin = get_daylight_delta(47.37, 8.54, date(2026, 2, 12))["autumn_twin"]
        assert date(2025, 10, 25) <= twin <= date(2025, 10, 31)

    def test_hour_mark_lands_on_the_crossing_day(self):
        from services.solar_service import get_daylight_delta

        ahead = get_daylight_delta(47.37, 8.54, date(2026, 1, 15))["hour_mark"]
        crossing = date(2026, 1, 15) + timedelta(days=ahead["days"])
        assert get_daylight_delta(47.37, 8.54, crossing)["hour_mark"] == \
            {"hours": ahead["hours"], "days": 0}

    def test_polar_night_yields_nothing(self):
        """No sunrise at all must mean no data, never a zero-filled result."""
        from services.solar_service import get_daylight_delta

        assert get_daylight_delta(89.0, 0.0, date(2026, 1, 10)) == {}


def _day(stamp, sunny, temp=5, weekday=0):
    return {"date": stamp, "weekday_index": weekday, "is_sunny": sunny,
            "sun_hours": 6 if sunny else 0, "temp_max": temp}


class TestWeatherService:

    def test_result_is_cached(self):
        from config import today
        from services import weather_service
        weather_service._cache.clear()

        with patch.object(weather_service, 'request_json') as mock_req:
            mock_req.return_value = {
                "daily": {
                    "time": [str(today()), str(today() + timedelta(days=1))],
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

        grey_then_sun = [_day("", False), _day("", False), _day("", True)]
        assert _analyze_forecast(grey_then_sun)["next_sunny_in_days"] == 2

        # Thursday, sun all the way through the weekend.
        sunny_week = [_day("", True, weekday=d % 7) for d in range(3, 10)]
        analysis = _analyze_forecast(sunny_week)
        assert analysis["sunny_streak"] == 7
        assert analysis["next_sunny_in_days"] is None
        assert analysis["weekend_sunny"] is True

    def test_analysis_looks_back_a_month(self):
        from services.weather_service import _analyze_forecast

        history = [_day("2026-01-02", True, temp=12)] + \
            [_day(f"2026-01-{d:02d}", False, temp=3) for d in range(3, 20)]
        today = [_day("2026-01-20", True, temp=11)]
        analysis = _analyze_forecast(today, history)
        assert analysis["grey_days_before"] == 17
        assert analysis["warmest_since"] == "2026-01-02"
        assert _analyze_forecast([_day("", True, temp=20)], history)["warmest_since"] == ""

    def test_low_cloud_lid(self):
        """Hochnebel: low cloud thick, nothing above - measured from the layers."""
        from services.weather_service import _low_cloud_lid

        times = [f"2026-01-20T{h:02d}:00" for h in range(24)]
        lid = {"time": times, "cloud_cover_low": [95] * 24,
               "cloud_cover_mid": [5] * 24, "cloud_cover_high": [10] * 24}
        overcast = {**lid, "cloud_cover_mid": [90] * 24}
        assert _low_cloud_lid(lid, "2026-01-20") is True
        assert _low_cloud_lid(overcast, "2026-01-20") is False
        assert _low_cloud_lid({}, "2026-01-20") is False

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
    "dusk": datetime(2026, 1, 20, 17, 43),
    "sunset_milestone": {"time": "17:30", "days": 9},
    "sunrise_milestone": {"time": "08:00", "days": 6},
    "hour_mark": {"hours": 10, "days": 21},
    "autumn_twin": date(2025, 11, 21),
    "sunrise_shift_sec": -50, "sunset_shift_sec": 87, "noon_gain_deg": 3.4,
}


def _ctx(day=JANUARY, solar=SOLAR, today=None, analysis=None, elevation=None,
         lang="en", customs=False, pollen=None):
    from services.uplift_engine import _build_context
    weather = {"today": today or {}, "analysis": analysis or {}, "elevation": elevation}
    return _build_context(solar, weather, day, lang, customs=customs, pollen=pollen)


# One context per signal, built to satisfy exactly its own condition.
PROBES = {
    "_turning_day": lambda: _ctx(date(2025, 12, 21)),
    "_equinox_day": lambda: _ctx(date(2026, 3, 20)),
    "_lichtmess": lambda: _ctx(date(2026, 2, 2), {**SOLAR, "delta_solstice_sec": 4260}),
    "_first_sun": lambda: _ctx(today={"is_sunny": True, "sun_hours": 6},
                               analysis={"grey_days_before": 6}),
    "_evenings_turned": lambda: _ctx(date(2025, 12, 14), {**SOLAR, "sunset_shift_sec": 9}),
    "_sun_ahead": lambda: _ctx(analysis={"next_sunny_in_days": 2, "next_sunny_weekday": 3,
                                         "next_sunny_hours": 5.6}),
    "_solstice_countdown": lambda: _ctx(date(2025, 12, 10)),
    "_mornings_turned": lambda: _ctx(),
    "_hour_mark": lambda: _ctx(solar={**SOLAR, "hour_mark": {"hours": 9, "days": 3}}),
    "_snow": lambda: _ctx(today={"code": 73, "snow_cm": 4}),
    "_custom": lambda: _ctx(date(2026, 12, 6), customs=True),
    "_hochnebel": lambda: _ctx(today={"low_cloud_lid": True, "is_sunny": False}),
    "_sunny_today": lambda: _ctx(today={"is_sunny": True, "sun_hours": 6.2}),
    "_sunset_milestone": lambda: _ctx(),
    "_warming": lambda: _ctx(analysis={"temp_trend": "warming", "temp_change": 3.1}),
    "_since_solstice": lambda: _ctx(),
    "_warmest_since": lambda: _ctx(today={"temp_max": 11},
                                   analysis={"warmest_since": "2025-12-28"}),
    "_pollen": lambda: _ctx(date(2026, 3, 1), pollen={"alder": 80}),
    "_fog": lambda: _ctx(today={"code": 45}),
    "_frost_clear": lambda: _ctx(today={"is_sunny": True, "sun_hours": 6, "temp_min": -4}),
    "_toads": lambda: _ctx(date(2026, 3, 5), today={"temp_min": 7, "precip": 4}),
    "_equinox_countdown": lambda: _ctx(date(2026, 3, 14)),
    "_sunrise_milestone": lambda: _ctx(),
    "_sunny_streak": lambda: _ctx(analysis={"sunny_streak": 4}),
    "_bees": lambda: _ctx(date(2026, 3, 1), today={"temp_max": 13, "sun_hours": 5}),
    "_daily_gain": lambda: _ctx(),
    "_autumn_twin": lambda: _ctx(),
    "_uv_strength": lambda: _ctx(date(2026, 3, 10), today={"uv": 3.4}),
    "_some_sun": lambda: _ctx(today={"is_sunny": False, "sun_hours": 2.4}),
    "_sunny_week": lambda: _ctx(analysis={"week_sun_hours": 30, "past_week_sun_hours": 8}),
    "_weekend_sunny": lambda: _ctx(date(2026, 1, 22), analysis={"weekend_sunny": True}),
    "_noon_sun": lambda: _ctx(),
    "_dusk_light": lambda: _ctx(),
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

    def test_wording_follows_strength_and_place(self):
        from services.uplift_engine import _daily_gain, _snow, _sunny_today

        assert _daily_gain(_ctx(solar={**SOLAR, "delta_daily_sec": 200})).pool == "daily_gain.fast"
        assert _snow(_ctx(today={"code": 73}, elevation=1500)).pool == "snow.alpine"
        assert _sunny_today(_ctx(date(2026, 5, 1), today={"is_sunny": True, "sun_hours": 9})) \
            .pool == "sunny_today"

    def test_one_day_away_reads_tomorrow(self):
        from services.uplift_engine import Picker, _lead, _sunset_milestone

        for d in range(10):
            ctx = _ctx(solar={**SOLAR, "sunset_milestone": {"time": "17:30", "days": 1}})
            text = _lead(ctx, _sunset_milestone(ctx), Picker("x", JANUARY + timedelta(days=d)))
            assert "1 day" not in text and "tomorrow" in text, text

    def test_the_day_of_an_event_leads_with_it(self):
        """Sechseläuten comes once a year; it must not lose a draw to the weather."""
        from services.uplift_engine import Picker, _select

        ctx = _ctx(date(2026, 4, 20), today={"is_sunny": True, "sun_hours": 7},
                   analysis={"grey_days_before": 6}, customs=True)
        for place in ("a", "b", "c", "d", "e"):
            assert _select(ctx, Picker(place, ctx.today)).pool == "custom.sechselaeuten"

    @pytest.mark.parametrize('year,advent', [(2022, date(2022, 11, 27)), (2026, date(2026, 11, 29))])
    def test_christmas_markets_run_through_advent(self, year, advent):
        from services.uplift_engine import _custom

        assert _custom(_ctx(advent - timedelta(days=1), customs=True)) is None
        assert _custom(_ctx(advent, customs=True)).pool == "custom.christmas_markets"

    def test_samichlaus_outranks_the_markets(self):
        from services.uplift_engine import _custom

        assert _custom(_ctx(date(2026, 12, 6), customs=True)).pool == "custom.samichlaus"

    def test_same_message_all_day_and_another_on_request(self):
        from services.uplift_engine import generate_uplift_data

        first = generate_uplift_data(47.37, 8.54)["text"]
        assert generate_uplift_data(47.37, 8.54)["text"] == first

        texts = [generate_uplift_data(47.37, 8.54, variant=v)["text"] for v in range(10)]
        assert all(a != b for a, b in zip(texts, texts[1:])), "the button must change something"

    def test_a_pool_is_used_up_before_a_line_returns(self):
        from services.uplift_engine import Picker

        pool = ["a", "b", "c", "d", "e"]
        days = [Picker("47.37:8.54", JANUARY + timedelta(days=d)).pick(pool, "x") for d in range(5)]
        assert sorted(days) == pool

    def test_pollen_stays_rare(self):
        """Hay fever: pollen may only come up on one day in POLLEN_EVERY_DAYS."""
        from services.uplift_engine import POLLEN_EVERY_DAYS, Picker

        days = range(POLLEN_EVERY_DAYS * 10)
        allowed = sum(Picker("47.37:8.54", JANUARY + timedelta(days=d)).every(POLLEN_EVERY_DAYS, "pollen")
                      for d in days)
        assert allowed == 10

    @pytest.mark.parametrize('elevation,region', [
        (408, "lowland"),       # Zurich
        (1560, "alpine"),       # Davos
        (None, "lowland"),      # not reported
    ])
    def test_region_follows_elevation(self, elevation, region):
        assert _ctx(elevation=elevation).region == region

    def test_nature_lines_follow_region_and_weather(self):
        from services import uplift_content as content
        from services.uplift_engine import Picker, _companion, _season

        alpine = _ctx(date(2026, 2, 10), elevation=1500)
        line = _companion(alpine, _season(alpine), Picker("x", alpine.today))
        assert line in content.NATURE["alpine"][2]["any"]["en"]

        # A frost line only on a frosty day.
        frost = content.NATURE["lowland"][10]["frost"]["en"]
        for d in range(20):
            day = date(2026, 10, 1) + timedelta(days=d)
            warm = _ctx(day, today={"temp_min": 8, "temp_max": 18})
            assert _companion(warm, _season(warm), Picker("x", day)) not in frost

    @pytest.mark.parametrize('year,expected', [
        (2019, date(2019, 4, 8)),       # moved forward out of Holy Week
        (2022, date(2022, 4, 25)),      # moved back off Easter Monday
        (2024, date(2024, 4, 15)),
        (2025, date(2025, 4, 28)),
        (2026, date(2026, 4, 20)),
    ])
    def test_sechselaeuten_date(self, year, expected):
        from services.uplift_engine import _sechselaeuten

        assert _sechselaeuten(year) == expected

    def test_customs_only_around_zurich_and_aargau(self):
        from services.uplift_engine import _custom, _in_customs_area

        assert _in_customs_area(47.37, 8.54) and _in_customs_area(47.39, 8.05)   # Zurich, Aarau
        assert not _in_customs_area(46.95, 7.45)                                 # Bern
        assert _custom(_ctx(date(2026, 12, 6), customs=False)) is None
        soon = _custom(_ctx(date(2026, 4, 17), customs=True))
        assert soon.pool == "custom.sechselaeuten_soon" and soon.data["days_until"] == 3

    def test_a_year_of_messages(self):
        """
        Every day of a year, lowland and alpine, both languages: each message
        is complete, every pool it reaches exists, and no placeholder leaks.
        """
        from services.solar_service import get_daylight_delta
        from services.uplift_engine import Picker, _compose

        weathers = [
            {},
            {"is_sunny": True, "sun_hours": 7, "temp_min": -3, "temp_max": 4, "uv": 3.2},
            {"is_sunny": False, "sun_hours": 0.5, "code": 73, "snow_cm": 5, "temp_min": -1,
             "temp_max": 1, "precip": 6, "low_cloud_lid": True},
        ]
        start = date(2026, 1, 1)
        for offset in range(365):
            day = start + timedelta(days=offset)
            solar = get_daylight_delta(47.37, 8.54, day)
            for elevation, weather in ((420, weathers[offset % 3]), (1500, weathers[(offset + 1) % 3])):
                for lang in ("en", "de"):
                    ctx = _ctx(day, solar, today=weather, elevation=elevation, lang=lang, customs=True)
                    text = " ".join(_compose(ctx, Picker("47.37:8.54", day)))
                    assert text and "None" not in text, (day, lang)
                    assert not re.search(r"\{\w+\}", text), (day, lang, text)

    @pytest.mark.parametrize('lang', ['en', 'de', 'fr'])
    def test_generates_text_in_any_language(self, lang):
        from services.uplift_engine import generate_uplift_data

        result = generate_uplift_data(47.37, 8.54, lang=lang)
        assert result["text"]
        assert set(result) == {"text", "lead", "companion", "facts"}
        assert result["text"] == f"{result['lead']} {result['companion']}"

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
        """
        Every pool, variants included, may only use what its signal provides,
        in every language. Variants share their signal's data.
        """
        from services import uplift_content as content
        from services.uplift_engine import SIGNALS, _PLACEHOLDER

        data = {}
        for signal in SIGNALS:
            fired = signal(PROBES[signal.__name__]())
            data[fired.key] = set(fired.data)

        for name, pool in content.SIGNALS.items():
            key = name.split(".")[0]
            assert key in data, f"pool {name} belongs to no signal"
            for lang, templates in pool.items():
                for template in templates:
                    missing = set(_PLACEHOLDER.findall(template)) - data[key]
                    assert not missing, f"{name}/{lang}: {template}"

        for phase in content.PHASES.values():
            for templates in phase.values():
                assert not any("{" in t for t in templates), "phase lines take no figures"

    def test_every_pool_speaks_both_languages_equally(self):
        from services import uplift_content as content

        pools = list(content.SIGNALS.values()) + list(content.PHASES.values()) + \
            [content.SUN_ENJOYMENT] + \
            [tag for region in content.NATURE.values() for month in region.values()
             for tag in month.values()]
        for pool in pools:
            assert len(pool["en"]) == len(pool["de"]) > 0

    def test_swiss_spelling(self):
        import inspect
        from services import uplift_content

        assert "ß" not in inspect.getsource(uplift_content)

    def test_the_sky_follows_the_sun_not_the_code(self):
        """Code 80 ("showers") with ten hours of sun is a sunny day in the box too."""
        from services.uplift_engine import _sky

        assert _sky({"code": 80, "is_sunny": True, "sun_hours": 10}) == "sunny"
        assert _sky({"code": 3, "sun_hours": 2}) == "mixed"
        assert _sky({"code": 61, "sun_hours": 0, "precip": 5}) == "rain"
        assert _sky({"code": 73, "is_sunny": True, "sun_hours": 6}) == "snow"
        assert _sky({}) is None

    @pytest.mark.parametrize('day,gains', [
        (date(2026, 1, 20), True), (date(2026, 10, 5), False), (date(2026, 5, 1), False),
    ])
    def test_gains_only_shown_while_they_are_gains(self, day, gains):
        from services.solar_service import get_daylight_delta
        from services.uplift_engine import _format_facts

        facts = _format_facts(_ctx(day, get_daylight_delta(47.37, 8.54, day)))
        assert facts["gains"] is gains

    def test_template_needing_a_missing_fact_is_not_used(self):
        from services.uplift_engine import _backed

        templates = ["Backed {day_length}.", "Unbacked {bad_days}."]
        assert _backed(templates, {"day_length": "8h"}) == ["Backed {day_length}."]
        assert _backed(templates, {}) == []

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
