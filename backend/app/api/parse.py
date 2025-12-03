"""Parse API endpoints"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.parse_service import ParseService

router = APIRouter()


class ParseRequest(BaseModel):
    raw_path: str
    output_path: str


class ParseResponse(BaseModel):
    success: bool
    results: dict[str, int] | None = None
    error: str | None = None


@router.post("/", response_model=ParseResponse)
async def parse_files(request: ParseRequest):
    """Parse raw NSE files and generate normalized CSV"""
    try:
        service = ParseService()
        results = await service.parse_files(
            raw_path=request.raw_path, output_path=request.output_path
        )
        return ParseResponse(success=True, results=results)
    except Exception as e:
        return ParseResponse(success=False, error=str(e))
