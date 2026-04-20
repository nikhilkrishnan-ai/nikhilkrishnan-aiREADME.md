import functions_framework

@functions_framework.http
def analyze_jump_cloud(request):
    return {"status": "Connected", "message": "NK, your GitHub link is working!"}, 200
