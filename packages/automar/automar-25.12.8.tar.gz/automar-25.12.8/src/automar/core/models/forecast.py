# -*- coding: utf-8 -*-
"""
Feature synthesis utilities for multi-day forecasting

Generates synthetic feature vectors for days beyond the first prediction
using conditional autoregression based on model predictions and historical patterns.
"""

from typing import Dict, Any, Optional


def compute_synthesis_statistics(dataframe) -> Dict[str, float]:
    """
    Analyze training data to learn typical UP/DOWN day patterns for feature synthesis

    Args:
        dataframe: Training dataframe with 'Labels' column (1=UP, 0=DOWN)
                   and financial features (Close, Volume, etc.)

    Returns:
        Dictionary of statistics for feature synthesis:
        - up_day_return_mean/std: Average and std of returns on UP days
        - down_day_return_mean/std: Average and std of returns on DOWN days
        - up_day_volume_ratio: Relative volume on UP vs DOWN days
        - feature means/stds for normalization
    """
    import numpy as np

    if "Labels" not in dataframe.columns:
        raise ValueError("Dataframe must have 'Labels' column for synthesis stats")

    # Separate UP and DOWN days
    up_days = dataframe[dataframe["Labels"] == 1]
    down_days = dataframe[dataframe["Labels"] == 0]

    # Calculate returns if Close column exists
    stats = {}

    if "Close" in dataframe.columns:
        # Calculate daily returns
        up_returns = up_days["Close"].pct_change().dropna()
        down_returns = down_days["Close"].pct_change().dropna()

        stats["up_day_return_mean"] = float(up_returns.mean())
        stats["up_day_return_std"] = float(up_returns.std())
        stats["down_day_return_mean"] = float(down_returns.mean())
        stats["down_day_return_std"] = float(down_returns.std())
    else:
        # Fallback defaults if Close not available
        stats["up_day_return_mean"] = 0.015  # 1.5% typical gain
        stats["up_day_return_std"] = 0.005
        stats["down_day_return_mean"] = -0.012  # 1.2% typical loss
        stats["down_day_return_std"] = 0.005

    # Volume analysis if available
    if "Volume" in dataframe.columns:
        up_volume_mean = up_days["Volume"].mean()
        down_volume_mean = down_days["Volume"].mean()
        stats["up_day_volume_ratio"] = float(
            up_volume_mean / down_volume_mean if down_volume_mean > 0 else 1.2
        )
        stats["down_day_volume_ratio"] = 1.0  # Baseline
    else:
        stats["up_day_volume_ratio"] = 1.2  # UP days typically have 20% more volume
        stats["down_day_volume_ratio"] = 1.0

    # Store overall feature statistics for fallback synthesis
    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
    feature_cols = [c for c in numeric_cols if c not in ["Labels", "Date"]]

    stats["feature_means"] = {}
    stats["feature_stds"] = {}
    for col in feature_cols:
        stats["feature_means"][col] = float(dataframe[col].mean())
        stats["feature_stds"][col] = float(dataframe[col].std())

    return stats


