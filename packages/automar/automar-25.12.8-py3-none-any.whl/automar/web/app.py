# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import tempfile
from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    BackgroundTasks,
    Query,
)
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import threading
import time
import uuid

# Import from new modular structure
from automar.web.api.models import (
    ExtractResponse,
    PCAResponse,
    TuningResponse,
    TrainingResponse,
    CrossvalidateResponse,
    TuningProgress,
    JobStatus,
    TuningProgressCallback,
)
from automar.web.api.jobs import (
    get_job,
    update_job,
    add_job,
    stop_thread,
    cleanup_progress_store,
    progress_store,
    active_job_threads,
    progress_store_timestamps,
)
from automar.web.api.preload import preload_lightweight_modules, preload_torch
from automar.shared.config.path_resolver import get_output_dir

from automar.shared.config.schemas import (
    ExtractOptions,
    PCAOptions,
    LoaderOptions,
    TuningOptions,
    TrainingOptions,
    CrossvalidateOptions,
    GlobalConfig,
)
from automar.shared.runners import (
    run_extraction,
    run_pca,
    run_tuning,
    run_training,
    run_crossvalidation,
)
from automar.shared.persistence.library import (
    ValidFormats,
    VALID_INDUSTRY,
    Periods,
    write_df,
    read_df,
)
from automar.shared.config.config_utils import merge

# Persistent job storage using SQLite
from automar.shared.persistence.job_store import get_job_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting automar API server...")
    # Initialize job store and load existing jobs
    job_store = get_job_store()
    print(f"Job storage initialized at: {job_store.db_path}")

    # Clean up old jobs on startup (7 days)
    deleted = job_store.cleanup_old_jobs(days=7)
    if deleted > 0:
        print(f"Cleaned up {deleted} old jobs")

    # Clean up old progress entries
    progress_cleaned = cleanup_progress_store()
    if progress_cleaned > 0:
        print(f"Cleaned up {progress_cleaned} old progress entries")

    # Start preloading lightweight ML modules after 2s delay
    # (gives time for initial UI requests to complete first)
    import asyncio

    asyncio.create_task(delayed_lightweight_preload())

    yield
    # Shutdown
    print("Shutting down automar API server...")


async def delayed_lightweight_preload():
    """Delay lightweight module preload to not interfere with initial UI load"""
    import asyncio

    await asyncio.sleep(2)
    preload_lightweight_modules()


# Custom JSONResponse with UTF-8 charset
class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"


app = FastAPI(
    title="Automar API",
    description="REST API for financial data extraction, PCA analysis, and model training",
    version="1.0.1",
    lifespan=lifespan,
    default_response_class=UTF8JSONResponse,
)

# Add CORS middleware
# Allow both dev and production origins
import os

# In production, frontend is served from same origin, but allow dev origins too
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS
    + ["*"],  # Allow all origins since frontend is bundled
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include endpoint routers
from automar.web.api.endpoints import (
    extraction,
    pca,
    metadata,
    jobs,
    training,
    prediction,
    files,
    search_space,
    hyperparameters,
    visualizations,
    settings,
    acquisition,  # Phase 3 - Unified Acquisition System
)

app.include_router(extraction.router)
app.include_router(pca.router)
app.include_router(metadata.router)
app.include_router(jobs.router)
app.include_router(training.router)
app.include_router(prediction.router)
app.include_router(files.router)
app.include_router(search_space.router)
app.include_router(hyperparameters.router)
app.include_router(visualizations.router)
app.include_router(settings.router)
app.include_router(acquisition.router)  # Phase 3 - Unified Acquisition System


# Suppress Chrome DevTools protocol requests (silently return 204 No Content)
@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def suppress_chrome_devtools():
    """Silently handle Chrome DevTools protocol requests to prevent 404 errors"""
    return Response(status_code=204)


