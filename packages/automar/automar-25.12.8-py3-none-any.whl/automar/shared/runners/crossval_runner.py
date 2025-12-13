# -*- coding: utf-8 -*-
"""
Cross-validation runner for Automar

Handles K-fold cross-validation for model evaluation
"""


def run_crossvalidation(cfg):
    """
    CLI wrapper for cross-validation

    Args:
        cfg: Configuration object with cross-validation parameters

    Returns:
        None (prints result to console)
    """
    from automar.shared.core.common import run_crossvalidation_common

    crossval_results, out_path, total_samples = run_crossvalidation_common(
        cfg, progress_callback=None
    )
    # Don't print here - run_crossvalidation_common already prints the results
