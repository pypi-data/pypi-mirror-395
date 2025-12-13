"""
Hyperparameter management utilities for manual configuration.
"""

import tomllib  # Python 3.11+ built-in for reading TOML
import tomli_w  # For writing TOML
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# Default hyperparameter templates
# Note: epochs is NOT included - it's configured via the form field
DEFAULT_GRU_HYPERPARAMS = {
    "model": {
        "input_dim": 20,
        "output_dim": 1,
        "hidden_dim": 32,
        "n_layers": 2,
        "drop_prob": 0.4,
    },
    "criterion": {},
    "optimizer": {"lr": 0.001},
    "scheduler": {
        "mode": "min",
        "factor": 0.75,
        "patience": 6,
        "min_lr": 1e-08,
    },
}

DEFAULT_TRANSFORMER_HYPERPARAMS = {
    "model": {
        "input_dim": 20,
        "output_dim": 1,
        "hidden_dim": 32,
        "n_layers": 2,
        "drop_prob": 0.4,
        "head_div": 2,
    },
    "criterion": {},
    "optimizer": {"lr": 0.001},
    "scheduler": {
        "mode": "min",
        "factor": 0.75,
        "patience": 6,
        "min_lr": 1e-08,
    },
}

DEFAULT_LOGREG_HYPERPARAMS = {
    "window_inc": 3.0,
    "alphabet_size": 10.0,
    "feature_selection": "none",
}


def get_default_template(model_type: str) -> Dict:
    """Get default hyperparameter template for model type."""
    templates = {
        "gru": DEFAULT_GRU_HYPERPARAMS,
        "transformer": DEFAULT_TRANSFORMER_HYPERPARAMS,
        "log-reg": DEFAULT_LOGREG_HYPERPARAMS,
        "logreg": DEFAULT_LOGREG_HYPERPARAMS,
    }
    return templates.get(model_type.lower(), {})


def validate_hyperparameters(
    model_type: str, toml_content: str
) -> Tuple[bool, List[str], Dict]:
    """
    Validate hyperparameter TOML content.

    Returns:
        (is_valid, errors, parsed_config)
    """
    errors = []

    try:
        config = tomllib.loads(toml_content)
    except tomllib.TOMLDecodeError as e:
        return False, [f"TOML syntax error: {str(e)}"], {}

    model_lower = model_type.lower()

    # Validate based on model type
    if model_lower in ["gru", "transformer"]:
        # Check required sections
        if "model" not in config:
            errors.append("Missing required section: [model]")
        if "optimizer" not in config:
            errors.append("Missing required section: [optimizer]")
        if "scheduler" not in config:
            errors.append("Missing required section: [scheduler]")

        # Check required fields in [model]
        if "model" in config:
            required_model_fields = [
                "input_dim",
                "output_dim",
                "hidden_dim",
                "n_layers",
                "drop_prob",
            ]
            if model_lower == "transformer":
                required_model_fields.append("head_div")

            for field in required_model_fields:
                if field not in config["model"]:
                    errors.append(f"Missing required field in [model]: {field}")

        # Validate value ranges
        if "model" in config:
            # output_dim must be 1 (binary classification)
            if "output_dim" in config["model"]:
                output_dim = config["model"]["output_dim"]
                if output_dim != 1:
                    errors.append(
                        f"output_dim must be 1 (binary classification), got {output_dim}"
                    )

            if "drop_prob" in config["model"]:
                drop_prob = config["model"]["drop_prob"]
                if not (0 <= drop_prob <= 1):
                    errors.append(f"drop_prob must be between 0 and 1, got {drop_prob}")

        if "optimizer" in config and "lr" not in config["optimizer"]:
            errors.append("Missing required field in [optimizer]: lr")

    elif model_lower in ["log-reg", "logreg"]:
        required_fields = ["window_inc", "alphabet_size", "feature_selection"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")

        if "feature_selection" in config:
            valid_selections = ["chi2", "none", "random"]
            if config["feature_selection"] not in valid_selections:
                errors.append(
                    f"feature_selection must be one of {valid_selections}, got {config['feature_selection']}"
                )

    is_valid = len(errors) == 0
    return is_valid, errors, config


def save_manual_hyperparameters(
    model_type: str,
    toml_content: str,
    custom_name: Optional[str] = None,
    base_dir: Path = Path("out/hyper/manual"),
) -> Path:
    """Save manually-defined hyperparameters to file."""
    # Create directory
    model_dir = base_dir / model_type.lower()
    model_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if custom_name:
        # Sanitize custom name
        safe_name = "".join(c for c in custom_name if c.isalnum() or c in "-_")
        filename = f"{safe_name}_{timestamp}.toml"
    else:
        filename = f"manual_config_{timestamp}.toml"

    file_path = model_dir / filename
    file_path.write_text(toml_content)

    return file_path


def list_manual_configs(
    model_type: Optional[str] = None, base_dir: Path = Path("out/hyper/manual")
) -> List[Dict]:
    """List all manually-created hyperparameter files."""
    if not base_dir.exists():
        return []

    if model_type:
        model_dirs = [base_dir / model_type.lower()]
    else:
        model_dirs = [d for d in base_dir.iterdir() if d.is_dir()]

    # Get absolute base_dir for consistent path resolution
    abs_base_dir = base_dir.resolve()
    # Get project root for consistent path resolution
    from automar.shared.config.path_resolver import get_project_root

    project_root = get_project_root()

    configs = []
    for model_dir in model_dirs:
        if not model_dir.exists():
            continue

        for file_path in sorted(
            model_dir.glob("*.toml"), key=lambda p: p.stat().st_mtime, reverse=True
        ):
            # Return path relative to project root for consistent resolution
            configs.append(
                {
                    "file_path": str(file_path.resolve().relative_to(project_root)),
                    "model_type": model_dir.name,
                    "filename": file_path.name,
                    "created_date": datetime.fromtimestamp(
                        file_path.stat().st_ctime
                    ).isoformat(),
                    "modified_date": datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat(),
                    "file_size": file_path.stat().st_size,
                }
            )

    return configs
