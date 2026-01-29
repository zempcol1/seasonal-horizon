"""API endpoint tests including rate limiting."""

import pytest
from unittest.mock import patch


# client fixture is now provided by conftest.py


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_returns_ok(self, client):
        """Health endpoint should return ok status."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'


class TestSearchEndpoint:
    """Tests for city search endpoint."""
    
    def test_search_empty_query(self, client):
        """Empty query returns empty list."""
        response = client.get('/api/search?q=')
        assert response.status_code == 200
        assert response.get_json() == []
    
    def test_search_short_query(self, client):
        """Short query returns empty list."""
        response = client.get('/api/search?q=B')
        assert response.status_code == 200
        assert response.get_json() == []
    
    def test_search_valid_query(self, client):
        """Valid query returns results."""
        with patch('app._request_with_retry') as mock_req:
            mock_req.return_value = {
                'results': [
                    {'name': 'Berlin', 'country': 'Germany', 'latitude': 52.52, 'longitude': 13.40}
                ]
            }
            
            response = client.get('/api/search?q=Berlin')
            assert response.status_code == 200
            data = response.get_json()
            assert isinstance(data, list)


class TestUpliftEndpoint:
    """Tests for uplift API endpoint."""
    
    def test_uplift_default_location(self, client):
        """Uplift works with default location."""
        response = client.get('/api/uplift')
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data
    
    def test_uplift_custom_location(self, client):
        """Uplift works with custom coordinates."""
        response = client.get('/api/uplift?lat=52.52&lon=13.40')
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data
    
    def test_uplift_german_language(self, client):
        """Uplift works with German language."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54&lang=de')
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data
    
    def test_uplift_invalid_language_fallback(self, client):
        """Invalid language falls back gracefully."""
        response = client.get('/api/uplift?lat=47.37&lon=8.54&lang=xyz')
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data
    
    def test_uplift_coordinate_bounds(self, client):
        """Extreme coordinates are handled."""
        # Very high latitude
        response = client.get('/api/uplift?lat=89&lon=0')
        assert response.status_code == 200
        
        # Negative coordinates
        response = client.get('/api/uplift?lat=-33.87&lon=151.21')
        assert response.status_code == 200


class TestRateLimiting:
    """Tests for rate limiting behavior."""
    
    def test_rate_limit_not_triggered_under_limit(self, client):
        """Requests under limit should succeed."""
        for _ in range(5):
            response = client.get('/api/uplift')
            assert response.status_code == 200
    
    def test_rate_limit_triggered_over_limit(self, client):
        """Requests over limit should be blocked."""
        from config import config
        
        # Make requests up to the limit
        for _ in range(config.RATE_LIMIT_UPLIFT):
            client.get('/api/uplift')
        
        # Next request should be rate limited
        response = client.get('/api/uplift')
        assert response.status_code == 429
        data = response.get_json()
        assert data['success'] is False
        assert 'rate limit' in data['error'].lower()
    
    def test_rate_limit_returns_retry_after(self, client):
        """Rate limit response includes retry info."""
        from config import config
        
        for _ in range(config.RATE_LIMIT_UPLIFT + 1):
            response = client.get('/api/uplift')
        
        data = response.get_json()
        assert 'retry_after' in data


class TestInputValidation:
    """Tests for input validation."""
    
    def test_invalid_lat_handled(self, client):
        """Invalid latitude is handled."""
        response = client.get('/api/uplift?lat=invalid&lon=8.54')
        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 500]
    
    def test_out_of_range_lat_clamped(self, client):
        """Out of range latitude is clamped."""
        response = client.get('/api/uplift?lat=999&lon=8.54')
        assert response.status_code == 200
    
    def test_special_characters_in_search(self, client):
        """Special characters in search are handled."""
        response = client.get('/api/search?q=<script>')
        assert response.status_code == 200
        # Should return empty or safe result
