"""Tests for run-full automation endpoint"""

import shutil
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_run_full_without_settings():
    """Test run-full without configured settings"""
    response = client.post("/run-full/")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    # Should return error if settings not configured
    if not data.get("success"):
        assert "error" in data


def test_run_full_with_settings():
    """Test run-full with configured settings"""
    # First set up settings
    temp_dir = tempfile.mkdtemp()
    try:
        settings = {
            "raw_path": str(Path(temp_dir) / "raw"),
            "processed_path": str(Path(temp_dir) / "processed"),
            "output_path": str(Path(temp_dir) / "output"),
            "scheduler": "off",
            "custom_cron": "",
        }

        client.post("/settings/save", json=settings)

        # Now try run-full
        response = client.post("/run-full/")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
    finally:
        shutil.rmtree(temp_dir)
