import functions_framework

@functions_framework.http
def analyze_jump_cloud(request):
    # This grabs the raw text before it even becomes JSON
    raw_data = request.get_data(as_text=True)
    data = request.get_json(silent=True) or {}
    
    # We look for 'a' or 'lat' or 'lat1' - covering all bases
    lt1 = data.get('a') or data.get('lat') or data.get('lat1') or 0
    lt2 = data.get('c') or data.get('prev_lat') or data.get('lat2') or 0

    # If it's still 0, we'll send back the raw text so we can see the error
    return {
        "status": "Check Raw Data" if lt1 == 0 else "Data Received",
        "received_lat1": lt1,
        "received_lat2": lt2,
        "what_google_saw": raw_data
    }
