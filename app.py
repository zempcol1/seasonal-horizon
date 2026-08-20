from flask import Flask, render_template, request, jsonify

from config import config
from services.geocoding import search_cities
from services.logging_service import get_logger, log_event
from services.rate_limiter import rate_limit
from services.uplift_engine import generate_uplift_data

app = Flask(__name__)
app.config['DEBUG'] = config.DEBUG

logger = get_logger()
log_event('startup', f'debug={config.DEBUG}')

LANGUAGES = ('en', 'de')


@app.route('/')
def index():
    # Defaults come from config so the client does not hardcode its own.
    return render_template(
        'index.html',
        version=config.VERSION,
        default_city=config.DEFAULT_CITY,
        default_lat=config.DEFAULT_LAT,
        default_lon=config.DEFAULT_LON,
    )


@app.route('/api/search')
@rate_limit(config.RATE_LIMIT_SEARCH)
def search_city():
    try:
        return jsonify(search_cities(request.args.get('q', '')))
    except Exception as e:
        log_event('error', f'search:{str(e)[:50]}')
        return jsonify([])


@app.route('/api/uplift')
@rate_limit(config.RATE_LIMIT_UPLIFT)
def api_uplift():
    try:
        lat = max(-90, min(90, float(request.args.get('lat', config.DEFAULT_LAT))))
        lon = max(-180, min(180, float(request.args.get('lon', config.DEFAULT_LON))))
        lang = request.args.get('lang', 'en')
        if lang not in LANGUAGES:
            lang = 'en'

        data = generate_uplift_data(lat, lon, lang=lang)
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
