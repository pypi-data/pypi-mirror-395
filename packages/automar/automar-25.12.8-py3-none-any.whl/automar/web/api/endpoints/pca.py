# -*- coding: utf-8 -*-
"""PCA analysis endpoints."""
from datetime import datetime
from pathlib import Path
from typing import Optional
import tempfile
import uuid
import re

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import JSONResponse

from automar.shared.config.schemas import ExtractOptions, PCAOptions, GlobalConfig
from automar.shared.runners import run_pca
from automar.shared.persistence.library import read_df
from automar.web.api.models import PCAResponse, JobStatus
from automar.web.api.jobs import add_job, update_job
from automar.shared.persistence.job_store import get_job_store

router = APIRouter(prefix="/pca", tags=["pca"])


@router.post("", response_model=PCAResponse)
async def perform_pca(
    extract_options: str = Form(...),
    pca_options: str = Form(...),
    input_file: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None,
):
    """
    Perform PCA on extracted data or uploaded file or selected dataset.

    This is now a background operation that returns a job ID.
    """
    try:
        import json

        # Parse JSON strings
        extract_opts = ExtractOptions.model_validate(json.loads(extract_options))
        pca_opts = PCAOptions.model_validate(json.loads(pca_options))

        cfg = GlobalConfig(command="pca", extract=extract_opts, pca=pca_opts)

        job_id = str(uuid.uuid4())

        # Handle uploaded file - save temporarily
        temp_file_path = None
        if input_file:
            content = await input_file.read()
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=Path(input_file.filename).suffix
            ) as tmp:
                temp_file_path = Path(tmp.name)
                tmp.write(content)

        # Store complete input parameters (use mode='json' to serialize dates)
        job_inputs = {
            "extract": extract_opts.model_dump(mode="json"),
            "pca": pca_opts.model_dump(mode="json"),
            "uploaded_file": input_file.filename if input_file else None,
        }

        # Create job context with industry metadata
        job_context = {}
        if extract_opts.industry:
            job_context["industry"] = extract_opts.industry

        add_job(
            job_id,
            JobStatus(
                job_id=job_id,
                status="pending",
                type="pca",
                model=None,
                result=None,
                error=None,
                inputs=job_inputs,
                context=job_context if job_context else None,
            ),
        )

        # Run in background
        background_tasks.add_task(
            run_pca_background, job_id, cfg, temp_file_path, pca_opts.dataset_path
        )

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "PCA job started",
                "job_id": job_id,
                "check_status_at": f"/jobs/{job_id}",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_pca_background(
    job_id: str,
    cfg: GlobalConfig,
    temp_file_path: Optional[Path],
    dataset_path: Optional[str],
):
    """Background task for PCA analysis"""
    try:
        start_time = datetime.now()
        start_time_iso = start_time.isoformat()

        update_job(job_id, {"status": "running", "started_at": start_time_iso})

        # Load dataset
        dataset = None
        if temp_file_path:
            dataset = read_df(temp_file_path)
        elif dataset_path:
            dataset_path_obj = Path(dataset_path)
            if not dataset_path_obj.exists():
                raise FileNotFoundError(f"Dataset not found: {dataset_path}")

            # Check if this is a SQLite database
            if dataset_path_obj.suffix.lower() in [".sqlite", ".sqlite3", ".db"]:
                # Load SQLite data with gap validation (same as other jobs)
                from automar.shared.persistence.library import (
                    create_connection,
                    load_df_from_sqlite,
                    TABLE_NAME,
                )

                conn = create_connection(dataset_path_obj, mkfolder=False)
                try:
                    dataset = load_df_from_sqlite(
                        TABLE_NAME,
                        conn,
                        comp_name=cfg.extract.ticker,
                        ind_name=cfg.extract.industry,
                        start_date=(
                            str(cfg.extract.datest) if cfg.extract.datest else None
                        ),
                        end_date=(
                            str(cfg.extract.datend) if cfg.extract.datend else None
                        ),
                        validate_continuity=True,  # Enable gap detection for PCA jobs
                    )
                except Exception as e:
                    conn.close()
                    # Re-raise with context about what operation was being performed
                    operation_context = f"loading data for PCA analysis ({cfg.extract.industry or cfg.extract.ticker})"
                    raise ValueError(
                        f"Cannot complete {operation_context}: {str(e)}"
                    ) from e
                conn.close()
                dataset = dataset.dropna(ignore_index=True)
            else:
                # Regular file formats (feather, parquet, csv, etc.)
                dataset = read_df(dataset_path_obj)

        # Run PCA
        pca, pca_df, pca_file_path, df_file_path = run_pca(cfg, dataset)

        # Determine industry: prioritize user selection (extract_options.industry) over dataset extraction
        # This is important for SQLite mode where user explicitly selects a sector
        industry = cfg.extract.industry
        if not industry:
            # Fallback: extract industry from dataset (for regular file mode)
            from automar.web.api.utils import extract_industry_from_dataset

            industry = extract_industry_from_dataset(dataset)

        # Calculate timing
        end_time = datetime.now()
        end_time_iso = end_time.isoformat()
        duration_seconds = (end_time - start_time).total_seconds()

        # Format duration
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        duration_human = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        timing_info = {
            "started_at": start_time_iso,
            "completed_at": end_time_iso,
            "duration_seconds": duration_seconds,
            "duration_human": duration_human,
        }

        # Prepare file paths
        file_paths = {}
        if pca_file_path:
            file_paths["pca_object"] = str(pca_file_path)
        if df_file_path:
            file_paths["pca_dataframe"] = str(df_file_path)

        update_job(
            job_id,
            {
                "status": "completed",
                "result": {
                    "status": "success",
                    "message": "PCA completed successfully",
                    "n_components": pca.n_components_,
                    "explained_variance": (
                        pca.explained_variance_ratio_.tolist()
                        if hasattr(pca, "explained_variance_ratio_")
                        else None
                    ),
                    "file_paths": file_paths,
                    "industry": industry,
                },
                "timing": timing_info,
                "completed_at": end_time_iso,
            },
        )

    except Exception as e:
        update_job(job_id, {"status": "failed", "error": str(e)})
    finally:
        # Clean up temporary file
        if temp_file_path and temp_file_path.exists():
            try:
                temp_file_path.unlink()
            except Exception as cleanup_error:
                print(f"Warning: Failed to cleanup temporary PCA file: {cleanup_error}")


