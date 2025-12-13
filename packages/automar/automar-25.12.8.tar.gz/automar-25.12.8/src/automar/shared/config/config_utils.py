from __future__ import annotations
import argparse
import tomllib
import tomli_w
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import ValidationError

from automar.shared.config.schemas import GlobalConfig
from automar.shared.config.path_resolver import get_project_root


def _deep_update_dict(a: dict, b: dict) -> dict:
    """Recursively merge dict b into dict a without mutating inputs."""
    out = a.copy()
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_update_dict(out.get(k, {}), v)
        elif isinstance(v, dict):
            out[k] = _deep_update_dict({}, v)
        else:
            out[k] = v if v is not None else out.get(k)
    return out


def from_toml(path: Path | str) -> GlobalConfig:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    return GlobalConfig.model_validate(data)


def from_cli(ns: argparse.Namespace) -> GlobalConfig:
    cmd = ns.command
    d: Dict[str, Any] = {"command": cmd}

    def pull(prefix: str, fields: list[str]):
        sub = {}
        for f in fields:
            if hasattr(ns, f):
                value = getattr(ns, f)
                # Only include non-None values to avoid triggering validation
                if value is not None:
                    sub[f] = value
        return sub

    # Only pull extract options for commands that use them
    if cmd in ["extract", "pca", "tune", "train", "crossvalidate", "predict"]:
        d["extract"] = pull(
            "",
            [
                "ticker",
                "industry",
                "history",
                "skip",
                "dir_path",
                "extract_file",
                "format",
                "datest",
                "datend",
            ],
        )

    # Only pull PCA options for commands that use them
    if cmd in ["pca", "tune", "train", "crossvalidate", "predict"]:
        d["pca"] = pull(
            "",
            [
                "n_components",
                "alpha",
                "drop",
                "data_file",
                "pca_file",
                "pca_force",
                "notdf",
                "pca_df_file",
            ],
        )

    # Only pull loader options for commands that use them
    if cmd in ["tune", "train", "crossvalidate", "predict"]:
        d["loader"] = pull(
            "",
            [
                "tsize",
                "batch_size",
                "val_size",
                "test_size",
                "dopca",
                "device",
                "cores",
                "seed",
                "scaler",
            ],
        )

    # Only pull tune options for commands that use them
    if cmd in ["tune", "train", "crossvalidate", "predict"]:
        d["tune"] = pull(
            "",
            [
                "tuning_path",
                "param_path",
                "num_samples",
                "epochs",
                "gpu_per_trial",
                "model",
            ],
        )

    # Only pull train options for commands that use them
    if cmd in ["train", "crossvalidate", "predict"]:
        d["train"] = pull("", ["cfg_path", "pca_path", "model_path", "id"])

    # Only pull crossvalidate options for commands that use them
    if cmd == "crossvalidate":
        d["crossvalidate"] = pull("", ["out_path", "n_split"])

    # Only pull prediction options for the predict command
    if cmd == "predict":
        d["predict"] = pull("", ["model_path", "save_dir", "mode"])

    # Only pull API options for the API command
    if cmd == "api":
        d["api"] = pull("", ["host", "port", "reload", "workers"])

    return GlobalConfig.model_validate(d)


def merge(cli_cfg: GlobalConfig, file_cfg: GlobalConfig | None) -> GlobalConfig:
    if file_cfg is None:
        return cli_cfg

    merged_dict = _deep_update_dict(file_cfg.model_dump(), cli_cfg.model_dump())
    return GlobalConfig.model_validate(merged_dict)


def get_config_root() -> Path:
    """
    Get the root directory where config.toml should be located.

    This does NOT read from config.toml to avoid circular dependency.
    Returns the base directory for config storage based only on installation location.
    """
    from automar.shared.config.path_resolver import get_package_root
    import os

    package_root = get_package_root()

    # Repository mode: config.toml in repository root
    if package_root.name == "src":
        return package_root.parent

    # Installed package mode: config.toml in user's .automar directory
    if "site-packages" in str(package_root):
        env_data_dir = os.getenv("AUTOMAR_DATA_DIR")
        if env_data_dir:
            data_path = Path(env_data_dir)
            data_path.mkdir(parents=True, exist_ok=True)
            return data_path

        home_data_dir = Path.home() / ".automar"
        home_data_dir.mkdir(parents=True, exist_ok=True)
        return home_data_dir

    # Fallback: check for .git or pyproject.toml in parent
    potential_repo_root = package_root.parent
    if (potential_repo_root / ".git").exists() or (
        potential_repo_root / "pyproject.toml"
    ).exists():
        return potential_repo_root

    # Default: user's home directory
    home_data_dir = Path.home() / ".automar"
    home_data_dir.mkdir(parents=True, exist_ok=True)
    return home_data_dir