# Health check endpoint - must be defined BEFORE static files mount
@app.get("/health")
async def health_check():
    """Health check endpoint with dependency status"""
    # Check for optional dependencies WITHOUT importing them (to avoid blocking on startup)
    # Use importlib.util.find_spec which only checks if module is importable
    import importlib.util

    pytorch_available = importlib.util.find_spec("torch") is not None
    torcheval_available = importlib.util.find_spec("torcheval") is not None
    ray_available = importlib.util.find_spec("ray") is not None

    warnings = []
    if not pytorch_available:
        warnings.append(
            {
                "type": "missing_dependency",
                "severity": "warning",
                "title": "PyTorch not installed",
                "message": "Hyperparameter tuning, training, and cross-validation jobs for GRU and Transformer models will not be available.",
                "install_command": "See installation guide for PyTorch setup instructions",
                "install_url": "https://pytorch.org/get-started/locally/",
                "affects": ["tune", "train", "crossvalidate"],
            }
        )
    elif not torcheval_available:
        # Only show torcheval warning if PyTorch is installed
        warnings.append(
            {
                "type": "missing_dependency",
                "severity": "warning",
                "title": "TorchEval not installed",
                "message": "TorchEval is required for training and cross-validation jobs. PyTorch must be installed before installing TorchEval.",
                "install_command": "pip install torcheval",
                "install_url": "https://meta-pytorch.org/torcheval/stable/",
                "affects": ["train", "crossvalidate"],
            }
        )

    if not ray_available:
        warnings.append(
            {
                "type": "missing_dependency",
                "severity": "warning",
                "title": "Ray not installed",
                "message": "Hyperparameter tuning, training, and cross-validation jobs will not be available. Note: Ray does not support Python 3.13 on Windows (Linux users are unaffected).",
                "install_command": 'pip install -U "ray[data,train,tune,serve]"',
                "install_url": "https://docs.ray.io/en/latest/ray-overview/installation.html",
                "affects": ["tune", "train", "crossvalidate"],
            }
        )

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "pytorch": pytorch_available,
            "torcheval": torcheval_available,
            "ray": ray_available,
        },
        "warnings": warnings,
    }


@app.get("/devices")
async def get_devices():
    """Get available compute devices (CPU/CUDA)"""
    devices = ["cpu"]
    default_device = "cpu"

    try:
        import torch

        if torch.cuda.is_available():
            cuda_count = torch.cuda.device_count()
            for i in range(cuda_count):
                devices.append(f"cuda:{i}")
            devices.append("cuda")
            default_device = "cuda"
    except Exception:
        # Catch all exceptions - ImportError, AttributeError, RuntimeError, etc.
        pass

    return {"devices": devices, "default": default_device}


# Mount static files for frontend (always in web/static/)
# SvelteKit builds directly to src/automar/web/static/ (see frontend/svelte.config.js)
from automar.shared.config.path_resolver import get_package_root

package_root = get_package_root()
static_dir = package_root / "web" / "static"

if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
    print(f"[OK] Serving frontend from: {static_dir}")
else:
    print(f"[WARNING] Frontend build not found at {static_dir}")
    print("  Options:")
    print("    1. Build frontend: cd frontend && npm install && npm run build")
    print(
        "    2. Run in development mode with separate frontend server (http://localhost:5173)"
    )
    print("    3. Install package with BUILD_WEB=1: BUILD_WEB=1 pip install .")

    @app.get("/")
    async def root():
        """Root endpoint with API information (development mode)"""
        return {
            "name": "Automar API",
            "version": "1.0.1",
            "mode": "development",
            "message": "Frontend should be running separately on http://localhost:5173",
            "endpoints": {
                "extract": "/extract",
                "pca": "/pca",
                "tune": "/tune",
                "train": "/train",
                "crossvalidate": "/crossvalidate",
                "jobs": "/jobs/{job_id}",
            },
            "docs": "/docs",
        }


