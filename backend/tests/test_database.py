"""Tests for database service"""

import shutil
import tempfile
from pathlib import Path

import pytest

from app.services.database import Database


@pytest.fixture
def temp_db():
    """Create temporary database"""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test.db"
    db = Database(db_path=db_path)
    yield db
    shutil.rmtree(temp_dir)


def test_create_download(temp_db):
    """Test creating a download record"""
    download_id = temp_db.create_download(
        file_name="test.zip",
        file_type="cm_bhavcopy",
        url="https://example.com/test.zip",
        date_str="2023-12-01",
        file_path="/tmp/test.zip",
    )

    assert download_id is not None
    assert download_id > 0


def test_get_download(temp_db):
    """Test getting a download"""
    download_id = temp_db.create_download(
        file_name="test.zip",
        file_type="cm_bhavcopy",
        url="https://example.com/test.zip",
        date_str="2023-12-01",
        file_path="/tmp/test.zip",
    )

    download = temp_db.get_download(download_id)
    assert download is not None
    assert download["file_name"] == "test.zip"
    assert download["status"] == "pending"


def test_update_download_status(temp_db):
    """Test updating download status"""
    download_id = temp_db.create_download(
        file_name="test.zip",
        file_type="cm_bhavcopy",
        url="https://example.com/test.zip",
        date_str="2023-12-01",
        file_path="/tmp/test.zip",
    )

    temp_db.update_download_status(download_id, "downloading", progress=50.0)
    download = temp_db.get_download(download_id)
    assert download["status"] == "downloading"
    assert download["progress"] == 50.0


def test_get_downloads_by_status(temp_db):
    """Test getting downloads by status"""
    temp_db.create_download(
        file_name="test1.zip",
        file_type="cm_bhavcopy",
        url="https://example.com/test1.zip",
        date_str="2023-12-01",
        file_path="/tmp/test1.zip",
    )

    temp_db.create_download(
        file_name="test2.zip",
        file_type="fo_bhavcopy",
        url="https://example.com/test2.zip",
        date_str="2023-12-01",
        file_path="/tmp/test2.zip",
    )

    downloads = temp_db.get_downloads_by_status("pending")
    assert len(downloads) >= 2


def test_get_downloads_by_date_range(temp_db):
    """Test getting downloads by date range"""
    temp_db.create_download(
        file_name="test1.zip",
        file_type="cm_bhavcopy",
        url="https://example.com/test1.zip",
        date_str="2023-12-01",
        file_path="/tmp/test1.zip",
    )

    temp_db.create_download(
        file_name="test2.zip",
        file_type="fo_bhavcopy",
        url="https://example.com/test2.zip",
        date_str="2023-12-05",
        file_path="/tmp/test2.zip",
    )

    downloads = temp_db.get_downloads_by_date_range("2023-12-01", "2023-12-03")
    assert len(downloads) >= 1


def test_retry_download(temp_db):
    """Test retry functionality"""
    download_id = temp_db.create_download(
        file_name="test.zip",
        file_type="cm_bhavcopy",
        url="https://example.com/test.zip",
        date_str="2023-12-01",
        file_path="/tmp/test.zip",
    )

    temp_db.update_download_status(download_id, "failed", error_message="Test error")
    temp_db.increment_retry(download_id)

    download = temp_db.get_download(download_id)
    assert download["retry_count"] == 1

    temp_db.reset_download(download_id)
    download = temp_db.get_download(download_id)
    assert download["status"] == "pending"
    assert download["error_message"] is None