def get_config_path() -> Path:
    """
    Get the path to config.toml file.

    Uses the config root (NOT project root) to avoid circular dependency.
    """
    return get_config_root() / "config.toml"


def _schema_defaults_dict() -> Dict[str, Any]:
    defaults_cfg = GlobalConfig(command="gui")
    defaults_dict = defaults_cfg.model_dump(mode="json", exclude_none=True)
    defaults_dict.pop("command", None)
    return {"defaults": defaults_dict}


def _to_toml_ready(value: Any) -> Any:
    from pathlib import PurePath

    if isinstance(value, dict):
        cleaned = {}
        for key, val in value.items():
            if val is None:
                continue
            cleaned[key] = _to_toml_ready(val)
        return cleaned
    if isinstance(value, (list, tuple)):
        return [_to_toml_ready(item) for item in value if item is not None]
    if isinstance(value, PurePath):
        return str(value)
    return value


def ensure_config_file() -> Path:
    config_path = get_config_path()
    if not config_path.is_file():
        save_config(_schema_defaults_dict())
    return config_path


def load_config() -> Optional[Dict[str, Any]]:
    """
    Load config.toml as a raw dictionary (not validated as GlobalConfig).

    Returns:
        Dict if config.toml exists, None otherwise
    """
    config_path = ensure_config_file()

    with config_path.open("rb") as fh:
        return tomllib.load(fh)


def save_config(config: Dict[str, Any]) -> Path:
    """
    Save a config dictionary to config.toml.

    Args:
        config: Dictionary to save

    Returns:
        Path to the saved config file
    """
    config_path = get_config_path()

    # Ensure parent directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    toml_ready = _to_toml_ready(config)
    with config_path.open("wb") as fh:
        tomli_w.dump(toml_ready, fh)

    return config_path


def dump_schema_defaults_to_config() -> Path:
    """
    Overwrite the defaults section in config.toml with schema defaults.
    Preserves other user-defined sections.
    """
    current_config = load_config() or {}
    current_config["defaults"] = _schema_defaults_dict()["defaults"]
    return save_config(current_config)


def get_effective_defaults() -> GlobalConfig:
    """
    Build a GlobalConfig instance using schema defaults plus any overrides
    defined under [defaults] in config.toml.
    """
    defaults_cfg = GlobalConfig(command="gui")
    config_data = load_config() or {}
    overrides = config_data.get("defaults")
    if overrides:
        merged = _deep_update_dict(
            defaults_cfg.model_dump(),
            {"command": defaults_cfg.command, **overrides},
        )
        try:
            defaults_cfg = GlobalConfig.model_validate(merged)
        except ValidationError as exc:
            print(f"Warning: Ignoring invalid defaults in config.toml: {exc}")
    return defaults_cfg


def update_config_paths(
    root: Optional[str] = None, overrides: Optional[Dict[str, Optional[str]]] = None
) -> Path:
    """
    Update [paths] section in config.toml while preserving other sections.

    Args:
        root: New root directory path
        overrides: Dict of operation -> path overrides (None value removes override)

    Returns:
        Path to the saved config file
    """
    # Load existing config or create new one
    config = load_config()
    if config is None:
        config = {}

    # Ensure [paths] section exists
    if "paths" not in config:
        config["paths"] = {}

    # Update root if provided
    if root is not None:
        if root:  # Set root override
            config["paths"]["root"] = root
        elif "root" in config["paths"]:  # Remove root override (use default)
            del config["paths"]["root"]

    # Update overrides if provided
    if overrides:
        for operation, path in overrides.items():
            if path:  # Set override
                config["paths"][operation] = path
            elif operation in config["paths"]:  # Remove override (use default)
                del config["paths"][operation]

    # Clean up empty [paths] section
    if "paths" in config and len(config["paths"]) == 0:
        del config["paths"]

    # Save config (preserves all other sections)
    return save_config(config)
