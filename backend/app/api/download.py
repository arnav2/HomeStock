"""Download API endpoints with individual file support and retry"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.database import db
from app.services.download_service import DownloadService

router = APIRouter()


class DownloadRequest(BaseModel):
    start_date: str
    end_date: str
    urls: dict[str, str]
    raw_path: str


class SingleFileDownloadRequest(BaseModel):
    file_type: str
    date_str: str
    url: str | None = None
    raw_path: str
    custom_urls: dict[str, str] | None = None


class RetryDownloadRequest(BaseModel):
    download_id: int


class DownloadResponse(BaseModel):
    success: bool
    downloaded: list[str]
    missing: list[str]
    error: str | None = None


class SingleFileDownloadResponse(BaseModel):
    success: bool
    download_id: int | None = None
    file_path: str | None = None
    message: str | None = None
    error: str | None = None


class DownloadStatusResponse(BaseModel):
    success: bool
    downloads: list[dict]
    error: str | None = None


@router.post("/", response_model=DownloadResponse)
async def download_files(request: DownloadRequest):
    """Download NSE files for the given date range"""
    try:
        service = DownloadService()
        result = await service.download_files(
            start_date=request.start_date,
            end_date=request.end_date,
            urls=request.urls,
            raw_path=request.raw_path,
        )
        return DownloadResponse(
            success=True, downloaded=result.get("downloaded", []), missing=result.get("missing", [])
        )
    except Exception as e:
        return DownloadResponse(success=False, downloaded=[], missing=[], error=str(e))


@router.post("/single", response_model=SingleFileDownloadResponse)
async def download_single_file(request: SingleFileDownloadRequest):
    """Download a single file with progress tracking"""
    try:
        service = DownloadService()
        result = await service.download_single_file(
            file_type=request.file_type,
            date_str=request.date_str,
            url=request.url,
            raw_path=request.raw_path,
            custom_urls=request.custom_urls or {},
        )
        return SingleFileDownloadResponse(**result)
    except Exception as e:
        return SingleFileDownloadResponse(success=False, error=str(e))


@router.post("/retry", response_model=SingleFileDownloadResponse)
async def retry_download(request: RetryDownloadRequest):
    """Retry a failed download"""
    try:
        service = DownloadService()
        result = await service.retry_download(request.download_id)
        return SingleFileDownloadResponse(**result)
    except Exception as e:
        return SingleFileDownloadResponse(success=False, error=str(e))


@router.get("/status", response_model=DownloadStatusResponse)
async def get_download_status(
    start_date: str | None = None, end_date: str | None = None, status: str | None = None
):
    """Get download status"""
    try:
        if status:
            downloads = db.get_downloads_by_status(status)
        elif start_date and end_date:
            downloads = db.get_downloads_by_date_range(start_date, end_date)
        else:
            downloads = (
                db.get_downloads_by_status("pending")
                + db.get_downloads_by_status("downloading")
                + db.get_downloads_by_status("failed")
            )

        # Convert to dict list
        download_list = []
        for d in downloads:
            download_dict = {
                "id": d["id"],
                "file_name": d["file_name"],
                "file_type": d["file_type"],
                "url": d["url"],
                "date_str": d["date_str"],
                "file_path": d["file_path"],
                "status": d["status"],
                "progress": d["progress"],
                "error_message": d["error_message"],
                "retry_count": d["retry_count"],
                "created_at": d["created_at"],
                "updated_at": d["updated_at"],
                "completed_at": d["completed_at"],
            }
            download_list.append(download_dict)

        return DownloadStatusResponse(success=True, downloads=download_list)
    except Exception as e:
        return DownloadStatusResponse(success=False, downloads=[], error=str(e))


@router.get("/{download_id}")
async def get_download(download_id: int):
    """Get a specific download by ID"""
    download = db.get_download(download_id)
    if not download:
        raise HTTPException(status_code=404, detail="Download not found")

    return {
        "success": True,
        "download": {
            "id": download["id"],
            "file_name": download["file_name"],
            "file_type": download["file_type"],
            "url": download["url"],
            "date_str": download["date_str"],
            "file_path": download["file_path"],
            "status": download["status"],
            "progress": download["progress"],
            "error_message": download["error_message"],
            "retry_count": download["retry_count"],
            "created_at": download["created_at"],
            "updated_at": download["updated_at"],
            "completed_at": download["completed_at"],
        },
    }
