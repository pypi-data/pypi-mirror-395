# -*- coding: utf-8 -*-
"""
Feature importance computation methods for autoregressive synthesis.

This module provides multiple methods to compute feature importance scores
that guide how carefully each feature should be synthesized during multi-day
forecasting.
"""

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import roc_auc_score


def compute_permutation_importance_auroc(
    model, val_loader_or_dict, device=None, n_repeats=5, set_type="val"
):
    """
    Measure feature importance by permuting each feature and measuring AUROC drop.

    This is the GOLD STANDARD method for measuring what the trained model actually uses.

    Args:
        model: Trained neural network or MUSE model
        val_loader_or_dict: Validation DataLoader (neural nets) or dict (MUSE)
        device: 'cuda' or 'cpu' for neural networks
        n_repeats: Number of permutation repeats (5 is good balance, 10 for max rigor)
        set_type: 'val' or 'test'

    Returns:
        Dict mapping feature_idx -> importance score (higher = more important)

    Example:
        {0: 0.18,  # Feature 0 (Close): 18% importance
         1: 0.12,  # Feature 1 (RSI): 12% importance
         ...}

    Time complexity:
        - Neural nets (GPU): ~10 seconds for 42 features × 5 repeats
        - Neural nets (CPU): ~1-2 minutes
        - MUSE: ~2 minutes (slow for MUSE - use PCA+AUROC instead)
    """
    from automar.core.models.evaluation import prob_predictor, eval_auroc

    # Ensure model is in evaluation mode
    if hasattr(model, "eval"):
        model.eval()

    # 1. Compute baseline AUROC
    baseline_probs = prob_predictor(model, val_loader_or_dict, set_type, device)

    # 2. Extract data and ensure CPU for AUROC computation
    if isinstance(val_loader_or_dict, DataLoader):
        # Neural network path
        X_all = val_loader_or_dict.dataset.tensors[0].cpu().numpy()
        y_all = val_loader_or_dict.dataset.tensors[1].cpu().numpy()
        is_neural_net = True

        # Create CPU-only loader for baseline AUROC
        baseline_probs_cpu = (
            baseline_probs.cpu()
            if isinstance(baseline_probs, torch.Tensor)
            else baseline_probs
        )
        cpu_baseline_dataset = TensorDataset(
            torch.FloatTensor(X_all).cpu(), torch.FloatTensor(y_all).cpu()
        )
        cpu_baseline_loader = DataLoader(
            cpu_baseline_dataset,
            batch_size=val_loader_or_dict.batch_size,
            shuffle=False,
        )
        baseline_auroc = eval_auroc(baseline_probs_cpu, cpu_baseline_loader)
        if isinstance(baseline_auroc, torch.Tensor):
            baseline_auroc = baseline_auroc.item()
    else:
        # MUSE path
        X_all = val_loader_or_dict["X"][set_type]
        y_all = val_loader_or_dict["Y"][set_type]
        is_neural_net = False

        # Compute baseline AUROC for MUSE
        baseline_auroc = eval_auroc(baseline_probs, val_loader_or_dict, set_type)
        if isinstance(baseline_auroc, torch.Tensor):
            baseline_auroc = baseline_auroc.item()

    n_features = X_all.shape[-1]  # Last dimension is features
    feature_importances = {}

    # 3. For each feature, permute and measure AUROC drop
    for feat_idx in range(n_features):
        auroc_drops = []

        for repeat in range(n_repeats):
            # Create permuted copy
            X_permuted = X_all.copy()

            # Permute this feature across all samples
            if len(X_permuted.shape) == 3:  # Neural net: (batch, seq_len, features)
                perm_indices = np.random.permutation(X_permuted.shape[0])
                X_permuted[:, :, feat_idx] = X_permuted[perm_indices, :, feat_idx]
            else:  # MUSE: (batch, features)
                perm_indices = np.random.permutation(X_permuted.shape[0])
                X_permuted[:, feat_idx] = X_permuted[perm_indices, feat_idx]

            # Compute AUROC with permuted feature
            if is_neural_net:
                permuted_dataset = TensorDataset(
                    torch.FloatTensor(X_permuted), torch.FloatTensor(y_all)
                )
                permuted_loader = DataLoader(
                    permuted_dataset,
                    batch_size=val_loader_or_dict.batch_size,
                    shuffle=False,
                )
                perm_probs = prob_predictor(model, permuted_loader, device=device)

                # Ensure both predictions and targets are on CPU for AUROC computation
                perm_probs_cpu = (
                    perm_probs.cpu()
                    if isinstance(perm_probs, torch.Tensor)
                    else perm_probs
                )
                y_cpu = torch.FloatTensor(y_all).cpu()

                # Create CPU-only loader for AUROC
                cpu_dataset = TensorDataset(torch.FloatTensor(X_permuted).cpu(), y_cpu)
                cpu_loader = DataLoader(
                    cpu_dataset, batch_size=val_loader_or_dict.batch_size, shuffle=False
                )

                perm_auroc = eval_auroc(perm_probs_cpu, cpu_loader)
                if isinstance(perm_auroc, torch.Tensor):
                    perm_auroc = perm_auroc.item()
            else:
                # MUSE
                perm_probs = model.predict_proba(X_permuted)[:, 1]
                perm_auroc = roc_auc_score(y_all, perm_probs)

            # Measure drop (positive = feature is important)
            auroc_drop = max(0, baseline_auroc - perm_auroc)
            auroc_drops.append(float(auroc_drop))

        # Average across repeats
        feature_importances[feat_idx] = np.mean(auroc_drops)

    # 4. Normalize to sum to 1.0
    total_importance = sum(feature_importances.values())
    if total_importance > 0:
        feature_importances = {
            k: v / total_importance for k, v in feature_importances.items()
        }

    return feature_importances


