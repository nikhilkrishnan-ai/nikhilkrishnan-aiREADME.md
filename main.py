import functions_framework
import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c # Returns distance in kilometers

@functions_framework.http
def analyze_jump_cloud(request):
    data = request.get_json(silent=True)
    if not data:
        return {"error": "No data provided"}, 400

    # Current Coordinates
    curr_lat = data.get('lat')
    curr_lon = data.get('lon')
    
    # Last Known Coordinates (for testing, we send these in the request)
    prev_lat = data.get('prev_lat')
    prev_lon = data.get('prev_lon')
    time_diff = data.get('seconds_elapsed', 1)

    distance = haversine(prev_lat, prev_lon, curr_lat, curr_lon)
    # Calculate speed: Distance / Time (km per second * 3600 = km/h)
    calculated_speed = (distance / time_diff) * 3600

    # If speed > 200 km/h, it's likely a spoof or a major signal jump
    is_spoof = calculated_speed > 200

    return {
        "status": "SPOOF_DETECTED" if is_spoof else "Clear",
        "distance_km": round(distance, 2),
        "calculated_speed_kmh": round(calculated_speed, 2),
        "analyst": "NK_Forensics"
    }, 200
