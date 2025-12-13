"""
Visualization data preparation utilities for the web interface.

This module handles loading and formatting data from completed jobs for visualization.
All functions return JSON-serializable dictionaries ready for Plotly.js rendering.
"""

from pathlib import Path
from typing import Dict, Any

# NOTE: Heavy imports (torch, numpy, pandas) are done lazily inside functions
# to avoid blocking API startup. Do NOT import them at module level!


def load_job_visualization_data(job_id: str) -> Dict[str, Any]:
    """
    Central function to load all available visualization data for a job.

    Args:
        job_id: The job ID to load data for

    Returns:
        Dictionary with available visualization types and metadata

    Raises:
        ValueError: If job not found or not completed
    """
    # Import here to avoid circular dependency
    from automar.web.api.jobs import get_job

    job = get_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")

    if job.status != "completed":
        raise ValueError(f"Job {job_id} not completed (status: {job.status})")

    available = []

    # Check what visualizations are available based on job type
    if job.type == "crossvalidate":
        available.append(
            {
                "type": "cross-validation",
                "title": "Cross-Validation Results",
                "description": "Boxplots and tables showing metric distributions across folds",
            }
        )

        # Growing windows diagram
        available.append(
            {
                "type": "growing-windows",
                "title": "Growing Windows Diagram",
                "description": "Visualization of data splits across cross-validation folds",
            }
        )

        # Confusion matrix if we have the model
        if job.result and "output_path" in job.result:
            available.append(
                {
                    "type": "confusion-matrix",
                    "title": "Confusion Matrix",
                    "description": "Classification confusion matrix",
                }
            )

    elif job.type == "training":
        # Confusion matrix (evaluation on test set)
        available.append(
            {
                "type": "confusion-matrix",
                "title": "Confusion Matrix",
                "description": "Classification confusion matrix from trained model",
            }
        )

        # Training history if available in model checkpoint
        if job.result and "model_path" in job.result:
            model_path = Path(job.result["model_path"])
            if model_path.exists():
                try:
                    import torch  # Lazy import - only when actually checking model files

                    checkpoint = torch.load(
                        model_path, map_location="cpu", weights_only=False
                    )
                    # For log-reg, checkpoint is MUSE object (not dict), so check type first
                    if (
                        isinstance(checkpoint, dict)
                        and "training_history" in checkpoint
                    ):
                        available.append(
                            {
                                "type": "training-history",
                                "title": "Training History",
                                "description": "Loss, AUROC, and learning rate evolution",
                            }
                        )
                except Exception:
                    pass  # Model file exists but can't load - skip training history

    elif job.type == "tuning":
        # Tuning progress if statistics file exists
        if job.result and "config_path" in job.result:
            config_path = Path(job.result["config_path"])
            stats_path = config_path.with_suffix(".stats.json")
            if stats_path.exists():
                available.append(
                    {
                        "type": "tuning-progress",
                        "title": "Tuning Progress",
                        "description": "AUROC evolution across tuning trials",
                    }
                )

    elif job.type == "pca":
        if job.result and "file_paths" in job.result:
            if "pca_object" in job.result["file_paths"]:
                available.append(
                    {
                        "type": "pca-analysis",
                        "title": "PCA Analysis",
                        "description": "Explained variance heatmap and correlation matrix",
                    }
                )

    elif job.type == "extract":
        # Extract jobs show stock price time series
        available.append(
            {
                "type": "extraction-summary",
                "title": "Stock Time Series",
                "description": "Interactive stock price and volume charts",
            }
        )

    elif job.type == "prediction":
        # Prediction jobs show different viz based on mode
        mode = job.result.get("mode", "eval") if job.result else "eval"

        if mode == "eval":
            # Evaluation mode: show confusion matrix with full classification metrics
            available.append(
                {
                    "type": "confusion-matrix",
                    "title": "Confusion Matrix",
                    "description": "Classification metrics and confusion matrix from evaluation",
                }
            )
        else:  # forecast
            available.append(
                {
                    "type": "prediction-probability",
                    "title": "Next Day Forecast",
                    "description": "Predicted probability for next trading day",
                }
            )

    return {
        "job_id": job_id,
        "job_type": job.type,
        "model": job.model,
        "available_visualizations": available,
    }