def compute_gradient_importance(model, val_loader, device):
    """
    Compute feature importance using input gradients (Integrated Gradients style).

    FAST method for neural networks - measures sensitivity of predictions to inputs.

    Args:
        model: Trained GRU/Transformer
        val_loader: Validation DataLoader
        device: 'cuda' or 'cpu'

    Returns:
        Dict mapping feature_idx -> importance score

    Time complexity: ~3 seconds (GPU), ~8 seconds (CPU)

    Note: Can underestimate importance when gradients saturate (sigmoid near 0/1).
          Use ensemble with permutation for robustness.
    """
    model.eval()
    gradient_magnitudes = None
    n_batches = 0

    for X, y in val_loader:
        X = X.to(device).float()
        X.requires_grad = True

        # Forward pass
        output = model(X)
        probs = torch.sigmoid(output)

        # Compute gradients w.r.t. input
        grad_outputs = torch.ones_like(probs)
        grads = torch.autograd.grad(
            outputs=probs,
            inputs=X,
            grad_outputs=grad_outputs,
            create_graph=False,
            retain_graph=False,
        )[0]

        # Attribution: |gradient| × |input| (Integrated Gradients approximation)
        attributions = (grads * X).abs()

        # Average across batch and sequence
        if len(attributions.shape) == 3:  # (batch, seq_len, features)
            attributions = attributions.mean(dim=(0, 1))
        else:
            attributions = attributions.mean(dim=0)

        if gradient_magnitudes is None:
            gradient_magnitudes = attributions.detach().cpu().numpy()
        else:
            gradient_magnitudes += attributions.detach().cpu().numpy()

        n_batches += 1

    # Average across batches
    gradient_magnitudes /= n_batches

    # Normalize to sum to 1.0
    gradient_magnitudes = gradient_magnitudes / gradient_magnitudes.sum()

    # Convert to dictionary
    return {i: float(gradient_magnitudes[i]) for i in range(len(gradient_magnitudes))}


