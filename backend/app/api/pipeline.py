"""Pipeline API endpoints for full workflow"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.pipeline_service import PipelineService

router = APIRouter()


class PipelineRequest(BaseModel):
    start_date: str
    end_date: str
    urls: dict[str, str]
    raw_path: str
    template_path: str | None = None
    intermediate_path: str | None = None
    output_path: str | None = None
    worksheet_mapping: dict[str, str] | None = None
    worksheets_to_output: list[str] | None = None


class PipelineConfirmationRequest(BaseModel):
    start_date: str
    end_date: str
    raw_path: str
    template_path: str | None = None
    intermediate_path: str | None = None
    output_path: str | None = None
    worksheet_mapping: dict[str, str] | None = None
    worksheets_to_output: list[str] | None = None
    confirmed: bool = True


class PipelineResponse(BaseModel):
    success: bool
    phases: list[dict]
    current_phase: str | None = None
    requires_user_confirmation: bool | None = False
    verification_warnings: list[dict] | None = None
    output_path: str | None = None
    message: str | None = None
    error: str | None = None


@router.post("/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest):
    """Run pipeline: Download -> Verify -> (wait for confirmation)
    Returns verification results and waits for user confirmation
    """
    try:
        service = PipelineService()
        result = await service.run_full_pipeline(
            start_date=request.start_date,
            end_date=request.end_date,
            urls=request.urls,
            raw_path=request.raw_path,
            template_path=request.template_path,
            intermediate_path=request.intermediate_path,
            output_path=request.output_path,
            worksheet_mapping=request.worksheet_mapping,
            worksheets_to_output=request.worksheets_to_output,
        )

        return PipelineResponse(**result)
    except Exception as e:
        return PipelineResponse(success=False, phases=[], error=str(e))


@router.post("/confirm", response_model=PipelineResponse)
async def confirm_and_continue(request: PipelineConfirmationRequest):
    """User confirms verification and continues with Excel processing"""
    if not request.confirmed:
        return PipelineResponse(
            success=False, phases=[], error="User did not confirm. Pipeline cancelled."
        )

    try:
        service = PipelineService()
        result = await service.continue_pipeline_after_confirmation(
            start_date=request.start_date,
            end_date=request.end_date,
            raw_path=request.raw_path,
            template_path=request.template_path,
            intermediate_path=request.intermediate_path,
            output_path=request.output_path,
            worksheet_mapping=request.worksheet_mapping,
            worksheets_to_output=request.worksheets_to_output,
        )

        return PipelineResponse(**result)
    except Exception as e:
        return PipelineResponse(success=False, phases=[], error=str(e))


@router.post("/verify-only")
async def verify_only(start_date: str, end_date: str, raw_path: str):
    """Verify downloads without running full pipeline"""
    try:
        service = PipelineService()
        return await service.run_verification_phase(
            start_date=start_date,
            end_date=end_date,
            raw_path=raw_path,
        )
    except Exception as e:
        return {"success": False, "error": str(e)}
