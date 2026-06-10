"""Unit tests for python_gps_webhook.py Flask endpoints."""

import json
import pytest
from python_gps_webhook import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestHomeEndpoint:
    def test_home_returns_ok(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"SERVER IS LIVE" in resp.data


class TestAnalyzeJumpEndpoint:
    def test_spoofing_detected_high_speed(self, client):
        resp = client.post(
            "/api/analyze-jump",
            data=json.dumps({"speed": 200}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "SPOOFING DETECTED"
        assert body["input_speed"] == 200

    def test_clear_low_speed(self, client):
        resp = client.post(
            "/api/analyze-jump",
            data=json.dumps({"speed": 50}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "Clear"

    def test_boundary_speed_150_is_clear(self, client):
        resp = client.post(
            "/api/analyze-jump",
            data=json.dumps({"speed": 150}),
            content_type="application/json",
        )
        body = resp.get_json()
        assert body["status"] == "Clear"

    def test_boundary_speed_151_is_spoofing(self, client):
        resp = client.post(
            "/api/analyze-jump",
            data=json.dumps({"speed": 151}),
            content_type="application/json",
        )
        body = resp.get_json()
        assert body["status"] == "SPOOFING DETECTED"

    def test_response_contains_time(self, client):
        resp = client.post(
            "/api/analyze-jump",
            data=json.dumps({"speed": 10}),
            content_type="application/json",
        )
        body = resp.get_json()
        assert "time" in body


class TestGPSAnalytics:

    def test_missing_speed_defaults_to_zero(self, client):
        resp = client.post(
            "/api/analyze-jump",
            data=json.dumps({
                "latitude": 24.4686,
                "longitude": 54.3001
            }),
            content_type="application/json",
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "Clear"
        assert body["input_speed"] == 0

    def test_missing_speed_returns_400(self, client):
        resp = client.post(
            "/api/analyze-jump",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert resp.status_code == 400
        body = resp.get_json()
        assert "error" in body
