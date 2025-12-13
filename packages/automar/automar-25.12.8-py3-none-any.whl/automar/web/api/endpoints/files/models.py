# -*- coding: utf-8 -*-
"""Model file operations and metadata endpoints."""
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["files", "models"])


@router.get("/model-files")
async def list_model_files():
    """
    List all available model files (.pth) in out/models/

    Returns metadata for each model including model_type for filtering
    """
    try:
        import torch
        import warnings
        from numba.core.errors import NumbaTypeSafetyWarning

        # Suppress Numba warning from WEASEL-MUSE (sktime) model deserialization
        # The int64→uint32 cast is safe for WEASEL word indices (always < 4 billion)
        warnings.filterwarnings("ignore", category=NumbaTypeSafetyWarning)

        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        models_dir = project_root / "out" / "models"

        if not models_dir.exists():
            return {"model_files": []}

        model_files = []

        # Recursively find all .pth files
        for pth_file in models_dir.rglob("*.pth"):
            try:
                # Try to extract metadata from checkpoint
                checkpoint = torch.load(
                    pth_file, map_location="cpu", weights_only=False
                )

                if isinstance(checkpoint, dict) and "model_type" in checkpoint:
                    # Checkpoint with metadata (both NN and log-reg)
                    model_type = checkpoint["model_type"]
                    hyperparams = checkpoint.get("hyperparameters", {})
                    training_history = checkpoint.get("training_history", {})
                    training_context = checkpoint.get("training_context", {})

                    # Get final validation AUROC if available (from training history or cached)
                    val_auroc = None
                    if training_history and "val_auroc" in training_history:
                        val_auroc = training_history["val_auroc"][-1]

                    metadata = {
                        "model_type": model_type,
                        "val_auroc": val_auroc,
                        "has_hyperparameters": bool(hyperparams),
                        "has_training_history": bool(training_history),
                        "ticker": training_context.get(
                            "ticker"
                        ),  # None or ticker symbol
                        "industry": training_context.get("industry"),
                    }
                else:
                    # Old format (MUSE object without metadata wrapper)
                    metadata = {
                        "model_type": "log-reg",
                        "ticker": None,  # Unknown for old models
                        "industry": None,
                    }

                # Get file stats
                stat = pth_file.stat()

                model_files.append(
                    {
                        "name": pth_file.name,
                        "path": str(pth_file.relative_to(project_root)),
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "metadata": metadata,
                    }
                )

            except Exception as e:
                # If we can't load the file, still include it but with minimal info
                stat = pth_file.stat()
                model_files.append(
                    {
                        "name": pth_file.name,
                        "path": str(pth_file.relative_to(project_root)),
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "metadata": {"error": str(e)},
                    }
                )

        # Sort by modification time (newest first)
        model_files.sort(key=lambda x: x["modified"], reverse=True)

        return {"model_files": model_files}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing model files: {str(e)}"
        )
