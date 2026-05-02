from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "SERVER IS LIVE"

@app.route('/api/analyze-jump', methods=['POST'])
def analyze_jump():
    try:
        data = request.get_json(force=True)
        # We use float() to make sure Python treats it as a number
        speed = float(data.get('speed', 0))
        
        status = "SPOOFING DETECTED" if speed > 150 else "Clear"
        
        return jsonify({
            "input_speed": speed,
            "status": status,
            "time": str(datetime.now())
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("--- GEOSENSE STARTING ON PORT 5001 ---")
    app.run(host='0.0.0.0', port=5001, debug=False)