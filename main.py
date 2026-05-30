import functions_framework

@functions_framework.http
def analyze_jump_cloud(request):
    # Process incoming JSON payload safely from the trigger
    payload = request.get_json(silent=True) or {}
    
    # Extract structural values sent from PowerShell / edge client
    val1 = payload.get('a', 'No Data')
    val2 = payload.get('c', 'No Data')

    # Return standard clean JSON response dictionary
    return {
        "status": "success",
        "message": "NK, telemetry ingestion pipeline active!",
        "received_a": val1,
        "received_c": val2,
        "full_payload": payload
    }
