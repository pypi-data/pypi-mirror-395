# -*- coding: utf-8 -*-
"""Data extraction endpoints."""
from datetime import datetime
from pathlib import Path
import tempfile
import uuid

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

from automar.shared.config.schemas import ExtractOptions, GlobalConfig
from automar.shared.runners import run_extraction
from automar.shared.persistence.library import write_df, FinderSt
from automar.web.api.models import ExtractResponse, JobStatus
from automar.web.api.jobs import add_job, update_job

router = APIRouter(prefix="/extract", tags=["extraction"])


@router.post("", response_model=ExtractResponse)
async def extract_data(options: ExtractOptions, background_tasks: BackgroundTasks):
    """
    Extract financial data based on ticker or industry.

    This is a background operation that returns a job ID.
    The job will complete quickly if data already exists (when force=False).
    """
    try:
        # Validate ticker vs industry
        if not options.ticker and not options.industry:
            raise HTTPException(
                status_code=400,
                detail="Must specify either ticker or industry (or both)",
            )

        # Create config object
        cfg = GlobalConfig(command="extract", extract=options)

        job_id = str(uuid.uuid4())

        # Store complete input parameters (use mode='json' to serialize dates)
        job_inputs = {
            "extract": options.model_dump(mode="json"),
        }

        add_job(
            job_id,
            JobStatus(
                job_id=job_id,
                status="pending",
                type="extract",
                model=None,
                result=None,
                error=None,
                inputs=job_inputs,
            ),
        )

        # Run in background
        background_tasks.add_task(run_extraction_background, job_id, cfg)

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Data extraction job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_extraction_background(job_id: str, cfg: GlobalConfig):
    """Background task for data extraction"""
    try:
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Run extraction
        df = run_extraction(cfg.extract)

        # Calculate timing
        end_time = datetime.now()
        end_time_iso = end_time.isoformat()
        duration_seconds = (end_time - start_time).total_seconds()

        # Format duration as human-readable
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        duration_human = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        timing_info = {
            "started_at": start_time_iso,
            "completed_at": end_time_iso,
            "duration_seconds": duration_seconds,
            "duration_human": duration_human,
        }

        # Get the actual file path and extraction status from dataframe metadata
        output_paths = []
        if hasattr(df, "attrs") and "file_path" in df.attrs:
            output_paths.append(df.attrs["file_path"])

        # Check extraction status to determine if file was loaded or newly extracted
        extraction_status = df.attrs.get("extraction_status", None)
        was_loaded = extraction_status == FinderSt.SUCCESS

        # Customize message based on whether file existed
        if was_loaded:
            message = "Loaded existing data from file"
            action = "loaded"
        else:
            message = "Downloaded and saved new data"
            action = "downloaded"

        # Get actual date range from the extracted data
        # This is important because when using 'history' instead of explicit dates,
        # cfg.extract.datest will be None. We need the actual dates from the dataframe.
        actual_date_start = None
        actual_date_end = None
        if "Date" in df.columns and len(df) > 0:
            import pandas as pd

            # Ensure Date column is datetime
            if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
                df["Date"] = pd.to_datetime(df["Date"])

            actual_date_start = df["Date"].min().strftime("%Y-%m-%d")
            actual_date_end = df["Date"].max().strftime("%Y-%m-%d")

        # Get the actual industry from the dataframe
        # When a ticker is provided without an industry, the extraction service
        # determines the industry automatically. We need to capture this actual
        # industry rather than just echoing the input (which could be None).
        actual_industry = cfg.extract.industry
        if actual_industry is None and "Industry" in df.columns and len(df) > 0:
            # Get the industry from the dataframe
            # If a ticker was provided, get the industry for that ticker
            if cfg.extract.ticker:
                ticker_data = df[
                    df["Company"].str.upper() == cfg.extract.ticker.upper()
                ]
                if len(ticker_data) > 0:
                    actual_industry = ticker_data["Industry"].iloc[0]
            # Otherwise, get the first industry (for industry-based extractions)
            if actual_industry is None:
                actual_industry = df["Industry"].iloc[0]

        update_job(
            job_id,
            {
                "status": "completed",
                "result": {
                    "status": "success",
                    "message": message,
                    "action": action,  # "loaded" or "downloaded"
                    "rows": len(df),
                    "columns": len(df.columns),
                    "ticker": cfg.extract.ticker,
                    "industry": actual_industry,
                    "format": cfg.extract.format,
                    "date_start": actual_date_start,
                    "date_end": actual_date_end,
                    "output_paths": output_paths,
                    "extraction_status": (
                        extraction_status.name if extraction_status else None
                    ),
                },
                "timing": timing_info,
                "completed_at": end_time_iso,
            },
        )

    except Exception as e:
        update_job(job_id, {"status": "failed", "error": str(e)})


@router.post("/download")
async def download_extracted_data(options: ExtractOptions):
    """
    Extract data and return as downloadable file.
    """
    try:
        cfg = GlobalConfig(command="extract", extract=options)

        df = run_extraction(cfg.extract)

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{options.format}"
        ) as tmp:
            write_df(df, Path(tmp.name))
            tmp_path = tmp.name

        return FileResponse(
            path=tmp_path,
            media_type="application/octet-stream",
            filename=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{options.format}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
