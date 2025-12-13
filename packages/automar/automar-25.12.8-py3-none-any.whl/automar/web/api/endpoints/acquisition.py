# -*- coding: utf-8 -*-
"""
Data acquisition endpoints (Phase 3 - Unified Acquisition System).

These endpoints provide access to the unified data acquisition system
for downloading missing companies, extending date ranges, and backfilling gaps.
"""
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List
import uuid

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from automar.shared.services.data_acquisition import (
    UnifiedDataAcquisition,
    DataAcquisitionRequest,
    AcquisitionMode,
    download_missing_companies,
    update_industry_to_date,
    backfill_all_gaps,
)
from automar.shared.services.gap_analyzer import GapAnalyzer
from automar.shared.config.path_resolver import get_output_dir
from automar.web.api.models import JobStatus
from automar.web.api.jobs import add_job, update_job

router = APIRouter(prefix="/acquire", tags=["acquisition"])


# ============================================================================
# Request/Response Models
# ============================================================================


class AcquireDataOptions(BaseModel):
    """Options for data acquisition operations."""

    mode: str = Field(
        ...,
        description="Acquisition mode: 'missing_companies', 'date_extension', 'backfill_gaps', 'full_industry', 'single_ticker'",
    )
    industry: str = Field(..., description="Industry name (GICS format)")
    companies: Optional[List[str]] = Field(
        None, description="List of company tickers (required for some modes)"
    )
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    db_path: Optional[str] = Field(
        None, description="Database path (default: out/data/data.sqlite)"
    )
    skip: bool = Field(
        True, description="Skip companies with insufficient data (default: true)"
    )
    gap_info: Optional[dict] = Field(
        None, description="Gap analysis result (required for backfill mode)"
    )


class DownloadMissingOptions(BaseModel):
    """Options for downloading missing companies."""

    industry: str = Field(..., description="Industry name (GICS format)")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    db_path: Optional[str] = Field(
        None, description="Database path (default: out/data/data.sqlite)"
    )


class UpdateIndustryOptions(BaseModel):
    """Options for updating industry to target date."""

    industry: str = Field(..., description="Industry name (GICS format)")
    target_date: Optional[str] = Field(
        None, description="Target date (YYYY-MM-DD, default: today)"
    )
    db_path: Optional[str] = Field(
        None, description="Database path (default: out/data/data.sqlite)"
    )


class BackfillGapsOptions(BaseModel):
    """Options for backfilling date gaps."""

    industry: str = Field(..., description="Industry name (GICS format)")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    db_path: Optional[str] = Field(
        None, description="Database path (default: out/data/data.sqlite)"
    )


# ============================================================================
# Endpoints
# ============================================================================


