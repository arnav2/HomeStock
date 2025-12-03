"""Tests for parse endpoints"""

import shutil
import tempfile
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def temp_parse_dir():
    """Create temporary directories for parsing"""
    temp_dir = tempfile.mkdtemp()
    raw_dir = Path(temp_dir) / "raw"
    output_dir = Path(temp_dir) / "output"
    raw_dir.mkdir()
    output_dir.mkdir()

    # Create a test zip file
    test_zip = raw_dir / "test.zip"
    with zipfile.ZipFile(test_zip, "w") as zf:
        zf.writestr("test.csv", "col1,col2\nval1,val2\nval3,val4")

    yield {"raw": raw_dir, "output": output_dir}
    shutil.rmtree(temp_dir)


def test_parse_endpoint(temp_parse_dir):
    """Test parse endpoint"""
    response = client.post(
        "/parse/",
        json={"raw_path": str(temp_parse_dir["raw"]), "output_path": str(temp_parse_dir["output"])},
    )

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    if data.get("success"):
        assert "results" in data


def test_parse_endpoint_invalid_path():
    """Test parse endpoint with invalid path"""
    response = client.post(
        "/parse/", json={"raw_path": "/nonexistent/path", "output_path": "/tmp/output"}
    )

    assert response.status_code == 200
    data = response.json()
    # Should handle error gracefully
    assert "success" in data


def test_parse_endpoint_empty_directory():
    """Test parse endpoint with empty directory"""
    temp_dir = tempfile.mkdtemp()
    try:
        response = client.post("/parse/", json={"raw_path": temp_dir, "output_path": temp_dir})

        assert response.status_code == 200
        data = response.json()
        assert "success" in data
    finally:
        shutil.rmtree(temp_dir)
