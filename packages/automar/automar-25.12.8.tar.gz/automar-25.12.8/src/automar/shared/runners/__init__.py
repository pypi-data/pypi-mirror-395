# -*- coding: utf-8 -*-
"""
Runner modules for Automar CLI commands

These modules contain the core logic for each CLI command:
- extract_runner: Data extraction logic
- pca_runner: PCA analysis logic
- tune_runner: Hyperparameter tuning logic
- train_runner: Model training logic
- crossval_runner: Cross-validation logic
- predict_runner: Model prediction/inference logic
- api_runner: API server startup
- gui_runner: GUI mode (API + browser)
"""

from automar.shared.runners.extract_runner import run_extraction
from automar.shared.runners.pca_runner import run_pca
from automar.shared.runners.tune_runner import run_tuning
from automar.shared.runners.train_runner import run_training
from automar.shared.runners.crossval_runner import run_crossvalidation
from automar.shared.runners.predict_runner import run_prediction
from automar.shared.runners.api_runner import run_api
from automar.shared.runners.gui_runner import run_gui, has_web_ui

__all__ = [
    "run_extraction",
    "run_pca",
    "run_tuning",
    "run_training",
    "run_crossvalidation",
    "run_prediction",
    "run_api",
    "run_gui",
    "has_web_ui",
]
