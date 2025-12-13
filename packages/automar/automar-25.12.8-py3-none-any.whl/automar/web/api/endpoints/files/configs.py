# -*- coding: utf-8 -*-
"""Configuration and parameter file operations endpoints."""
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

from automar.shared.persistence.job_store import get_job_store

router = APIRouter(tags=["files", "configs"])


@router.get("/parameter-files")
async def list_parameter_files():
    """Get list of available hyperparameter TOML files with job metadata enrichment"""
    try:
        from pathlib import Path
        import re

        # Get base folder - same logic as tuning save location
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        parameter_files = []

        # Look in the exact directory where tuning saves files
        # This matches the save logic: project_root / cfg.tune.param_path (default "out/hyper")
        # Search recursively through model subdirectories (gru/, transformer/, logreg/)
        param_dir = project_root / "out" / "hyper"  # Default parameter directory

        # Build a map of config_path -> job metadata for faster lookup
        job_store = get_job_store()
        all_jobs = job_store.get_all_jobs()
        config_to_job = {}

        for job_id, job in all_jobs.items():
            if (
                job.get("type") == "tuning"
                and job.get("status") == "completed"
                and job.get("result")
            ):
                config_path = job["result"].get("config_path")
                if config_path:
                    # Normalize path for comparison (resolve to absolute path)
                    try:
                        normalized_path = str(Path(config_path).resolve())
                        config_to_job[normalized_path] = {
                            "job_id": job_id,
                            "ticker": job["result"].get("ticker"),
                            "industry": job["result"].get("industry"),
                            "best_score": job["result"].get("best_score"),
                            "total_trials": job["result"].get("total_trials"),
                            "model": job["result"].get("model"),
                            "used_pca": job["result"].get(
                                "used_pca"
                            ),  # PCA compatibility flag
                        }
                    except Exception:
                        # Skip if path resolution fails
                        pass

        if param_dir.exists():
            for file_path in param_dir.rglob("*_hyperparameters_*.toml"):
                if file_path.is_file():
                    # Try to find associated job
                    normalized_file_path = str(file_path.resolve())
                    job_metadata = config_to_job.get(normalized_file_path)

                    # Extract model type from filename (fallback if no job metadata)
                    model_from_filename = "unknown"
                    filename_parts = file_path.stem.split("_")
                    for part in filename_parts:
                        if part.upper() in ["GRU", "TRANSFORMER", "LOG-REG"]:
                            model_from_filename = part.upper()
                            break

                    # Extract score from simple TOML regex (fallback)
                    score = None
                    try:
                        with open(file_path, "r") as f:
                            text = f.read()
                            score_match = re.search(
                                r"(?:score|best_score|accuracy)\s*=\s*([\d.]+)",
                                text,
                            )
                            if score_match:
                                score = float(score_match.group(1))
                    except:
                        pass

                    # Build file metadata
                    file_info = {
                        "name": file_path.name,
                        "path": str(file_path),
                        "relative_path": str(file_path.relative_to(project_root)),
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime,
                        "model_type": (
                            job_metadata.get("model", model_from_filename)
                            if job_metadata
                            else model_from_filename
                        ),
                        "score": (
                            job_metadata.get("best_score", score)
                            if job_metadata
                            else score
                        ),
                        "directory": file_path.parent.name,
                    }

                    # Enrich with job metadata if available
                    if job_metadata:
                        file_info.update(
                            {
                                "ticker": job_metadata["ticker"],
                                "industry": job_metadata["industry"],
                                "has_ticker_data": bool(job_metadata["ticker"]),
                                "job_id": job_metadata["job_id"],
                                "total_trials": job_metadata["total_trials"],
                                "used_pca": job_metadata.get(
                                    "used_pca"
                                ),  # PCA compatibility flag
                            }
                        )
                    else:
                        # Fallback: infer from filename (less reliable but works for old files)
                        has_ticker = bool(re.search(r"\([A-Z]+\)", file_path.name))
                        ticker_match = re.search(r"\(([A-Z]+)\)", file_path.name)
                        ticker = ticker_match.group(1) if ticker_match else None

                        # Extract industry name - stop at '(' for ticker or at model type pattern
                        # Pattern: IndustryName_MODEL_hyperparameters or IndustryName(TICK)_MODEL_hyperparameters
                        industry_match = re.match(
                            r"^([^(]+?)(?:\([A-Z]+\))?_(?:GRU|TRANSFORMER|LOG-REG|log-reg|gru|transformer)_",
                            file_path.name,
                        )
                        industry = (
                            industry_match.group(1).strip() if industry_match else None
                        )

                        file_info.update(
                            {
                                "ticker": ticker,
                                "industry": industry,
                                "has_ticker_data": has_ticker,
                                "job_id": None,
                                "total_trials": None,
                                "used_pca": None,  # Unknown for legacy files without job metadata
                            }
                        )

                    parameter_files.append(file_info)

        # Sort by modification time (newest first)
        parameter_files.sort(key=lambda x: x["modified"], reverse=True)

        return {"parameter_files": parameter_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
