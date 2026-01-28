# Seasonal Horizon

A Flask application designed to help you stay connected with the natural rhythm of daylight throughout the year. During the dark winter months, it provides encouraging context about the returning light. In summer, it reminds you to appreciate the abundance before it fades.

The core idea: every day, you receive a short, contextual message that frames the current daylight situation in a positive, motivating way—whether that means celebrating spring's rapid gains or acknowledging winter's slow but steady progress since the solstice.

## What It Does

- Displays sunrise, sunset, and total daylight duration for your location
- Tracks daily, weekly, and seasonal changes in daylight
- Generates narrative messages that put the numbers in human context
- Uses weather forecast data to add relevant observations (e.g., "grey skies, but the light is still gaining")

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python app.py

# Run tests
pytest
```

The application will be available at `http://localhost:8080`.

## Project Structure

```
├── app.py                 # Flask application entry point
├── wsgi.py               # WSGI entry point for production
├── requirements.txt      # Python dependencies
├── services/             # Business logic modules
│   ├── solar_service.py  # Daylight calculations
│   ├── weather_service.py # Weather API integration
│   ├── uplift_engine.py  # Narrative text generation
│   └── uplift_content.py # Content templates
├── templates/            # Jinja2 HTML templates
│   └── index.html
├── static/               # Static assets
│   └── style.css
└── tests/                # Test suite
    └── test_basic.py
```

## Deployment

This application is configured for deployment on PythonAnywhere. The `wsgi.py` file serves as the WSGI entry point.

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/uplift?lat=<lat>&lon=<lon>` - Get daylight data and narrative message
- `GET /api/search?q=<query>` - Search for cities by name

## Changelog

- **v0.3** - Smart forecast narratives with 7-day weather analysis
- **v0.2** - Location selection and improved text generation
- **v0.1** - Initial release