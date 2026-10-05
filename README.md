# Seasonal Horizon

A small web app that finds what is good about the season you are in. Its heart is the stretch from the winter solstice to spring: after Christmas, when the cold, grey, dark and wet start to weigh, it collects the evidence that the sun is still there, life is not gone, and the light is coming back.

Tuned for Central and Western Europe - Switzerland, Germany, Austria, the Benelux, northern and western France, northern Italy - one timezone, one climate band.

## Principles

- **Notice, don't forecast.** Each message is a true observation, measured or plausible for the region, plus at most one small invitation.
- **Evidence over comfort.** In winter, show the signals (minutes gained, the next later sunset, the first hazel catkins) rather than just saying "hang in there".
- **Weather is something to look forward to.** "Sun in two days", the light off fresh snow, the sun above the Hochnebel - not a to-do list.
- **Nothing unmeasured is stated.** A fact we could not fetch silently removes every sentence that needed it.

## Seasons

| Phase | Dates | Message | Hard facts |
|-------|-------|---------|------------|
| Darkening | Nov 1 - Dec 21 | Coziness and low light; a countdown to the turn in the last two weeks | A few |
| **Returning light** | Dec 21 - Mar 20 | Spotting the signals that spring is coming | Full signal board |
| Spring | Mar 20 - Jun 21 | Blossom, green, long evenings | A few |
| Summer | Jun 21 - Sep 22 | Abundance, warm evenings | A few |
| Autumn | Sep 22 - Oct 31 | Colours, harvest, golden light | A few |

Nature observations differ between lowland and alpine locations (from about 800 m).

## How a message is made

Each message is a **lead** plus a **companion** line.

- The lead comes from the strongest **signal** of the day: one true, good thing about today.
  - **Light**, calculated: minutes gained, sunset and sunrise milestones, the day passing a whole hour, the autumn day it is now as long as, usable light until dusk, the sun higher at noon, the first later sunsets in December.
  - **Weather**, from sunshine hours rather than weather codes, and from the past month: sun in two days, the first sun after a grey stretch, the warmest day in weeks, a brighter week ahead, UV strength, fresh snow, Hochnebel with sun above it.
  - **Nature tied to measurements**: bees above ten degrees, toads on mild wet nights, pollen - the last only on one day in seven, out of consideration for hay fever.
  - **Customs**, around Zurich and Aargau only: Sechseläuten, Knabenschiessen, Samichlaus, the Christmas markets in Advent.
  - The day of an event (the solstice, the equinox, Sechseläuten) always leads. When nothing stands out, a line about the phase of the year does.
- The companion is a nature line for the month and region (lowland or alpine), tagged by weather so a frost line only appears on a frosty day. On a sunny winter day it is a suggestion for getting out into the sun instead.
- The message stays the same all day for one place, and each pool steps through its lines day by day, so nothing repeats until the pool is used up. "Another thought" asks for a different one.

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
│   ├── solar_service.py  # Daylight, calculated with astral
│   ├── weather_service.py # Forecast and sunshine hours
│   ├── uplift_engine.py  # Signals and message composition
│   ├── uplift_content.py # Content templates (EN/DE)
│   ├── geocoding.py      # City search
│   ├── api_client.py     # HTTP retries and caching
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
- `GET /api/uplift?lat=<lat>&lon=<lon>&lang=<en|de>&v=<n>` - Today's message and figures; `v` > 0 asks for another message
- `GET /api/search?q=<query>` - Search for cities by name
- `GET /health` - Health check endpoint

## Changelog

- **v0.6** - Rebuilt around what is good about today, tuned for Central Europe: light calculated locally, weather read from sunshine hours and the past month, nature lines by region and weather, customs for Zurich and Aargau, and one message a day with a button for another
- **v0.5** - Winter leads with the returning light: spring signs by region, suggestions for using the sun, hemisphere-aware seasons, a short mode for the tropics, and a guarantee that nothing is stated that was not measured
- **v0.4.1** - Added basic logging, rate limiting and more tests. Cleaner mobile layout
- **v0.4** - Multi-language support (English/German), rate limiting, improved German translations
- **v0.3** - Smart forecast narratives with 7-day weather analysis
- **v0.2** - Location selection and improved text generation
- **v0.1** - Initial release