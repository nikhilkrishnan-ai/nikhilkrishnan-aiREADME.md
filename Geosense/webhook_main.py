from fastapi import FastAPI, Header, HTTPException, Request
import uvicorn

app = FastAPI(title="GeoSense Data Pipeline")

# 🔒 സെക്യൂരിറ്റിക്ക് വേണ്ടിയുള്ള സീക്രട്ട് കീ (ഇത് ആർക്കും കൊടുക്കരുത്!)
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

    # (ഭാവിയിൽ ഇവിടെയാണ് നമ്മൾ Power BI / OneLake-ലേക്ക് ഡാറ്റ വിടുന്ന കോഡ് ചേർക്കുന്നത്)

    # 4. സക്സസ് മെസ്സേജ് തിരിച്ചു കൊടുക്കുന്നു
    return {"status": "success", "message": "GeoSense Data securely received!"}

if __name__ == "__main__":
    # ലോക്കൽ സർവർ റൺ ചെയ്യാൻ
    uvicorn.run(app, host="0.0.0.0", port=8000)