def synthesize_next_day_features(
    last_window,
    predicted_direction: int,
    training_stats: Dict[str, Any],
    industry_avg: Optional[Any] = None,
):
    """
    Generate synthetic features for the next day using conditional autoregression

    This function creates plausible feature vectors for day +1 based on:
    1. Model's UP/DOWN prediction (50% weight)
    2. Industry momentum if available (30% weight)
    3. Ticker momentum from recent history (20% weight)
    4. Realistic stochastic noise

    Args:
        last_window: Recent feature history, shape (tsize, n_features)
                     where last row is most recent day
        predicted_direction: Model's prediction (1=UP, 0=DOWN)
        training_stats: Statistics from compute_synthesis_statistics()
        industry_avg: Optional industry average features, shape (n_features,)

    Returns:
        Synthetic feature vector for next day, shape (n_features,)
    """
    import numpy as np

    if len(last_window.shape) != 2:
        raise ValueError(
            f"last_window must be 2D (tsize, n_features), got shape {last_window.shape}"
        )

    last_day = last_window[-1]  # Most recent day
    n_features = last_window.shape[1]

    # 1. Select appropriate return statistics based on prediction
    if predicted_direction == 1:  # UP
        typical_return = training_stats["up_day_return_mean"]
        return_std = training_stats["up_day_return_std"]
        volume_ratio = training_stats["up_day_volume_ratio"]
    else:  # DOWN
        typical_return = training_stats["down_day_return_mean"]
        return_std = training_stats["down_day_return_std"]
        volume_ratio = training_stats["down_day_volume_ratio"]

    # 2. Calculate momentum signals
    # Ticker momentum: recent 5-day trend
    if len(last_window) >= 5:
        ticker_momentum = (last_window[-1] - last_window[-5]).mean() / (
            np.abs(last_window[-5]).mean() + 1e-8
        )
    else:
        ticker_momentum = 0.0

    # Industry momentum: if provided
    if industry_avg is not None:
        # Compare last day to industry average
        industry_momentum = (last_day - industry_avg).mean() / (
            np.abs(industry_avg).mean() + 1e-8
        )
    else:
        industry_momentum = 0.0

    # 3. Weighted combination of signals
    # 50% model prediction, 30% industry, 20% ticker momentum
    predicted_return = (
        0.5 * typical_return + 0.3 * industry_momentum + 0.2 * ticker_momentum
    )

    # Add realistic Gaussian noise
    noise = np.random.normal(0, return_std)
    predicted_return += noise

    # 4. Generate synthetic features
    # Simple approach: apply return multiplicatively to all features
    # This assumes features are price-like (OHLC, indicators scale with price)
    synthetic_features = last_day * (1 + predicted_return)

    # Adjust specific feature indices if we know the structure
    # For now, apply return uniformly with some feature-specific variation

    # Add small random variations to make features more realistic
    feature_noise = np.random.normal(0, 0.01, size=n_features)
    synthetic_features = synthetic_features * (1 + feature_noise)

    # Special handling for volume-like features (if we can identify them)
    # Volume typically increases on UP days, decreases on DOWN days
    # This is a heuristic - in production, you'd want to identify which features are volume
    synthetic_features = synthetic_features * volume_ratio

    # Ensure no negative values for features that should be positive
    # (e.g., prices, volume)
    synthetic_features = np.clip(synthetic_features, 0, None)

    return synthetic_features


def synthesize_next_day_features_structured(
    last_window,
    predicted_direction: int,
    training_stats: Dict[str, Any],
    industry_avg: Optional[Any] = None,
    feature_names: Optional[list] = None,
):
    """
    Advanced feature synthesis with structure-aware generation

    This version attempts to identify and synthesize specific feature types
    (OHLC, volume, technical indicators) more accurately.

    Args:
        last_window: Recent feature history, shape (tsize, n_features)
        predicted_direction: Model's prediction (1=UP, 0=DOWN)
        training_stats: Statistics from compute_synthesis_statistics()
        industry_avg: Optional industry average features
        feature_names: List of feature names for structure-aware synthesis

    Returns:
        Synthetic feature vector for next day, shape (n_features,)
    """
    # For now, use simple approach - can be enhanced later
    # with feature name detection (Open, High, Low, Close, Volume, RSI, etc.)
    return synthesize_next_day_features(
        last_window, predicted_direction, training_stats, industry_avg
    )


