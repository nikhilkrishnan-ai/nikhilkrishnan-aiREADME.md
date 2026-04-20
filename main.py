import functions_framework

@functions_framework.http
def analyze_jump_cloud(request):
    request_json = request.get_json(silent=True)
    
    # We get the speed from the data sent to the URL
    speed = request_json.get('speed', 0) if request_json else 0
    
    if speed > 47.5:
        return {"status": "SPOOF_DETECTED", "speed": speed, "analyst": "NK"}, 200
    else:
        return {"status": "Clear", "speed": speed, "analyst": "NK"}, 200
