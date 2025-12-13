# -*- coding: utf-8 -*-
"""Settings management endpoints."""
import os
import shutil
from pathlib import Path
from typing import Dict, Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from automar.shared.config.path_resolver import (
    get_project_root,
    get_output_dir,
    get_config_path,
)
from automar.shared.config.config_utils import (
    load_config,
    save_config,
    update_config_paths,
    get_effective_defaults,
    dump_schema_defaults_to_config,
)
from automar.shared.services.file_utils import open_folder_in_explorer

router = APIRouter(prefix="/settings", tags=["settings"])


# Pydantic models for request/response
class PathValidationRequest(BaseModel):
    path: str = Field(..., description="Path to validate")


class PathValidationResponse(BaseModel):
    valid: bool
    exists: bool
    can_create: bool
    writable: bool
    readable: bool
    disk_space_gb: float
    has_existing_data: bool
    existing_files_count: int
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)


class StoragePathsUpdate(BaseModel):
    root: Optional[str] = Field(None, description="Root directory path")
    overrides: Optional[Dict[str, Optional[str]]] = Field(
        None, description="Dict of operation -> path overrides"
    )


class StoragePathsResponse(BaseModel):
    current: Dict[str, str]  # Currently active paths
    source: Dict[str, str]  # Source of each path (config.toml, env, default)
    default: Dict[str, str]  # True defaults without any config overrides
    config_path: str


class UpdatePathsResponse(BaseModel):
    success: bool
    config_path: str
    validation_warnings: List[str] = Field(default_factory=list)


# List of all operations that have output directories
OPERATIONS = [
    "data",
    "pca",
    "pca_data",
    "hyper",
    "models",
    "cross",
    "preds",
    "jobs",
    "ray",
    "search_spaces",
]


def get_path_source(operation: str, config: dict) -> str:
    """
    Determine the source of a path configuration.

    Returns: "config.toml", "env", or "default"
    """
    if config and "paths" in config:
        if operation in config["paths"]:
            return "config.toml"
        if "root" in config["paths"]:
            return "config.toml"

    # Check for environment variable
    if os.getenv("AUTOMAR_DATA_DIR"):
        return "env"

    return "default"


def resolve_operation_path(
    operation: str, config: dict, use_pending: bool = False
) -> Path:
    """
    Resolve the path for a specific operation.

    Args:
        operation: Name of the operation (data, pca, models, etc.)
        config: Loaded configuration dict
        use_pending: If True, use pending config.toml values; if False, use current runtime values

    Returns:
        Path: Resolved path for the operation
    """
    if use_pending and config and "paths" in config:
        # Check for specific operation override in config
        if operation in config["paths"]:
            return Path(config["paths"][operation])

        # Check for root override in config
        if "root" in config["paths"]:
            root = Path(config["paths"]["root"])
            # Handle special cases for nested paths
            if operation == "pca_data":
                return root / "out" / "pca" / "data"
            return root / "out" / operation

    # For current paths or when no pending config, use runtime resolution
    if not use_pending:
        # Special handling for nested paths
        if operation == "pca_data":
            return get_output_dir("pca") / "data"
        return get_output_dir(operation)

    # Default fallback (pending, but no config overrides)
    root = get_project_root()
    if operation == "pca_data":
        return root / "out" / "pca" / "data"
    return root / "out" / operation


@router.get("/paths", response_model=StoragePathsResponse)
async def get_storage_paths():
    """
    Get current storage paths configuration.

    Returns information about where data is currently being stored.
    """
    # Clear path_resolver cache to ensure we get fresh paths (thread-safe)
    from automar.shared.config import path_resolver

    with path_resolver._config_lock:
        path_resolver._config_loaded = False
        path_resolver._config_cache = None

    # Load config.toml if it exists
    config = load_config()

    current_paths = {}
    default_paths = {}
    source = {}

    # Get true default root (without config override)
    from automar.shared.config.path_resolver import get_package_root

    package_root = get_package_root()
    if package_root.name == "src":
        true_default_root = package_root.parent
    elif "site-packages" in str(package_root):
        env_data_dir = os.getenv("AUTOMAR_DATA_DIR")
        if env_data_dir:
            true_default_root = Path(env_data_dir)
        else:
            true_default_root = Path.home() / ".automar"
    else:
        true_default_root = package_root.parent

    default_paths["root"] = str(true_default_root)

    # Get root path
    current_root = get_project_root()
    current_paths["root"] = str(current_root)
    source["root"] = get_path_source("root", config)

    # Get operation-specific paths
    for operation in OPERATIONS:
        current_paths[operation] = str(resolve_operation_path(operation, config))
        source[operation] = get_path_source(operation, config)

        # Default path (without any config)
        if operation == "pca_data":
            default_paths[operation] = str(true_default_root / "out" / "pca" / "data")
        else:
            default_paths[operation] = str(true_default_root / "out" / operation)

    return StoragePathsResponse(
        current=current_paths,
        source=source,
        default=default_paths,
        config_path=str(get_config_path()),
    )


