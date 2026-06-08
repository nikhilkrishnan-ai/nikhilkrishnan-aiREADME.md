import os

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="GeoSense Data Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        os.environ.get("ALLOWED_ORIGINS", "").split(",")
        if os.environ.get("ALLOWED_ORIGINS")
        else []
    ),
    allow_methods=["POST"],
    allow_headers=["X-Api-Key", "Content-Type"],
)

SECRET_KEY = os.environ.get("GEOSENSE_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("GEOSENSE_SECRET_KEY environment variable is not set")

MAX_PAYLOAD_BYTES = 1_048_576  # 1 MB


@app.post("/webhook")
async def receive_gps_data(request: Request, x_api_key: str = Header(None)):
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.body()
    if len(body) > MAX_PAYLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Payload too large")

    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc

    print("Received GeoSense data:", payload)

    return {"status": "success", "message": "GeoSense Data securely received!"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="127.0.0.1", port=port)
