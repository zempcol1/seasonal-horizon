from flask import Flask, render_template, jsonify, request
from config import Config
from services.solar_service import get_sun_times, get_daylight_stats
from services.uplift_engine import generate_uplift
import requests
from datetime import date

# explizit static_url_path setzen, damit statische Dateien nur unter /static/ liegen
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config.from_object(Config)

@app.route("/")
def index():
	# pass ISO date (YYYY-MM-DD) so template can show current date
	return render_template("index.html", today=date.today().isoformat())

@app.route("/api/solar")
def api_solar():
	lat = request.args.get("lat", type=float) or Config.DEFAULT_LAT
	lon = request.args.get("lon", type=float) or Config.DEFAULT_LON
	try:
		sun = get_sun_times(lat, lon)
		stats = get_daylight_stats(lat, lon)
		# keep response small and clear
		return jsonify({
			"sun_times": sun,
			"daylight": stats
		})
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route("/api/uplift")
def api_uplift():
	lat = request.args.get("lat", type=float) or Config.DEFAULT_LAT
	lon = request.args.get("lon", type=float) or Config.DEFAULT_LON
	try:
		text = generate_uplift(lat, lon)
		return jsonify({"uplift": text})
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route("/api/geocode")
def api_geocode():
	city = request.args.get("city", type=str)
	if not city:
		return jsonify({"error": "missing city parameter"}), 400
	try:
		url = "https://nominatim.openstreetmap.org/search"
		params = {"q": city, "format": "json", "limit": 1}
		headers = {"User-Agent": "SeasonalHorizon/1.0 (contact@example.com)"}
		r = requests.get(url, params=params, headers=headers, timeout=6)
		r.raise_for_status()
		data = r.json()
		if not data:
			return jsonify({"error": "no results"}), 404
		top = data[0]
		lat = float(top.get("lat"))
		lon = float(top.get("lon"))
		name = top.get("display_name", city)
		return jsonify({"lat": lat, "lon": lon, "name": name})
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route("/api/geocode_suggest")
def api_geocode_suggest():
    q = request.args.get("city", type=str)
    if not q:
        return jsonify([])  # no query => empty list
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": q, "format": "json", "limit": 8, "addressdetails": 0}
        headers = {"User-Agent": "SeasonalHorizon/1.0 (contact@example.com)"}
        r = requests.get(url, params=params, headers=headers, timeout=6)
        r.raise_for_status()
        data = r.json()
        out = []
        for item in data:
            try:
                out.append({
                    "name": item.get("display_name"),
                    "lat": float(item.get("lat")),
                    "lon": float(item.get("lon"))
                })
            except Exception:
                continue
        return jsonify(out)
    except Exception:
        return jsonify([]), 200

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
