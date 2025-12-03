"""Download service for NSE files with rate limiting and progress tracking"""

from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path

import requests

from app.services.database import db
from app.services.rate_limiter import nse_rate_limiter
from app.services.utils import get_date_tuple, log_message


class DownloadService:
    """Service for downloading NSE data files with rate limiting"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }

    def _generate_urls(self, date_str: str, custom_urls: dict[str, str] = None) -> dict[str, str]:
        """Generate NSE URLs for a given date.

        Returns dict with keys: fo_udiff, fo_participant_oi, cm_delivery, cm_udiff, cm_bhavcopy
        """
        tu = get_date_tuple(date_str)
        day, month, year, month_int = tu

        urls = {}

        # Use custom URLs if provided, otherwise generate default URLs
        if custom_urls and custom_urls.get("fo_udiff"):
            urls["fo_udiff"] = custom_urls["fo_udiff"]
        else:
            urls["fo_udiff"] = (
                f"https://www.nseindia.com/archives/nsccl/mwpl/combineoi_{day:02d}{month_int:02d}{year}.zip"
            )

        if custom_urls and custom_urls.get("fo_participant_oi"):
            urls["fo_participant_oi"] = custom_urls["fo_participant_oi"]
        else:
            urls["fo_participant_oi"] = urls["fo_udiff"]

        if custom_urls and custom_urls.get("cm_delivery"):
            urls["cm_delivery"] = custom_urls["cm_delivery"]
        else:
            urls["cm_delivery"] = (
                f"https://www.nseindia.com/archives/equities/mto/MTO_{day:02d}{month_int:02d}{year}.DAT"
            )

        if custom_urls and custom_urls.get("cm_udiff"):
            urls["cm_udiff"] = custom_urls["cm_udiff"]
        else:
            urls["cm_udiff"] = (
                f"https://www.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{day:02d}{month}{year}bhav.csv.zip"
            )

        if custom_urls and custom_urls.get("cm_bhavcopy"):
            urls["cm_bhavcopy"] = custom_urls["cm_bhavcopy"]
        else:
            urls["cm_bhavcopy"] = (
                f"https://www.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{day:02d}{month}{year}bhav.csv.zip"
            )

        if custom_urls and custom_urls.get("fo_bhavcopy"):
            urls["fo_bhavcopy"] = custom_urls["fo_bhavcopy"]
        else:
            urls["fo_bhavcopy"] = (
                f"https://www.nseindia.com/content/historical/DERIVATIVES/{year}/{month}/fo{day:02d}{month}{year}bhav.csv.zip"
            )

        return urls

    def _download_file_with_progress(
        self,
        url: str,
        output_path: Path,
        download_id: int | None = None,
        progress_callback: Callable | None = None,
    ) -> bool:
        """Download a single file from URL with progress tracking and rate limiting"""
        try:
            # Apply rate limiting
            nse_rate_limiter.wait_if_needed()

            log_message(f"Downloading: {url}")
            if download_id:
                db.update_download_status(download_id, "downloading", progress=0.0)

            response = requests.get(url, headers=self.headers, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded_size = 0

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # Update progress
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                        else:
                            progress = 50.0  # Unknown size, show 50%

                        if download_id:
                            db.update_download_status(download_id, "downloading", progress=progress)

                        if progress_callback:
                            progress_callback(progress)

            log_message(f"Downloaded: {output_path.name}")
            if download_id:
                db.update_download_status(download_id, "completed", progress=100.0)
            return True

        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            log_message(f"Failed to download {url}: {error_msg}")
            if download_id:
                db.update_download_status(
                    download_id, "failed", progress=0.0, error_message=error_msg
                )
            return False

    async def download_single_file(
        self,
        file_type: str,
        date_str: str,
        url: str,
        raw_path: str,
        custom_urls: dict[str, str] = None,
    ) -> dict:
        """Download a single file with database tracking

        Returns dict with download_id and status
        """
        # Generate URL if not provided
        if not url:
            urls = self._generate_urls(date_str, custom_urls)
            url = urls.get(file_type, "")
            if not url:
                return {"success": False, "error": f"Unknown file type: {file_type}"}

        # Determine file extension
        if url.endswith(".zip"):
            ext = ".zip"
        elif url.endswith(".DAT"):
            ext = ".DAT"
        else:
            ext = ".csv"

        filename = f"{file_type}_{date_str}{ext}"
        raw_path_obj = Path(raw_path) if raw_path else Path.cwd() / "raw_data"
        raw_path_obj.mkdir(parents=True, exist_ok=True)
        output_file = raw_path_obj / filename

        # Check if already exists
        if output_file.exists():
            # Check if we have a completed record
            downloads = db.get_downloads_by_date_range(date_str, date_str)
            for d in downloads:
                if d["file_name"] == filename and d["status"] == "completed":
                    return {
                        "success": True,
                        "download_id": d["id"],
                        "message": "File already exists",
                        "file_path": str(output_file),
                    }

        # Create download record
        download_id = db.create_download(
            file_name=filename,
            file_type=file_type,
            url=url,
            date_str=date_str,
            file_path=str(output_file),
        )

        # Download file
        success = self._download_file_with_progress(url, output_file, download_id)

        if success:
            return {
                "success": True,
                "download_id": download_id,
                "file_path": str(output_file),
                "message": "Download completed",
            }
        return {"success": False, "download_id": download_id, "error": "Download failed"}

    async def download_files(
        self, start_date: str, end_date: str, urls: dict[str, str], raw_path: str
    ) -> dict[str, list[str]]:
        """Download files for date range (backward compatible)
        Returns dict with 'downloaded' and 'missing' lists
        """
        downloaded = []
        missing = []

        # Parse date range using date objects to avoid naive datetimes
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        # Ensure raw_path exists
        raw_path_obj = Path(raw_path) if raw_path else Path.cwd() / "raw_data"
        raw_path_obj.mkdir(parents=True, exist_ok=True)

        # Iterate through dates
        current_date = start
        while current_date <= end:
            date_str = current_date.isoformat()
            date_urls = self._generate_urls(date_str, urls)

            # Download each file type
            for file_type, url in date_urls.items():
                if not url:
                    continue

                result = await self.download_single_file(file_type, date_str, url, raw_path, urls)
                if result.get("success"):
                    downloaded.append(result.get("file_path", "").split("/")[-1])
                else:
                    missing.append(f"{file_type}_{date_str} ({url})")

            current_date += timedelta(days=1)

        return {"downloaded": downloaded, "missing": missing}

    async def retry_download(self, download_id: int) -> dict:
        """Retry a failed download"""
        download = db.get_download(download_id)
        if not download:
            return {"success": False, "error": "Download not found"}

        if download["status"] == "completed":
            return {"success": False, "error": "Download already completed"}

        # Reset download status
        db.reset_download(download_id)
        db.increment_retry(download_id)

        # Retry download
        output_file = Path(download["file_path"])
        success = self._download_file_with_progress(download["url"], output_file, download_id)

        if success:
            return {"success": True, "download_id": download_id, "message": "Retry successful"}
        return {"success": False, "download_id": download_id, "error": "Retry failed"}
