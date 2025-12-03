"""Tests for pipeline endpoints"""

import shutil
import tempfile
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def temp_pipeline_dir():
    """Create temporary directories for pipeline testing"""
    temp_dir = tempfile.mkdtemp()
    raw_dir = Path(temp_dir) / "raw"
    processed_dir = Path(temp_dir) / "processed"
    output_dir = Path(temp_dir) / "output"

    raw_dir.mkdir()
    processed_dir.mkdir()
    output_dir.mkdir()

    # Create a test zip file
    test_zip = raw_dir / "test.zip"
    with zipfile.ZipFile(test_zip, "w") as zf:
        zf.writestr("test.csv", "col1,col2\nval1,val2\nval3,val4")

    yield {"raw": raw_dir, "processed": processed_dir, "output": output_dir}
    shutil.rmtree(temp_dir)


def test_pipeline_run_basic(temp_pipeline_dir):
    """Test basic pipeline run"""
    response = client.post(
        "/pipeline/run",
        json={
            "start_date": "2023-12-01",
            "end_date": "2023-12-01",
            "urls": {},
            "raw_path": str(temp_pipeline_dir["raw"]),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "phases" in data


def test_pipeline_verify_only(temp_pipeline_dir):
    """Test verify-only endpoint"""
    response = client.post(
        "/pipeline/verify-only",
        params={
            "start_date": "2023-12-01",
            "end_date": "2023-12-01",
            "raw_path": str(temp_pipeline_dir["raw"]),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "phase" in data


def test_pipeline_confirm(temp_pipeline_dir):
    """Test pipeline confirmation endpoint"""
    response = client.post(
        "/pipeline/confirm",
        json={
            "start_date": "2023-12-01",
            "end_date": "2023-12-01",
            "raw_path": str(temp_pipeline_dir["raw"]),
            "intermediate_path": str(temp_pipeline_dir["processed"]),
            "output_path": str(temp_pipeline_dir["output"]),
            "confirmed": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "phases" in data


def test_pipeline_confirm_cancelled(temp_pipeline_dir):
    """Test pipeline confirmation when user cancels"""
    response = client.post(
        "/pipeline/confirm",
        json={
            "start_date": "2023-12-01",
            "end_date": "2023-12-01",
            "raw_path": str(temp_pipeline_dir["raw"]),
            "confirmed": False,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data.get("success") == False
    assert "error" in data


def test_pipeline_with_template(temp_pipeline_dir):
    """Test pipeline with Excel template"""
    # Create a simple template
    from openpyxl import Workbook

    template_path = temp_pipeline_dir["processed"] / "template.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws["A1"] = "Header1"
    wb.save(template_path)

    response = client.post(
        "/pipeline/run",
        json={
            "start_date": "2023-12-01",
            "end_date": "2023-12-01",
            "urls": {},
            "raw_path": str(temp_pipeline_dir["raw"]),
            "template_path": str(template_path),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
