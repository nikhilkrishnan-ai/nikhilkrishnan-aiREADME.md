import json
import math
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_coords(point_str):
    """Parse coordinates from format: '24.3198761°, 54.5381226°' (handles corrupted encoding)"""
    # Handle both proper and corrupted degree symbols
    point_str = point_str.replace('Â°', '°').replace('Â', '')
    parts = point_str.split('°, ')
    lat = float(parts[0])
    lon = float(parts[1].replace('°', '').strip())
    return (lat, lon)

def haversine_distance(coord1, coord2):
    """Calculate distance between two GPS coordinates in kilometers"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    R = 6371  # Earth radius in km
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def time_diff_minutes(time1, time2):
    """Calculate time difference in minutes"""
    t1 = datetime.strptime(time1[11:19], '%H:%M:%S')
    t2 = datetime.strptime(time2[11:19], '%H:%M:%S')
    return abs((t2 - t1).total_seconds() / 60)

def calculate_velocity(distance_km, time_minutes):
    """Calculate velocity in km/h"""
    if time_minutes == 0:
        return 0
    return (distance_km / time_minutes) * 60

# Load timeline data
with open('Timelineapril7.json', 'r') as f:
    timeline_data = json.load(f)

report = {
    "analysis_date": "April 9, 2026",
    "data_date": "April 7, 2026",
    "spoofing_indicators": []
}

print("\n" + "="*80)
print("GPS SPOOFING DETECTION ANALYSIS - APRIL 7, 2026")
print("="*80 + "\n")

total_jumps = 0
max_velocity = 0
suspicious_points = []

for entry_idx, entry in enumerate(timeline_data):
    points = entry['timelinePath']
    start_time = entry['startTime'][11:19]
    end_time = entry['endTime'][11:19]
    
    print(f"📊 Entry {entry_idx + 1}: {start_time} to {end_time}")
    print("-" * 80)
    
    for i in range(len(points) - 1):
        current_point = points[i]
        next_point = points[i + 1]
        
        current_coords = parse_coords(current_point['point'])
        next_coords = parse_coords(next_point['point'])
        
        distance_km = haversine_distance(current_coords, next_coords)
        distance_m = distance_km * 1000
        
        current_time = current_point['time']
        next_time = next_point['time']
        
        time_minutes = time_diff_minutes(current_time, next_time)
        velocity_kmh = calculate_velocity(distance_km, time_minutes)
        
        # Spoofing indicators
        if distance_m > 100:  # More than 100 meters jump
            total_jumps += 1
            suspicious_points.append({
                'entry': entry_idx + 1,
                'from_time': current_time[11:19],
                'to_time': next_time[11:19],
                'distance_m': distance_m,
                'velocity_kmh': velocity_kmh
            })
            
            print(f"  ⚠️  POSITION JUMP: {distance_m:.2f}m ({velocity_kmh:.1f} km/h)")
            print(f"      {current_time[11:19]} → {next_time[11:19]}")
            print(f"      From: {current_point['point']}")
            print(f"      To:   {next_point['point']}")
        
        if velocity_kmh > max_velocity:
            max_velocity = velocity_kmh
        
        # Flag impossible speeds (civilian vehicle max ~180 km/h, human ~40 km/h)
        if velocity_kmh > 200:
            print(f"  🚨 IMPOSSIBLE VELOCITY: {velocity_kmh:.1f} km/h at {current_time[11:19]}")
    
    print()

# Generate report
print("="*80)
print("SUMMARY REPORT")
print("="*80 + "\n")

print(f"✓ Total Timeline Entries: {len(timeline_data)}")
print(f"✓ Total Data Points: {sum(len(e['timelinePath']) for e in timeline_data)}")
print(f"✓ Position Jumps Detected: {total_jumps}")
print(f"✓ Maximum Velocity: {max_velocity:.1f} km/h")
print(f"✓ Location: Dubai/UAE Area (approx 24.32°N, 54.53°E)\n")

print("SPOOFING LIKELIHOOD ASSESSMENT:")
print("-" * 80)

if total_jumps > 5:
    print("🔴 HIGH - Multiple significant GPS jumps detected")
    print("   Indicates: Active GPS spoofing or signal interference\n")
elif total_jumps > 2:
    print("🟡 MEDIUM - Several position anomalies detected")
    print("   Indicates: Possible signal degradation or spoofing attempts\n")
else:
    print("🟢 LOW - Minimal position anomalies")
    print("   Likely: Natural GPS receiver accuracy variations\n")

if max_velocity > 150:
    print("🔴 VELOCITY ANOMALY - Impossible speeds detected")
    print("   Indicates: Spoofing between distant locations\n")

report["spoofing_indicators"] = suspicious_points
report["total_jumps"] = total_jumps
report["max_velocity_kmh"] = max_velocity
report["assessment"] = "HIGH PROBABILITY OF GPS SPOOFING" if total_jumps > 5 else "POTENTIAL GPS ANOMALIES"

# Save report
with open('spoofing_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print("="*80)
print(f"✓ Detailed report saved to: spoofing_report.json")
print("="*80 + "\n")
