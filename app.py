import os
from flask import Flask, render_template, request, jsonify
import requests
import time
import logging

app = Flask(__name__)

# Production configuration
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
app.config['PROPAGATE_EXCEPTIONS'] = True

# Configure logging for production
if not app.debug:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Simple cache for geocoding
_geo_cache = {}
_geo_cache_ttl = 3600  # 1 hour

def _request_with_retry(url, params, max_retries=3, timeout=6):
    """Make HTTP request with retry logic."""
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            time.sleep(0.3 * (attempt + 1))
        except requests.exceptions.RequestException:
            time.sleep(0.2 * (attempt + 1))
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search_city():
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    cache_key = query.lower()
    if cache_key in _geo_cache:
        data, ts = _geo_cache[cache_key]
        if time.time() - ts < _geo_cache_ttl:
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
        app.logger.exception("Search error")
        return jsonify([])

@app.route('/api/uplift')
def api_uplift():
    from services.uplift_engine import generate_uplift_data
    try:
        lat = float(request.args.get('lat', 47.37))
        lon = float(request.args.get('lon', 8.54))
        city = request.args.get('city', '')
        lang = request.args.get('lang', 'en')
        
        # Validate language
        if lang not in ['en', 'de']:
            lang = 'en'
        
        data = generate_uplift_data(lat, lon, city, lang=lang)
        return jsonify({"success": True, **data})
    except Exception as e:
        app.logger.exception("Uplift error")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Only for local development
    app.run(debug=True, port=8080)
