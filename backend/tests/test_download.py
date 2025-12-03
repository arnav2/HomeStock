"""Tests for download endpoints"""

import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def temp_download_dir():
    """Create temporary directory for downloads"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


def test_download_endpoint_basic(temp_download_dir):
    """Test basic download endpoint"""
    response = client.post(
        "/download/",
        json={
            "start_date": "2023-12-01",
            "end_date": "2023-12-01",
            "urls": {},
            "raw_path": str(temp_download_dir),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "downloaded" in data
    assert "missing" in data


def test_download_endpoint_invalid_date():
    """Test download endpoint with invalid date"""
    response = client.post(
        "/download/",
        json={
            "start_date": "invalid-date",
            "end_date": "2023-12-01",
            "urls": {},
            "raw_path": "/tmp/test",
        },
    )

    assert response.status_code == 200  # Returns error in response body
    data = response.json()
    assert data.get("success") == False or "error" in data


def test_download_single_file(temp_download_dir):
    """Test single file download endpoint"""
    response = client.post(
        "/download/single",
        json={
            "file_type": "cm_bhavcopy",
            "date_str": "2023-12-01",
            "url": "",
            "raw_path": str(temp_download_dir),
            "custom_urls": {},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    if data.get("success"):
        assert "download_id" in data


def test_download_status():
    """Test download status endpoint"""
    response = client.get("/download/status")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "downloads" in data


def test_download_status_with_filters():
    """Test download status with date filters"""
    response = client.get("/download/status?start_date=2023-12-01&end_date=2023-12-05")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "downloads" in data


def test_download_status_with_status_filter():
    """Test download status with status filter"""
    response = client.get("/download/status?status=failed")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "downloads" in data


def test_get_download_by_id():
    """Test getting download by ID"""
    # First create a download
    response = client.post(
        "/download/single",
        json={
            "file_type": "cm_bhavcopy",
            "date_str": "2023-12-01",
            "url": "",
            "raw_path": "/tmp/test",
            "custom_urls": {},
        },
    )

    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("download_id"):
            download_id = data["download_id"]

            # Get the download
            response = client.get(f"/download/{download_id}")
            assert response.status_code == 200
            data = response.json()
            assert "success" in data
            assert "download" in data


def test_get_nonexistent_download():
    """Test getting non-existent download"""
    response = client.get("/download/99999")
    assert response.status_code == 404


def test_retry_download():
    """Test retry download endpoint"""
    # First create a download that might fail
    response = client.post(
        "/download/single",
        json={
            "file_type": "cm_bhavcopy",
            "date_str": "2023-12-01",
            "url": "https://invalid-url-that-will-fail.com/file.zip",
            "raw_path": "/tmp/test",
            "custom_urls": {},
        },
    )

    if response.status_code == 200:
        data = response.json()
        if data.get("download_id"):
            download_id = data["download_id"]

            # Try to retry
            response = client.post("/download/retry", json={"download_id": download_id})
            assert response.status_code == 200
            data = response.json()
            assert "success" in data


def test_retry_nonexistent_download():
    """Test retry non-existent download"""
    response = client.post("/download/retry", json={"download_id": 99999})
    assert response.status_code == 200
    data = response.json()
    assert data.get("success") == False
