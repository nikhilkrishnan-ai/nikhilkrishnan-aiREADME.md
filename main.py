import functions_framework
import math

@functions_framework.http
def analyze_jump_cloud(request):
    data = request.get_json(silent=True) or {}
    
    # We use .get() with a default of 0.0 to prevent crashing
    lat = float(data.get('lat', 0.0))
    lon = float(data.get('lon', 0.0))
    p_lat = float(data.get('prev_lat', 0.0))
    p_lon = float(data.get('prev_lon', 0.0))
    seconds = float(data.get('seconds_elapsed', 1.0))

    # Haversine calculation
    R = 6371.0
    dlat = math.radians(lat - p_lat)
    dlon = math.radians(lon - p_lon)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(p_lat)) * math.cos(math.radians(lat)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    speed_kmh = (distance / seconds) * 3600 if seconds > 0 else 0

    return {
        "status": "SPOOF_DETECTED" if speed_kmh > 200 else "Clear",
        "debug_info": {
            "received_lat": lat,
            "received_prev_lat": p_lat,
            "calculated_distance_km": round(distance, 4),
            "calculated_speed_kmh": round(speed_kmh, 2)
        }
    }, 200
