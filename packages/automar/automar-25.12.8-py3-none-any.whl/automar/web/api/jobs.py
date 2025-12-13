"""
Job management utilities for the API.

Handles job storage, retrieval, and lifecycle management using SQLite backend.
"""

from typing import Optional, Dict, Any
import threading
import time

from automar.web.api.models import JobStatus
from automar.shared.persistence.job_store import get_job_store

# Progress tracking (in-memory with auto-cleanup)
progress_store: Dict[str, Dict] = {}

# Active background task threads (for cancellation)
active_job_threads: Dict[str, threading.Thread] = {}
progress_store_timestamps: Dict[str, float] = {}


def get_job(job_id: str) -> Optional[JobStatus]:
    """Get job from persistent storage"""
    job_store = get_job_store()
    job_data = job_store.get_job(job_id)
    if not job_data:
        return None
    # Convert dict to JobStatus model
    return JobStatus(**job_data)


def update_job(job_id: str, updates: Dict[str, Any]):
    """Update job in persistent storage"""
    job_store = get_job_store()
    job_store.update_job(job_id, updates)


def add_job(job_id: str, job_status: JobStatus):
    """Add job to persistent storage"""
    job_store = get_job_store()
    job_store.add_job(job_id, job_status.dict())


def stop_thread(thread: threading.Thread):
    """Inject KeyboardInterrupt into a running thread (like Ctrl+C)"""
    import ctypes

    if not thread or not thread.is_alive():
        return False

    # Inject KeyboardInterrupt exception into the thread
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), ctypes.py_object(KeyboardInterrupt)
    )

    if res == 0:
        # Thread ID not found
        return False
    elif res > 1:
        # Multiple threads affected - this shouldn't happen, revert
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), None)
        return False

    return True


def cleanup_progress_store():
    """Remove progress entries older than 1 hour"""
    current_time = time.time()
    one_hour = 3600
    to_remove = [
        key
        for key, timestamp in progress_store_timestamps.items()
        if current_time - timestamp > one_hour
    ]
    for key in to_remove:
        progress_store.pop(key, None)
        progress_store_timestamps.pop(key, None)
    return len(to_remove)
