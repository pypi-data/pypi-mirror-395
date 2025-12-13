# -*- coding: utf-8 -*-
"""
Model prediction/inference runner for Automar

Handles inference using trained models on new/different datasets
"""


def run_prediction(cfg, progress_callback=None):
    """
    Run inference using a trained model on new data

    Args:
        cfg: GlobalConfig with predict, extract, pca, loader options
        progress_callback: Optional callback for progress updates

    Returns:
        Dictionary with predictions, metrics, and metadata
    """
    from automar.shared.core.common import run_prediction_common

    return run_prediction_common(cfg, progress_callback)


def save_predictions_to_disk(cfg, results, model_path, ind_name, tick_name):
    """
    Save prediction results to disk (CSV and JSON)

    Args:
        cfg: Configuration object
        results: Prediction results dictionary
        model_path: Path to model file
        ind_name: Industry name
        tick_name: Ticker name (or None for industry-level)
    """
    import pandas as pd
    import json
    from pathlib import Path
    from automar.shared.config.path_resolver import get_project_root
    from automar.shared.persistence.library import date_ender

    project_root = get_project_root()

    # Determine save directory
    if cfg.predict.save_dir:
        save_dir = Path(cfg.predict.save_dir)
        if not save_dir.is_absolute():
            save_dir = project_root / save_dir
    else:
        mode_folder = "eval" if cfg.predict.mode == "eval" else "forecast"
        model_folder = results["model_type"].lower().replace("-", "")
        save_dir = project_root / "out" / "preds" / mode_folder / model_folder

    save_dir.mkdir(exist_ok=True, parents=True)

    # Generate filename with descriptive parameters
    # Format: {model}_{industry}({ticker})_{date}_{mode}_{Ndays}
    # Example: GRU_Consumer Discretionary(EBAY)_2025-11-21_forecast_11days
    base_name = f"{results['model_type']}_{ind_name}"
    if tick_name:
        base_name += f"({tick_name})"
    base_name += f"_{date_ender(cfg.extract.datend)}"

    mode_suffix = "evaluation" if cfg.predict.mode == "eval" else "forecast"
    base_name += f"_{mode_suffix}"

    # Add forecast_days for forecast mode (makes it clear what the job does)
    if cfg.predict.mode == "forecast" and cfg.predict.forecast_days:
        base_name += f"_{cfg.predict.forecast_days}days"

    # Convert predictions to UP/DOWN
    pred_strings = ["UP" if p == 1 else "DOWN" for p in results["predictions"]]

    # Build DataFrame based on mode
    if cfg.predict.mode == "eval":
        actual_strings = ["UP" if a == 1 else "DOWN" for a in results["labels"]]

        # Trim dates to match predictions length
        # (WEASEL-MUSE or other processing may result in fewer predictions than raw data points)
        test_dates = results.get("dates", [])
        test_dates = test_dates[-len(pred_strings) :] if test_dates else []

        pred_df = pd.DataFrame(
            {
                "date": test_dates,
                "prediction": pred_strings,
                "probability": results["probabilities"],
                "actual": actual_strings,
            }
        )
    else:
        pred_df = pd.DataFrame(
            {
                "date": results.get("forecast_dates", []),
                "day_ahead": list(range(1, len(pred_strings) + 1)),
                "prediction": pred_strings,
                "probability": results["probabilities"],
            }
        )

    # Save CSV
    csv_path = save_dir / f"{base_name}.csv"
    pred_df.to_csv(csv_path, index=False)

    # Save metrics as JSON (eval mode only)
    json_path = None
    if cfg.predict.mode == "eval":
        metrics_data = {
            "model_path": str(model_path),
            "model_type": results["model_type"],
            "dataset": results["dataset"],
            "metrics": results["metrics"],
            "confusion_matrix": results["confusion_matrix"],
        }
        json_path = save_dir / f"{base_name}_metrics.json"
        with open(json_path, "w") as f:
            json.dump(metrics_data, f, indent=2)

    # Store paths in results
    results["output_paths"] = {
        "predictions_csv": str(csv_path),
        "metrics_json": str(json_path),
    }

    # Print summary
    print(f"\n{'='*60}")
    print(f"Prediction Mode: {cfg.predict.mode.upper()}")
    print(f"{'='*60}")

    if cfg.predict.mode == "eval":
        print(f"\nPredictions saved to:")
        print(f"  CSV: {csv_path}")
        print(f"  Metrics: {json_path}")
        print(f"\nPerformance:")
        print(f"  AUROC:    {results['metrics']['auroc']:.4f}")
        print(f"  Accuracy: {results['metrics']['accuracy']:.4f}")
        print(f"  Samples:  {len(results['predictions'])}")
    else:
        print(f"\nForecast Result:")
        forecast_dates = results.get("forecast_dates", [])
        if forecast_dates:
            print(f"  Date:        {forecast_dates[0]}")
        print(
            f"  Prediction:  {results['predictions'][0]} ({'UP' if results['predictions'][0] == 1 else 'DOWN'})"
        )
        print(f"  Probability: {results['probabilities'][0]:.2f}%")
        print(f"\nPrediction saved to: {csv_path}")
