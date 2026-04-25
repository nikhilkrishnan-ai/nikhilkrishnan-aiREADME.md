import math
from datetime import datetime, timedelta

def get_velocity_forensic(p1, p2, use_haversine=False):
    """
    Calculates velocity between two points with a performance pre-filter.
    """
    # 1. Error Handling: Detect nulls or corrupted data structures
    try:
        lat1, lon1 = float(p1['lat']), float(p1['lon'])
        lat2, lon2 = float(p2['lat']), float(p2['lon'])
        ts1, ts2 = p1['ts'], p2['ts']
    except (TypeError, ValueError, KeyError):
        return None, 0

    # Calculate time difference in hours
    dt = (ts2 - ts1).total_seconds()
    if dt <= 0: 
        return None, 0 # Ignore zero-time or backdated points
    
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    # 2. Optimized Euclidean Pre-filter for local points (< ~1.1km)
    if abs(d_lat) < 0.01 and abs(d_lon) < 0.01 and not use_haversine:
        # Flat-plane approximation for speed
        km_per_deg_lat = 111.32
        # Adjusting longitude based on the average latitude
        km_per_deg_lon = 40075 * math.cos(math.radians(lat1)) / 360
        dist = math.sqrt((d_lat * km_per_deg_lat)**2 + (d_lon * km_per_deg_lon)**2)
    else:
        # 3. Fallback to Haversine for large jumps or precision
        r = 6371  # Earth radius in km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        d_phi = math.radians(d_lat)
        d_lambda = math.radians(d_lon)
        a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda/2)**2
        dist = 2 * r * math.atan2(math.sqrt(a), math.sqrt(1-a))

    velocity = dist / (dt / 3600)
    return velocity, dist

def process_forensic_stream(data_stream, velocity_threshold=250):
    """
    Main processing loop with Moving Average Windowing.
    """
    cleaned_results = []
    valid_window = [] # Store last 3 'non-jump' points
    
    for current_pt in data_stream:
        # Initial point setup
        if not valid_window:
            if current_pt.get('lat') is not None and current_pt.get('lon') is not None:
                current_pt['is_jump'] = False
                valid_window.append(current_pt)
                cleaned_results.append(current_pt)
            continue

        # Compare current point against the last valid anchor
        last_anchor = valid_window[-1]
        velocity, distance = get_velocity_forensic(last_anchor, current_pt)
        
        # 4. Moving Average / Jitter Logic
        if velocity is not None and velocity > velocity_threshold:
            current_pt['is_jump'] = True
            current_pt['velocity_flag'] = round(velocity, 2)
            # CRITICAL: We do NOT add this jump point to our window.
        else:
            current_pt['is_jump'] = False
            current_pt['velocity_flag'] = round(velocity, 2) if velocity else 0
            valid_window.append(current_pt)
            # Keep the window to the last 3 clean points
            if len(valid_window) > 3:
                valid_window.pop(0)

        cleaned_results.append(current_pt)
        
    return cleaned_results
    # --- FINAL TEST BLOCK (Internal File Writing) ---
if __name__ == "__main__":
    now = datetime.now()
    
    test_data = [
        {'ts': now, 'lat': 24.4539, 'lon': 54.3773},
        {'ts': now + timedelta(minutes=5), 'lat': 24.4540, 'lon': 54.3774},
        {'ts': now + timedelta(minutes=10), 'lat': 25.2048, 'lon': 55.2708},
        {'ts': now + timedelta(minutes=15), 'lat': 24.4541, 'lon': 54.3775},
        {'ts': now + timedelta(minutes=20), 'lat': None, 'lon': 54.3776},
    ]

    # This creates the file automatically from inside Python
    with open("nk_forensic_report.txt", "w") as f:
        f.write("--- GPS JUMP ANALYSIS REPORT ---\n")
        f.write(f"Generated for: Nk\n")
        f.write(f"Timestamp: {datetime.now()}\n\n")
        
        results = process_forensic_stream(test_data)

        for i, pt in enumerate(results):
            status = "JUMP_DETECTED" if pt.get('is_jump') else "NORMAL"
            v = pt.get('velocity_flag', 0)
            output_line = f"Point {i}: {status} | Lat: {pt['lat']} | Vel: {v} km/h\n"
            
            # This prints to the screen AND writes to the file
            print(output_line.strip())
            f.write(output_line)

    print("\n[SUCCESS] Report saved to 'nk_forensic_report.txt'")