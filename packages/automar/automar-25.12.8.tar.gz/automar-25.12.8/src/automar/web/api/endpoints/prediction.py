# -*- coding: utf-8 -*-
"""Prediction/inference endpoints."""
from datetime import datetime
import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from automar.shared.config.schemas import (
    PredictionOptions,
    ExtractOptions,
    PCAOptions,
    LoaderOptions,
    TuningOptions,
    TrainingOptions,
    GlobalConfig,
)
from automar.web.api.models import JobStatus, PredictionResponse
from automar.web.api.jobs import add_job, update_job

# DO NOT import run_prediction here - defer to background task to keep endpoint fast
# from ...runners.predict_runner import run_prediction

router = APIRouter(tags=["prediction"])


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


@router.post("/start-prediction", response_model=PredictionResponse)
async def start_prediction(
    predict_options: PredictionOptions,
    extract_options: ExtractOptions,
    pca_options: PCAOptions,
    loader_options: LoaderOptions,
    tuning_options: TuningOptions,
    training_options: TrainingOptions,
    background_tasks: BackgroundTasks,
):
    """
    Start a prediction job using a trained model

    Similar to /train endpoint but loads model instead of training.
    Returns immediately with job_id for status polling.
    """
    try:
        cfg = GlobalConfig(
            command="predict",
            predict=predict_options,
            extract=extract_options,
            pca=pca_options,
            loader=loader_options,
            tune=tuning_options,
            train=training_options,
        )

        job_id = str(uuid.uuid4())

        # Extract model type from model file path (fast - just from filename)
        model_type = "unknown"
        if predict_options.model_path:
            from pathlib import Path

            model_path = Path(predict_options.model_path)
            # Infer model type from path (fast, no file I/O)
            # Paths typically like: out/models/gru/GRU_Technology_2025-10-27.pth
            path_lower = str(model_path).lower()
            if (
                "/gru/" in path_lower
                or "\\gru\\" in path_lower
                or path_lower.startswith("gru")
            ):
                model_type = "GRU"
            elif (
                "/transformer/" in path_lower
                or "\\transformer\\" in path_lower
                or path_lower.startswith("transformer")
            ):
                model_type = "transformer"
            elif (
                "/logreg/" in path_lower
                or "\\logreg\\" in path_lower
                or "/log-reg/" in path_lower
                or "\\log-reg\\" in path_lower
            ):
                model_type = "log-reg"
            # If still unknown, it will be updated when job completes

        # Create job with proper signature (use mode='json' to serialize Path objects)
        job_status = JobStatus(
            job_id=job_id,
            status="pending",
            type="prediction",
            model=model_type,
            inputs={
                "predict": predict_options.model_dump(mode="json"),
                "extract": extract_options.model_dump(mode="json"),
                "pca": pca_options.model_dump(mode="json"),
                "loader": loader_options.model_dump(mode="json"),
                "tuning": tuning_options.model_dump(mode="json"),
                "training": training_options.model_dump(mode="json"),
            },
        )

        add_job(job_id, job_status)

        # Add background task
        background_tasks.add_task(run_prediction_background, job_id, cfg)

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Prediction job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_prediction_background(job_id: str, cfg: GlobalConfig):
    """Background task for running prediction"""
    try:
        # Import run_prediction here to avoid blocking the endpoint response
        # This defers the heavy torch/numpy imports until the background task runs
        from automar.shared.runners.predict_runner import run_prediction

        # Capture start time
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        # Update status to running with start time
        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Run prediction
        results = run_prediction(cfg)

        # Calculate timing
        end_time = datetime.now()
        timing_info = calculate_timing_info(start_time_iso, end_time)

        # Extract dataset info for job metadata
        dataset_info = results.get("dataset", {})
        ticker = dataset_info.get("ticker")
        industry = dataset_info.get("industry")

        # Update job with results and timing
        update_job(
            job_id,
            {
                "status": "completed",
                "timing": timing_info,
                "completed_at": timing_info["completed_at"],
                "model": results.get(
                    "model_type", "unknown"
                ),  # Update model type from results
                "result": {
                    "metrics": results.get("metrics"),
                    "confusion_matrix": results.get("confusion_matrix"),
                    "output_paths": results.get("output_paths", {}),
                    "model_type": results.get("model_type"),
                    "model_path": results.get("model_path"),
                    "dataset": dataset_info,
                    "num_predictions": len(results.get("predictions", [])),
                    "mode": cfg.predict.mode,
                    "ticker": ticker,
                    "industry": industry,
                    "used_pca": cfg.loader.dopca,
                    # Add forecast-specific data
                    "predictions": results.get("predictions", []),
                    "probabilities": results.get("probabilities", []),
                    "forecast_date": results.get(
                        "forecast_date"
                    ),  # Single day (legacy)
                    "forecast_dates": results.get("forecast_dates", []),  # Multi-day
                    "forecast_days": results.get("forecast_days"),  # Number of days
                },
            },
        )

    except Exception as e:
        import traceback
        from automar.web.api.jobs import get_job

        # Calculate timing even on failure
        end_time = datetime.now()
        job = get_job(job_id)
        timing = None
        if job and job.started_at:
            timing = calculate_timing_info(job.started_at, end_time)

        error_msg = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        update_job(
            job_id,
            {
                "status": "failed",
                "error": error_msg,
                "completed_at": end_time.isoformat(),
                "timing": timing,
            },
        )
