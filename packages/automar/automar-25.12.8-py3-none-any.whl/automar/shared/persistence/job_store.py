# -*- coding: utf-8 -*-
"""
Persistent job storage using optimized SQLite.
Replaces in-memory job storage to survive server restarts.

Storage Location:
    Jobs are stored in out/jobs/jobs.db
    This folder can be safely deleted to clear all job history.
    The database file will be automatically recreated when needed.

Space Efficiency:
    Heavily optimized for minimal disk usage:
    - Small page size (1024 bytes vs default 4096)
    - No wasted space (auto_vacuum)
    - Minimal indexes (only essential ones)
    - Compact JSON storage
    Target: 3-4 KB per job (vs 5-15 KB unoptimized)
"""
import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, Any
from contextlib import contextmanager
from datetime import datetime


class JobStore:
    """Space-optimized SQLite-backed job storage"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            # Store in out/jobs/ at project root
            from automar.shared.config.path_resolver import get_project_root

            project_root = get_project_root()
            storage_dir = project_root / "out" / "jobs"
            storage_dir.mkdir(parents=True, exist_ok=True)
            db_path = storage_dir / "jobs.db"

        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """Initialize database with space-optimized settings"""
        with self._get_conn() as conn:
            # Space optimization: Use smaller page size (1024 vs default 4096)
            # This reduces wasted space for small records
            conn.execute("PRAGMA page_size = 1024")

            # Reclaim space from deleted records automatically
            conn.execute("PRAGMA auto_vacuum = FULL")

            # Better concurrency with Write-Ahead Logging
            conn.execute("PRAGMA journal_mode = WAL")

            # Reduce cache size to minimize memory (use disk instead)
            conn.execute("PRAGMA cache_size = -2000")  # 2MB cache

            # Create minimal schema - only essential fields
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    type TEXT,
                    model TEXT,
                    result TEXT,
                    error TEXT,
                    progress TEXT,
                    cancelled INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    inputs TEXT,
                    timing TEXT,
                    started_at TEXT,
                    completed_at TEXT
                ) WITHOUT ROWID
            """
            )
            # WITHOUT ROWID saves ~8-12 bytes per row by eliminating internal rowid

            # Minimal indexing - only for common queries
            # Status index for filtering running/pending jobs
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_status ON jobs(status) WHERE status IN ('running', 'pending')
            """
            )
            # Partial index only for active jobs - saves space vs full index

            # Migrations: Add new columns if they don't exist (for existing databases)
            cursor = conn.execute("PRAGMA table_info(jobs)")
            columns = [row[1] for row in cursor.fetchall()]

            if "model" not in columns:
                conn.execute("ALTER TABLE jobs ADD COLUMN model TEXT")

            if "cancelled" not in columns:
                conn.execute("ALTER TABLE jobs ADD COLUMN cancelled INTEGER DEFAULT 0")

            if "inputs" not in columns:
                conn.execute("ALTER TABLE jobs ADD COLUMN inputs TEXT")

            if "timing" not in columns:
                conn.execute("ALTER TABLE jobs ADD COLUMN timing TEXT")

            if "started_at" not in columns:
                conn.execute("ALTER TABLE jobs ADD COLUMN started_at TEXT")

            if "completed_at" not in columns:
                conn.execute("ALTER TABLE jobs ADD COLUMN completed_at TEXT")

            if "locked" not in columns:
                conn.execute("ALTER TABLE jobs ADD COLUMN locked INTEGER DEFAULT 0")

            conn.commit()

    @contextmanager
    def _get_conn(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def add_job(self, job_id: str, job_data: Dict[str, Any]):
        """Add a new job"""
        now = datetime.now().isoformat()

        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO jobs (job_id, status, type, model, result, error, progress, created_at, updated_at, inputs, timing, started_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    job_id,
                    job_data.get("status", "pending"),
                    job_data.get("type"),
                    job_data.get("model"),
                    # Compact JSON - no whitespace
                    (
                        json.dumps(job_data.get("result"), separators=(",", ":"))
                        if job_data.get("result")
                        else None
                    ),
                    job_data.get("error"),
                    (
                        json.dumps(
                            job_data.get("progress").__dict__, separators=(",", ":")
                        )
                        if hasattr(job_data.get("progress"), "__dict__")
                        else (
                            json.dumps(job_data.get("progress"), separators=(",", ":"))
                            if job_data.get("progress")
                            else None
                        )
                    ),
                    now,
                    now,
                    # New fields
                    (
                        json.dumps(job_data.get("inputs"), separators=(",", ":"))
                        if job_data.get("inputs")
                        else None
                    ),
                    (
                        json.dumps(job_data.get("timing"), separators=(",", ":"))
                        if job_data.get("timing")
                        else None
                    ),
                    job_data.get("started_at"),
                    job_data.get("completed_at"),
                ),
            )
            conn.commit()

    def update_job(self, job_id: str, updates: Dict[str, Any]):
        """Update an existing job"""
        import time

        # Retry logic to handle race conditions with add_job
        # Background tasks may start before add_job completes
        max_retries = 10
        retry_delay = 0.1  # 100ms

        for attempt in range(max_retries):
            if self.get_job(job_id):
                break
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        else:
            # Job still doesn't exist after retries - this shouldn't happen
            # but we'll handle it gracefully by logging instead of crashing
            print(
                f"Warning: Attempted to update non-existent job {job_id}, skipping update"
            )
            return

        now = datetime.now().isoformat()
        set_clauses = []
        params = []

        if "status" in updates:
            set_clauses.append("status = ?")
            params.append(updates["status"])

        if "result" in updates:
            set_clauses.append("result = ?")
            # Compact JSON
            params.append(
                json.dumps(updates["result"], separators=(",", ":"))
                if updates["result"]
                else None
            )

        if "error" in updates:
            set_clauses.append("error = ?")
            params.append(updates["error"])

        if "progress" in updates:
            set_clauses.append("progress = ?")
            progress = updates["progress"]
            if hasattr(progress, "__dict__"):
                params.append(json.dumps(progress.__dict__, separators=(",", ":")))
            else:
                params.append(
                    json.dumps(progress, separators=(",", ":")) if progress else None
                )

        # New fields
        if "inputs" in updates:
            set_clauses.append("inputs = ?")
            params.append(
                json.dumps(updates["inputs"], separators=(",", ":"))
                if updates["inputs"]
                else None
            )

        if "timing" in updates:
            set_clauses.append("timing = ?")
            params.append(
                json.dumps(updates["timing"], separators=(",", ":"))
                if updates["timing"]
                else None
            )

        if "started_at" in updates:
            set_clauses.append("started_at = ?")
            params.append(updates["started_at"])

        if "completed_at" in updates:
            set_clauses.append("completed_at = ?")
            params.append(updates["completed_at"])

        set_clauses.append("updated_at = ?")
        params.append(now)

        params.append(job_id)

        with self._get_conn() as conn:
            conn.execute(
                f"""
                UPDATE jobs
                SET {', '.join(set_clauses)}
                WHERE job_id = ?
            """,
                params,
            )
            conn.commit()

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get a job by ID"""
        with self._get_conn() as conn:
            row = conn.execute(
                """
                SELECT * FROM jobs WHERE job_id = ?
            """,
                (job_id,),
            ).fetchone()

            if not row:
                return None

            return self._row_to_dict(row)

    def get_all_jobs(self) -> Dict[str, Dict[str, Any]]:
        """Get all jobs"""
        with self._get_conn() as conn:
            rows = conn.execute(
                """
                SELECT * FROM jobs ORDER BY created_at DESC
            """
            ).fetchall()

            return {row["job_id"]: self._row_to_dict(row) for row in rows}

    def get_active_jobs(self) -> Dict[str, Dict[str, Any]]:
        """Get running and pending jobs"""
        with self._get_conn() as conn:
            rows = conn.execute(
                """
                SELECT * FROM jobs
                WHERE status IN ('running', 'pending')
                ORDER BY created_at DESC
            """
            ).fetchall()

            return {row["job_id"]: self._row_to_dict(row) for row in rows}

    def cancel_job(self, job_id: str):
        """Mark a job as cancelled"""
        with self._get_conn() as conn:
            conn.execute(
                """
                UPDATE jobs
                SET cancelled = 1, updated_at = ?
                WHERE job_id = ?
            """,
                (datetime.now().isoformat(), job_id),
            )
            conn.commit()

    def is_cancelled(self, job_id: str) -> bool:
        """Check if a job has been cancelled"""
        with self._get_conn() as conn:
            row = conn.execute(
                """
                SELECT cancelled FROM jobs WHERE job_id = ?
            """,
                (job_id,),
            ).fetchone()
            return bool(row["cancelled"]) if row else False

    def delete_job(self, job_id: str):
        """Delete a job"""
        with self._get_conn() as conn:
            conn.execute("DELETE FROM jobs WHERE job_id = ?", (job_id,))
            conn.commit()

    def toggle_lock(self, job_id: str) -> bool:
        """Toggle the lock status of a job and return the new locked state"""
        with self._get_conn() as conn:
            # Get current lock status
            row = conn.execute(
                "SELECT locked FROM jobs WHERE job_id = ?", (job_id,)
            ).fetchone()

            if not row:
                raise ValueError(f"Job {job_id} not found")

            current_locked = bool(row["locked"]) if row["locked"] else False
            new_locked = not current_locked

            # Update the lock status
            conn.execute(
                """
                UPDATE jobs
                SET locked = ?, updated_at = ?
                WHERE job_id = ?
            """,
                (int(new_locked), datetime.now().isoformat(), job_id),
            )
            conn.commit()

            return new_locked

    def cleanup_old_jobs(self, days: int = 7):
        """Delete completed/failed/cancelled jobs older than specified days (excluding locked jobs)"""
        from datetime import timedelta

        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        with self._get_conn() as conn:
            result = conn.execute(
                """
                DELETE FROM jobs
                WHERE created_at < ?
                  AND status IN ('completed', 'failed', 'cancelled')
                  AND (locked IS NULL OR locked = 0)
            """,
                (cutoff,),
            )
            deleted_count = result.rowcount
            conn.commit()

            # Run VACUUM to reclaim space after cleanup
            if deleted_count > 0:
                conn.execute("VACUUM")

            return deleted_count

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite row to job dict"""
        # Handle columns which may not exist in older databases
        try:
            model = row["model"]
        except (KeyError, IndexError):
            model = None

        try:
            cancelled = bool(row["cancelled"])
        except (KeyError, IndexError):
            cancelled = False

        try:
            inputs = json.loads(row["inputs"]) if row["inputs"] else None
        except (KeyError, IndexError):
            inputs = None

        try:
            timing = json.loads(row["timing"]) if row["timing"] else None
        except (KeyError, IndexError):
            timing = None

        try:
            started_at = row["started_at"]
        except (KeyError, IndexError):
            started_at = None

        try:
            completed_at = row["completed_at"]
        except (KeyError, IndexError):
            completed_at = None

        try:
            locked = bool(row["locked"])
        except (KeyError, IndexError):
            locked = False

        return {
            "job_id": row["job_id"],
            "status": row["status"],
            "type": row["type"],
            "model": model,
            "result": json.loads(row["result"]) if row["result"] else None,
            "error": row["error"],
            "progress": json.loads(row["progress"]) if row["progress"] else None,
            "cancelled": cancelled,
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "inputs": inputs,
            "timing": timing,
            "started_at": started_at,
            "completed_at": completed_at,
            "locked": locked,
        }


# Singleton instance
_job_store: Optional[JobStore] = None


def get_job_store(db_path: str = None) -> JobStore:
    """Get or create the global job store instance"""
    global _job_store
    if _job_store is None:
        _job_store = JobStore(db_path)
    return _job_store
