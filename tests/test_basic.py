"""Basic tests for the Seasonal Horizon application."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ===== BASIC ENDPOINT TESTS =====

def test_homepage_returns_200(client):
    """Test that the homepage returns HTTP 200."""
    response = client.get('/')
    assert response.status_code == 200


def test_homepage_contains_title(client):
    """Test that the homepage contains the app title."""
    response = client.get('/')
    assert b'Seasonal Horizon' in response.data


def test_uplift_api_returns_json(client):
    """Test that the uplift API returns valid JSON with expected keys."""
    response = client.get('/api/uplift?lat=47.37&lon=8.54')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = response.get_json()
    assert 'success' in data
    
    if data['success']:
        assert 'text' in data
        assert 'facts' in data
        assert 'highlights' in data
        assert isinstance(data['text'], str)
        assert isinstance(data['facts'], dict)
        assert isinstance(data['highlights'], list)
        
        expected_keys = ['sunrise', 'sunset', 'day_length', 'delta_yesterday']
        for key in expected_keys:
            assert key in data['facts'], f"Missing key: {key}"


def test_uplift_api_with_default_location(client):
    """Test uplift API works with default location parameters."""
    response = client.get('/api/uplift')
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data


def test_search_api_returns_json(client):
    """Test that the search API returns valid JSON."""
    response = client.get('/api/search?q=Berlin')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = response.get_json()
    assert isinstance(data, list)


def test_search_api_short_query(client):
    """Test that search API handles short queries gracefully."""
    response = client.get('/api/search?q=B')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_search_api_empty_query(client):
    """Test that search API handles empty queries."""
    response = client.get('/api/search?q=')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


# ===== CONTENT QUALITY TESTS =====

class TestNarrativeContent:
    """Tests for narrative text generation quality."""
    
    def test_text_not_empty(self, client):
        """Ensure generated text is not empty."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54')
        data = response.get_json()
        
        if data['success']:
            assert len(data['text']) > 50, "Text should be meaningful, not just a few words"
    
    def test_text_contains_time_references(self, client):
        """Text should contain time-related information."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54')
        data = response.get_json()
        
        if data['success']:
            text = data['text'].lower()
            time_words = ['day', 'light', 'sun', 'minute', 'hour', 'morning', 'evening', 
                         'sunrise', 'sunset', 'daylight']
            has_time_reference = any(word in text for word in time_words)
            assert has_time_reference, "Text should reference time/light concepts"
    
    def test_highlights_are_in_text(self, client):
        """All highlights should appear in the text."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54')
        data = response.get_json()
        
        if data['success'] and data.get('highlights'):
            text = data['text']
            for highlight in data['highlights']:
                assert highlight in text, f"Highlight '{highlight}' not found in text"
    
    def test_highlights_reasonable_length(self, client):
        """Highlights should be short phrases."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54')
        data = response.get_json()
        
        if data['success'] and data.get('highlights'):
            for highlight in data['highlights']:
                word_count = len(highlight.split())
                assert word_count <= 4, f"Highlight too long: '{highlight}'"


# ===== GEOGRAPHIC/SEASONAL SCENARIO TESTS =====

class TestSeasonalScenarios:
    """Tests simulating different geographic and seasonal conditions."""
    
    def _mock_solar_data(self, day_length_hours, delta_daily_min, delta_solstice_min):
        """Create mock solar data."""
        return {
            "day_len_sec": day_length_hours * 3600,
            "delta_daily_sec": delta_daily_min * 60,
            "delta_weekly_sec": delta_daily_min * 60 * 7,
            "delta_solstice_sec": delta_solstice_min * 60,
            "sunrise": datetime(2024, 1, 15, 8, 30),
            "sunset": datetime(2024, 1, 15, 16, 30),
        }
    
    def _mock_weather_data(self, is_good=True, temp=15):
        """Create mock weather data."""
        return {
            "forecast": [
                {"code": 0 if is_good else 61, "temp_max": temp, "is_good": is_good, "is_bad": not is_good}
                for _ in range(7)
            ],
            "today": {"code": 0 if is_good else 61, "is_good": is_good, "is_bad": not is_good},
            "analysis": {
                "temp_trend": "stable",
                "temp_change": 0,
                "good_streak_length": 7 if is_good else 0,
                "bad_streak_length": 0 if is_good else 7,
                "weekend_outlook": "good" if is_good else "bad",
            }
        }
    
    @patch('services.uplift_engine.get_daylight_delta')
    @patch('services.uplift_engine.fetch_daily_weather')
    def test_italian_summer_positive_tone(self, mock_weather, mock_solar, client):
        """Summer in Italy should produce positive, abundant-light messaging."""
        # Rome in June: ~15h daylight, peak light
        mock_solar.return_value = self._mock_solar_data(
            day_length_hours=15.5, 
            delta_daily_min=0,  # Near solstice, minimal change
            delta_solstice_min=0
        )
        mock_weather.return_value = self._mock_weather_data(is_good=True, temp=28)
        
        response = client.get('/api/uplift?lat=41.90&lon=12.50')  # Rome
        data = response.get_json()
        
        assert data['success']
        text = data['text'].lower()
        
        # Should mention long days or peak light
        positive_indicators = ['peak', 'longest', 'maximum', 'abundant', '15h', 'generous']
        has_positive = any(ind in text for ind in positive_indicators)
        
        # Should NOT focus on darkness or loss
        negative_indicators = ['dark', 'short days', 'losing light', 'winter']
        has_negative = any(ind in text for ind in negative_indicators)
        
        assert has_positive or not has_negative, "Summer text should be positive about light"
    
    @patch('services.uplift_engine.get_daylight_delta')
    @patch('services.uplift_engine.fetch_daily_weather')
    def test_norwegian_winter_encouraging_tone(self, mock_weather, mock_solar, client):
        """Winter in Norway should acknowledge darkness but be encouraging about gains."""
        # Tromsø in January: ~4h daylight, but gaining after solstice
        mock_solar.return_value = self._mock_solar_data(
            day_length_hours=4, 
            delta_daily_min=3,  # Gaining 3 min/day
            delta_solstice_min=45  # 45 min gained since solstice
        )
        mock_weather.return_value = self._mock_weather_data(is_good=False, temp=-5)
        
        response = client.get('/api/uplift?lat=69.65&lon=18.96')  # Tromsø
        data = response.get_json()
        
        assert data['success']
        text = data['text'].lower()
        
        # Should mention gains or progress
        progress_indicators = ['gain', 'more', 'returning', 'climb', 'progress', 'solstice', 'longer']
        has_progress = any(ind in text for ind in progress_indicators)
        
        # Should have actual daylight facts
        assert '4h' in text or 'daylight' in text or 'sunrise' in text
        
        assert has_progress, "Winter text should mention light gains or progress"
    
    @patch('services.uplift_engine.get_daylight_delta')
    @patch('services.uplift_engine.fetch_daily_weather')  
    def test_rainy_day_still_positive(self, mock_weather, mock_solar, client):
        """Even on rainy days, messaging should find something positive."""
        mock_solar.return_value = self._mock_solar_data(
            day_length_hours=10, 
            delta_daily_min=2,
            delta_solstice_min=120
        )
        mock_weather.return_value = self._mock_weather_data(is_good=False, temp=12)
        
        response = client.get('/api/uplift?lat=51.50&lon=-0.12')  # London
        data = response.get_json()
        
        assert data['success']
        text = data['text'].lower()
        
        # Should acknowledge weather but also mention light
        has_light_mention = any(word in text for word in ['light', 'day', 'sun', 'minutes'])
        assert has_light_mention, "Even rainy day text should discuss daylight"
    
    @patch('services.uplift_engine.get_daylight_delta')
    @patch('services.uplift_engine.fetch_daily_weather')  
    def test_spring_acceleration_mentioned(self, mock_weather, mock_solar, client):
        """During spring, rapid gains should be highlighted."""
        # March: rapid gains of 3-4 min/day
        mock_solar.return_value = self._mock_solar_data(
            day_length_hours=12, 
            delta_daily_min=4,  # Rapid spring gains
            delta_solstice_min=180
        )
        mock_weather.return_value = self._mock_weather_data(is_good=True, temp=14)
        
        with patch('services.uplift_engine.date') as mock_date:
            mock_date.today.return_value = date(2024, 3, 20)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            
            response = client.get('/api/uplift?lat=52.52&lon=13.40')  # Berlin
            data = response.get_json()
        
        assert data['success']
        text = data['text'].lower()
        
        # Should mention speed of change
        speed_indicators = ['fast', 'rapid', 'accelerat', 'sprint', 'steep', 'quick']
        has_speed = any(ind in text for ind in speed_indicators)
        
        # Or at minimum mention the minutes gained
        has_minutes = '4 minute' in text or '+4' in text or '4 min' in text
        
        assert has_speed or has_minutes, "Spring text should highlight rapid gains"


# ===== FACTS VALIDATION TESTS =====

class TestFactsAccuracy:
    """Tests to ensure facts are reasonable."""
    
    def test_day_length_format(self, client):
        """Day length should be in Xh Ym format."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54')
        data = response.get_json()
        
        if data['success']:
            day_length = data['facts']['day_length']
            assert 'h' in day_length and 'm' in day_length
    
    def test_sunrise_sunset_format(self, client):
        """Times should be in HH:MM format."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54')
        data = response.get_json()
        
        if data['success']:
            sunrise = data['facts']['sunrise']
            sunset = data['facts']['sunset']
            
            if sunrise != "--:--":
                assert ':' in sunrise
                assert len(sunrise) == 5
            
            if sunset != "--:--":
                assert ':' in sunset
                assert len(sunset) == 5
    
    def test_delta_has_sign(self, client):
        """Delta values should have + or - prefix."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54')
        data = response.get_json()
        
        if data['success']:
            delta_yesterday = data['facts']['delta_yesterday']
            # Should start with + or - or be 0
            assert delta_yesterday.startswith('+') or delta_yesterday.startswith('-') or '0' in delta_yesterday
