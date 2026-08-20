"""Pytest configuration and fixtures."""

import os
import sys
from datetime import date, timedelta
from unittest.mock import patch

import pytest

# Ensure the app module is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _solar_payload(days=60):
    """An Open-Meteo daylight response with a plausible upward trend."""
    start = date.today() - timedelta(days=days - 1)
    return {
        "daily": {
            "daylight_duration": [30000 + i * 120 for i in range(days)],
            "sunrise": [f"{start + timedelta(days=i)}T07:30" for i in range(days)],
            "sunset": [f"{start + timedelta(days=i)}T17:30" for i in range(days)],
        }
    }


def _weather_payload(days=7):
    start = date.today()
    return {
        "daily": {
            "time": [str(start + timedelta(days=i)) for i in range(days)],
            "weathercode": [0, 1, 3, 61, 2, 0, 0][:days],
            "temperature_2m_max": [8, 9, 11, 10, 12, 13, 14][:days],
            "temperature_2m_min": [1, 2, 3, 4, 4, 5, 6][:days],
            "precipitation_sum": [0, 0, 1, 6, 0, 0, 0][:days],
            "precipitation_probability_max": [0, 10, 40, 80, 20, 0, 0][:days],
        }
    }


_GEO_PAYLOAD = {
    "results": [
        {"name": "Zurich", "country": "Switzerland", "admin1": "Zurich",
         "latitude": 47.37, "longitude": 8.54},
    ]
}


@pytest.fixture(autouse=True)
def stub_upstream():
    """
    Keep the suite off the network.

    Each service imports request_json into its own namespace, so all three are
    patched separately. Without this the tests took minutes on a bad
    connection and quietly changed meaning depending on the live forecast.
    """
    from services import geocoding, solar_service, weather_service

    solar_service._cache.clear()
    weather_service._cache.clear()
    geocoding._cache.clear()

    with patch.object(solar_service, 'request_json', return_value=_solar_payload()), \
         patch.object(weather_service, 'request_json', return_value=_weather_payload()), \
         patch.object(geocoding, 'request_json', return_value=_GEO_PAYLOAD):
        yield


@pytest.fixture(scope="session")
def app_instance():
    """Create application instance for testing."""
    from app import app
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app_instance):
    """Create a test client for the Flask application."""
    with app_instance.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset rate limiter between tests."""
    from services.rate_limiter import get_limiter
    get_limiter()._requests.clear()
    yield