def synthesize_next_day_features_weighted(
    last_window,
    predicted_direction: int,
    predicted_probability: float,
    training_stats: Dict[str, Any],
    feature_names: list,
    feature_importances: Dict,
    industry_avg: Optional[Any] = None,
):
    """
    Enhanced synthesis with importance-based weighting.

    Features with high importance are synthesized carefully using sophisticated methods,
    while low-importance features use simpler approximations. This improves forecast
    accuracy by focusing computational effort where it matters most.

    Args:
        last_window: Recent history (tsize, n_features)
        predicted_direction: 1=UP, 0=DOWN
        predicted_probability: P(UP) from model [0, 1]
        training_stats: Statistics from compute_synthesis_statistics()
        feature_names: List of feature names
        feature_importances: Dict[feature_idx -> importance] from training
        industry_avg: Optional sector features

    Returns:
        Synthetic feature vector (n_features,)
    """
    import numpy as np

    last_day = last_window[-1]
    n_features = len(feature_names)
    synthetic = np.zeros(n_features)

    # Probability-weighted statistics
    prob_up = predicted_probability
    prob_down = 1 - predicted_probability

    weighted_return_mean = (
        prob_up * training_stats["up_day_return_mean"]
        + prob_down * training_stats["down_day_return_mean"]
    )
    weighted_return_std = np.sqrt(
        prob_up * training_stats["up_day_return_std"] ** 2
        + prob_down * training_stats["down_day_return_std"] ** 2
    )
    weighted_volume_ratio = (
        prob_up * training_stats["up_day_volume_ratio"]
        + prob_down * training_stats["down_day_volume_ratio"]
    )

    # Sample return
    actual_return = weighted_return_mean + np.random.normal(0, weighted_return_std)

    # Map feature_importances to array (handle both idx and name keys)
    if isinstance(list(feature_importances.keys())[0], int):
        # Importance by index
        importances_array = np.array(
            [feature_importances.get(i, 0.5) for i in range(n_features)]
        )
    else:
        # Importance by name
        importances_array = np.array(
            [feature_importances.get(name, 0.5) for name in feature_names]
        )

    # Normalize to [0, 1]
    if importances_array.max() > importances_array.min():
        importances_normalized = (importances_array - importances_array.min()) / (
            importances_array.max() - importances_array.min()
        )
    else:
        importances_normalized = np.ones(n_features) * 0.5

    # Compute percentile thresholds ONCE (before loop)
    # This ensures distribution adapts to actual importance values
    high_threshold = np.percentile(importances_normalized, 75)  # Top 25%
    medium_threshold = np.percentile(importances_normalized, 50)  # Top 50%

    # Synthesize each feature with importance-based weighting
    for i, name in enumerate(feature_names):
        importance = importances_normalized[i]
        name_lower = name.lower()

        # Determine synthesis weight based on importance percentile
        if importance >= high_threshold:  # High importance (top quartile)
            synthesis_weight = 1.0
        elif importance >= medium_threshold:  # Medium importance (2nd quartile)
            synthesis_weight = 0.6
        else:  # Low importance (bottom half)
            synthesis_weight = 0.2

        # Feature-type specific synthesis
        if name_lower in ["open", "high", "low", "close"]:
            # OHLC: Apply return
            careful_value = last_day[i] * (1 + actual_return)
            lazy_value = last_day[i] * (1 + np.random.normal(0, 0.01))
            synthetic[i] = (
                synthesis_weight * careful_value + (1 - synthesis_weight) * lazy_value
            )

        elif "volume" in name_lower:
            # Volume: Direction-dependent
            volume_return = np.random.normal(0, 0.1)
            careful_value = last_day[i] * weighted_volume_ratio * (1 + volume_return)
            lazy_value = last_day[i] * (1 + np.random.normal(0, 0.05))
            synthetic[i] = (
                synthesis_weight * careful_value + (1 - synthesis_weight) * lazy_value
            )

        elif name_lower in ["rsi1", "rsi2", "wr1", "wr2"]:
            # Bounded oscillators (0-100)
            mean_reversion = 0.7 * last_day[i] + 0.3 * 50
            direction_bias = (prob_up - 0.5) * 20
            careful_value = np.clip(mean_reversion + direction_bias, 0, 100)
            # Lazy: add small random walk instead of exact carry-forward
            lazy_value = np.clip(last_day[i] + np.random.normal(0, 2), 0, 100)
            synthetic[i] = (
                synthesis_weight * careful_value + (1 - synthesis_weight) * lazy_value
            )

        elif name_lower in ["k", "d"]:
            # Stochastic oscillators (0-100)
            mean_rev = 0.7 * last_day[i] + 0.3 * 50
            direction_bias = (prob_up - 0.5) * 30
            careful_value = np.clip(mean_rev + direction_bias, 0, 100)
            # Lazy: add small random walk instead of exact carry-forward
            lazy_value = np.clip(last_day[i] + np.random.normal(0, 2), 0, 100)
            synthetic[i] = (
                synthesis_weight * careful_value + (1 - synthesis_weight) * lazy_value
            )

        elif name_lower.startswith("ma"):
            # Moving averages
            careful_value = last_day[i] * (1 + actual_return * 0.5)
            lazy_value = last_day[i]
            synthetic[i] = (
                synthesis_weight * careful_value + (1 - synthesis_weight) * lazy_value
            )

        elif name_lower in ["diff", "dea", "macd"]:
            # MACD components
            careful_value = last_day[i] + actual_return * last_day[i] * 0.5
            lazy_value = last_day[i]
            synthetic[i] = (
                synthesis_weight * careful_value + (1 - synthesis_weight) * lazy_value
            )

        elif name_lower in ["cci1", "cci2"]:
            # CCI
            careful_value = last_day[i] * 0.8 + actual_return * 100
            lazy_value = last_day[i]
            synthetic[i] = (
                synthesis_weight * careful_value + (1 - synthesis_weight) * lazy_value
            )

        elif "industry" in name_lower or "avg" in name_lower:
            # Industry/PCA features - use actual values
            if industry_avg is not None and i < len(industry_avg):
                synthetic[i] = industry_avg[i] * (1 + np.random.normal(0, 0.02))
            else:
                synthetic[i] = last_day[i]

        else:
            # Unknown features - weighted synthesis
            careful_value = last_day[i] * (1 + actual_return * 0.5)
            lazy_value = last_day[i]
            synthetic[i] = (
                synthesis_weight * careful_value + (1 - synthesis_weight) * lazy_value
            )

    return synthetic


