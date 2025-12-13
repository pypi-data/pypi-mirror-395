# -*- coding: utf-8 -*-
"""
Hyperparameter tuning runner for Automar

Handles hyperparameter optimization using Ray Tune
"""


def run_tuning(cfg):
    """
    CLI wrapper for hyperparameter tuning

    Args:
        cfg: Configuration object with tuning parameters

    Returns:
        None (prints result to console)
    """
    from automar.shared.core.common import run_tuning_common

    results, config_file_path = run_tuning_common(cfg, progress_callback=None)
    print(f"Optimal hyperparameters stored as {config_file_path}")
