# -*- coding: utf-8 -*-
"""Hyperparameter tuning endpoint."""
from datetime import datetime
from pathlib import Path
import threading
import uuid

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from automar.shared.config.schemas import (
    ExtractOptions,
    PCAOptions,
    LoaderOptions,
    TuningOptions,
    GlobalConfig,
)
from automar.web.api.models import (
    TuningResponse,
    JobStatus,
    TuningProgress,
    TuningProgressCallback,
)
from automar.web.api.jobs import add_job, update_job, get_job, active_job_threads
from automar.shared.persistence.job_store import get_job_store
from automar.web.api.utils import extract_industry_from_dataset, cleanup_uploaded_files

router = APIRouter(tags=["tuning"])


def calculate_timing_info(start_time_iso: str, end_time: datetime) -> dict:
    """Calculate timing information for a job"""
    start_time = datetime.fromisoformat(start_time_iso.replace("Z", "+00:00"))
    duration_seconds = (end_time - start_time).total_seconds()
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    seconds = int(duration_seconds % 60)

    if hours > 0:
        duration_human = f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        duration_human = f"{minutes}m {seconds}s"
    else:
        duration_human = f"{seconds}s"

    return {
        "started_at": start_time_iso,
        "completed_at": end_time.isoformat(),
        "duration_seconds": duration_seconds,
        "duration_human": duration_human,
    }


@router.post("/tune", response_model=TuningResponse)
async def hyperparameter_tuning(
    extract_options: ExtractOptions,
    pca_options: PCAOptions,
    loader_options: LoaderOptions,
    tuning_options: TuningOptions,
    background_tasks: BackgroundTasks,
):
    """
    Perform hyperparameter tuning. This is a long-running operation.

    For immediate response, use the async version with job tracking.
    """
    try:
        # CRITICAL: Validate custom search space BEFORE accepting the job
        if tuning_options.search_space_path:
            from pathlib import Path
            from automar.shared.services.search_space_manager import (
                validate_search_space_file,
            )

            from automar.shared.config.path_resolver import get_project_root

            project_root = get_project_root()
            search_space_file = project_root / tuning_options.search_space_path

            # Check file exists
            if not search_space_file.exists():
                raise HTTPException(
                    status_code=400,
                    detail=f"Custom search space file not found: {tuning_options.search_space_path}",
                )

            # Validate search space structure
            is_valid, errors = validate_search_space_file(str(search_space_file))
            if not is_valid:
                error_message = "Invalid search space file:\n" + "\n".join(
                    f"  - {err}" for err in errors
                )
                raise HTTPException(status_code=400, detail=error_message)

        cfg = GlobalConfig(
            command="tune",
            extract=extract_options,
            pca=pca_options,
            loader=loader_options,
            tune=tuning_options,
        )

        # For long-running tasks, we'll create a job
        import uuid

        job_id = str(uuid.uuid4())

        # Store complete input parameters for session recovery (use mode='json' to serialize dates)
        job_inputs = {
            "extract": extract_options.model_dump(mode="json"),
            "pca": pca_options.model_dump(mode="json"),
            "loader": loader_options.model_dump(mode="json"),
            "tuning": tuning_options.model_dump(mode="json"),
        }

        # Initialize progress with correct total_trials from the start
        total_trials = tuning_options.num_samples
        initial_progress = TuningProgress(
            total_trials=total_trials,
            completed_trials=0,
            running_trials=0,
            start_time=None,
            last_update=None,
        )

        # Extract context information
        industry = None
        if extract_options.industry:
            # Prefer explicitly selected industry (from SQLite industry selector)
            industry = extract_options.industry
        elif pca_options.dataset_path:
            # Fall back to extracting from dataset for regular files
            industry = extract_industry_from_dataset(pca_options.dataset_path)

        job_context = {
            "with_pca": loader_options.dopca,
            "industry": industry if industry else None,
        }

        add_job(
            job_id,
            JobStatus(
                job_id=job_id,
                status="pending",
                type="tuning",
                model=tuning_options.model,
                result=None,
                error=None,
                inputs=job_inputs,
                progress=initial_progress,
                context=job_context,
            ),
        )

        # Run in background
        background_tasks.add_task(run_tuning_background, job_id, cfg)

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Tuning job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_tuning_with_callback(cfg: GlobalConfig, callback: TuningProgressCallback):
    """API wrapper for hyperparameter tuning with progress callback"""
    from automar.shared.core.common import run_tuning_common

    results, config_file_path = run_tuning_common(cfg, progress_callback=callback)

    # Store the actual saved path in results for job tracking
    results.actual_config_path = str(config_file_path)
    results.actual_filename = config_file_path.name

    return results


