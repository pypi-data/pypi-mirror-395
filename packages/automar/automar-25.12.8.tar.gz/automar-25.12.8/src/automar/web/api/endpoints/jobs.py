# -*- coding: utf-8 -*-
"""Job management endpoints."""
from fastapi import APIRouter, HTTPException

from automar.web.api.models import JobStatus
from automar.web.api.jobs import get_job, update_job, active_job_threads, stop_thread
from automar.shared.persistence.job_store import get_job_store

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/all")
async def get_all_jobs():
    """Get all jobs from database (for session recovery)"""
    job_store = get_job_store()
    all_jobs = job_store.get_all_jobs()
    return all_jobs


@router.get("/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Check the status of a long-running job"""
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.delete("/{job_id}")
async def cancel_job(job_id: str):
    """Cancel a running or pending job"""
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status not in ["running", "pending"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job with status '{job.status}'. Only running or pending jobs can be cancelled.",
        )

    # Mark job as cancelled in database
    job_store = get_job_store()
    job_store.cancel_job(job_id)

    # If the job is running in a background thread, stop it (like Ctrl+C)
    thread = active_job_threads.get(job_id)
    if thread and thread.is_alive():
        stop_thread(thread)
        message = f"Job {job_id} has been cancelled (thread interrupted)"
    else:
        # Job hasn't started yet (pending) or already finished
        update_job(job_id, {"status": "cancelled", "error": "Job cancelled by user"})
        message = f"Job {job_id} has been cancelled"

    return {"status": "success", "message": message, "job_id": job_id}


@router.delete("/{job_id}/permanent")
async def delete_job_permanently(job_id: str):
    """Permanently delete a job from the database"""
    job_store = get_job_store()
    job = job_store.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Prevent deletion of running or pending jobs
    if job["status"] in ["running", "pending"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete job with status '{job['status']}'. Cancel the job first.",
        )

    # Delete the job
    job_store.delete_job(job_id)

    return {
        "status": "success",
        "message": f"Job {job_id} has been permanently deleted",
        "job_id": job_id,
    }


@router.post("/{job_id}/lock")
async def toggle_job_lock(job_id: str):
    """Toggle the lock status of a job to prevent/allow auto-cleanup"""
    job_store = get_job_store()

    try:
        new_locked_state = job_store.toggle_lock(job_id)
        return {
            "status": "success",
            "message": f"Job {job_id} has been {'locked' if new_locked_state else 'unlocked'}",
            "job_id": job_id,
            "locked": new_locked_state,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