def validate_synthetic_features(
    synthetic, last_window, predicted_direction: int
) -> bool:
    """
    Validate that synthetic features are reasonable

    Checks:
    - No NaN or Inf values
    - Values within reasonable bounds relative to recent history
    - Direction-consistent price movement (if detectable)

    Args:
        synthetic: Synthetic features to validate
        last_window: Recent history for comparison
        predicted_direction: Expected direction (1=UP, 0=DOWN)

    Returns:
        True if features pass validation, False otherwise
    """
    import numpy as np

    # Check for invalid values
    if np.any(np.isnan(synthetic)) or np.any(np.isinf(synthetic)):
        return False

    # Check that values are within reasonable bounds (e.g., not 1000x last day)
    last_day = last_window[-1]
    ratio = synthetic / (last_day + 1e-8)

    # Features should not change by more than 50% in one day (generous bound)
    if np.any(ratio > 1.5) or np.any(ratio < 0.5):
        return False

    # All checks passed
    return True


def run_forecast(model, device, data_df, ind_mean, cfg, checkpoint):
    """
    Multi-day forecast for neural network models (GRU, Transformer)

    Note: Imports torch locally (following pattern from training_service.py)
    """
    import torch
    import numpy as np
    import pandas as pd
    from automar.shared.services.tuning_service import SCALERS

    forecast_days = cfg.predict.forecast_days or 1
    synthesis_stats = checkpoint.get("synthesis_stats")
    feature_names = checkpoint.get("feature_names", [])
    feature_importances = checkpoint.get("feature_importances", {})

    # Extract optimal threshold from checkpoint (stored as fraction 0-1)
    threshold = 0.5  # Default fallback
    if checkpoint and isinstance(checkpoint, dict):
        test_metrics = checkpoint.get("test_metrics")
        if test_metrics and isinstance(test_metrics, dict):
            threshold = test_metrics.get("threshold", 0.5)

    if forecast_days > 1 and not synthesis_stats:
        import warnings

        warnings.warn("Computing synthesis stats from current data", UserWarning)
        synthesis_stats = compute_synthesis_statistics(data_df)

    # Fallback to uniform weights if no importance available (backward compatibility)
    if not feature_importances and feature_names:
        n_features = len(feature_names)
        feature_importances = {i: 1.0 / n_features for i in range(n_features)}

    # Prepare scaler (reuse from tuning_service)
    scaler = SCALERS[cfg.loader.scaler]()
    feature_df = (
        data_df.drop(columns=["Labels"])
        if "Labels" in data_df.columns
        else data_df.iloc[:, :-1]
    )
    all_features = feature_df.values
    scaler.fit(all_features[: int(len(all_features) * 0.8)])

    current_window = scaler.transform(all_features[-cfg.loader.tsize :])
    industry_avg = _extract_industry_features(ind_mean, all_features.shape[1])

    # Forecast loop
    predictions, probabilities, forecast_dates = [], [], []
    last_date = data_df.index[-1]

    for day_ahead in range(forecast_days):
        input_tensor = torch.FloatTensor(current_window).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(input_tensor)
            prob = torch.sigmoid(output).squeeze().item()
            pred = int(prob > threshold)  # Use optimal threshold from checkpoint

        next_date = pd.bdate_range(start=last_date, periods=day_ahead + 2)[-1]
        predictions.append(pred)
        probabilities.append(prob * 100)
        forecast_dates.append(next_date)

        if day_ahead < forecast_days - 1:
            # Use importance-weighted synthesis if available
            if feature_importances and feature_names:
                synthetic = synthesize_next_day_features_weighted(
                    scaler.inverse_transform(current_window),
                    pred,
                    prob,  # Pass probability for weighting
                    synthesis_stats,
                    feature_names,
                    feature_importances,
                    industry_avg,
                )
            else:
                # Fallback to simple synthesis for backward compatibility
                synthetic = synthesize_next_day_features(
                    scaler.inverse_transform(current_window),
                    pred,
                    synthesis_stats,
                    industry_avg,
                )
            current_window = np.vstack(
                [
                    current_window[1:],
                    scaler.transform(synthetic.reshape(1, -1)).flatten(),
                ]
            )

    return {
        "predictions": predictions,
        "probabilities": probabilities,
        "labels": [],
        "metrics": {"threshold": threshold * 100},  # Convert to percentage for frontend
        "confusion_matrix": [],
        "forecast_dates": [d.strftime("%Y-%m-%d") for d in forecast_dates],
        "forecast_days": forecast_days,
        "mode": "forecast",
    }