def run_tuning_background(job_id: str, cfg: GlobalConfig):
    """Background task for hyperparameter tuning with progress tracking"""
    from datetime import datetime
    import time

    # Register this thread for cancellation support
    active_job_threads[job_id] = threading.current_thread()

    try:
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Initialize progress tracking
        total_trials = cfg.tune.num_samples
        progress = TuningProgress(
            total_trials=total_trials,
            completed_trials=0,
            running_trials=0,
            start_time=start_time_iso,
            last_update=start_time_iso,
        )
        update_job(job_id, {"progress": progress})

        # Create progress callback
        callback = TuningProgressCallback(job_id, cfg)

        # Run the actual tuning process with callback
        results = run_tuning_with_callback(cfg, callback)

        # Extract industry from dataset and ticker from config
        industry = None
        if cfg.extract.industry:
            # Prefer explicitly selected industry (from SQLite industry selector)
            industry = cfg.extract.industry
        elif cfg.pca.dataset_path:
            # Fall back to extracting from dataset for regular files
            industry = extract_industry_from_dataset(cfg.pca.dataset_path)
        ticker = cfg.extract.ticker if cfg.extract.ticker else None

        # IMPORTANT: Fetch the UPDATED progress from the database (callback has been updating it)
        job = get_job(job_id)
        if job and job.progress:
            progress = job.progress

        # Update progress with final results
        progress.completed_trials = cfg.tune.num_samples
        progress.running_trials = 0
        progress.last_update = datetime.now().isoformat()

        # Get the actual file path from the tuning results
        # The run_tuning_with_callback function now stores the actual saved path
        if hasattr(results, "actual_config_path") and hasattr(
            results, "actual_filename"
        ):
            full_config_path = results.actual_config_path
            actual_filename = results.actual_filename
        else:
            # Fallback - this shouldn't happen with the updated tuning function
            from pathlib import Path

            from automar.shared.config.path_resolver import get_project_root

            project_root = get_project_root()
            test_path = project_root / cfg.tune.param_path
            actual_filename = f"best_config.toml"  # Generic fallback
            full_config_path = str(test_path / actual_filename)

        # Calculate timing
        end_time = datetime.now()
        end_time_iso = end_time.isoformat()
        duration_seconds = (end_time - start_time).total_seconds()

        # Format duration as human-readable
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)

        if hours > 0:
            duration_human = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            duration_human = f"{minutes}m {seconds}s"
        else:
            duration_human = f"{seconds}s"

        timing_info = {
            "started_at": start_time_iso,
            "completed_at": end_time_iso,
            "duration_seconds": duration_seconds,
            "duration_human": duration_human,
        }

        update_job(
            job_id,
            {
                "status": "completed",
                "result": {
                    "status": "success",
                    "message": "Hyperparameter tuning completed successfully",
                    "best_score": progress.best_score,
                    "best_params": progress.best_params,
                    "param_path": cfg.tune.param_path,
                    "model": cfg.tune.model,
                    "total_trials": progress.completed_trials,
                    "config_filename": actual_filename,
                    "config_path": full_config_path,
                    "ticker": ticker,
                    "industry": industry,
                    "used_pca": cfg.loader.dopca,  # Store PCA usage for compatibility filtering
                },
                "timing": timing_info,
                "completed_at": end_time_iso,
            },
        )

    except KeyboardInterrupt:
        # Job was cancelled by user
        end_time = datetime.now()
        job = get_job(job_id)
        timing = None
        if job and job.started_at:
            timing = calculate_timing_info(job.started_at, end_time)
        update_job(
            job_id,
            {
                "status": "cancelled",
                "error": "Job cancelled by user",
                "completed_at": end_time.isoformat(),
                "timing": timing,
            },
        )
    except Exception as e:
        end_time = datetime.now()
        job = get_job(job_id)
        timing = None
        if job and job.started_at:
            timing = calculate_timing_info(job.started_at, end_time)
        update_job(
            job_id,
            {
                "status": "failed",
                "error": str(e),
                "completed_at": end_time.isoformat(),
                "timing": timing,
            },
        )
    finally:
        # Clean up uploaded files
        cleanup_uploaded_files(cfg)
        # Clean up thread registration
        active_job_threads.pop(job_id, None)
