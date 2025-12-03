"""Pipeline service orchestrating the full workflow:
Download -> Verify -> User Confirm -> Copy to Excel -> Run Formulas -> Output
"""

from pathlib import Path

from app.services.database import db
from app.services.download_service import DownloadService
from app.services.excel_service import ExcelService
from app.services.utils import get_settings, log_message
from app.services.verification_service import VerificationService


class PipelineService:
    """Service for orchestrating the full data processing pipeline"""

    def __init__(self):
        self.download_service = DownloadService()
        self.verification_service = VerificationService()
        self.excel_service = ExcelService()

    async def run_download_phase(
        self, start_date: str, end_date: str, urls: dict[str, str], raw_path: str
    ) -> dict:
        """Phase 1: Download files
        Returns dict with download results
        """
        log_message("=== Phase 1: Downloading files ===")
        result = await self.download_service.download_files(
            start_date=start_date, end_date=end_date, urls=urls, raw_path=raw_path
        )

        return {
            "phase": "download",
            "success": True,
            "downloaded": result.get("downloaded", []),
            "missing": result.get("missing", []),
            "message": f"Downloaded {len(result.get('downloaded', []))} files",
        }

    async def run_verification_phase(self, start_date: str, end_date: str, raw_path: str) -> dict:
        """Phase 2: Verify downloaded files
        Returns dict with verification results
        """
        log_message("=== Phase 2: Verifying downloads ===")
        result = await self.verification_service.verify_downloads(
            start_date=start_date, end_date=end_date, raw_path=raw_path
        )

        if result.get("all_valid"):
            return {
                "phase": "verification",
                "success": True,
                "verified_count": result.get("verified_count", 0),
                "invalid_count": result.get("invalid_count", 0),
                "verified_files": result.get("verified_files", []),
                "invalid_files": result.get("invalid_files", []),
                "message": f"All {result.get('verified_count', 0)} files verified successfully",
                "requires_confirmation": True,
            }
        return {
            "phase": "verification",
            "success": False,
            "verified_count": result.get("verified_count", 0),
            "invalid_count": result.get("invalid_count", 0),
            "verified_files": result.get("verified_files", []),
            "invalid_files": result.get("invalid_files", []),
            "message": f"Found {result.get('invalid_count', 0)} invalid files. Please review before proceeding.",
            "requires_confirmation": True,
        }

    async def run_excel_processing_phase(
        self,
        start_date: str,
        end_date: str,
        raw_path: str,
        template_path: str | None,
        intermediate_path: str,
        output_path: str,
        worksheet_mapping: dict | None = None,
        worksheets_to_output: list[str] | None = None,
    ) -> dict:
        """Phase 3: Copy data to Excel, run formulas, create output
        Returns dict with processing results
        """
        log_message("=== Phase 3: Processing Excel files ===")

        # Get verified files
        verification = await self.verification_service.verify_downloads(
            start_date=start_date, end_date=end_date, raw_path=raw_path
        )

        # Prepare source files list
        source_files = []
        for file_info in verification.get("verified_files", []):
            # Get file type from download record if available
            file_type = file_info.get("file_type", "")
            if not file_type and "download_id" in file_info:
                download = db.get_download(file_info["download_id"])
                if download:
                    file_type = download.get("file_type", "")

            source_files.append(
                {
                    "file_path": file_info["file_path"],
                    "file_type": file_type,
                    "worksheet_name": None,  # Will use mapping
                }
            )

        # Run full pipeline
        template = Path(template_path) if template_path else None
        intermediate = Path(intermediate_path)
        output = Path(output_path)

        result = self.excel_service.process_full_pipeline(
            source_files=source_files,
            template_path=template,
            intermediate_path=intermediate,
            output_path=output,
            worksheet_mapping=worksheet_mapping,
            worksheets_to_output=worksheets_to_output,
        )

        if result.get("success"):
            return {
                "phase": "excel_processing",
                "success": True,
                "intermediate_path": str(intermediate),
                "output_path": str(output),
                "worksheets": result.get("copy_to_output", {}).get("worksheets_copied", []),
                "message": f"Successfully created output file: {output.name}",
            }
        return {
            "phase": "excel_processing",
            "success": False,
            "error": result.get("error", "Unknown error"),
            "message": f"Failed to process Excel files: {result.get('error')}",
        }

    async def run_full_pipeline(
        self,
        start_date: str,
        end_date: str,
        urls: dict[str, str],
        raw_path: str,
        template_path: str | None = None,
        intermediate_path: str | None = None,
        output_path: str | None = None,
        worksheet_mapping: dict | None = None,
        worksheets_to_output: list[str] | None = None,
        skip_verification: bool = False,
    ) -> dict:
        """Run full pipeline: Download -> Verify -> Process -> Output

        Args:
            start_date: Start date for downloads (YYYY-MM-DD).
            end_date: End date for downloads (YYYY-MM-DD).
            urls: Optional custom URL overrides for specific file types.
            raw_path: Directory where raw downloaded files are stored.
            template_path: Optional Excel template path for processing.
            intermediate_path: Path for intermediate Excel file with formulas.
            output_path: Final output Excel file path.
            worksheet_mapping: Optional mapping from file types to worksheet names.
            worksheets_to_output: Optional list of worksheet names to include in final output.
            skip_verification: If True, skip verification phase (for testing)

        Returns dict with all phase results
        """
        settings = get_settings()

        # Set default paths
        if not intermediate_path:
            intermediate_path = settings.get(
                "processed_path", str(Path(raw_path).parent / "intermediate")
            )
        if not output_path:
            output_path = settings.get("output_path", str(Path(raw_path).parent / "output"))

        results = {
            "phases": [],
            "success": False,
            "current_phase": None,
            "config": {
                "start_date": start_date,
                "end_date": end_date,
                "raw_path": raw_path,
                "template_path": template_path,
                "intermediate_path": intermediate_path,
                "output_path": output_path,
                "worksheet_mapping": worksheet_mapping,
                "worksheets_to_output": worksheets_to_output,
            },
        }

        try:
            # Phase 1: Download
            download_result = await self.run_download_phase(start_date, end_date, urls, raw_path)
            results["phases"].append(download_result)
            results["current_phase"] = "download"

            if not download_result.get("success"):
                results["error"] = "Download phase failed"
                return results

            # Phase 2: Verification
            if not skip_verification:
                verification_result = await self.run_verification_phase(
                    start_date, end_date, raw_path
                )
                results["phases"].append(verification_result)
                results["current_phase"] = "verification"

                # Verification phase doesn't block - it just reports status
                # User confirmation will be handled by API endpoint
                if verification_result.get("invalid_count", 0) > 0:
                    results["requires_user_confirmation"] = True
                    results["verification_warnings"] = verification_result.get("invalid_files", [])

            # Note: Excel processing will be triggered after user confirmation
            # via separate endpoint

            results["success"] = True
            results["message"] = "Download and verification completed. Ready for user confirmation."

        except Exception as e:
            log_message(f"Pipeline error: {e!s}")
            results["error"] = str(e)
            results["success"] = False

        return results

    async def continue_pipeline_after_confirmation(
        self,
        start_date: str,
        end_date: str,
        raw_path: str,
        template_path: str | None,
        intermediate_path: str | None = None,
        output_path: str | None = None,
        worksheet_mapping: dict | None = None,
        worksheets_to_output: list[str] | None = None,
    ) -> dict:
        """Continue pipeline after user confirmation
        Runs Excel processing phase
        """
        settings = get_settings()

        if not intermediate_path:
            intermediate_path = settings.get(
                "processed_path", str(Path(raw_path).parent / "intermediate")
            )
        if not output_path:
            output_path = settings.get("output_path", str(Path(raw_path).parent / "output"))

        # Phase 3: Excel Processing
        excel_result = await self.run_excel_processing_phase(
            start_date=start_date,
            end_date=end_date,
            raw_path=raw_path,
            template_path=template_path,
            intermediate_path=intermediate_path,
            output_path=output_path,
            worksheet_mapping=worksheet_mapping,
            worksheets_to_output=worksheets_to_output,
        )

        return {
            "phases": [excel_result],
            "success": excel_result.get("success", False),
            "current_phase": "excel_processing",
            "output_path": excel_result.get("output_path"),
            "message": excel_result.get("message", ""),
        }