@app.get("/progress/{operation_id}")
async def get_progress(operation_id: str):
    """Get progress for a long-running operation"""
    # Opportunistic cleanup on progress checks
    if len(progress_store) > 100:  # Only cleanup if store is getting large
        cleanup_progress_store()

    if operation_id not in progress_store:
        raise HTTPException(status_code=404, detail="Operation not found")

    return progress_store[operation_id]


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    purpose: str = Query(
        ..., description="Purpose of upload: 'data', 'config', 'model'"
    ),
):
    """
    Upload a file for use in other endpoints.

    Checks if an identical file already exists in datasets/ to avoid duplicates.
    Returns a file path that can be used in subsequent requests.
    """
    try:
        import hashlib

        # Read file content
        content = await file.read()

        # Calculate hash of uploaded file
        file_hash = hashlib.sha256(content).hexdigest()

        # Check if identical file exists in project directories
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()

        # Directories to search based on purpose
        search_dirs = []
        if purpose == "data":
            search_dirs.append(project_root / "out" / "data")
        elif purpose == "config":
            search_dirs.extend(
                [
                    project_root / "out" / "hyper",
                    project_root / "examples",
                ]
            )
        elif purpose == "model":
            search_dirs.append(project_root / "out" / "models")

        # Search for duplicate files
        file_ext = Path(file.filename).suffix
        for search_dir in search_dirs:
            if search_dir.exists():
                for existing_file in search_dir.rglob(f"*{file_ext}"):
                    if existing_file.is_file():
                        # Compare hash
                        with open(existing_file, "rb") as f:
                            existing_hash = hashlib.sha256(f.read()).hexdigest()

                        if existing_hash == file_hash:
                            # Found identical file! Use it instead of copying
                            relative_path = existing_file.relative_to(project_root)
                            return {
                                "status": "success",
                                "message": f"Using existing file (duplicate detected): {relative_path}",
                                "file_path": str(relative_path),
                                "file_id": "existing",
                                "original_filename": file.filename,
                                "duplicate_of": str(relative_path),
                            }

        # No duplicate found - proceed with normal upload
        upload_dir = get_output_dir("uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save file with unique name
        import uuid

        file_id = str(uuid.uuid4())
        file_ext = Path(file.filename).suffix
        file_path = upload_dir / f"{purpose}_{file_id}{file_ext}"

        with open(file_path, "wb") as f:
            f.write(content)

        return {
            "status": "success",
            "message": "File uploaded successfully",
            "file_path": str(file_path),
            "file_id": file_id,
            "original_filename": file.filename,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def extract_industry_from_dataset(dataset_or_path) -> Optional[str]:
    """
    Extract the most common industry from a dataset.

    Args:
        dataset_or_path: Either a pandas DataFrame or a path to a dataset file

    Returns:
        Most common industry name, or None if not found
    """
    try:
        import pandas as pd

        # Load dataset if path provided
        if isinstance(dataset_or_path, (str, Path)):
            df = read_df(Path(dataset_or_path))
        else:
            df = dataset_or_path

        # Extract industry using the same logic as main.py
        if "Industry" in df.columns:
            industry = df["Industry"].value_counts().idxmax()
            return str(industry) if pd.notna(industry) else None

        return None
    except Exception as e:
        print(f"Warning: Could not extract industry from dataset: {e}")
        return None


def cleanup_uploaded_files(cfg: GlobalConfig):
    """
    Clean up uploaded files that were used for this job.
    Only deletes files in out/uploads/ directory, not files from out/data/out/hyper/out/models.
    """
    try:
        # Get absolute path to uploads directory relative to project root
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        upload_dir = project_root / "out" / "uploads"

        if not upload_dir.exists():
            return

        # Check all paths in the config that might point to uploaded files
        paths_to_check = []

        # Check dataset_path (used for data files)
        if cfg.pca.dataset_path:
            paths_to_check.append(Path(cfg.pca.dataset_path))

        # Check config file path (used for hyperparameter files)
        if hasattr(cfg, "train") and cfg.train.cfg_path:
            paths_to_check.append(Path(cfg.train.cfg_path))

        # Delete only files that are in uploads/ directory
        for path in paths_to_check:
            # Make path absolute if needed
            if not path.is_absolute():
                path = project_root / path

            # Only delete if it's in uploads/ directory
            try:
                path.resolve().relative_to(upload_dir.resolve())
                if path.exists() and path.is_file():
                    path.unlink()
                    print(f"Cleaned up uploaded file: {path}")
            except ValueError:
                # Path is not in uploads/ directory - don't delete
                pass

    except Exception as e:
        # Don't fail the job if cleanup fails
        print(f"Warning: Failed to cleanup uploaded files: {e}")


@app.delete("/cleanup/{file_id}")
async def cleanup_file(file_id: str):
    """Clean up uploaded files"""
    try:
        upload_dir = get_output_dir("uploads")
        # Find and delete files matching the file_id
        deleted = []
        for file_path in upload_dir.glob(f"*_{file_id}*"):
            file_path.unlink()
            deleted.append(str(file_path))

        if not deleted:
            raise HTTPException(status_code=404, detail="File not found")

        return {
            "status": "success",
            "message": "Files cleaned up",
            "deleted_files": deleted,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/tuning/{job_id}")
async def download_tuning_results(job_id: str):
    """Download tuning results TOML file"""
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "completed" or not job.result:
        raise HTTPException(
            status_code=400, detail="Job not completed or no results available"
        )

    if "config_path" not in job.result:
        raise HTTPException(status_code=400, detail="No config file path available")

    config_path = Path(job.result["config_path"])
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"Config file not found: {config_path}"
        )

    return FileResponse(
        path=str(config_path),
        media_type="application/octet-stream",
        filename=job.result.get("config_filename", "tuning_results.toml"),
    )


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return UTF8JSONResponse(
        status_code=400, content={"error": "Bad Request", "detail": str(exc)}
    )


@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request, exc):
    return UTF8JSONResponse(
        status_code=404, content={"error": "Not Found", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
