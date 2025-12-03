"""File verification service to check downloaded files"""

import zipfile
from pathlib import Path

from app.services.database import db


class VerificationService:
    """Service for verifying downloaded files"""

    def __init__(self):
        pass

    def verify_zip_file(self, file_path: Path) -> dict[str, any]:
        """Verify a ZIP file is valid and can be extracted
        Returns dict with 'valid', 'error', 'file_count', 'size'
        """
        try:
            if not file_path.exists():
                return {"valid": False, "error": "File does not exist", "file_count": 0, "size": 0}

            file_size = file_path.stat().st_size

            if file_size == 0:
                return {"valid": False, "error": "File is empty", "file_count": 0, "size": 0}

            # Try to open and list contents
            try:
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    file_list = zip_ref.namelist()
                    # Try to test the zip
                    zip_ref.testzip()

                    return {
                        "valid": True,
                        "error": None,
                        "file_count": len(file_list),
                        "size": file_size,
                        "files": file_list[:10],  # First 10 files
                    }
            except zipfile.BadZipFile:
                return {
                    "valid": False,
                    "error": "Invalid ZIP file format",
                    "file_count": 0,
                    "size": file_size,
                }
            except Exception as e:
                return {
                    "valid": False,
                    "error": f"ZIP error: {e!s}",
                    "file_count": 0,
                    "size": file_size,
                }

        except Exception as e:
            return {
                "valid": False,
                "error": f"Verification error: {e!s}",
                "file_count": 0,
                "size": 0,
            }

    def verify_dat_file(self, file_path: Path) -> dict[str, any]:
        """Verify a DAT file is valid
        Returns dict with 'valid', 'error', 'size', 'line_count'
        """
        try:
            if not file_path.exists():
                return {"valid": False, "error": "File does not exist", "size": 0, "line_count": 0}

            file_size = file_path.stat().st_size

            if file_size == 0:
                return {"valid": False, "error": "File is empty", "size": 0, "line_count": 0}

            # Try to read first few lines
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    line_count = len(lines)

                    return {
                        "valid": True,
                        "error": None,
                        "size": file_size,
                        "line_count": line_count,
                        "preview": lines[:5] if lines else [],
                    }
            except Exception as e:
                return {
                    "valid": False,
                    "error": f"Read error: {e!s}",
                    "size": file_size,
                    "line_count": 0,
                }

        except Exception as e:
            return {
                "valid": False,
                "error": f"Verification error: {e!s}",
                "size": 0,
                "line_count": 0,
            }

    def verify_csv_file(self, file_path: Path) -> dict[str, any]:
        """Verify a CSV file is valid
        Returns dict with 'valid', 'error', 'size', 'row_count'
        """
        try:
            if not file_path.exists():
                return {"valid": False, "error": "File does not exist", "size": 0, "row_count": 0}

            file_size = file_path.stat().st_size

            if file_size == 0:
                return {"valid": False, "error": "File is empty", "size": 0, "row_count": 0}

            # Try to read CSV
            import csv

            try:
                with open(file_path, encoding="utf-8") as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    row_count = len(rows) - 1 if rows else 0  # Exclude header

                    return {
                        "valid": True,
                        "error": None,
                        "size": file_size,
                        "row_count": row_count,
                        "header": rows[0] if rows else [],
                    }
            except Exception as e:
                return {
                    "valid": False,
                    "error": f"CSV parse error: {e!s}",
                    "size": file_size,
                    "row_count": 0,
                }

        except Exception as e:
            return {
                "valid": False,
                "error": f"Verification error: {e!s}",
                "size": 0,
                "row_count": 0,
            }

    def verify_file(self, file_path: Path) -> dict[str, any]:
        """Verify a file based on its extension"""
        file_path = Path(file_path)

        if file_path.suffix.lower() == ".zip":
            return self.verify_zip_file(file_path)
        if file_path.suffix.lower() == ".dat":
            return self.verify_dat_file(file_path)
        if file_path.suffix.lower() == ".csv":
            return self.verify_csv_file(file_path)
        # Generic file check
        if file_path.exists():
            return {"valid": True, "error": None, "size": file_path.stat().st_size}
        return {"valid": False, "error": "File does not exist", "size": 0}

    async def verify_downloads(
        self, start_date: str, end_date: str, raw_path: str
    ) -> dict[str, any]:
        """Verify all downloaded files for a date range
        Returns summary with valid/invalid files
        """
        raw_path_obj = Path(raw_path)

        verified_files = []
        invalid_files = []

        # Get downloads from database
        downloads = db.get_downloads_by_date_range(start_date, end_date)

        for download in downloads:
            file_path = Path(download["file_path"])
            result = self.verify_file(file_path)

            file_info = {
                "download_id": download["id"],
                "file_name": download["file_name"],
                "file_type": download["file_type"],
                "date_str": download["date_str"],
                "file_path": str(file_path),
                "verification": result,
            }

            if result.get("valid"):
                verified_files.append(file_info)
            else:
                invalid_files.append(file_info)

        # Also check for files in directory that might not be in database
        if raw_path_obj.exists():
            for file_path in raw_path_obj.iterdir():
                if file_path.is_file():
                    # Check if already verified
                    already_verified = any(
                        f["file_path"] == str(file_path) for f in verified_files + invalid_files
                    )

                    if not already_verified:
                        result = self.verify_file(file_path)
                        file_info = {
                            "file_name": file_path.name,
                            "file_path": str(file_path),
                            "verification": result,
                        }

                        if result.get("valid"):
                            verified_files.append(file_info)
                        else:
                            invalid_files.append(file_info)

        return {
            "success": True,
            "verified_count": len(verified_files),
            "invalid_count": len(invalid_files),
            "verified_files": verified_files,
            "invalid_files": invalid_files,
            "all_valid": len(invalid_files) == 0,
        }
