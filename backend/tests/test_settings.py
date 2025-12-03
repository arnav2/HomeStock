"""Tests for settings endpoints"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_settings():
    """Test getting settings"""
    response = client.get("/settings/get")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "settings" in data


def test_save_settings():
    """Test saving settings"""
    settings = {
        "raw_path": "/tmp/test_raw",
        "processed_path": "/tmp/test_processed",
        "output_path": "/tmp/test_output",
        "scheduler": "daily-7am",
        "custom_cron": "",
    }

    response = client.post("/settings/save", json=settings)
    assert response.status_code == 200
    data = response.json()
    assert data.get("success") == True
    assert "settings" in data


def test_save_settings_invalid():
    """Test saving invalid settings"""
    response = client.post("/settings/save", json={"raw_path": "", "invalid_field": "value"})

    assert response.status_code == 200
    data = response.json()
    # Should handle gracefully
    assert "success" in data


def test_test_path_valid():
    """Test path testing with valid path"""
    import tempfile

    temp_dir = tempfile.mkdtemp()

    try:
        response = client.post("/settings/test-path", json={"path": temp_dir})

        assert response.status_code == 200
        data = response.json()
        assert "accessible" in data
        assert data.get("accessible") == True
    finally:
        import shutil

        shutil.rmtree(temp_dir)


def test_test_path_invalid():
    """Test path testing with invalid path"""
    response = client.post("/settings/test-path", json={"path": "/nonexistent/path/12345"})

    assert response.status_code == 200
    data = response.json()
    assert "accessible" in data
    assert data.get("accessible") == False


def test_settings_roundtrip():
    """Test saving and retrieving settings"""
    settings = {
        "raw_path": "/tmp/test_raw",
        "processed_path": "/tmp/test_processed",
        "output_path": "/tmp/test_output",
        "scheduler": "custom",
        "custom_cron": "0 7 * * *",
    }

    # Save
    response = client.post("/settings/save", json=settings)
    assert response.status_code == 200

    # Get
    response = client.get("/settings/get")
    assert response.status_code == 200
    data = response.json()

    if data.get("success") and data.get("settings"):
        saved_settings = data["settings"]
        assert saved_settings.get("raw_path") == settings["raw_path"]
        assert saved_settings.get("scheduler") == settings["scheduler"]