def _prepare_confusion_matrix_for_prediction(job) -> Dict[str, Any]:
    """
    Prepare confusion matrix data from a completed prediction job in eval mode.

    This is a helper function that extracts pre-computed metrics from prediction
    job results, avoiding the need to reload and re-evaluate models.

    Args:
        job: The prediction job object

    Returns:
        Dictionary with confusion matrix data

    Raises:
        ValueError: If job is not in eval mode or metrics unavailable
    """
    import pandas as pd  # Lazy import
    from pathlib import Path

    mode = job.result.get("mode", "eval") if job.result else "eval"
    if mode != "eval":
        raise ValueError(f"Job {job.job_id} is in forecast mode, not eval mode")

    # Get metrics from job result
    if not job.result or "metrics" not in job.result:
        raise ValueError(f"Job {job.job_id} has no metrics in result")

    metrics = job.result["metrics"]
    model_type = job.result.get("model_type", "unknown")

    # Extract confusion matrix
    if "confusion_matrix" not in job.result:
        raise ValueError(f"Job {job.job_id} has no confusion_matrix in result")

    confusion_matrix = job.result["confusion_matrix"]

    # Get threshold from metrics or use default (50% as percentage to match frontend expectations)
    threshold = metrics.get("threshold", 50.0)

    return {
        "job_id": job.job_id,
        "model": model_type,
        "matrix": confusion_matrix,
        "labels": ["Negative", "Positive"],
        "metrics": {
            "accuracy": float(metrics["accuracy"]),
            "precision": float(metrics["precision"]),
            "recall": float(metrics["recall"]),
            "fscore": float(metrics["fscore"]),
            "auroc": float(metrics["auroc"]),
        },
        "threshold": float(threshold),
    }


