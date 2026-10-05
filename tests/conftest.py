"""Pytest configuration and fixtures."""

import os
import sys
from datetime import date, timedelta
from unittest.mock import patch

import pytest

# Ensure the app module is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _weather_payload(days=7):
    start = date.today()
    return {
        "elevation": 422,
        "daily": {
            "time": [str(start + timedelta(days=i)) for i in range(days)],
            "weathercode": [0, 1, 3, 61, 2, 0, 0][:days],
            "temperature_2m_max": [8, 9, 11, 10, 12, 13, 14][:days],
            "temperature_2m_min": [1, 2, 3, 4, 4, 5, 6][:days],
            "sunshine_duration": [h * 3600 for h in (6, 5, 1, 0, 4, 7, 7)][:days],
            "daylight_duration": [10 * 3600] * days,
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

    Each service imports request_json into its own namespace, so both are
    patched separately. Without this the tests took minutes on a bad
    connection and quietly changed meaning depending on the live forecast.
    Daylight is calculated, so it needs no stub.
    """
    from services import geocoding, weather_service

    weather_service._cache.clear()
    geocoding._cache.clear()

    with patch.object(weather_service, 'request_json', return_value=_weather_payload()), \
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
