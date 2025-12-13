# -*- coding: utf-8 -*-
"""Model training endpoint."""
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
    GlobalConfig,
)
from automar.shared.runners import run_training
from automar.web.api.models import (
    TrainingResponse,
    JobStatus,
    TuningProgress,
)
from automar.web.api.jobs import add_job, update_job, get_job, active_job_threads
from automar.shared.persistence.job_store import get_job_store
from automar.web.api.utils import extract_industry_from_dataset, cleanup_uploaded_files

router = APIRouter(tags=["training"])


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


@router.post("/train", response_model=TrainingResponse)
async def train_model(
    extract_options: ExtractOptions,
    pca_options: PCAOptions,
    loader_options: LoaderOptions,
    tuning_options: TuningOptions,
    training_options: TrainingOptions,
    background_tasks: BackgroundTasks,
):
    """
    Train a model with specified hyperparameters.

    This is a long-running operation that returns a job ID.
    """
    try:
        cfg = GlobalConfig(
            command="train",
            extract=extract_options,
            pca=pca_options,
            loader=loader_options,
            tune=tuning_options,
            train=training_options,
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
        }

        # Initialize progress with epochs from tuning_options (only for GRU/Transformer)
        # Log-reg trains in a single step, so no progress tracking
        initial_progress = None
        if tuning_options.model.lower() in ["gru", "transformer"]:
            # This is the default, may be overridden by hyperparameter file later
            initial_progress = TuningProgress(
                total_trials=tuning_options.epochs,
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
                type="training",
                model=tuning_options.model,
                result=None,
                error=None,
                inputs=job_inputs,
                progress=initial_progress,
                context=job_context,
            ),
        )

        background_tasks.add_task(run_training_background, job_id, cfg)

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Training job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_training_background(job_id: str, cfg: GlobalConfig):
    """Background task for model training"""
    from datetime import datetime

    # Register this thread for cancellation support
    active_job_threads[job_id] = threading.current_thread()

    try:
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Check for cancellation before starting
        job_store = get_job_store()
        if job_store.is_cancelled(job_id):
            raise KeyboardInterrupt("Job cancelled by user")

        # Initialize progress tracking for neural network training only
        if cfg.tune.model.lower() in ["gru", "transformer"]:
            import tomli
            from pathlib import Path
            from automar.shared.persistence.library import read_df

            from automar.shared.config.path_resolver import get_project_root

            project_root = get_project_root()

            # Determine config path (same logic as in run_training)
            if cfg.pca.data_file:
                new_df = read_df(cfg.pca.data_file)
                if new_df is not None and cfg.extract.industry:
                    ind_name = cfg.extract.industry
                elif new_df is not None:
                    ind_name = new_df["Industry"].value_counts().idxmax()
                else:
                    from automar.shared.core.common import build_final_df

                    new_df, ind_name = build_final_df(cfg)
            else:
                from automar.shared.core.common import build_final_df

                new_df, ind_name = build_final_df(cfg)

            tick_name = cfg.extract.ticker if cfg.extract.ticker else None

            if tick_name:
                file_name = f"{ind_name}({tick_name})_{cfg.tune.model}_hyperparameters_{cfg.train.id}.toml"
            else:
                file_name = (
                    f"{ind_name}_{cfg.tune.model}_hyperparameters_{cfg.train.id}.toml"
                )

            cfg_path = cfg.train.cfg_path or (
                project_root / cfg.tune.param_path / file_name
            )

            # Load hyperparameters to get total epochs
            total_epochs = cfg.tune.epochs  # default
            if cfg_path.exists():
                with open(cfg_path, "rb") as ff:
                    ray_results = tomli.load(ff)
                    total_epochs = ray_results.get("epochs", cfg.tune.epochs)

            # Initialize progress with total epochs
            progress = TuningProgress(
                total_trials=total_epochs,
                completed_trials=0,
                running_trials=1,
                start_time=start_time_iso,
                last_update=start_time_iso,
            )
            update_job(job_id, {"progress": progress})

            # Define progress callback
            def training_progress_callback(
                epoch_num, total_epochs, avg_losses, val_auroc, val_lr
            ):
                """Called after each training epoch"""
                # Check for cancellation
                job_store = get_job_store()
                if job_store.is_cancelled(job_id):
                    raise KeyboardInterrupt("Job cancelled by user")

                # Create fresh progress object instead of modifying existing one
                best_score = None
                if val_auroc and len(val_auroc) > 0:
                    best_score = max(val_auroc)

                new_progress = TuningProgress(
                    total_trials=total_epochs,
                    completed_trials=epoch_num,
                    running_trials=1 if epoch_num < total_epochs else 0,
                    best_score=best_score,
                    start_time=start_time_iso,
                    last_update=datetime.now().isoformat(),
                )

                update_job(job_id, {"progress": new_progress})

            # Run training WITH callback
            result = run_training(cfg, progress_callback=training_progress_callback)
            mdl_path = result[0] if isinstance(result, tuple) else result
            logreg_results = None
        else:
            # Log-reg: no progress tracking during training
            result = run_training(cfg)
            mdl_path = result[0] if isinstance(result, tuple) else result
            logreg_results = result[1] if isinstance(result, tuple) else None

        # Extract industry from dataset and ticker from config
        industry = None
        if cfg.extract.industry:
            # Prefer explicitly selected industry (from SQLite industry selector)
            industry = cfg.extract.industry
        elif cfg.pca.dataset_path:
            # Fall back to extracting from dataset for regular files
            industry = extract_industry_from_dataset(cfg.pca.dataset_path)
        ticker = cfg.extract.ticker if cfg.extract.ticker else None

        # Extract validation AUROC
        val_auroc = None
        if cfg.tune.model.lower() == "log-reg":
            # For log-reg, get AUROC from training results
            if logreg_results and "val_auroc" in logreg_results:
                val_auroc = float(logreg_results["val_auroc"])
        else:
            # For GRU/Transformer, get best AUROC from progress tracking
            job = get_job(job_id)
            if job and job.progress and job.progress.best_score is not None:
                val_auroc = float(job.progress.best_score)

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

        result_data = {
            "model_path": mdl_path,
            "model_type": cfg.tune.model,
            "ticker": ticker,
            "industry": industry,
            "used_pca": cfg.loader.dopca,
        }

        # Add validation AUROC for log-reg if available
        if val_auroc is not None:
            result_data["val_auroc"] = val_auroc

        update_job(
            job_id,
            {
                "status": "completed",
                "result": result_data,
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
