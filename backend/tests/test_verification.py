"""Tests for verification service"""

import shutil
import tempfile
import zipfile
from pathlib import Path

import pytest

from app.services.verification_service import VerificationService


@pytest.fixture
def temp_files():
    """Create temporary test files"""
    temp_dir = tempfile.mkdtemp()

    # Create valid zip
    valid_zip = Path(temp_dir) / "valid.zip"
    with zipfile.ZipFile(valid_zip, "w") as zf:
        zf.writestr("test.csv", "col1,col2\nval1,val2")

    # Create invalid zip (empty)
    invalid_zip = Path(temp_dir) / "invalid.zip"
    invalid_zip.touch()

    # Create valid CSV
    valid_csv = Path(temp_dir) / "valid.csv"
    valid_csv.write_text("col1,col2\nval1,val2\nval3,val4")

    # Create valid DAT
    valid_dat = Path(temp_dir) / "valid.dat"
    valid_dat.write_text("line1|data1|data2\nline2|data3|data4")

    yield {
        "valid_zip": valid_zip,
        "invalid_zip": invalid_zip,
        "valid_csv": valid_csv,
        "valid_dat": valid_dat,
        "dir": temp_dir,
    }
    shutil.rmtree(temp_dir)


def test_verify_zip_valid(temp_files):
    """Test verifying valid ZIP file"""
    service = VerificationService()
    result = service.verify_zip_file(temp_files["valid_zip"])

    assert result["valid"] == True
    assert result["file_count"] > 0
    assert result["size"] > 0


def test_verify_zip_invalid(temp_files):
    """Test verifying invalid ZIP file"""
    service = VerificationService()
    result = service.verify_zip_file(temp_files["invalid_zip"])

    assert result["valid"] == False
    assert "error" in result


def test_verify_csv(temp_files):
    """Test verifying CSV file"""
    service = VerificationService()
    result = service.verify_csv_file(temp_files["valid_csv"])

    assert result["valid"] == True
    assert result["row_count"] > 0


def test_verify_dat(temp_files):
    """Test verifying DAT file"""
    service = VerificationService()
    result = service.verify_dat_file(temp_files["valid_dat"])

    assert result["valid"] == True
    assert result["line_count"] > 0


def test_verify_nonexistent_file():
    """Test verifying non-existent file"""
    service = VerificationService()
    result = service.verify_file(Path("/nonexistent/file.zip"))

    assert result["valid"] == False
    assert "error" in result
