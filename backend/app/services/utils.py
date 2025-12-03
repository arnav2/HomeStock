"""Utility functions"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent.parent.parent / "settings.json"
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"

# Setup logging
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def get_settings():
    """Load settings from JSON file"""
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE) as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error("Error loading settings: %s", e)
        return {}


def save_settings(settings):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        logger.error("Error saving settings: %s", e)
        return False


def log_message(message):
    """Log a message"""
    logger.info(message)


def get_date_tuple(date_str=None):
    """Get date tuple in format (day, month_name, year, month_int)
    Example: (15, 'DEC', 2023, 12)
    """
    if date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        dt = datetime.now(timezone.utc)

    day = dt.day
    year = dt.strftime("%Y")
    month_int = dt.month
    month_dict = {
        1: "JAN",
        2: "FEB",
        3: "MAR",
        4: "APR",
        5: "MAY",
        6: "JUN",
        7: "JUL",
        8: "AUG",
        9: "SEP",
        10: "OCT",
        11: "NOV",
        12: "DEC",
    }
    month = month_dict[month_int]

    return (day, month, year, month_int)
