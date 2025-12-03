"""Run full automation pipeline"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.download_service import DownloadService
from app.services.parse_service import ParseService
from app.services.utils import get_settings, log_message

router = APIRouter()


class RunFullResponse(BaseModel):
    success: bool
    message: str | None = None
    error: str | None = None


@router.post("/", response_model=RunFullResponse)
async def run_full_automation():
    """Run the full automation pipeline: download → parse"""
    try:
        log_message("Starting full automation pipeline...")

        # Get settings
        settings = get_settings()
        if not settings:
            return RunFullResponse(
                success=False,
                error="Settings not configured. Please configure paths in Settings page.",
            )

        raw_path = settings.get("raw_path", "")
        output_path = settings.get("output_path", "")

        if not raw_path or not output_path:
            return RunFullResponse(
                success=False, error="Raw path or output path not configured in settings."
            )

        # Step 1: Download files
        log_message("Step 1: Downloading files...")
        download_service = DownloadService()
        from datetime import datetime, timedelta, timezone

        today_dt = datetime.now(timezone.utc)
        today = today_dt.strftime("%Y-%m-%d")
        yesterday = (today_dt - timedelta(days=1)).strftime("%Y-%m-%d")

        download_result = await download_service.download_files(
            start_date=yesterday,
            end_date=today,
            urls={},  # Will use default URLs
            raw_path=raw_path,
        )

        log_message(f"Downloaded {len(download_result.get('downloaded', []))} files")
        log_message(f"Missing {len(download_result.get('missing', []))} files")

        # Step 2: Parse files
        log_message("Step 2: Parsing files...")
        parse_service = ParseService()
        await parse_service.parse_files(raw_path=raw_path, output_path=output_path)

        log_message("Full automation completed successfully!")

        return RunFullResponse(
            success=True,
            message=f"Downloaded {len(download_result.get('downloaded', []))} files. Parsed successfully.",
        )
    except Exception as e:
        error_msg = str(e)
        log_message(f"Error in full automation: {error_msg}")
        return RunFullResponse(success=False, error=error_msg)
