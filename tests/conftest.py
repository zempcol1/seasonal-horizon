"""Pytest configuration and fixtures."""

import pytest
import sys
import os

# Ensure the app module is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
    limiter = get_limiter()
    limiter._requests.clear()
    yield
