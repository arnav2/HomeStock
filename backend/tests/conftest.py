"""Pytest configuration and fixtures"""

import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test.db"
    db = Database(db_path=db_path)
    yield db
    shutil.rmtree(temp_dir)


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_settings():
    """Sample settings for testing"""
    return {
        "raw_path": "/tmp/test_raw",
        "processed_path": "/tmp/test_processed",
        "output_path": "/tmp/test_output",
        "scheduler": "off",
        "custom_cron": "",
    }