@router.get("-files")
async def list_pca_files():
    """Get list of available PCA pickle files with job metadata enrichment"""
    try:
        # Get base folder
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        pca_files = []

        # Look in the default out/pca/ directory (PCA objects)
        pca_dir = project_root / "out" / "pca"

        # Build a map of pca file paths -> job metadata for faster lookup
        job_store = get_job_store()
        all_jobs = job_store.get_all_jobs()
        pca_path_to_job = {}

        for job_id, job in all_jobs.items():
            if (
                job.get("type") == "pca"
                and job.get("status") == "completed"
                and job.get("result")
            ):
                file_paths = job["result"].get("file_paths", {})
                pca_object_path = file_paths.get("pca_object")
                if pca_object_path:
                    # Normalize path for comparison
                    try:
                        normalized_path = str(Path(pca_object_path).resolve())
                        pca_path_to_job[normalized_path] = {
                            "job_id": job_id,
                            "industry": job["result"].get("industry"),
                        }
                    except Exception:
                        # Skip if path resolution fails
                        pass

        if pca_dir.exists():
            # Search for .joblib (current format), .pkl, and .pickle files
            for pattern in ["*.joblib", "*.pkl", "*.pickle"]:
                for file_path in pca_dir.glob(pattern):
                    if file_path.is_file():
                        # Try to find associated job
                        normalized_file_path = str(file_path.resolve())
                        job_metadata = pca_path_to_job.get(normalized_file_path)

                        # Build file info
                        file_info = {
                            "name": file_path.name,
                            "path": str(file_path),
                            "relative_path": str(
                                file_path.resolve().relative_to(project_root)
                            ),
                            "size": file_path.stat().st_size,
                            "modified": file_path.stat().st_mtime,
                        }

                        # Enrich with job metadata if available
                        if job_metadata:
                            file_info.update(
                                {
                                    "industry": job_metadata["industry"],
                                    "job_id": job_metadata["job_id"],
                                }
                            )
                        else:
                            # Fallback: infer from filename
                            # Pattern: pca_IndustryName_... or IndustryName_pca_...
                            # Industry names may contain underscores (e.g., Consumer_Staples)
                            industry_match = re.match(
                                r"^(?:pca_)?([^_]+(?:_[^_]+)*?)_(?:\d{4}-\d{2}-\d{2}|[0-9]+y)",
                                file_path.name,
                                re.IGNORECASE,
                            )
                            industry = (
                                industry_match.group(1).strip()
                                if industry_match
                                else None
                            )
                            file_info.update({"industry": industry, "job_id": None})

                        pca_files.append(file_info)

        # Sort by modification time (newest first)
        pca_files.sort(key=lambda x: x["modified"], reverse=True)

        return {"pca_files": pca_files}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing parameter files: {str(e)}"
        )