def prepare_confusion_matrix_data(job_id: str) -> Dict[str, Any]:
    """
    Prepare confusion matrix data for visualization by loading the trained model
    and evaluating it on test data.

    Supports both training jobs (recomputes from model) and prediction jobs in eval mode
    (uses pre-computed metrics).

    Args:
        job_id: The job ID to get confusion matrix for

    Returns:
        Dictionary with confusion matrix data including:
        - matrix: 2x2 confusion matrix [[TN, FP], [FN, TP]]
        - labels: ["Negative", "Positive"]
        - metrics: accuracy, precision, recall, fscore, auroc
        - model: model type

    Raises:
        ValueError: If job not found, not a training/prediction job, or data unavailable
    """
    import torch  # Lazy import
    import numpy as np  # Lazy import
    from automar.web.api.jobs import get_job

    job = get_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")

    # Handle prediction jobs separately (simpler - metrics already computed)
    if job.type == "prediction":
        return _prepare_confusion_matrix_for_prediction(job)

    if job.type != "training":
        raise ValueError(
            f"Job {job_id} is not a training or prediction job (type: {job.type})"
        )

    if job.status != "completed":
        raise ValueError(f"Job {job_id} is not completed (status: {job.status})")

    if not job.result or "model_path" not in job.result:
        raise ValueError(f"Job {job_id} has no model_path in result")

    model_path = Path(job.result["model_path"])
    if not model_path.exists():
        raise ValueError(f"Model file not found: {model_path}")

    # Load the model checkpoint early to check for cached metrics
    checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
    model_type = job.result.get("model_type", job.model)

    # Check if test metrics are cached in checkpoint (new models)
    # For log-reg, checkpoint is MUSE object (not dict), so check type first
    if (
        isinstance(checkpoint, dict)
        and "test_metrics" in checkpoint
        and checkpoint["test_metrics"] is not None
    ):
        # Use cached metrics - instant response, no recomputation needed
        return {
            "job_id": job_id,
            "model": model_type,
            "matrix": checkpoint["test_metrics"]["confusion_matrix"],
            "labels": ["Negative", "Positive"],
            "metrics": {
                "accuracy": checkpoint["test_metrics"]["accuracy"],
                "precision": checkpoint["test_metrics"]["precision"],
                "recall": checkpoint["test_metrics"]["recall"],
                "fscore": checkpoint["test_metrics"]["fscore"],
                "auroc": checkpoint["test_metrics"]["auroc"],
            },
            "threshold": checkpoint["test_metrics"]["threshold"],
        }

    # Fallback: Recompute metrics for old models that don't have cached test_metrics
    # Get job inputs to reconstruct the test data
    if not job.inputs:
        raise ValueError(f"Job {job.job_id} has no input parameters")

    # Recreate the config from job inputs
    from automar.shared.config.schemas import (
        GlobalConfig,
        ExtractOptions,
        PCAOptions,
        LoaderOptions,
        TuningOptions,
        TrainingOptions,
    )

    cfg = GlobalConfig(
        command="train",
        extract=ExtractOptions(**job.inputs["extract"]),
        pca=PCAOptions(**job.inputs["pca"]),
        loader=LoaderOptions(**job.inputs["loader"]),
        tune=TuningOptions(**job.inputs["tuning"]),
        train=TrainingOptions(**job.inputs["training"]),
    )

    # Reconstruct test data using same logic as training
    from .tuning_service import prepare_loaders
    from automar.core.preprocessing.extractor import df_industry_split, df_industry_avg
    from automar.shared.core.common import build_final_df
    from automar.shared.persistence.library import read_df
    from automar.shared.config.path_resolver import get_project_root

    project_root = get_project_root()

    # Rebuild dataframe (same as run_training)
    if cfg.pca.data_file:
        new_df = read_df(cfg.pca.data_file)
        new_df = new_df.dropna(ignore_index=True)
        if "Unnamed: 0" in new_df.columns:
            new_df = new_df.drop(["Unnamed: 0"], axis=1)
        if cfg.extract.industry:
            ind_name = cfg.extract.industry
        else:
            ind_name = new_df["Industry"].value_counts().idxmax()
    else:
        new_df, ind_name = build_final_df(cfg)

    tick_name = cfg.extract.ticker if cfg.extract.ticker else None

    # Apply PCA if needed (same logic as run_training)
    if tick_name:
        tick_df, ind_df = df_industry_split(new_df, industry=ind_name, ticker=tick_name)
        ind_mean = df_industry_avg(ind_df)
        tick_df = tick_df.drop(["Company", "Industry"], axis=1)
        tick_df = tick_df.set_index("Date")
    else:
        ind_mean_w_labels = df_industry_avg(new_df, 0)
        ind_mean_w_labels.Labels = ind_mean_w_labels.Labels.round()

    if cfg.train.pca_path:
        from .pca_service import load_pca, build_pca_df

        pca0 = load_pca(cfg.train.pca_path)
        cfg.loader.dopca = False

        if tick_name:
            _, pca_df = build_pca_df(pca0, ind_df)
            tick_df = tick_df.join(pca_df, on="Date")
        else:
            _, pca_df = build_pca_df(pca0, new_df[new_df["Industry"] == ind_name])
            ind_mean_w_labels = ind_mean_w_labels.join(pca_df, on="Date")

    # Prepare data loaders
    if model_type.lower() in ["gru", "transformer"]:
        # Neural network models use sequential loaders
        if tick_name:
            full_loaders = prepare_loaders(cfg, tick_df, avg_df=ind_mean)
        else:
            full_loaders = prepare_loaders(cfg, ind_mean_w_labels)
    else:
        # Logistic regression uses dict loaders
        from automar.core.preprocessing.loaders import vecs_to_dict

        if tick_name:
            seq_vecs, pca_obj = prepare_loaders(
                cfg, tick_df, avg_df=ind_mean, mode="reg"
            )
        else:
            seq_vecs, pca_obj = prepare_loaders(cfg, ind_mean_w_labels, mode="reg")
        full_loaders = vecs_to_dict(seq_vecs, pca=pca_obj)

    # Get test loader
    if isinstance(full_loaders, tuple):
        _, _, test_loader = full_loaders  # train, val, test
    else:
        # Dict loaders (log-reg)
        test_loader = full_loaders

    # Load and evaluate model
    from automar.core.models.evaluation import (
        prob_predictor,
        eval_roc_thresh,
        confu_matrix,
        pred_accuracy,
        pred_precision,
        pred_recall,
        pred_Fscore,
        eval_auroc,
    )

    device = cfg.loader.device or "cpu"

    if model_type.lower() in ["gru", "transformer"]:
        # Neural network model
        from automar.core.models import nn

        # Reconstruct hyperparameters from checkpoint
        if "hyperparameters" in checkpoint:
            ray_results = checkpoint["hyperparameters"]
        else:
            raise ValueError("No hyperparameters found in model checkpoint")

        # Extract model-specific parameters (not training params like epochs, lr, etc.)
        if "model" not in ray_results:
            raise ValueError("No model parameters found in hyperparameters")

        model_params = ray_results["model"]

        # Select model class
        if model_type.lower() == "gru":
            model_class = nn.GRUNet
        else:  # transformer
            model_class = nn.Transnet

        # Recreate model architecture with model-specific parameters only
        model_trained = model_class(**model_params)
        model_trained.load_state_dict(checkpoint["model_state_dict"])
        model_trained.to(device)
        model_trained.eval()
    else:
        # Logistic regression - checkpoint is the MUSE model object directly
        if isinstance(checkpoint, dict):
            model_trained = checkpoint.get("model", checkpoint)
        else:
            model_trained = checkpoint  # Already the MUSE model object

    # Generate predictions
    # For log-reg (dict loaders), need to specify set_type="test"
    if model_type.lower() in ["gru", "transformer"]:
        prob_preds = prob_predictor(model_trained, test_loader, device=device)
        threshold = eval_roc_thresh(prob_preds, test_loader)
    else:
        # Log-reg uses dict loaders
        prob_preds = prob_predictor(model_trained, test_loader, set_type="test")
        threshold = eval_roc_thresh(prob_preds, test_loader, set_type="test")

    # Compute confusion matrix and metrics
    # For log-reg, need to pass set_type="test"
    if model_type.lower() in ["gru", "transformer"]:
        con_mat = confu_matrix(prob_preds, test_loader, threshold)
        accuracy = pred_accuracy(prob_preds, test_loader, threshold)
        precision = pred_precision(prob_preds, test_loader, threshold)
        recall = pred_recall(prob_preds, test_loader, threshold)
        fscore = pred_Fscore(prob_preds, test_loader, threshold)
        auroc = eval_auroc(prob_preds, test_loader)
    else:
        # Log-reg uses dict loaders
        con_mat = confu_matrix(prob_preds, test_loader, threshold, set_type="test")
        accuracy = pred_accuracy(prob_preds, test_loader, threshold, set_type="test")
        precision = pred_precision(prob_preds, test_loader, threshold, set_type="test")
        recall = pred_recall(prob_preds, test_loader, threshold, set_type="test")
        fscore = pred_Fscore(prob_preds, test_loader, threshold, set_type="test")
        auroc = eval_auroc(prob_preds, test_loader, set_type="test")

    # Convert tensors to Python types
    if hasattr(con_mat, "cpu"):
        con_mat = con_mat.cpu().numpy()
    if hasattr(accuracy, "item"):
        accuracy = accuracy.item()
    if hasattr(precision, "item"):
        precision = precision.item()
    if hasattr(recall, "item"):
        recall = recall.item()
    if hasattr(fscore, "item"):
        fscore = fscore.item()
    if hasattr(auroc, "item"):
        auroc = auroc.item()

    # Confusion matrix format: sklearn returns [[TN, FP], [FN, TP]]
    matrix = (
        con_mat.tolist()
        if isinstance(con_mat, np.ndarray)
        else [[int(x) for x in row] for row in con_mat]
    )

    return {
        "job_id": job_id,
        "model": model_type,
        "matrix": matrix,
        "labels": ["Negative", "Positive"],
        "metrics": {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "fscore": float(fscore),
            "auroc": float(auroc),
        },
        "threshold": float(threshold),
    }


