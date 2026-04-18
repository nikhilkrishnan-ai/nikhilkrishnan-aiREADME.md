import json
import math
import sys
sys.stdout.reconfigure(encoding='utf-8')
def parse_coords(point_str):
    """Parse coordinates from format: '24.3198761°, 54.5381226°'"""
    # Handle both proper and corrupted degree symbols
    point_str = point_str.replace('Â°', '°').replace('Â', '').replace('', '')
    parts = point_str.split('°, ')
    if len(parts) == 1 and '°' not in point_str:
        parts = point_str.split(', ')
    lat = float(parts[0].replace('°', ''))
    lon = float(parts[1].replace('°', '').strip())
    return (lat, lon)

def haversine_distance(coord1, coord2):
    """Calculate distance between two GPS coordinates in meters"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    R = 6371000  # Earth radius in meters
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

# Load timeline data
with open('Timelineapril7.json', 'r') as f:
    timeline_data = json.load(f)

print("=" * 70)
print("GPS JUMP ANALYSIS - April 7, 2026 Timeline")
print("=" * 70)

anomalies = []

for entry_idx, entry in enumerate(timeline_data):
    points = entry['timelinePath']
    start_time = entry['startTime']
    end_time = entry['endTime']
    
    print(f"\n📍 Entry {entry_idx + 1}: {start_time[11:19]} to {end_time[11:19]}")
    print("-" * 70)
    
    for i in range(len(points) - 1):
        current_point = points[i]
        next_point = points[i + 1]
        
        current_coords = parse_coords(current_point['point'])
        next_coords = parse_coords(next_point['point'])
        
        distance = haversine_distance(current_coords, next_coords)
        
        current_time = current_point['time']
        next_time = next_point['time']
        
        # Flag as anomaly if jump > 50 meters
        if distance > 50:
            anomalies.append({
                'entry': entry_idx + 1,
                'from_time': current_time[11:19],
                'to_time': next_time[11:19],
                'from_point': current_point['point'],
                'to_point': next_point['point'],
                'distance': distance
            })
            print(f"⚠️  JUMP DETECTED: {distance:.2f}m")
            print(f"   From: {current_point['point']} at {current_time[11:19]}")
            print(f"   To:   {next_point['point']} at {next_time[11:19]}")
            print()

print("\n" + "=" * 70)
print(f"SUMMARY: Found {len(anomalies)} GPS jumps > 50 meters")
print("=" * 70)

if anomalies:
    for i, anom in enumerate(anomalies, 1):
        print(f"\n{i}. Entry {anom['entry']} - {anom['distance']:.2f}m jump")
        print(f"   {anom['from_time']} → {anom['to_time']}")
        print(f"   {anom['from_point']} → {anom['to_point']}")
else:
    print("\n✅ No significant GPS jumps detected!")
