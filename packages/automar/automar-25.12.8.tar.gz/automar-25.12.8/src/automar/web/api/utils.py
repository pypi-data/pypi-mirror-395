# -*- coding: utf-8 -*-
"""Utility functions for API endpoints."""
from pathlib import Path
from typing import Optional

from automar.shared.config.schemas import GlobalConfig
from automar.shared.persistence.library import read_df
from automar.shared.config.path_resolver import get_output_dir


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
        upload_dir = get_output_dir("uploads")
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

        # Delete files that are in uploads directory
        for file_path in paths_to_check:
            try:
                # Check if file is in uploads directory
                file_path.relative_to(upload_dir)
                # If we get here, file is in uploads dir - delete it
                if file_path.exists():
                    file_path.unlink()
                    print(f"Cleaned up uploaded file: {file_path}")
            except ValueError:
                # File is not in uploads directory - skip
                pass
            except Exception as e:
                print(f"Warning: Could not delete uploaded file {file_path}: {e}")

    except Exception as e:
        print(f"Warning: Error during file cleanup: {e}")
