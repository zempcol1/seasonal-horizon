# Seasonal Horizon

A small web app that finds what is good about the season you are in. Its heart is the stretch from the winter solstice to spring: when the cold, grey and dark start to weigh, it collects the evidence that the sun is still there and the light is coming back.

Tuned for Central and Western Europe (Switzerland, Germany, Austria, the Benelux, northern France and Italy).

## How it works

- One short message a day: a true, good thing about today, plus a line from nature. The same all day for one place; "Another thought" asks for a different one.
- Light is calculated (minutes gained, later sunsets, the sun higher at noon); weather comes from Open-Meteo's sunshine hours; nature lines follow month, region (lowland or alpine) and weather.
- Nothing is stated that was not measured, and shrinking days are never the topic.
- English and German.

## Run locally

```bash
pip install -r requirements-dev.txt
python app.py        # http://localhost:8080
pytest
```

## Changelog

- **v0.6.1** - Made for the iPhone home screen: seasonal icon, no white bar, settings that stay put
- **v0.6** - Rebuilt around what is good about today: light calculated, weather from sunshine hours, nature by region and weather, seasonal look
- **v0.5** - Winter leads with the returning light
- **v0.4** - English and German, rate limiting
- **v0.3** - Forecast narratives
- **v0.2** - Location selection
- **v0.1** - Initial release
