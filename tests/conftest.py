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