def prepare_cross_validation_data(job_id: str) -> Dict[str, Any]:
    """
    Prepare cross-validation results for visualization.

    Args:
        job_id: The cross-validation job ID

    Returns:
        Dictionary with fold results, mean metrics, and statistics

    Raises:
        ValueError: If job not found or not a cross-validation job
    """
    from automar.web.api.jobs import get_job

    job = get_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")

    if job.type != "crossvalidate":
        raise ValueError(f"Job {job_id} is not a cross-validation job")

    if not job.result or "cv_metrics" not in job.result:
        raise ValueError(f"Job {job_id} has no cross-validation results")

    fold_results = job.result[
        "cv_metrics"
    ]  # This is the actual field name in job results
    all_metrics = job.result.get("mean_metrics", {})

    # Separate mean and std metrics
    # The API stores them as: mean_accuracy, std_accuracy, mean_auc, std_auc, etc.
    mean_metrics = {}
    std_metrics = {}

    for key, value in all_metrics.items():
        if key.startswith("mean_"):
            # Extract metric name: mean_accuracy -> accuracy
            metric_name = key[5:]  # Remove 'mean_' prefix
            mean_metrics[metric_name] = value
        elif key.startswith("std_"):
            # Extract metric name: std_accuracy -> accuracy
            metric_name = key[4:]  # Remove 'std_' prefix
            std_metrics[metric_name] = value

    # If std_metrics is empty, calculate them from fold_results
    if not std_metrics and fold_results:
        import numpy as np

        for metric_name in mean_metrics.keys():
            values = [fold.get(metric_name, 0) for fold in fold_results]
            std_metrics[metric_name] = float(np.std(values))

    return {
        "job_id": job_id,
        "model": job.model,
        "fold_results": fold_results,
        "mean_metrics": mean_metrics,
        "std_metrics": std_metrics,
        "n_folds": job.result.get("n_folds", len(fold_results)),
    }


