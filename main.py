import functions_framework
import math

@functions_framework.http
def analyze_jump_cloud(request):
    d = request.get_json(silent=True) or {}
    # Using very short keys to avoid typing errors
    lt1, ln1 = float(d.get('a', 0)), float(d.get('b', 0))
    lt2, ln2 = float(d.get('c', 0)), float(d.get('d', 0))

    R = 6371.0
    dlat, dlon = math.radians(lt2-lt1), math.radians(ln2-ln1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lt1)) * math.cos(math.radians(lt2)) * math.sin(dlon/2)**2
    dist = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return {
        "status": "SPOOF_DETECTED" if dist > 5 else "Clear",
        "dist_km": round(dist, 2),
        "received": {"p1": lt1, "p2": lt2}
    }
