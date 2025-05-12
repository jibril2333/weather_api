from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # 允许跨域访问

def get_coordinates(city_name):
    # 简化版城市 -> 经纬度映射，可扩展或用 geocoding API 替代
    city_map = {
        "tokyo": (35.6895, 139.6917),
        "osaka": (34.6937, 135.5023),
        "kyoto": (35.0116, 135.7681),
        "sapporo": (43.0618, 141.3545)
    }
    return city_map.get(city_name.lower())

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    coords = get_coordinates(city)
    if not coords:
        return jsonify({"error": "City not supported"}), 400

    lat, lon = coords
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Asia/Tokyo",
        "models": "jma_seamless"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather"}), 500

    data = response.json()
    return jsonify({
        "city": city,
        "date": data["daily"]["time"][0],
        "temperature_max": data["daily"]["temperature_2m_max"][0],
        "temperature_min": data["daily"]["temperature_2m_min"][0]
    })

if __name__ == "__main__":
    app.run(debug=True)