def prepare_training_history_data(job_id: str) -> Dict[str, Any]:
    """
    Prepare training history data for visualization.

    Args:
        job_id: The training job ID

    Returns:
        Dictionary with epochs, losses, AUROC, and learning rates

    Raises:
        ValueError: If job not found or no training history available
    """
    import torch  # Lazy import

    from automar.web.api.jobs import get_job

    job = get_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")

    if job.type != "training":
        raise ValueError(f"Job {job_id} is not a training job")

    if not job.result or "model_path" not in job.result:
        raise ValueError(f"Job {job_id} has no model path")

    model_path = Path(job.result["model_path"])
    if not model_path.exists():
        raise ValueError(f"Model file not found: {model_path}")

    # Load model checkpoint
    try:
        checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
    except Exception as e:
        raise ValueError(f"Failed to load model checkpoint: {e}")

    if "training_history" not in checkpoint:
        raise ValueError(
            "Training history not available. "
            "This model was trained before training history was implemented."
        )

    history = checkpoint["training_history"]

    # Validate required fields
    required_fields = ["epochs", "train_loss", "val_auroc", "val_lr"]
    missing = [f for f in required_fields if f not in history]
    if missing:
        raise ValueError(f"Training history missing fields: {missing}")

    return {
        "job_id": job_id,
        "model": job.model,
        "epochs": history["epochs"],
        "train_loss": [float(x) for x in history["train_loss"]],
        "val_auroc": [float(x) for x in history["val_auroc"]],
        "val_lr": [float(x) for x in history["val_lr"]],
    }


def prepare_tuning_statistics_data(job_id: str) -> Dict[str, Any]:
    """
    Prepare hyperparameter tuning statistics for visualization.

    Args:
        job_id: The tuning job ID

    Returns:
        Dictionary with tuning iterations, AUROC values, and best trial info

    Raises:
        ValueError: If job not found or no tuning statistics available
    """
    from automar.web.api.jobs import get_job

    job = get_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")

    if job.type != "tuning":
        raise ValueError(f"Job {job_id} is not a tuning job")

    if not job.result or "config_path" not in job.result:
        raise ValueError(f"Job {job_id} has no config path")

    config_path = Path(job.result["config_path"])
    stats_path = config_path.with_suffix(".stats.json")

    if not stats_path.exists():
        raise ValueError(
            "Tuning statistics not available. "
            "This tuning job was run before statistics saving was implemented."
        )

    # Load statistics
    import json

    with open(stats_path, "r") as f:
        stats = json.load(f)

    # Compute smoothed AUROC (max seen so far)
    auroc_values = stats.get("auroc", [])
    auroc_smooth = []
    max_so_far = 0
    for val in auroc_values:
        max_so_far = max(max_so_far, val)
        auroc_smooth.append(max_so_far)

    return {
        "job_id": job_id,
        "model": job.model,
        "iterations": stats.get("iterations", []),
        "auroc": auroc_values,
        "auroc_smooth": auroc_smooth,
        "best_score": stats.get("best_score"),
        "num_trials": stats.get("num_trials"),
        "top_trials": stats.get("top_trials", [])[:10],  # Top 10 trials
    }


