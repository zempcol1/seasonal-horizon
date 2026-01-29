import os
from flask import Flask, render_template, request, jsonify
import requests
import time

from config import config
from services.logging_service import get_logger, log_event
from services.rate_limiter import rate_limit

app = Flask(__name__)

# Configuration
app.config['DEBUG'] = config.DEBUG

# Logger
logger = get_logger()

# Log startup
log_event('startup', f'debug={config.DEBUG}')

# Simple cache for geocoding
_geo_cache = {}


def _request_with_retry(url, params, max_retries=None, timeout=None):
    """Make HTTP request with retry logic."""
    max_retries = max_retries or config.API_MAX_RETRIES
    timeout = timeout or config.API_TIMEOUT
    
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            time.sleep(0.3 * (attempt + 1))
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                log_event('api_fail', f'{url}:{str(e)[:50]}')
            time.sleep(0.2 * (attempt + 1))
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/search')
@rate_limit(config.RATE_LIMIT_SEARCH)
def search_city():
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    cache_key = query.lower()
    if cache_key in _geo_cache:
        data, ts = _geo_cache[cache_key]
        if time.time() - ts < config.CACHE_TTL_GEO:
            return jsonify(data)
    
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        data = _request_with_retry(url, {"name": query, "count": 8, "language": "en"})
        if data:
            results = data.get('results', [])
            _geo_cache[cache_key] = (results, time.time())
            return jsonify(results)
        return jsonify([])
    except Exception as e:
        log_event('error', f'search:{str(e)[:50]}')
        return jsonify([])


@app.route('/api/uplift')
@rate_limit(config.RATE_LIMIT_UPLIFT)
def api_uplift():
    from services.uplift_engine import generate_uplift_data
    try:
        lat = float(request.args.get('lat', config.DEFAULT_LAT))
        lon = float(request.args.get('lon', config.DEFAULT_LON))
        city = request.args.get('city', '')
        lang = request.args.get('lang', 'en')
        
        # Validate inputs
        lat = max(-90, min(90, lat))
        lon = max(-180, min(180, lon))
        if lang not in ['en', 'de']:
            lang = 'en'
        
        data = generate_uplift_data(lat, lon, city, lang=lang)
        return jsonify({"success": True, **data})
    except Exception as e:
        log_event('error', f'uplift:{str(e)[:50]}')
        return jsonify({"success": False, "error": "Could not generate data"}), 500


@app.route('/health')
def health():
    """Simple health check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
