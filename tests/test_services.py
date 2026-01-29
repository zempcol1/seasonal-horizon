"""Tests for service modules."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import date, datetime
import time


class TestSolarService:
    """Tests for solar_service module."""
    
    def test_get_daylight_delta_caching(self):
        """Test that results are cached."""
        from services import solar_service
        
        # Clear cache
        solar_service._cache.clear()
        
        with patch.object(solar_service, '_request_with_retry') as mock_req:
            mock_req.return_value = {
                "daily": {
                    "daylight_duration": [28800, 29000, 29200],
                    "sunrise": ["2024-01-15T08:00", "2024-01-16T07:58", "2024-01-17T07:56"],
                    "sunset": ["2024-01-15T16:00", "2024-01-16T16:03", "2024-01-17T16:06"]
                }
            }
            
            # First call
            result1 = solar_service.get_daylight_delta(47.37, 8.54)
            assert mock_req.call_count == 1
            
            # Second call should use cache
            result2 = solar_service.get_daylight_delta(47.37, 8.54)
            assert mock_req.call_count == 1  # No additional call
            
            assert result1 == result2
    
    def test_get_daylight_delta_handles_empty_response(self):
        """Test handling of empty API response."""
        from services import solar_service
        solar_service._cache.clear()
        
        with patch.object(solar_service, '_request_with_retry') as mock_req:
            mock_req.return_value = None
            result = solar_service.get_daylight_delta(47.37, 8.54)
            assert result == {}
    
    def test_get_daylight_delta_handles_missing_data(self):
        """Test handling of incomplete API response."""
        from services import solar_service
        solar_service._cache.clear()
        
        with patch.object(solar_service, '_request_with_retry') as mock_req:
            mock_req.return_value = {"daily": {}}
            result = solar_service.get_daylight_delta(47.37, 8.54)
            assert result == {}


class TestWeatherService:
    """Tests for weather_service module."""
    
    def test_fetch_daily_weather_caching(self):
        """Test that weather results are cached."""
        from services import weather_service
        weather_service._cache.clear()
        
        with patch('services.weather_service.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "daily": {
                    "time": ["2024-01-15", "2024-01-16"],
                    "weathercode": [0, 3],
                    "temperature_2m_max": [10, 12],
                    "temperature_2m_min": [2, 4],
                    "precipitation_sum": [0, 0],
                    "precipitation_probability_max": [0, 10]
                }
            }
            mock_get.return_value = mock_response
            
            result1 = weather_service.fetch_daily_weather(47.37, 8.54)
            assert mock_get.call_count == 1
            
            result2 = weather_service.fetch_daily_weather(47.37, 8.54)
            assert mock_get.call_count == 1  # Cached
    
    def test_is_good_weather(self):
        """Test weather classification."""
        from services.weather_service import _is_good_weather, _is_bad_weather
        
        # Good weather codes
        assert _is_good_weather(0) is True
        assert _is_good_weather(1) is True
        assert _is_good_weather(2) is True
        
        # Not good
        assert _is_good_weather(3) is False
        assert _is_good_weather(61) is False
        
        # Bad weather codes
        assert _is_bad_weather(61) is True
        assert _is_bad_weather(95) is True
        
        # Not bad
        assert _is_bad_weather(0) is False
        assert _is_bad_weather(3) is False
    
    def test_analyze_forecast_temperature_trends(self):
        """Test temperature trend detection."""
        from services.weather_service import _analyze_forecast
        
        # Warming trend
        forecast = [{"is_good": True, "is_bad": False, "date": datetime(2024, 1, 15)}] * 7
        temps_warming = [10, 11, 12, 15, 16, 17, 18]
        analysis = _analyze_forecast(forecast, temps_warming)
        assert analysis["temp_trend"] in ["warming", "warming_strong"]
        
        # Cooling trend
        temps_cooling = [18, 17, 16, 12, 11, 10, 9]
        analysis = _analyze_forecast(forecast, temps_cooling)
        assert analysis["temp_trend"] in ["cooling", "cooling_strong"]
        
        # Stable
        temps_stable = [15, 15, 15, 15, 15, 15, 15]
        analysis = _analyze_forecast(forecast, temps_stable)
        assert analysis["temp_trend"] == "stable"


class TestRateLimiter:
    """Tests for rate_limiter module."""
    
    def test_allows_requests_under_limit(self):
        """Test that requests under limit are allowed."""
        from services.rate_limiter import RateLimiter
        
        limiter = RateLimiter()
        ip = "192.168.1.1"
        
        for _ in range(5):
            assert limiter.is_allowed(ip, 10) is True
    
    def test_blocks_requests_over_limit(self):
        """Test that requests over limit are blocked."""
        from services.rate_limiter import RateLimiter
        
        limiter = RateLimiter()
        ip = "192.168.1.2"
        
        # Use up the limit
        for _ in range(5):
            limiter.is_allowed(ip, 5)
        
        # Next request should be blocked
        assert limiter.is_allowed(ip, 5) is False
    
    def test_different_ips_independent(self):
        """Test that different IPs have independent limits."""
        from services.rate_limiter import RateLimiter
        
        limiter = RateLimiter()
        
        # Fill up IP1
        for _ in range(5):
            limiter.is_allowed("ip1", 5)
        
        # IP2 should still be allowed
        assert limiter.is_allowed("ip2", 5) is True
    
    def test_get_remaining(self):
        """Test remaining request count."""
        from services.rate_limiter import RateLimiter
        
        limiter = RateLimiter()
        ip = "192.168.1.3"
        
        assert limiter.get_remaining(ip, 10) == 10
        
        limiter.is_allowed(ip, 10)
        assert limiter.get_remaining(ip, 10) == 9


class TestUpliftEngine:
    """Tests for uplift_engine scenarios."""
    
    def test_detect_scenario_rain_clearing(self):
        """Test rain clearing soon scenario detection."""
        from services.uplift_engine import detect_scenario
        
        weather_data = {
            "forecast": [
                {"is_good": False, "is_bad": True},
                {"is_good": False, "is_bad": True},
                {"is_good": True, "is_bad": False},
            ],
            "today": {"is_good": False, "is_bad": True},
            "analysis": {
                "next_good_day": "Wednesday",
                "next_good_day_index": 2,
                "temp_trend": "stable",
                "good_streak_length": 0,
                "bad_streak_length": 2,
            }
        }
        
        solar_data = {
            "day_len_sec": 36000,
            "delta_daily_sec": 120,
            "delta_solstice_sec": 3600,
        }
        
        scenario, data = detect_scenario(weather_data, solar_data, date(2024, 2, 15))
        # Should be one of the expected scenarios
        assert scenario in ["rain_clearing_soon", "light_fighter", "post_solstice_grind", "stable_focus_light"]
    
    def test_generate_uplift_data_returns_expected_keys(self):
        """Test that generate_uplift_data returns all expected keys."""
        from services.uplift_engine import generate_uplift_data
        
        with patch('services.uplift_engine.get_daylight_delta') as mock_solar, \
             patch('services.uplift_engine.fetch_daily_weather') as mock_weather:
            
            mock_solar.return_value = {
                "day_len_sec": 36000,
                "delta_daily_sec": 120,
                "delta_weekly_sec": 840,
                "delta_solstice_sec": 3600,
                "sunrise": datetime(2024, 1, 15, 8, 0),
                "sunset": datetime(2024, 1, 15, 18, 0),
            }
            
            mock_weather.return_value = {
                "forecast": [{"code": 0, "temp_max": 10, "is_good": True, "is_bad": False}],
                "today": {"code": 0, "is_good": True, "is_bad": False},
                "analysis": {"temp_trend": "stable", "good_streak_length": 1},
            }
            
            result = generate_uplift_data(47.37, 8.54, "Zurich", lang="en")
            
            assert "text" in result
            assert "facts" in result
            assert "highlights" in result
            assert isinstance(result["text"], str)
            assert len(result["text"]) > 0
    
    def test_language_support(self):
        """Test that both languages work."""
        from services.uplift_engine import generate_uplift_data
        
        with patch('services.uplift_engine.get_daylight_delta') as mock_solar, \
             patch('services.uplift_engine.fetch_daily_weather') as mock_weather:
            
            mock_solar.return_value = {
                "day_len_sec": 36000,
                "delta_daily_sec": 120,
                "delta_weekly_sec": 840,
                "delta_solstice_sec": 3600,
                "sunrise": datetime(2024, 1, 15, 8, 0),
                "sunset": datetime(2024, 1, 15, 18, 0),
            }
            
            mock_weather.return_value = {
                "forecast": [{"code": 0, "temp_max": 10, "is_good": True, "is_bad": False}],
                "today": {"code": 0, "is_good": True, "is_bad": False},
                "analysis": {"temp_trend": "stable"},
            }
            
            result_en = generate_uplift_data(47.37, 8.54, lang="en")
            result_de = generate_uplift_data(47.37, 8.54, lang="de")
            
            # Both should return valid results
            assert len(result_en["text"]) > 0
            assert len(result_de["text"]) > 0


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_extreme_latitudes(self):
        """Test behavior with extreme latitudes."""
        from services.uplift_engine import generate_uplift_data
        
        with patch('services.uplift_engine.get_daylight_delta') as mock_solar, \
             patch('services.uplift_engine.fetch_daily_weather') as mock_weather:
            
            # Simulate polar region with very long day
            mock_solar.return_value = {
                "day_len_sec": 86400,  # 24 hours
                "delta_daily_sec": 0,
                "delta_weekly_sec": 0,
                "delta_solstice_sec": 0,
                "sunrise": None,
                "sunset": None,
            }
            mock_weather.return_value = {}
            
            result = generate_uplift_data(70.0, 25.0)  # Northern Norway
            assert "text" in result
    
    def test_missing_solar_data(self):
        """Test handling when solar data is unavailable."""
        from services.uplift_engine import generate_uplift_data
        
        with patch('services.uplift_engine.get_daylight_delta') as mock_solar, \
             patch('services.uplift_engine.fetch_daily_weather') as mock_weather:
            
            mock_solar.return_value = {}
            mock_weather.return_value = {}
            
            result = generate_uplift_data(47.37, 8.54)
            assert "text" in result
            assert "facts" in result
    
    def test_invalid_language_fallback(self):
        """Test that invalid language falls back to English."""
        from services.uplift_engine import generate_uplift_data
        
        with patch('services.uplift_engine.get_daylight_delta') as mock_solar, \
             patch('services.uplift_engine.fetch_daily_weather') as mock_weather:
            
            mock_solar.return_value = {
                "day_len_sec": 36000,
                "delta_daily_sec": 120,
                "sunrise": datetime(2024, 1, 15, 8, 0),
                "sunset": datetime(2024, 1, 15, 18, 0),
            }
            mock_weather.return_value = {"forecast": [], "today": {}, "analysis": {}}
            
            # Invalid language should fallback gracefully
            result = generate_uplift_data(47.37, 8.54, lang="fr")
            assert "text" in result
