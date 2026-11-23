import math

from flask import Flask, render_template, request, jsonify

from config import config
from services.geocoding import search_cities
from services.logging_service import get_logger, log_event
from services.rate_limiter import rate_limit
from services.uplift_engine import current_phase, generate_uplift_data

app = Flask(__name__)
app.config['DEBUG'] = config.DEBUG

logger = get_logger()
log_event('startup', f'debug={config.DEBUG}')

LANGUAGES = ('en', 'de')


def _lang():
    """The requested language, English if it is not one we have."""
    lang = request.args.get('lang', 'en')
    return lang if lang in LANGUAGES else 'en'


def _coordinate(name, default, limit):
    """A coordinate from the query, clamped to its range; None if it is not a number."""
    try:
        value = float(request.args.get(name, default))
    except ValueError:
        return None
    return max(-limit, min(limit, value)) if math.isfinite(value) else None


@app.route('/')
def index():
    # Defaults come from config so the client does not hardcode its own.
    return render_template(
        'index.html',
        version=config.VERSION,
        default_city=config.DEFAULT_CITY,
        default_lat=config.DEFAULT_LAT,
        default_lon=config.DEFAULT_LON,
        phase=current_phase(),
    )


@app.route('/api/search')
@rate_limit(config.RATE_LIMIT_SEARCH)
def search_city():
    try:
        return jsonify(search_cities(request.args.get('q', ''), _lang()))
    except Exception as e:
        log_event('error', f'search:{str(e)[:50]}')
        return jsonify([])


@app.route('/api/uplift')
@rate_limit(config.RATE_LIMIT_UPLIFT)
def api_uplift():
    lat = _coordinate('lat', config.DEFAULT_LAT, 90)
    lon = _coordinate('lon', config.DEFAULT_LON, 180)
    if lat is None or lon is None:
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400
    try:
        lang = _lang()
        # 0 is today's message; the "another" button counts up from there.
        variant = max(0, min(999, request.args.get('v', 0, type=int)))

        data = generate_uplift_data(lat, lon, lang=lang, variant=variant)
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
