"""Logs API endpoints"""

from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

LOG_FILE = Path(__file__).parent.parent.parent / "logs" / "app.log"


class LogsResponse(BaseModel):
    success: bool
    logs: str | None = None
    error: str | None = None


@router.get("", response_model=LogsResponse)
async def get_logs():
    """Get last 200 lines of logs"""
    try:
        if LOG_FILE.exists():
            with open(LOG_FILE, encoding="utf-8") as f:
                lines = f.readlines()
                # Get last 200 lines
                last_lines = lines[-200:] if len(lines) > 200 else lines
                logs = "".join(last_lines)
            return LogsResponse(success=True, logs=logs)
        return LogsResponse(success=True, logs="No logs available yet.")
    except Exception as e:
        return LogsResponse(success=False, error=str(e))
