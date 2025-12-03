"""SQLite database for download tracking and file metadata"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "homestock.db"


class Database:
    """SQLite database manager for download tracking"""

    def __init__(self, db_path: Path = None):
        if db_path is None:
            self.db_path = DB_PATH
        else:
            self.db_path = Path(db_path) if not isinstance(db_path, Path) else db_path

        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Downloads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    url TEXT NOT NULL,
                    date_str TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    progress REAL DEFAULT 0.0,
                    error_message TEXT,
                    retry_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """)

            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_file_name ON downloads(file_name)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_status ON downloads(status)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_date_str ON downloads(date_str)
            """)

            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def create_download(
        self, file_name: str, file_type: str, url: str, date_str: str, file_path: str
    ) -> int:
        """Create a new download record"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO downloads
                (file_name, file_type, url, date_str, file_path, status)
                VALUES (?, ?, ?, ?, ?, 'pending')
            """,
                (file_name, file_type, url, date_str, file_path),
            )
            conn.commit()
            return cursor.lastrowid

    def update_download_status(
        self, download_id: int, status: str, progress: float = None, error_message: str = None
    ):
        """Update download status and progress"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            updates = ["status = ?", "updated_at = CURRENT_TIMESTAMP"]
            params = [status]

            if progress is not None:
                updates.append("progress = ?")
                params.append(progress)

            if error_message is not None:
                updates.append("error_message = ?")
                params.append(error_message)

            if status == "completed":
                updates.append("completed_at = CURRENT_TIMESTAMP")

            params.append(download_id)
            cursor.execute(
                f"""
                UPDATE downloads
                SET {", ".join(updates)}
                WHERE id = ?
            """,
                params,
            )
            conn.commit()

    def increment_retry(self, download_id: int):
        """Increment retry count"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE downloads
                SET retry_count = retry_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (download_id,),
            )
            conn.commit()

    def get_download(self, download_id: int) -> dict | None:
        """Get download by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM downloads WHERE id = ?", (download_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_downloads_by_status(self, status: str) -> list[dict]:
        """Get all downloads with a specific status"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM downloads WHERE status = ? ORDER BY created_at DESC", (status,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_downloads_by_date_range(self, start_date: str, end_date: str) -> list[dict]:
        """Get downloads in date range"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM downloads
                WHERE date_str BETWEEN ? AND ?
                ORDER BY date_str DESC, file_type
            """,
                (start_date, end_date),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_failed_downloads(self) -> list[dict]:
        """Get all failed downloads"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM downloads
                WHERE status = 'failed'
                ORDER BY updated_at DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    def reset_download(self, download_id: int):
        """Reset download to pending status for retry"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE downloads
                SET status = 'pending',
                    progress = 0.0,
                    error_message = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (download_id,),
            )
            conn.commit()


# Global database instance
db = Database()
