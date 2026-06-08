import os
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    origins=(
        os.environ.get("ALLOWED_ORIGINS", "").split(",")
        if os.environ.get("ALLOWED_ORIGINS")
        else []
    ),
)

API_KEY = os.environ.get("GEOSENSE_API_KEY")


@app.route('/')
def home():
    return "SERVER IS LIVE"


@app.route('/api/analyze-jump', methods=['POST'])
def analyze_jump():
    if API_KEY:
        provided_key = request.headers.get("X-Api-Key")
        if provided_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    raw_speed = data.get('speed')
    if raw_speed is None:
        return jsonify({"error": "Missing required field: speed"}), 400

    try:
        speed = float(raw_speed)
    except (TypeError, ValueError):
        return jsonify({"error": "Field 'speed' must be a number"}), 400

    status = "SPOOFING DETECTED" if speed > 150 else "Clear"

    return jsonify({
        "input_speed": speed,
        "status": status,
        "time": str(datetime.now())
    }), 200


if __name__ == "__main__":
    print("--- GEOSENSE STARTING ON PORT 5001 ---")
    app.run(host='127.0.0.1', port=5001, debug=False)