@router.post("/data")
async def acquire_data(options: AcquireDataOptions, background_tasks: BackgroundTasks):
    """
    Unified data acquisition endpoint (supports all acquisition modes).

    Acquisition modes:
    - missing_companies: Download specific companies
    - date_extension: Extend date range for existing companies
    - backfill_gaps: Fill date gaps for incomplete companies
    - full_industry: Download entire industry
    - single_ticker: Download single company

    Returns job ID for background processing.
    """
    try:
        # Validate mode
        valid_modes = [mode.value for mode in AcquisitionMode]
        if options.mode not in valid_modes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid mode: {options.mode}. Must be one of: {', '.join(valid_modes)}",
            )

        # Determine database path
        if options.db_path:
            db_path = Path(options.db_path)
        else:
            db_path = get_output_dir("data") / "data.sqlite"

        if not db_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Database file not found at {db_path}. Create database first using extraction endpoint.",
            )

        # Parse dates
        start_date = datetime.strptime(options.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(options.end_date, "%Y-%m-%d").date()

        # Create job
        job_id = str(uuid.uuid4())

        job_inputs = {
            "mode": options.mode,
            "industry": options.industry,
            "companies": options.companies,
            "start_date": options.start_date,
            "end_date": options.end_date,
            "db_path": str(db_path),
            "skip": options.skip,
        }

        add_job(
            job_id,
            JobStatus(
                job_id=job_id,
                status="pending",
                type="acquisition",
                model=None,
                result=None,
                error=None,
                inputs=job_inputs,
            ),
        )

        # Run in background
        background_tasks.add_task(
            run_acquisition_background,
            job_id,
            options.mode,
            options.industry,
            options.companies,
            start_date,
            end_date,
            db_path,
            options.skip,
            options.gap_info,
        )

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": f"Data acquisition job started (mode: {options.mode})",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/download-missing")
async def api_download_missing(
    options: DownloadMissingOptions, background_tasks: BackgroundTasks
):
    """
    Download missing companies for an industry (with gap analysis).

    This is a convenience endpoint that:
    1. Runs gap analysis
    2. Downloads missing companies
    3. Returns results

    Returns job ID for background processing.
    """
    try:
        # Determine database path
        if options.db_path:
            db_path = Path(options.db_path)
        else:
            db_path = get_output_dir("data") / "data.sqlite"

        if not db_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Database file not found at {db_path}",
            )

        # Parse dates
        start_date = datetime.strptime(options.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(options.end_date, "%Y-%m-%d").date()

        # Create job
        job_id = str(uuid.uuid4())

        job_inputs = {
            "operation": "download-missing",
            "industry": options.industry,
            "start_date": options.start_date,
            "end_date": options.end_date,
            "db_path": str(db_path),
        }

        add_job(
            job_id,
            JobStatus(
                job_id=job_id,
                status="pending",
                type="download-missing",
                model=None,
                result=None,
                error=None,
                inputs=job_inputs,
            ),
        )

        # Run in background
        background_tasks.add_task(
            run_download_missing_background,
            job_id,
            db_path,
            options.industry,
            start_date,
            end_date,
        )

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Download missing companies job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-industry")
async def api_update_industry(
    options: UpdateIndustryOptions, background_tasks: BackgroundTasks
):
    """
    Update industry data to target date (default: today).

    Handles both missing companies and date extensions.

    Returns job ID for background processing.
    """
    try:
        # Determine database path
        if options.db_path:
            db_path = Path(options.db_path)
        else:
            db_path = get_output_dir("data") / "data.sqlite"

        if not db_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Database file not found at {db_path}",
            )

        # Parse target date
        if options.target_date:
            target_date = datetime.strptime(options.target_date, "%Y-%m-%d").date()
        else:
            target_date = date.today()

        # Create job
        job_id = str(uuid.uuid4())

        job_inputs = {
            "operation": "update-industry",
            "industry": options.industry,
            "target_date": target_date.isoformat(),
            "db_path": str(db_path),
        }

        add_job(
            job_id,
            JobStatus(
                job_id=job_id,
                status="pending",
                type="update-industry",
                model=None,
                result=None,
                error=None,
                inputs=job_inputs,
            ),
        )

        # Run in background
        background_tasks.add_task(
            run_update_industry_background,
            job_id,
            db_path,
            options.industry,
            target_date,
        )

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Update industry job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backfill-gaps")
async def api_backfill_gaps(
    options: BackfillGapsOptions, background_tasks: BackgroundTasks
):
    """
    Fill date gaps for companies with incomplete data.

    Returns job ID for background processing.
    """
    try:
        # Determine database path
        if options.db_path:
            db_path = Path(options.db_path)
        else:
            db_path = get_output_dir("data") / "data.sqlite"

        if not db_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Database file not found at {db_path}",
            )

        # Parse dates
        start_date = datetime.strptime(options.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(options.end_date, "%Y-%m-%d").date()

        # Create job
        job_id = str(uuid.uuid4())

        job_inputs = {
            "operation": "backfill-gaps",
            "industry": options.industry,
            "start_date": options.start_date,
            "end_date": options.end_date,
            "db_path": str(db_path),
        }

        add_job(
            job_id,
            JobStatus(
                job_id=job_id,
                status="pending",
                type="backfill-gaps",
                model=None,
                result=None,
                error=None,
                inputs=job_inputs,
            ),
        )

        # Run in background
        background_tasks.add_task(
            run_backfill_gaps_background,
            job_id,
            db_path,
            options.industry,
            start_date,
            end_date,
        )

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Backfill gaps job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Background Task Handlers
# ============================================================================


def run_acquisition_background(
    job_id: str,
    mode: str,
    industry: str,
    companies: Optional[List[str]],
    start_date: date,
    end_date: date,
    db_path: Path,
    skip: bool,
    gap_info: Optional[dict],
):
    """Background task for unified data acquisition"""
    try:
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Create acquisition request
        request = DataAcquisitionRequest(
            mode=AcquisitionMode(mode),
            industry=industry,
            companies=companies,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            gap_info=gap_info,
        )

        # Execute acquisition
        acquisition = UnifiedDataAcquisition(db_path)
        result = acquisition.acquire(request)

        # Calculate timing
        end_time = datetime.now()
        end_time_iso = end_time.isoformat()
        duration_seconds = (end_time - start_time).total_seconds()

        # Format duration
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        duration_human = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        if result.success:
            update_job(
                job_id,
                {
                    "status": "completed",
                    "completed_at": end_time_iso,
                    "result": {
                        "mode": mode,
                        "companies_downloaded": result.companies_downloaded,
                        "companies_failed": result.companies_failed,
                        "rows_added": result.rows_added,
                        "rows_skipped": result.rows_skipped,
                        "date_range": [
                            (
                                result.date_range[0].isoformat()
                                if result.date_range[0]
                                else None
                            ),
                            (
                                result.date_range[1].isoformat()
                                if result.date_range[1]
                                else None
                            ),
                        ],
                        "summary": result.summary(),
                        "timing": {
                            "duration_seconds": duration_seconds,
                            "duration_human": duration_human,
                        },
                    },
                },
            )
        else:
            update_job(
                job_id,
                {
                    "status": "failed",
                    "completed_at": end_time_iso,
                    "error": result.error,
                },
            )

    except Exception as e:
        update_job(
            job_id,
            {
                "status": "failed",
                "error": str(e),
            },
        )


def run_download_missing_background(
    job_id: str,
    db_path: Path,
    industry: str,
    start_date: date,
    end_date: date,
):
    """Background task for download-missing command"""
    try:
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Execute download-missing (no user confirmation in API)
        result = download_missing_companies(
            db_file=db_path,
            industry=industry,
            start_date=start_date,
            end_date=end_date,
            no_confirm=True,  # API always auto-confirms
        )

        # Calculate timing
        end_time = datetime.now()
        end_time_iso = end_time.isoformat()
        duration_seconds = (end_time - start_time).total_seconds()

        # Format duration
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        duration_human = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        if result.success:
            update_job(
                job_id,
                {
                    "status": "completed",
                    "completed_at": end_time_iso,
                    "result": {
                        "companies_downloaded": result.companies_downloaded,
                        "companies_failed": result.companies_failed,
                        "rows_added": result.rows_added,
                        "rows_skipped": result.rows_skipped,
                        "summary": result.summary(),
                        "timing": {
                            "duration_seconds": duration_seconds,
                            "duration_human": duration_human,
                        },
                    },
                },
            )
        else:
            update_job(
                job_id,
                {
                    "status": "failed",
                    "completed_at": end_time_iso,
                    "error": result.error,
                },
            )

    except Exception as e:
        update_job(
            job_id,
            {
                "status": "failed",
                "error": str(e),
            },
        )


def run_update_industry_background(
    job_id: str,
    db_path: Path,
    industry: str,
    target_date: date,
):
    """Background task for update-industry command"""
    try:
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Execute update-industry
        result = update_industry_to_date(
            db_file=db_path,
            industry=industry,
            target_date=target_date,
        )

        # Calculate timing
        end_time = datetime.now()
        end_time_iso = end_time.isoformat()
        duration_seconds = (end_time - start_time).total_seconds()

        # Format duration
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        duration_human = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        if result.success:
            update_job(
                job_id,
                {
                    "status": "completed",
                    "completed_at": end_time_iso,
                    "result": {
                        "companies_downloaded": result.companies_downloaded,
                        "companies_failed": result.companies_failed,
                        "rows_added": result.rows_added,
                        "rows_skipped": result.rows_skipped,
                        "summary": result.summary(),
                        "timing": {
                            "duration_seconds": duration_seconds,
                            "duration_human": duration_human,
                        },
                    },
                },
            )
        else:
            update_job(
                job_id,
                {
                    "status": "failed",
                    "completed_at": end_time_iso,
                    "error": result.error,
                },
            )

    except Exception as e:
        update_job(
            job_id,
            {
                "status": "failed",
                "error": str(e),
            },
        )


def run_backfill_gaps_background(
    job_id: str,
    db_path: Path,
    industry: str,
    start_date: date,
    end_date: date,
):
    """Background task for backfill-gaps command"""
    try:
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Execute backfill-gaps (no user confirmation in API)
        result = backfill_all_gaps(
            db_file=db_path,
            industry=industry,
            start_date=start_date,
            end_date=end_date,
        )

        # Calculate timing
        end_time = datetime.now()
        end_time_iso = end_time.isoformat()
        duration_seconds = (end_time - start_time).total_seconds()

        # Format duration
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        duration_human = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        if result.success:
            update_job(
                job_id,
                {
                    "status": "completed",
                    "completed_at": end_time_iso,
                    "result": {
                        "companies_downloaded": result.companies_downloaded,
                        "companies_failed": result.companies_failed,
                        "rows_added": result.rows_added,
                        "rows_skipped": result.rows_skipped,
                        "summary": result.summary(),
                        "timing": {
                            "duration_seconds": duration_seconds,
                            "duration_human": duration_human,
                        },
                    },
                },
            )
        else:
            update_job(
                job_id,
                {
                    "status": "failed",
                    "completed_at": end_time_iso,
                    "error": result.error,
                },
            )

    except Exception as e:
        update_job(
            job_id,
            {
                "status": "failed",
                "error": str(e),
            },
        )