@router.get("/defaults")
async def get_default_settings():
    """
    Return effective defaults combining schema values with config.toml overrides.
    """
    defaults_cfg = get_effective_defaults()
    return {
        "config_path": str(get_config_path()),
        "defaults": defaults_cfg.model_dump(mode="json", exclude_none=True),
    }


@router.post("/defaults/reset")
async def reset_defaults_to_schema():
    """
    Reset the defaults section in config.toml to match schema defaults.
    """
    try:
        config_path = dump_schema_defaults_to_config()
        # Reset cached defaults in path resolver/utilities if needed
        from automar.shared.config import path_resolver

        with path_resolver._config_lock:
            path_resolver._config_loaded = False
            path_resolver._config_cache = None

        return {
            "status": "success",
            "config_path": str(config_path),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset defaults: {e}")


@router.post("/paths/validate", response_model=PathValidationResponse)
async def validate_storage_path(request: PathValidationRequest):
    """
    Validate a storage path before saving.

    Checks:
    - Path exists or can be created
    - Write permissions
    - Available disk space
    - Contains existing data (warning, not error)
    """
    path_str = request.path.strip()
    errors = []
    warnings = []

    # 1. Path format validation
    try:
        path = Path(path_str).resolve()
    except Exception as e:
        errors.append(f"Invalid path format: {e}")
        return PathValidationResponse(
            valid=False,
            exists=False,
            can_create=False,
            writable=False,
            readable=False,
            disk_space_gb=0.0,
            has_existing_data=False,
            existing_files_count=0,
            errors=errors,
        )

    # 2. Check if path is a reserved system path (basic check)
    reserved_paths = [
        Path("/"),
        Path("/root"),
        Path("/etc"),
        Path("/var"),
        Path("/usr"),
        Path("/bin"),
        Path("/sbin"),
        Path("/sys"),
        Path("/proc"),
        Path("/dev"),
    ]
    if os.name == "nt":  # Windows
        reserved_paths.extend(
            [Path("C:\\"), Path("C:\\Windows"), Path("C:\\Program Files")]
        )

    if path in reserved_paths or any(path == rp for rp in reserved_paths):
        errors.append("Cannot use system/reserved directories for data storage")

    # 3. Existence and creation check
    exists = path.exists()
    can_create = False

    if not exists:
        # Check if parent exists and we can create the directory
        parent = path.parent
        if parent.exists():
            can_create = os.access(parent, os.W_OK)
            if can_create:
                warnings.append("Path does not exist but can be created")
            else:
                errors.append(
                    f"Cannot create directory - no write permission in parent: {parent}"
                )
        else:
            # Try to find the closest existing parent
            current = path
            while not current.exists() and current != current.parent:
                current = current.parent

            if current.exists() and os.access(current, os.W_OK):
                can_create = True
                warnings.append(
                    f"Path does not exist but can be created (parent directories will be created)"
                )
            else:
                errors.append(
                    f"Parent directory does not exist and cannot be created: {parent}"
                )
    else:
        can_create = True  # Already exists

    # 4. Permission checks
    writable = False
    readable = False

    if exists:
        if not path.is_dir():
            errors.append("Path exists but is not a directory")
        else:
            writable = os.access(path, os.W_OK)
            readable = os.access(path, os.R_OK)

            if not writable:
                errors.append("No write permission on directory")
            if not readable:
                errors.append("No read permission on directory")
    elif can_create:
        # Check parent's permissions
        parent = path.parent
        while not parent.exists():
            parent = parent.parent
        writable = os.access(parent, os.W_OK)
        readable = os.access(parent, os.R_OK)

    # 5. Disk space check
    disk_space_gb = 0.0
    try:
        if exists:
            stat = shutil.disk_usage(path)
        else:
            # Check parent directory
            parent = path.parent
            while not parent.exists():
                parent = parent.parent
            stat = shutil.disk_usage(parent)

        disk_space_gb = stat.free / (1024**3)  # Convert to GB

        if disk_space_gb < 10:
            warnings.append(f"Low disk space: only {disk_space_gb:.1f} GB available")
        elif disk_space_gb < 50:
            warnings.append(
                f"Less than 50GB disk space available ({disk_space_gb:.1f} GB)"
            )

    except Exception as e:
        warnings.append(f"Could not check disk space: {e}")

    # 6. Check for existing data
    has_existing_data = False
    existing_files_count = 0

    if exists and path.is_dir():
        try:
            # Check for automar-specific directories
            automar_subdirs = [
                "data",
                "pca",
                "models",
                "hyper",
                "cross",
                "preds",
                "jobs",
                "ray",
            ]
            existing_subdirs = [d for d in automar_subdirs if (path / d).exists()]

            if existing_subdirs:
                has_existing_data = True
                # Count files in these directories
                for subdir in existing_subdirs:
                    existing_files_count += sum(
                        1 for _ in (path / subdir).rglob("*") if _.is_file()
                    )

                warnings.append(
                    f"Path contains existing Automar data in: {', '.join(existing_subdirs)} "
                    f"({existing_files_count} files)"
                )
            else:
                # Check if directory has any files
                files = list(path.iterdir())
                if files:
                    existing_files_count = len([f for f in files if f.is_file()])
                    if existing_files_count > 0:
                        warnings.append(
                            f"Directory is not empty ({existing_files_count} items found)"
                        )
        except Exception as e:
            warnings.append(f"Could not scan directory: {e}")

    # Determine if valid
    valid = len(errors) == 0

    return PathValidationResponse(
        valid=valid,
        exists=exists,
        can_create=can_create,
        writable=writable,
        readable=readable,
        disk_space_gb=round(disk_space_gb, 2),
        has_existing_data=has_existing_data,
        existing_files_count=existing_files_count,
        warnings=warnings,
        errors=errors,
    )


@router.post("/paths/reload")
async def reload_path_config():
    """
    Reload the path configuration from config.toml without restarting the server.

    This clears the cached config and forces a reload on the next path resolution.
    """
    # Clear the cache in path_resolver module
    import sys
    from automar.shared.config import path_resolver

    with path_resolver._config_lock:
        path_resolver._config_loaded = False
        path_resolver._config_cache = None

    # Force a reload by calling get_output_dir
    path_resolver.get_output_dir()

    return {"success": True, "message": "Path configuration reloaded"}


@router.post("/paths", response_model=UpdatePathsResponse)
async def update_storage_paths(update: StoragePathsUpdate):
    """
    Update config.toml with new storage paths.
    Validates paths before saving.
    """
    validation_warnings = []

    # Validate root path if provided (and not empty - empty means "remove override")
    if update.root and update.root.strip():
        validation = await validate_storage_path(
            PathValidationRequest(path=update.root)
        )
        if not validation.valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Root path validation failed",
                    "errors": validation.errors,
                    "warnings": validation.warnings,
                },
            )
        validation_warnings.extend(validation.warnings)

    # Validate override paths if provided
    if update.overrides:
        for operation, path_str in update.overrides.items():
            if path_str:  # Only validate non-empty overrides
                validation = await validate_storage_path(
                    PathValidationRequest(path=path_str)
                )
                if not validation.valid:
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "message": f"Override path validation failed for '{operation}'",
                            "errors": validation.errors,
                            "warnings": validation.warnings,
                        },
                    )
                validation_warnings.extend(validation.warnings)

    # Update config.toml
    try:
        # Normalize empty strings to empty string (not None) to trigger removal
        root_value = update.root if update.root is not None else None
        if root_value is not None and not root_value.strip():
            root_value = ""  # Empty string will trigger removal in update_config_paths

        config_path = update_config_paths(root=root_value, overrides=update.overrides)

        # Immediately reload the config cache so changes take effect
        from automar.shared.config import path_resolver

        with path_resolver._config_lock:
            path_resolver._config_loaded = False
            path_resolver._config_cache = None
        # Force reload by calling get_project_root
        path_resolver.get_project_root()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update config.toml: {e}",
        )

    return UpdatePathsResponse(
        success=True,
        config_path=str(config_path),
        validation_warnings=validation_warnings,
    )


@router.post("/open-output-folder")
async def open_output_folder():
    """
    Open the output folder in the system's file explorer.

    This uses the configured root path from Storage Configuration settings,
    respecting the priority:
    1. Custom path set in config.toml (if any)
    2. Environment variable AUTOMAR_DATA_DIR (if set and no custom path)
    3. Default path (fallback)
    """
    try:
        # Get the root directory path (respects config.toml settings)
        root_dir = get_project_root()

        # The output directory is root/out
        output_dir = root_dir / "out"

        # Create the directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Open the folder using the utility function
        open_folder_in_explorer(output_dir)

        return {"success": True, "path": str(output_dir)}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (RuntimeError, ValueError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
