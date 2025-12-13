# -*- coding: utf-8 -*-
"""Cross-validation endpoint."""
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
    TrainingOptions,
    CrossvalidateOptions,
    GlobalConfig,
)
from automar.web.api.models import (
    CrossvalidateResponse,
    JobStatus,
    TuningProgress,
)
from automar.web.api.jobs import add_job, update_job, get_job, active_job_threads
from automar.shared.persistence.job_store import get_job_store
from automar.web.api.utils import extract_industry_from_dataset, cleanup_uploaded_files

router = APIRouter(tags=["crossvalidation"])


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


@router.post("/crossvalidate", response_model=CrossvalidateResponse)
async def crossvalidate_model(
    extract_options: ExtractOptions,
    pca_options: PCAOptions,
    loader_options: LoaderOptions,
    tuning_options: TuningOptions,
    training_options: TrainingOptions,
    crossvalidate_options: CrossvalidateOptions,
    background_tasks: BackgroundTasks,
):
    """
    Perform cross-validation on a model.

    This is a long-running operation that returns a job ID.
    """
    try:
        cfg = GlobalConfig(
            command="crossvalidate",
            extract=extract_options,
            pca=pca_options,
            loader=loader_options,
            tune=tuning_options,
            train=training_options,
            crossvalidate=crossvalidate_options,
        )

        import uuid

        job_id = str(uuid.uuid4())

        # Store complete input parameters (use mode='json' to serialize dates)
        job_inputs = {
            "extract": extract_options.model_dump(mode="json"),
            "pca": pca_options.model_dump(mode="json"),
            "loader": loader_options.model_dump(mode="json"),
            "tuning": tuning_options.model_dump(mode="json"),
            "training": training_options.model_dump(mode="json"),
            "crossvalidate": crossvalidate_options.model_dump(mode="json"),
        }

        # Initialize progress with correct total_trials (folds) from the start
        initial_progress = TuningProgress(
            total_trials=crossvalidate_options.n_split,
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
                type="crossvalidate",
                model=tuning_options.model,
                result=None,
                error=None,
                inputs=job_inputs,
                progress=initial_progress,
                context=job_context,
            ),
        )

        background_tasks.add_task(run_crossvalidation_background, job_id, cfg)

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Cross-validation job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_crossvalidation_background(job_id: str, cfg: GlobalConfig):
    """Background task for cross-validation"""
    from pathlib import Path
    from datetime import datetime

    # Register this thread for cancellation support
    active_job_threads[job_id] = threading.current_thread()

    try:
        # Set start time BEFORE importing common (which can fail if Ray is missing)
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Import after setting start time so failures still show when job started
        from automar.shared.core.common import run_crossvalidation_common

        # Check for cancellation before starting
        job_store = get_job_store()
        if job_store.is_cancelled(job_id):
            raise KeyboardInterrupt("Job cancelled by user")

        # Initialize progress tracking with actual number of folds
        progress = TuningProgress(
            total_trials=cfg.crossvalidate.n_split,
            completed_trials=0,
            running_trials=1,
            start_time=start_time_iso,
            last_update=start_time_iso,
        )
        update_job(job_id, {"progress": progress})

        # Define progress callback
        def cv_progress_callback(fold_num, total_folds, fold_auroc):
            """Called after each CV fold"""
            # Check for cancellation
            job_store = get_job_store()
            if job_store.is_cancelled(job_id):
                raise KeyboardInterrupt("Job cancelled by user")

            # Create fresh progress object instead of modifying existing one
            new_progress = TuningProgress(
                total_trials=total_folds,
                completed_trials=fold_num,
                running_trials=1 if fold_num < total_folds else 0,
                best_score=fold_auroc,
                start_time=start_time_iso,
                last_update=datetime.now().isoformat(),
            )

            update_job(job_id, {"progress": new_progress})

        # Run cross-validation using common function WITH callback
        crossval_results, out_path, total_samples = run_crossvalidation_common(
            cfg, progress_callback=cv_progress_callback
        )

        # Extract industry from dataset and ticker from config
        industry = None
        if cfg.extract.industry:
            # Prefer explicitly selected industry (from SQLite industry selector)
            industry = cfg.extract.industry
        elif cfg.pca.dataset_path:
            # Fall back to extracting from dataset for regular files
            industry = extract_industry_from_dataset(cfg.pca.dataset_path)
        ticker = cfg.extract.ticker if cfg.extract.ticker else None

        # Extract metrics from the cross-validation results
        cv_metrics = []
        mean_metrics = {}

        try:
            # crossval_results is a list of tuples/lists: [(acc, auc, rec, fsc, prec), ...]
            # Convert to a more readable format
            metric_names = ["accuracy", "auc", "recall", "fscore", "precision"]

            for i, fold_results in enumerate(crossval_results):
                fold_metrics = {}
                for j, metric_name in enumerate(metric_names):
                    # Convert tensor to float if needed
                    value = fold_results[j]
                    if hasattr(value, "item"):  # PyTorch tensor
                        value = value.item()
                    elif hasattr(value, "cpu"):  # PyTorch tensor on GPU
                        value = value.cpu().item()
                    fold_metrics[metric_name] = float(value)
                fold_metrics["fold"] = i + 1
                cv_metrics.append(fold_metrics)

            # Calculate mean and std metrics across all folds
            for metric_name in metric_names:
                values = [fold[metric_name] for fold in cv_metrics]
                mean_metrics[f"mean_{metric_name}"] = sum(values) / len(values)
                mean_metrics[f"std_{metric_name}"] = (
                    sum((x - mean_metrics[f"mean_{metric_name}"]) ** 2 for x in values)
                    / len(values)
                ) ** 0.5

        except Exception as e:
            print(f"Error processing cross-validation results: {e}")
            cv_metrics = []
            mean_metrics = {}

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
                    "results_path": str(out_path),
                    "model_type": cfg.tune.model,
                    "output_file": out_path.name,
                    "cv_metrics": cv_metrics,
                    "mean_metrics": mean_metrics,
                    "total_folds": len(cv_metrics),
                    "total_samples": total_samples,
                    "ticker": ticker,
                    "industry": industry,
                    "used_pca": cfg.loader.dopca,
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