def prepare_extraction_summary_data(job_id: str) -> Dict[str, Any]:
    """
    Prepare extraction time series data for visualization.

    Loads the actual stock data from the extracted dataset and prepares it
    for Plotly time series visualization.

    Args:
        job_id: The extraction job ID

    Returns:
        Dictionary with stock time series data (OHLCV) and metadata

    Raises:
        ValueError: If job not found, not an extraction job, or data unavailable
    """
    import pandas as pd  # Lazy import
    import numpy as np
    from automar.web.api.jobs import get_job
    from automar.shared.persistence.library import read_df

    job = get_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")

    if job.type != "extract":
        raise ValueError(f"Job {job_id} is not an extraction job")

    if not job.result:
        raise ValueError(f"Job {job_id} has no result data")

    result = job.result

    # Get file path from output_paths list
    file_path = None
    if "output_paths" in result and result["output_paths"]:
        file_path = result["output_paths"][0]

    if not file_path:
        raise ValueError(f"Job {job_id} has no output file path")

    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise ValueError(f"Dataset file not found: {file_path}")

    # Load the dataset
    try:
        df = read_df(file_path)
    except Exception as e:
        raise ValueError(f"Failed to load dataset: {e}")

    # Ensure Date column exists
    if "Date" not in df.columns:
        raise ValueError("Dataset missing 'Date' column")

    # Convert Date to datetime if needed
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"])

    # Filter by the requested date range from job result
    # This ensures visualization only shows the date range user selected,
    # which is especially important for SQLite files that may contain
    # companies with very different history lengths
    date_start = result.get("date_start")
    date_end = result.get("date_end")

    if date_start or date_end:
        if date_start:
            date_start_dt = pd.to_datetime(date_start)
            df = df[df["Date"] >= date_start_dt]
        if date_end:
            date_end_dt = pd.to_datetime(date_end)
            df = df[df["Date"] <= date_end_dt]

    # Sort by date
    df = df.sort_values("Date")

    # Check if this is an industry dataset (multiple companies)
    # IMPORTANT: Check this BEFORE downsampling to preserve all companies
    has_company_col = "Company" in df.columns
    is_multi_company = has_company_col and df["Company"].nunique() > 1

    original_row_count = len(df)

    # For multi-company datasets, compute industry statistics on FULL data
    # before downsampling (downsampling rows destroys the average calculation)
    industry_avg_dates = None
    industry_avg_close = None
    industry_company_count = None

    if is_multi_company and "Close" in df.columns:
        # Compute industry average on FULL dataset (all companies, all dates)
        df_clean = df.copy()
        df_clean["Close"] = df_clean["Close"].replace([np.inf, -np.inf], np.nan)

        # Group by date and compute mean across all companies
        industry_stats = (
            df_clean.groupby("Date")["Close"].agg(["mean", "count"]).reset_index()
        )
        industry_stats = industry_stats.sort_values("Date")

        # Only include dates where we have at least 1 company with data
        industry_stats = industry_stats[industry_stats["count"] >= 1]

        # Drop any remaining NaN values
        industry_stats = industry_stats.dropna(subset=["mean"])

        # Downsample industry stats by DATES (not rows) if too many
        max_dates = 5000
        if len(industry_stats) > max_dates:
            # Sample every Nth date
            date_step = len(industry_stats) // max_dates
            industry_stats = industry_stats.iloc[::date_step].reset_index(drop=True)

        industry_avg_dates = industry_stats["Date"].dt.strftime("%Y-%m-%d").tolist()
        industry_avg_close = industry_stats["mean"].tolist()
        industry_company_count = industry_stats["count"].tolist()

    # For single-ticker datasets, downsample the raw data
    # (This is safe because there's only one company)
    if not is_multi_company:
        max_points = 5000
        if len(df) > max_points:
            # Keep every nth row to get approximately max_points
            step = len(df) // max_points
            df = df.iloc[::step].reset_index(drop=True)

    # Extract OHLCV data (for single-ticker view)
    dates = df["Date"].dt.strftime("%Y-%m-%d").tolist()

    # Prepare main data dict
    data = {
        "dates": dates,
        "ticker": result.get("ticker"),
        "industry": result.get("industry"),
        "rows": len(df),
        "original_rows": result.get("rows", original_row_count),
        "downsampled": len(df) < result.get("rows", original_row_count),
    }

    # Add OHLCV columns if they exist (for single-ticker view)
    if not is_multi_company:
        ohlcv_columns = ["Open", "High", "Low", "Close", "Volume"]
        for col in ohlcv_columns:
            if col in df.columns:
                # Convert to native Python types for JSON serialization
                values = df[col].replace([np.inf, -np.inf], np.nan).fillna(0).tolist()
                data[col.lower()] = values

    if is_multi_company:
        # Get list of companies
        companies = df["Company"].unique().tolist()
        data["companies"] = companies
        data["company_count"] = len(companies)

        # For each company, get their Close price time series
        # Downsample per-company data separately to avoid mixing companies
        company_data = {}
        max_points_per_company = 5000

        for company in companies:
            company_df = df[df["Company"] == company].sort_values("Date")

            # Downsample this company's data if needed
            if len(company_df) > max_points_per_company:
                step = len(company_df) // max_points_per_company
                company_df = company_df.iloc[::step].reset_index(drop=True)

            if "Close" in company_df.columns and len(company_df) > 0:
                # Get dates and close prices for this company
                company_close_series = company_df["Close"].replace(
                    [np.inf, -np.inf], np.nan
                )
                # Only include rows where we have valid data
                valid_mask = company_close_series.notna()
                valid_df = company_df[valid_mask]

                company_dates = valid_df["Date"].dt.strftime("%Y-%m-%d").tolist()
                company_close = company_close_series[valid_mask].tolist()

                company_data[company] = {
                    "dates": company_dates,
                    "close": company_close,
                }

        data["company_data"] = company_data

        # Add the pre-computed industry averages
        if industry_avg_dates is not None:
            data["industry_avg_dates"] = industry_avg_dates
            data["industry_avg_close"] = industry_avg_close
            data["industry_company_count"] = industry_company_count

    # Add technical indicators if available (optional - for future toggles)
    tech_indicators = ["MA1", "MA2", "MA3", "MA4", "RSI1", "RSI2", "MACD", "K", "D"]
    available_indicators = []
    for indicator in tech_indicators:
        if indicator in df.columns:
            available_indicators.append(indicator)

    data["available_indicators"] = available_indicators

    return data