def run_forecast_logreg(model, data_df, ind_mean, cfg, checkpoint=None):
    """
    Multi-day forecast for logistic regression models

    Note: Unlike neural networks, WEASEL-MUSE expects single feature vectors
    (n_features,) not time windows. We use only the most recent day.
    """
    import numpy as np
    import pandas as pd
    from automar.shared.services.tuning_service import SCALERS

    forecast_days = cfg.predict.forecast_days or 1
    synthesis_stats = None
    feature_names = checkpoint.get("feature_names", []) if checkpoint else []
    feature_importances = (
        checkpoint.get("feature_importances", {}) if checkpoint else {}
    )

    # Extract optimal threshold from checkpoint (stored as fraction 0-1)
    threshold = 0.5  # Default fallback
    if checkpoint and isinstance(checkpoint, dict):
        test_metrics = checkpoint.get("test_metrics")
        if test_metrics and isinstance(test_metrics, dict):
            threshold = test_metrics.get("threshold", 0.5)

    if forecast_days > 1:
        import warnings

        warnings.warn("Computing synthesis stats from current data", UserWarning)
        synthesis_stats = compute_synthesis_statistics(data_df)

    # Fallback to uniform weights if no importance available (backward compatibility)
    if not feature_importances and feature_names:
        n_features = len(feature_names)
        feature_importances = {i: 1.0 / n_features for i in range(n_features)}

    # Prepare scaler
    scaler = SCALERS[cfg.loader.scaler]()
    feature_df = (
        data_df.drop(columns=["Labels"])
        if "Labels" in data_df.columns
        else data_df.iloc[:, :-1]
    )
    all_features = feature_df.values
    scaler.fit(all_features[: int(len(all_features) * 0.8)])

    # IMPORTANT: Log-reg uses single feature vectors, NOT time windows
    # Start with the most recent day's features
    current_features = scaler.transform(all_features[-1:])  # Shape: (1, n_features)
    industry_avg = _extract_industry_features(ind_mean, all_features.shape[1])

    # Forecast loop
    predictions, probabilities, forecast_dates = [], [], []
    last_date = data_df.index[-1]

    for day_ahead in range(forecast_days):
        # Get probability from model
        probability = model.predict_proba(current_features)[0, 1]
        # Apply our optimized threshold (not sklearn's default 0.5)
        prediction = int(probability > threshold)

        next_date = pd.bdate_range(start=last_date, periods=day_ahead + 2)[-1]
        predictions.append(prediction)
        probabilities.append(float(probability * 100))
        forecast_dates.append(next_date)

        if day_ahead < forecast_days - 1:
            # Synthesize next day features
            # Note: For log-reg, we create a "pseudo-window" for synthesis functions
            # by repeating the current features (they expect window shape)
            current_unscaled = scaler.inverse_transform(current_features)
            pseudo_window = np.tile(current_unscaled, (cfg.loader.tsize, 1))

            # Use importance-weighted synthesis if available
            if feature_importances and feature_names:
                synthetic = synthesize_next_day_features_weighted(
                    pseudo_window,
                    int(prediction),
                    float(probability),  # Pass probability for weighting
                    synthesis_stats,
                    feature_names,
                    feature_importances,
                    industry_avg,
                )
            else:
                # Fallback to simple synthesis for backward compatibility
                synthetic = synthesize_next_day_features(
                    pseudo_window,
                    int(prediction),
                    synthesis_stats,
                    industry_avg,
                )

            # Update current features for next iteration
            current_features = scaler.transform(synthetic.reshape(1, -1))

    return {
        "predictions": predictions,
        "probabilities": probabilities,
        "labels": [],
        "metrics": {"threshold": threshold * 100},  # Convert to percentage for frontend
        "confusion_matrix": [],
        "forecast_dates": [d.strftime("%Y-%m-%d") for d in forecast_dates],
        "forecast_days": forecast_days,
        "mode": "forecast",
    }


def _extract_industry_features(ind_mean, n_features):
    """Extract industry average features for synthesis"""
    if ind_mean is None:
        return None
    ind_mean_df = (
        ind_mean.drop(columns=["Labels"]) if "Labels" in ind_mean.columns else ind_mean
    )
    features = ind_mean_df.values[-1]
    return features if len(features) == n_features else None