def compute_pca_auroc_hybrid(
    pca, feature_names, explained_variance_ratio, data_df, labels
):
    """
    Hybrid method: Combine PCA loadings (variance) with AUROC (prediction).

    FAST and MODEL-AGNOSTIC method. Works for all model types.

    Args:
        pca: Fitted sklearn PCA object
        feature_names: List of feature names
        explained_variance_ratio: pca.explained_variance_ratio_
        data_df: DataFrame with features (no Labels column)
        labels: Binary target (0/1)

    Returns:
        Dict mapping feature_name -> importance score

    Time complexity: ~2 seconds (instant, already computed during training)

    Best for: WEASEL-MUSE or rapid prototyping
    """
    # 1. PCA-based importance (variance)
    pca_importance = _compute_pca_importance(
        pca, feature_names, explained_variance_ratio
    )

    # 2. AUROC-based importance (predictive power)
    auroc_importance = _compute_auroc_importance(data_df, labels)

    # 3. Combine: Multiply (features need BOTH variance AND prediction power)
    combined_importance = {}
    for feat in feature_names:
        pca_score = pca_importance.get(feat, 0.0)
        auroc_score = auroc_importance.get(feat, 0.5)

        # Geometric mean
        combined_importance[feat] = (pca_score * auroc_score) ** 0.5

    # 4. Normalize
    total = sum(combined_importance.values())
    if total > 0:
        combined_importance = {k: v / total for k, v in combined_importance.items()}

    return combined_importance


def _compute_pca_importance(pca, feature_names, explained_variance_ratio):
    """Extract importance from PCA component loadings."""
    components = pca.components_
    n_components = components.shape[0]
    n_features = len(feature_names)

    feature_importance = np.zeros(n_features)

    for pc_idx in range(n_components):
        variance_weight = explained_variance_ratio[pc_idx]
        loadings = np.abs(components[pc_idx, :])
        feature_importance += loadings * variance_weight

    # Normalize
    total_importance = feature_importance.sum()

    if total_importance > 0:
        feature_importance = feature_importance / total_importance
    else:
        # Fallback to uniform weights if total is zero
        feature_importance = np.ones(n_features) / n_features

    return {feature_names[i]: float(feature_importance[i]) for i in range(n_features)}


def _compute_auroc_importance(data_df, labels):
    """Compute univariate AUROC for each feature."""
    feature_aurocs = {}

    # Ensure labels is a clean 1D numpy array
    if hasattr(labels, "values"):
        labels = labels.values
    labels = np.asarray(labels).flatten()

    for col in data_df.columns:
        try:
            feature_values = data_df[col].values
            valid_mask = np.isfinite(feature_values) & np.isfinite(labels)

            # Convert to scalar for comparison
            n_valid = int(valid_mask.sum())
            if n_valid < 10:
                feature_aurocs[col] = 0.5
                continue

            auroc = roc_auc_score(labels[valid_mask], feature_values[valid_mask])

            # AUROC is symmetric around 0.5
            feature_aurocs[col] = abs(auroc - 0.5) + 0.5

        except Exception as e:
            print(f"Warning: AUROC computation failed for feature '{col}': {e}")
            feature_aurocs[col] = 0.5

    return feature_aurocs


def compute_ensemble_importance(model, val_loader, device):
    """
    RECOMMENDED: Ensemble permutation (70%) + gradient (30%).

    Combines robustness of permutation with speed/local-sensitivity of gradient.

    Args:
        model: Trained GRU/Transformer
        val_loader: Validation DataLoader
        device: 'cuda' or 'cpu'

    Returns:
        Dict mapping feature_idx -> importance score

    Time complexity: ~13 seconds (GPU), ~1.5 minutes (CPU)

    Best for: Production neural network models
    """
    # Ensure model is in evaluation mode
    model.eval()

    # Compute both methods
    perm_importance = compute_permutation_importance_auroc(
        model, val_loader, device, n_repeats=5
    )
    grad_importance = compute_gradient_importance(model, val_loader, device)

    # Ensemble: 70% permutation (more reliable), 30% gradient (local info)
    ensemble = {}
    for feat_idx in perm_importance.keys():
        ensemble[feat_idx] = (
            0.7 * perm_importance[feat_idx] + 0.3 * grad_importance[feat_idx]
        )

    # Re-normalize
    total = sum(ensemble.values())
    if total > 0:
        ensemble = {k: v / total for k, v in ensemble.items()}

    return ensemble


