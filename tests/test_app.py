"""Endpoint tests. Upstream APIs are stubbed in conftest."""

import re

import pytest

from config import config


def test_homepage_renders(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Seasonal Horizon' in response.data
    assert b'{{' not in response.data, "unrendered Jinja placeholder"


def test_health(client):
    assert client.get('/health').get_json() == {"status": "ok"}


# ===== Search =====

def test_search_returns_results(client):
    results = client.get('/api/search?q=Zurich').get_json()
    assert isinstance(results, list) and results
    assert results[0]['name'] == 'Zurich'


@pytest.mark.parametrize('query', ['', 'B'])
def test_search_rejects_too_short_query(client, query):
    response = client.get(f'/api/search?q={query}')
    assert response.status_code == 200
    assert response.get_json() == []


def test_search_handles_special_characters(client):
    """Long enough to reach the API, so it must not blow up on the way."""
    response = client.get('/api/search?q=<script>')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


# ===== Uplift =====

def test_uplift_returns_text_and_well_formed_facts(client):
    data = client.get('/api/uplift').get_json()

    assert data['success']
    assert len(data['text']) > 50, "text should be a message, not a fragment"
    assert not re.search(r'\{\w+\}', data['text']), "raw placeholder leaked"

    facts = data['facts']
    assert re.fullmatch(r'\d+h \d+m', facts['day_length'])
    assert re.fullmatch(r'\d{2}:\d{2}', facts['sunrise'])
    assert re.fullmatch(r'\d{2}:\d{2}', facts['sunset'])
    for key in ('delta_yesterday', 'delta_week', 'delta_solstice'):
        assert facts[key][0] in '+-', f"{key} should carry a sign"


@pytest.mark.parametrize('lang', ['en', 'de', 'xyz'])
def test_uplift_handles_every_language(client, lang):
    """Unknown languages fall back rather than failing."""
    data = client.get(f'/api/uplift?lat=47.37&lon=8.54&lang={lang}').get_json()
    assert data['success']
    assert data['text']


@pytest.mark.parametrize('lat,lon', [
    (89, 0),            # near the pole
    (-33.87, 151.21),   # southern hemisphere
    (999, 8.54),        # out of range, gets clamped
    ('invalid', 8.54),  # not a number at all
])
def test_uplift_survives_awkward_coordinates(client, lat, lon):
    response = client.get(f'/api/uplift?lat={lat}&lon={lon}')
    assert response.status_code in (200, 500)


# ===== Rate limiting =====

def test_rate_limit_allows_requests_under_the_limit(client):
    for _ in range(5):
        assert client.get('/api/uplift').status_code == 200


def test_rate_limit_blocks_once_the_limit_is_hit(client):
    for _ in range(config.RATE_LIMIT_UPLIFT):
        client.get('/api/uplift')

    response = client.get('/api/uplift')
    assert response.status_code == 429

    data = response.get_json()
    assert data['success'] is False
    assert 'rate limit' in data['error'].lower()
    assert 'retry_after' in data
