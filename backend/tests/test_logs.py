"""Tests for logs endpoints"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_logs():
    """Test getting logs"""
    response = client.get("/logs")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "logs" in data


def test_logs_always_returns():
    """Test that logs endpoint always returns something"""
    response = client.get("/logs")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    # Should return logs or a message
    assert "logs" in data or "error" in data
