"""
Path resolution utility that works in both repository and installed package contexts.

This module provides functions to resolve paths correctly whether running from:
- Repository: Automar/src/shared/config/...
- Installed package: site-packages/shared/config/...

Path Resolution Priority:
1. Specific path in config.toml [paths].{operation}
2. Root path in config.toml [paths].root + /out/{operation}/
3. AUTOMAR_DATA_DIR environment variable + /out/{operation}/
4. Default location (repository or ~/.automar/)
"""

from pathlib import Path
import os
import threading

# Lazy-loaded config to avoid circular imports
_config_lock = threading.RLock()  # Reentrant lock for thread-safe lazy initialization
_config_cache = None
_config_loaded = False


def get_package_root():
    """
    Get the root directory of the shared package.

    Returns the directory containing the 'shared' package, whether running
    from repository (returns Automar/src/) or installed package (returns site-packages/).

    Returns:
        Path: The package root directory
    """
    # Get the directory containing this file (path_resolver.py)
    this_file = Path(__file__).resolve()
    config_dir = this_file.parent  # This is the 'shared/config/' directory
    shared_dir = config_dir.parent  # This is the 'shared/' directory

    # Return the parent of 'shared/' (either 'src/' or 'site-packages/')
    return shared_dir.parent


def get_project_root():
    """
    Get the project root directory for data storage.

    Priority order:
    1. config.toml [paths].root (if set)
    2. AUTOMAR_DATA_DIR environment variable (if set)
    3. Repository directory (Automar/) or ~/.automar/

    This is where 'out/' directories should be created.

    Returns:
        Path: The project root directory
    """
    # Check for config.toml root override first
    config = _load_config()
    if config and "paths" in config and "root" in config["paths"]:
        root_path = Path(config["paths"]["root"])
        root_path.mkdir(parents=True, exist_ok=True)
        return root_path

    package_root = get_package_root()

    # Check if we're in a repository by looking at the path structure
    # Repository structure: .../Automar/src/shared/
    # Installed package: .../site-packages/shared/

    # If package_root ends with 'src', we're in repository
    if package_root.name == "src":
        # Repository: return parent of src/ (the Automar/ directory)
        return package_root.parent

    # If 'site-packages' appears in the path, we're in an installed package
    if "site-packages" in str(package_root):
        # Check for environment variable override
        env_data_dir = os.getenv("AUTOMAR_DATA_DIR")
        if env_data_dir:
            data_path = Path(env_data_dir)
            # Create directory if it doesn't exist
            data_path.mkdir(parents=True, exist_ok=True)
            return data_path

        # Default to user's home directory
        home_data_dir = Path.home() / ".automar"
        home_data_dir.mkdir(parents=True, exist_ok=True)
        return home_data_dir

    # Fallback: check for .git or pyproject.toml in parent
    potential_repo_root = package_root.parent
    if (potential_repo_root / ".git").exists() or (
        potential_repo_root / "pyproject.toml"
    ).exists():
        return potential_repo_root

    # Default to user's home directory for unknown contexts
    home_data_dir = Path.home() / ".automar"
    home_data_dir.mkdir(parents=True, exist_ok=True)
    return home_data_dir


def get_assets_dir():
    """
    Get the assets directory containing default configuration files.

    Returns:
        Path: Path to shared/config/templates/
    """
    this_file = Path(__file__).resolve()
    config_dir = this_file.parent  # This is the 'shared/config/' directory
    return config_dir / "templates"


def get_hpt_defaults_dir():
    """
    Get the directory containing default hyperparameter search space files.

    Returns:
        Path: Path to shared/config/templates/hpt_defaults/
    """
    return get_assets_dir() / "hpt_defaults"


def _load_config():
    """
    Lazy-load config.toml to avoid circular imports.

    Thread-safe using double-checked locking pattern to prevent race conditions
    where multiple threads might try to load the config simultaneously.

    Returns:
        dict or None: Config dictionary if config.toml exists
    """
    global _config_cache, _config_loaded

    # First check (fast path) - no lock needed if already loaded
    if _config_loaded:
        return _config_cache

    # Acquire lock to ensure only one thread loads the config
    with _config_lock:
        # Second check (safety check) - another thread might have loaded while we waited
        if _config_loaded:
            return _config_cache

        try:
            # Import here to avoid circular dependency
            from .config_utils import load_config

            _config_cache = load_config()
            _config_loaded = True
            return _config_cache
        except Exception:
            # If config loading fails, return None and don't cache
            return None


def get_output_dir(subdir=None):
    """
    Get the output directory for results, models, datasets, etc.

    Path Resolution Priority:
    1. config.toml [paths].{subdir} (if subdir specified)
    2. config.toml [paths].root + /out/{subdir}/
    3. AUTOMAR_DATA_DIR env + /out/{subdir}/
    4. Default project root + /out/{subdir}/

    Args:
        subdir (str, optional): Subdirectory within out/ (e.g., 'models', 'data', 'pca')

    Returns:
        Path: Path to out/ or out/subdir/
    """
    # Load config if available
    config = _load_config()

    # Check for config.toml overrides
    if config and "paths" in config:
        # Priority 1: Specific operation override
        if subdir and subdir in config["paths"]:
            return Path(config["paths"][subdir])

        # Priority 2: Root override in config
        if "root" in config["paths"]:
            root = Path(config["paths"]["root"])
            if subdir:
                return root / "out" / subdir
            return root / "out"

    # Priority 3 & 4: Fall back to default logic (which handles AUTOMAR_DATA_DIR)
    out_dir = get_project_root() / "out"

    if subdir:
        return out_dir / subdir
    return out_dir


def resolve_path(path, relative_to_project=False):
    """
    Resolve a path that may be relative or absolute.

    Args:
        path (str or Path): Path to resolve
        relative_to_project (bool): If True and path is relative, resolve relative to project root

    Returns:
        Path: Resolved absolute path
    """
    path = Path(path)

    if path.is_absolute():
        return path

    if relative_to_project:
        return (get_project_root() / path).resolve()

    # Relative to current working directory
    return path.resolve()


def get_config_path() -> Path:
    """
    Get the path to config.toml file using the same logic as config_utils.
    """
    from .config_utils import get_config_path as _config_path

    return _config_path()
