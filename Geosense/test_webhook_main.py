"""Unit tests for Geosense/webhook_main.py FastAPI endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from webhook_main import app


@pytest.fixture()
def transport():
    return ASGITransport(app=app)


@pytest.mark.asyncio
class TestWebhookEndpoint:
    async def test_valid_request(self, transport):
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            resp = await ac.post(
                "/webhook",
                json={"lat": 24.45, "lon": 54.38, "anomaly": True},
                headers={"x-api-key": "Nk_GeoSense_Secret_2026"},
            )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"

    async def test_missing_api_key_returns_401(self, transport):
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            resp = await ac.post("/webhook", json={"lat": 0})
        assert resp.status_code == 401

    async def test_wrong_api_key_returns_401(self, transport):
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            resp = await ac.post(
                "/webhook",
                json={"lat": 0},
                headers={"x-api-key": "wrong_key"},
            )
        assert resp.status_code == 401

    async def test_invalid_json_returns_400(self, transport):
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            resp = await ac.post(
                "/webhook",
                content="not json",
                headers={
                    "x-api-key": "Nk_GeoSense_Secret_2026",
                    "content-type": "application/json",
                },
            )
        assert resp.status_code == 400

    async def test_empty_payload_accepted(self, transport):
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            resp = await ac.post(
                "/webhook",
                json={},
                headers={"x-api-key": "Nk_GeoSense_Secret_2026"},
            )
        assert resp.status_code == 200
