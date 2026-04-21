import functions_framework

@functions_framework.http
def analyze_jump_cloud(request):
    # This handles the data coming from your PowerShell test
    request_json = request.get_json(silent=True)
    
    # 47.5 m/s is roughly 171 km/h—fast enough to be a 'jump' or spoof
    THRESHOLD = 47.5 
    
    speed = 0
    if request_json and 'speed' in request_json:
        speed = request_json['speed']

    if speed > THRESHOLD:
        response = {
            "status": "SPOOF_DETECTED",
            "speed_observed": speed,
            "threshold_limit": THRESHOLD,
            "analyst": "NK_Forensics"
        }
    else:
        response = {
            "status": "Clear",
            "speed_observed": speed,
            "message": "Movement within normal limits."
        }

    return response, 200
