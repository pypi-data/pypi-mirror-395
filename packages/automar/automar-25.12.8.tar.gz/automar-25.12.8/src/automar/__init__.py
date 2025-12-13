"""
AuToMaR - Stock Market Prediction ML Framework

A comprehensive machine learning framework for time series-based stock market forecasting,
featuring deep learning models (GRU, Transformer, Logistic Regression), hyperparameter
tuning with Ray Tune, PCA analysis, and a full-featured web interface.

Package Structure:
    automar.core - Core ML library (models, preprocessing, visualization)
    automar.cli - Command-line interface
    automar.shared - Shared utilities and services
    automar.web - FastAPI web application

Usage:
    # CLI
    from automar.cli.main import main

    # Core ML
    from automar.core.models import GRU, Transformer, LogisticModel

    # Shared utilities
    from automar.shared.config import load_config

    # Web API
    from automar.web.app import app
"""

__version__ = "25.12.08"
__author__ = "Alejandro Gil (Kzurro), Sergio Pablo-García"

# Make subpackages easily accessible
__all__ = ["core", "cli", "shared", "web"]
