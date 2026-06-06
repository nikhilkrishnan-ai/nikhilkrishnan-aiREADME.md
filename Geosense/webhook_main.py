
from fastapi import FastAPI, Header, HTTPException, Request
import uvicorn

app = FastAPI(title="GeoSense Data Pipeline")

# 🔒 സെക്യൂരിറ്റിക്ക് വേണ്ടിയുള്ള സീക്രട്ട് കീ (ഇത് ആർക്കും കൊടുക്കരുത്!)
SECRET_KEY = "Nk_GeoSense_Secret_2026"

@app.post("/webhook")
async def receive_gps_data(request: Request, x_api_key: str = Header(None)):
    # 1. API Key കറക്റ്റ് ആണോ എന്ന് നോക്കുന്നു
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized Access! API Key തെറ്റാണ്.")

    # 2. വരുന്ന GPS/Anomaly ഡാറ്റ (JSON) സ്വീകരിക്കുന്നു
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Data Format. JSON മാത്രം അയക്കുക.")

    # 3. സ്വീകരിച്ച ഡാറ്റ പ്രോസസ്സ് ചെയ്യുന്നു (തൽക്കാലം ടെർമിനലിൽ പ്രിന്റ് ചെയ്യാൻ)
    print("🚀 പുതിയ GeoSense ഡാറ്റ കിട്ടി:", payload)

    # 4. സക്സസ് മെസ്സേജ് തിരിച്ചു കൊടുക്കുന്നു
    return {"status": "success", "message": "GeoSense Data securely received!"}

if __name__ == "__main__":
    # ഗൂഗിൾ ക്ലൗഡ് തരുന്ന പോർട്ട് (8080) എടുക്കുക, അല്ലെങ്കിൽ ലോക്കൽ ടെസ്റ്റിംഗിന് 8000 എടുക്കുക
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)