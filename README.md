# Seasonal Horizon

Seasonal Horizon is a small Flask app that shows daily daylight dynamics and a short "uplift" message based on your location. The UI is a single-page dashboard; settings open as an overlay and are stored in the browser.

Run:
- pip install -r requirements.txt
- python app.py

Core files:
- app.py — Flask entry point and APIs
- templates/index.html — single-page dashboard
- static/css/styles.css — basic styles
- services/ — solar, weather and uplift logic