from flask import Flask, render_template, request, jsonify

from config import config
from services.api_client import TTLCache, request_json
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
_geo_cache = TTLCache(config.CACHE_TTL_GEO)


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
    cached = _geo_cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        data = request_json(url, {"name": query, "count": 8, "language": "en"})
        if not data:
            return jsonify([])

        results = data.get('results', [])
        _geo_cache.set(cache_key, results)
        return jsonify(results)
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
