"""Scheduler service for running automation on schedule"""

import asyncio
import time
from threading import Thread

import schedule

from app.services.download_service import DownloadService
from app.services.parse_service import ParseService
from app.services.utils import get_settings, log_message


class SchedulerService:
    """Service for scheduling automated tasks"""

    def __init__(self):
        self.running = False
        self.thread = None

    def _run_automation(self):
        """Run the automation pipeline"""

        async def run():
            try:
                log_message("Scheduled automation started...")
                settings = get_settings()

                if not settings:
                    log_message("Settings not configured, skipping scheduled run")
                    return

                raw_path = settings.get("raw_path", "")
                output_path = settings.get("output_path", "")

                if not raw_path or not output_path:
                    log_message("Paths not configured, skipping scheduled run")
                    return

                # Download files
                download_service = DownloadService()
                from datetime import datetime, timedelta, timezone

                today_dt = datetime.now(timezone.utc)
                today = today_dt.strftime("%Y-%m-%d")
                yesterday = (today_dt - timedelta(days=1)).strftime("%Y-%m-%d")

                await download_service.download_files(
                    start_date=yesterday, end_date=today, urls={}, raw_path=raw_path
                )

                # Parse files
                parse_service = ParseService()
                await parse_service.parse_files(raw_path=raw_path, output_path=output_path)

                log_message("Scheduled automation completed")
            except Exception as e:
                log_message(f"Error in scheduled automation: {e!s}")

        asyncio.run(run())

    def start(self, cron_schedule: str = None):
        """Start the scheduler"""
        if self.running:
            return

        settings = get_settings()
        scheduler_type = settings.get("scheduler", "off")

        if scheduler_type == "off":
            return

        if scheduler_type == "daily-7am":
            schedule.every().day.at("07:00").do(self._run_automation)
        elif scheduler_type == "custom" and cron_schedule:
            # Parse cron string (simplified - only supports basic patterns)
            # Format: "minute hour day month weekday"
            # For now, we'll use a simple daily schedule
            # Full cron parsing would require a library like croniter
            schedule.every().day.at("07:00").do(self._run_automation)

        self.running = True

        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

        self.thread = Thread(target=run_scheduler, daemon=True)
        self.thread.start()
        log_message("Scheduler started")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        schedule.clear()
        log_message("Scheduler stopped")


# Global scheduler instance
scheduler = SchedulerService()