def prepare_prediction_probability_data(job_id: str) -> Dict[str, Any]:
    """
    Prepare prediction probability data for visualization.

    Handles prediction jobs (both eval and forecast modes).

    Args:
        job_id: The prediction job ID

    Returns:
        Dictionary with prediction probabilities, thresholds, and dates

    Raises:
        ValueError: If job not found or data unavailable
    """
    import pandas as pd  # Lazy import
    from automar.web.api.jobs import get_job

    job = get_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")

    if job.status != "completed":
        raise ValueError(f"Job {job_id} is not completed (status: {job.status})")

    if job.type != "prediction":
        raise ValueError(f"Job {job_id} is not a prediction job (type: {job.type})")

    return _prepare_prediction_job_data(job)


def _prepare_prediction_job_data(job) -> Dict[str, Any]:
    """
    Prepare visualization data from a completed prediction job.

    Reads the predictions CSV file and creates visualization data.
    """
    import pandas as pd
    from pathlib import Path

    if not job.result or "output_paths" not in job.result:
        raise ValueError(f"Job {job.job_id} has no output_paths in result")

    csv_path = job.result["output_paths"].get("predictions_csv")
    if not csv_path:
        raise ValueError(f"Job {job.job_id} has no predictions_csv path")

    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise ValueError(f"Predictions CSV not found: {csv_path}")

    # Read predictions CSV
    df = pd.read_csv(csv_path)

    mode = job.result.get("mode", "eval")
    model_type = job.result.get("model_type", "unknown")
    ticker = job.result.get("ticker")
    industry = job.result.get("industry")

    # Convert dates to strings
    dates = df["date"].tolist()
    predictions = df["prediction"].tolist()  # UP/DOWN strings
    probabilities = df["probability"].tolist()  # 0-100 percentage

    # Extract threshold from job results (already in percentage format 0-100)
    threshold = 50.0  # Default fallback
    if job.result.get("metrics"):
        # Get threshold from metrics (stored as percentage during prediction)
        threshold = job.result["metrics"].get("threshold", 50.0)

    data = {
        "job_id": job.job_id,
        "model": model_type,
        "ticker": ticker or f"{industry} (industry average)",
        "industry": industry,
        "mode": mode,
        "threshold": threshold,
        "dates": dates,
        "predictions": predictions,
        "probabilities": probabilities,
    }

    # Add actual labels if eval mode
    if mode == "eval" and "actual" in df.columns:
        actuals = df["actual"].tolist()
        data["actuals"] = actuals

    # For forecast mode, highlight the prediction
    if mode == "forecast" and len(dates) > 0:
        data["tomorrow_date"] = dates[0]
        data["tomorrow_probability"] = probabilities[0]
        data["prediction"] = "increase" if probabilities[0] > threshold else "decrease"

    # For eval mode, use last date as reference
    if mode == "eval" and len(dates) > 0:
        data["tomorrow_date"] = dates[-1]
        data["tomorrow_probability"] = probabilities[-1]
        data["prediction"] = "increase" if probabilities[-1] > threshold else "decrease"

    return data


