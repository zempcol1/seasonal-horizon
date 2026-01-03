# Seasonal Horizon

**Seasonal Horizon** is a Python/Flask web application designed to help users visualize and look forward to the changing seasons. Its primary goal is to combat "seasonal blues" by quantifying the rate of change towards better days.

While currently optimized to help users overcome winter by tracking the approach of spring, the architecture is designed to be season-agnostic, allowing for future extensions that track the approach of autumn or other seasonal shifts.

### Mission
To provide a daily psychological boost by visualizing positive environmental changes. It answers the question: "How is nature shifting around me right now?"

---

## Core Features

### 1. Smart Location Context
* **Auto-Detection:** The app attempts to approximate the user's location via IP address on the first visit.
* **Manual Override:** Users can search for and select specific cities to track the seasonal progression of different latitudes.

### 2. Daylight Dynamics
* **Daily Gain:** Precisely calculates how many minutes and seconds of daylight are gained (or lost) compared to the previous day.
* **Forecast:** Projects total daylight accumulation for the next 7 days and 30 days.
* **Golden Hour:** Calculates specific times for sunrise and sunset to help users capture the most sunlight.

### 3. Phenology & Nature Outlook
* **Temperature Thresholds:** Uses historical weather data to estimate when the "average" temperature will consistently cross comfortable milestones (e.g., above 10°C / 50°F).
* **Bio-Indicators:** A database of natural events linked to the current date and latitude (e.g., bird migrations, first blooms, dormancy periods).

### 4. Daily Seasonal Pulse (The "Uplift")
* A dynamic, generative text engine that creates a unique 1-2 sentence summary every day.
* **Logic:** It combines the hard data (daylight minutes) with nature facts to create a narrative.
* **Goal:** To encourage the user to check the app frequently.
* **Example Output:** "You have gained 3 minutes of light since yesterday; listen for the Great Tit's song, which typically shifts pitch this week as they begin to mark territory."

---

## Tech Stack & Libraries

* **Backend:** Python 3.10+, Flask
* **Frontend:** HTML5, CSS3 (TailwindCSS recommended for clean, neutral styling), Jinja2 templates.
* **Astronomy:** `astral` or `suntime` libraries for high-precision solar calculations.
* **Geolocation:** `geopy` or generic IP-geolocation APIs.
* **Data Source:** Open-Meteo API for historical climate data and weather forecasts.

---

## Project Structure

```text
seasonal_horizon/
├── app.py                 # Main Flask application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/               # Stylesheets
│   ├── js/                # Interactive elements
│   └── assets/            # Backgrounds and icons
├── templates/
│   ├── base.html          # Base template
│   ├── dashboard.html     # Main view showing stats and "Pulse"
│   └── settings.html      # Location and preferences
└── services/
    ├── solar_service.py   # Logic for sunrise, sunset, and day length delta
    ├── weather_service.py # Integration with Open-Meteo
    └── uplift_engine.py   # Logic to generate the daily encouraging text