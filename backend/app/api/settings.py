"""Settings API endpoints"""

import json
import os
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

SETTINGS_FILE = Path(__file__).parent.parent.parent / "settings.json"


class SettingsRequest(BaseModel):
    raw_path: str
    processed_path: str
    output_path: str
    scheduler: str
    custom_cron: str | None = None


class SettingsResponse(BaseModel):
    success: bool
    settings: dict | None = None
    error: str | None = None


class PathTestRequest(BaseModel):
    path: str


class PathTestResponse(BaseModel):
    accessible: bool
    error: str | None = None


@router.post("/save", response_model=SettingsResponse)
async def save_settings(request: SettingsRequest):
    """Save application settings to JSON file"""
    try:
        settings_data = {
            "raw_path": request.raw_path,
            "processed_path": request.processed_path,
            "output_path": request.output_path,
            "scheduler": request.scheduler,
            "custom_cron": request.custom_cron or "",
        }

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings_data, f, indent=2)

        return SettingsResponse(success=True, settings=settings_data)
    except Exception as e:
        return SettingsResponse(success=False, error=str(e))


@router.get("/get", response_model=SettingsResponse)
async def get_settings():
    """Get application settings from JSON file"""
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE) as f:
                settings = json.load(f)
            return SettingsResponse(success=True, settings=settings)
        return SettingsResponse(success=True, settings={})
    except Exception as e:
        return SettingsResponse(success=False, error=str(e))


@router.post("/test-path", response_model=PathTestResponse)
async def test_path(request: PathTestRequest):
    """Test if a folder path is accessible"""
    try:
        path = Path(request.path)
        accessible = path.exists() and path.is_dir() and os.access(path, os.W_OK)
        return PathTestResponse(accessible=accessible)
    except Exception as e:
        return PathTestResponse(accessible=False, error=str(e))