def prepare_growing_windows_data(job_id: str) -> Dict[str, Any]:
    """
    Prepare growing windows slices data for visualization.

    Reconstructs the growing windows cross-validation data splits from job configuration.

    Args:
        job_id: The cross-validation job ID

    Returns:
        Dictionary with window information for each fold

    Raises:
        ValueError: If job not found or not a cross-validation job
    """
    from automar.web.api.jobs import get_job

    job = get_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")

    if job.type != "crossvalidate":
        raise ValueError(f"Job {job_id} is not a cross-validation job")

    if not job.inputs:
        raise ValueError(f"Job {job.job_id} has no input parameters")

    # Extract configuration parameters (handle legacy key mismatch)
    cv_inputs = (
        job.inputs.get("crossvalidation") or job.inputs.get("crossvalidate") or {}
    )
    n_split = cv_inputs.get("n_split", 5)
    test_size = job.inputs.get("loader", {}).get("test_size", 0.2)
    val_size = job.inputs.get("loader", {}).get("val_size", 0.2)

    # Try to get total dataset size from job result or inputs
    total_samples = None

    # First, check if it's stored in the result
    if job.result:
        if "total_samples" in job.result:
            total_samples = job.result["total_samples"]
        elif "cv_metrics" in job.result:
            fold_results = job.result["cv_metrics"]
            # Try to get sample count from any fold that has it
            for fold in fold_results:
                if "n_samples" in fold or "total_samples" in fold:
                    total_samples = fold.get("n_samples") or fold.get("total_samples")
                    break

    # If not found, we'll leave it as None and won't show sample counts
    # (only show percentages)

    # Calculate growing windows splits
    # The test set is ALWAYS constant at test_size% of TOTAL data (taken from the end)
    # Training and validation sets grow progressively from the remaining data

    # Total data = 100%
    # Test set = test_size% (e.g., 15% or 20%) - CONSTANT across all folds
    # Available for train/val = (1 - test_size)% (e.g., 85% or 80%)

    windows = []

    for idx in range(1, n_split + 1):
        # Current window uses idx/n_split of the available (train+val) data
        current_fraction = idx / n_split

        # Available data for train+val (as fraction of TOTAL dataset)
        train_val_available = 1 - test_size

        # Current window's train+val portion (grows from 1/n to n/n of available data)
        current_train_val = train_val_available * current_fraction

        # Split train+val according to configured ratio
        # Within the current_train_val, split using the original ratio
        val_ratio = val_size / (1 - test_size)  # Val as fraction of (train+val)
        train_ratio = 1 - val_ratio

        current_val = current_train_val * val_ratio
        current_train = current_train_val * train_ratio

        # Test is ALWAYS the same (as fraction of TOTAL dataset)
        current_test = test_size

        # IMPORTANT: For visualization, we want percentages relative to TOTAL dataset (100%)
        # So train + val + test + unused = 100%
        # Where unused = data not yet used in this fold

        window_data = {
            "fold": idx,
            # Absolute sizes (as fraction of total dataset, 0.0 to 1.0)
            "train_size": float(current_train),
            "val_size": float(current_val),
            "test_size": float(current_test),
            "used_size": float(current_train + current_val + current_test),
            # Percentages (of total dataset, sum to 100%)
            "train_percent": float(current_train * 100),
            "val_percent": float(current_val * 100),
            "test_percent": float(current_test * 100),
            "used_percent": float((current_train + current_val + current_test) * 100),
        }

        # Add sample counts if we know total_samples
        if total_samples:
            window_data["train_samples"] = int(current_train * total_samples)
            window_data["val_samples"] = int(current_val * total_samples)
            window_data["test_samples"] = int(current_test * total_samples)
            window_data["used_samples"] = int(
                (current_train + current_val + current_test) * total_samples
            )

        windows.append(window_data)

    return {
        "job_id": job_id,
        "model": job.model,
        "n_folds": n_split,
        "test_size_config": test_size,
        "val_size_config": val_size,
        "total_samples": total_samples,
        "windows": windows,
    }


def prepare_pca_analysis_data(pca_file_path: str) -> Dict[str, Any]:
    """
    Prepare PCA analysis data for visualization.

    Args:
        pca_file_path: Path to the PCA object file (joblib format)

    Returns:
        Dictionary with explained variance, component matrices, etc.

    Raises:
        ValueError: If file not found or can't be loaded
    """
    import joblib  # Lazy import - PCA files are saved with joblib, not pickle
    import numpy as np  # Lazy import

    pca_path = Path(pca_file_path)
    if not pca_path.exists():
        raise ValueError(f"PCA file not found: {pca_path}")

    # Load PCA object (using joblib, same as pca.py)
    try:
        with open(pca_path, "rb") as f:
            data = joblib.load(f)
    except Exception as e:
        raise ValueError(f"Failed to load PCA object: {e}")

    # Handle both old format (direct PCA) and new format (dict with feature names)
    if isinstance(data, dict) and "pca" in data:
        pca = data["pca"]
        feature_names = data.get("feature_names", None)
    else:
        pca = data
        feature_names = None

    # Get the component loadings matrix (features × components)
    # This shows the contribution (loading/weight) of each feature to each component
    # Can be positive or negative (direction of contribution)
    components_matrix = pca.components_.T  # Transpose to get (features × components)

    # Get covariance matrix and convert to correlation matrix
    covariance_matrix = pca.get_covariance()

    # Calculate correlation matrix from covariance matrix
    # Correlation[i,j] = Covariance[i,j] / (std[i] * std[j])
    # where std[i] = sqrt(Variance[i]) = sqrt(Covariance[i,i])
    std_devs = np.sqrt(np.diag(covariance_matrix))  # Standard deviations
    correlation_matrix = covariance_matrix / np.outer(std_devs, std_devs)

    n_components = pca.n_components_

    # Generate labels
    component_labels = [f"PC{i+1}" for i in range(n_components)]

    # Feature names: use actual names if available, otherwise generate generic ones
    n_features = pca.components_.shape[1]
    if feature_names is None:
        feature_names = [f"Feature{i+1}" for i in range(n_features)]

    # Total variance explained
    total_variance = float(np.sum(pca.explained_variance_ratio_))

    return {
        "explained_variance_ratio": [float(x) for x in pca.explained_variance_ratio_],
        "components_matrix": components_matrix.tolist(),  # Feature loadings/contributions
        "component_labels": component_labels,
        "feature_names": feature_names,
        "correlation_matrix": correlation_matrix.tolist(),
        "total_variance_explained": total_variance,
        "n_components": n_components,
        "n_features": n_features,
    }