def adjust_importance_for_feature_groups(feature_importances, feature_names):
    """
    Address feature correlation by redistributing importance within correlated groups.

    Problem: Correlated features (MA1, MA2, MA3, MA4) may individually show low
    importance, but as a GROUP are critical. This happens because permuting any
    single MA leaves the others intact, so model can still predict well.

    Solution: Identify feature groups and boost their individual scores proportionally
    to the group's total importance.

    Args:
        feature_importances: Dict mapping feature_idx -> importance score
        feature_names: List of feature names

    Returns:
        Dict mapping feature_idx -> adjusted importance score

    Example:
        Before: MA1=0.02, MA2=0.02, MA3=0.02, MA4=0.02 (total=0.08, seems low)
        After:  MA1=0.04, MA2=0.04, MA3=0.04, MA4=0.04 (total=0.16, recognizes group)
    """
    # Define feature groups (correlated features)
    feature_groups = {
        "moving_averages": ["ma1", "ma2", "ma3", "ma4"],
        "rsi": ["rsi1", "rsi2"],
        "williams": ["wr1", "wr2"],
        "cci": ["cci1", "cci2"],
        "macd": ["diff", "dea", "macd"],
        "stochastic": ["k", "d"],
        "ohlc": ["open", "high", "low", "close"],
    }

    # Convert feature_names to lowercase map
    name_to_idx = {name.lower(): idx for idx, name in enumerate(feature_names)}

    adjusted_importances = feature_importances.copy()

    for group_name, group_features in feature_groups.items():
        # Find indices of features in this group
        group_indices = []
        for feat_name in group_features:
            if feat_name in name_to_idx:
                group_indices.append(name_to_idx[feat_name])

        if len(group_indices) <= 1:
            continue  # No correlation issue with single feature

        # Calculate total group importance
        group_total = sum(feature_importances.get(idx, 0.0) for idx in group_indices)

        # If group shows collective importance, boost individual members
        # Threshold: If group_total > 2x average per-feature importance
        avg_importance = sum(feature_importances.values()) / len(feature_importances)
        group_threshold = 2.0 * avg_importance * len(group_indices)

        if group_total > group_threshold:
            # Boost factor: 1.5x (conservative to avoid over-weighting)
            boost_factor = 1.5
            for idx in group_indices:
                adjusted_importances[idx] = feature_importances[idx] * boost_factor

    # Re-normalize to sum to 1.0
    total = sum(adjusted_importances.values())
    if total > 0:
        adjusted_importances = {k: v / total for k, v in adjusted_importances.items()}

    return adjusted_importances


def compute_cv_averaged_importance(train_fn, cv_loaders, feature_names, cfg, device):
    """
    Compute feature importance averaged across cross-validation folds.

    This provides more robust importance estimates and reduces overfitting risk.

    Args:
        train_fn: Training function
        cv_loaders: List of (train, val, test) loader tuples from CV
        feature_names: List of feature names
        cfg: Configuration
        device: 'cuda' or 'cpu'

    Returns:
        Dict mapping feature_idx -> averaged importance score
    """
    fold_importances = []

    for fold_idx, (train_loader, val_loader, test_loader) in enumerate(cv_loaders):
        print(f"Computing importance for fold {fold_idx + 1}/{len(cv_loaders)}...")

        # Train model on this fold
        trained_model = train_fn(
            cfg,
            train_loader=train_loader,
            val_loader=val_loader,
            tuning=False,
        )["model"]

        # Compute importance on the HELD-OUT test set (not validation!)
        # This ensures importance is computed on data the model hasn't seen
        fold_importance = compute_ensemble_importance(
            trained_model, test_loader, device
        )

        fold_importances.append(fold_importance)

    # Average importance across folds
    averaged_importance = {}
    n_features = len(fold_importances[0])

    for feat_idx in range(n_features):
        scores = [fold[feat_idx] for fold in fold_importances]
        averaged_importance[feat_idx] = sum(scores) / len(scores)

    # Re-normalize (shouldn't be needed, but safe)
    total = sum(averaged_importance.values())
    if total > 0:
        averaged_importance = {k: v / total for k, v in averaged_importance.items()}

    # Adjust for feature correlation groups
    adjusted_importance = adjust_importance_for_feature_groups(
        averaged_importance, feature_names
    )

    return adjusted_importance
