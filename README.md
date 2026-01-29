# Seasonal Horizon

A Flask application designed to help you stay connected with the natural rhythm of daylight throughout the year. During the dark winter months, it provides encouraging context about the returning light. In summer, it reminds you to appreciate the abundance before it fades.

## Features

- Displays sunrise, sunset, and total daylight duration for your location
- Tracks daily, weekly, and seasonal changes in daylight
- Generates narrative messages in English and German
- Weather-aware nature observations that adapt to current conditions
- Uses weather forecast data for contextual observations
- Built-in rate limiting and caching for production use

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python app.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=services --cov=app
```

The application will be available at `http://localhost:8080`.

## Configuration

Environment variables (all optional with sensible defaults):

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_DEBUG` | `false` | Enable debug mode |
| `API_TIMEOUT` | `8` | External API timeout (seconds) |
| `CACHE_TTL_WEATHER` | `300` | Weather cache TTL (seconds) |
| `RATE_LIMIT_UPLIFT` | `30` | Uplift API requests/minute |
| `RATE_LIMIT_SEARCH` | `60` | Search API requests/minute |
| `LOG_LEVEL` | `INFO` | Logging level |

## Project Structure

```
├── app.py                 # Flask application entry point
├── config.py              # Configuration management
├── wsgi.py               # WSGI entry point for production
├── requirements.txt      # Python dependencies
├── services/             # Business logic modules
│   ├── solar_service.py  # Daylight calculations
│   ├── weather_service.py # Weather API integration
│   ├── uplift_engine.py  # Narrative text generation
│   ├── uplift_content.py # Content templates (EN/DE)
│   ├── rate_limiter.py   # API rate limiting
│   └── logging_service.py # Minimal logging
├── templates/            # Jinja2 HTML templates
├── static/               # Static assets
└── tests/                # Test suite
```

## Deployment

This application is configured for deployment on PythonAnywhere. The `wsgi.py` file serves as the WSGI entry point.

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/uplift?lat=<lat>&lon=<lon>&lang=<en|de>` - Get daylight data and narrative
- `GET /api/search?q=<query>` - Search for cities by name
- `GET /health` - Health check endpoint

## Changelog

- **v0.4.1** - Added basic logging, rate limiting and more tests. Improved highlighting, cleaner mobile layout
- **v0.4** - Multi-language support (English/German), rate limiting, improved German translations
- **v0.3** - Smart forecast narratives with 7-day weather analysis
- **v0.2** - Location selection and improved text generation
- **v0.1** - Initial release