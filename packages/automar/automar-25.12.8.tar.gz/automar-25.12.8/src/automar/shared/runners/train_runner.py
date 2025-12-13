# -*- coding: utf-8 -*-
"""
Model training runner for Automar

Handles training of neural network and logistic regression models
"""

from pathlib import Path
from automar.shared.services.device_utils import _available_device_types


def _count_feature_columns(df):
    """Return number of feature columns, excluding target label if present."""
    if df is None:
        return 0
    return len([col for col in df.columns if col != "Labels"])


def run_training(cfg, progress_callback=None):
    """
    Train a machine learning model

    Args:
        cfg: Configuration object with training parameters
        progress_callback: Optional callback for progress updates (for API)

    Returns:
        Tuple of (model_path, training_results)
    """
    import tomli
    from automar.shared.services.tuning_service import prepare_loaders
    from automar.core.preprocessing.extractor import df_industry_split, df_industry_avg
    from automar.shared.core.common import build_final_df
    from automar.shared.persistence.library import read_df, date_ender

    # Lazy-load device if not set (avoids PyTorch import at API startup)
    if cfg.loader.device is None:
        cfg.loader.device = _available_device_types()[0]

    from automar.shared.config.path_resolver import get_project_root

    project_root = get_project_root()

    base_feature_count = None

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

    # Generate hyperparameter filename based on whether PCA is used
    # Include sector in filename only if PCA is active (sector data is used)
    if tick_name and (cfg.loader.dopca or cfg.train.pca_path):
        # PCA active: ticker + sector PCA components
        file_name = f"{ind_name}({tick_name})_{cfg.tune.model}_hyperparameters_{cfg.train.id}.toml"
    elif tick_name:
        # No PCA: ticker data only
        file_name = f"{tick_name}_{cfg.tune.model}_hyperparameters_{cfg.train.id}.toml"
    else:
        # Sector-level (no ticker)
        file_name = f"{ind_name}_{cfg.tune.model}_hyperparameters_{cfg.train.id}.toml"

    if cfg.train.manual_hyperparams_toml:
        import tomllib

        ray_results = tomllib.loads(cfg.train.manual_hyperparams_toml)
        # Set epochs for neural network models (GRU, transformer) only - log-reg doesn't use epochs
        if cfg.tune.model.lower() in ["gru", "transformer"]:
            ray_results["epochs"] = cfg.tune.epochs
    else:
        # Include model-specific subdirectory (same as tuning)
        model_subdir = cfg.tune.model.lower()
        if model_subdir == "log-reg":
            model_subdir = "logreg"
        cfg_path = cfg.train.cfg_path or (
            project_root / cfg.tune.param_path / model_subdir / file_name
        )

        if cfg_path.exists():
            with open(cfg_path, "rb") as ff:
                ray_results = tomli.load(ff)
                # Set epochs for neural network models (GRU, transformer) only - log-reg doesn't use epochs
                if cfg.tune.model.lower() in ["gru", "transformer"]:
                    ray_results["epochs"] = cfg.tune.epochs
        else:
            print(
                "Please, define training values for this model or run 'tune' to generate them via hyperparameter tuning."
            )
            exit(0)

    if cfg.train.mdl_path is None:
        # Use custom save_dir if provided (absolute or relative to base), otherwise use "out/models/{model}"
        if cfg.train.save_dir:
            models_path = Path(cfg.train.save_dir)
            if not models_path.is_absolute():
                models_path = project_root / models_path
        else:
            model_subdir = cfg.tune.model.lower()
            if model_subdir == "log-reg":
                model_subdir = "logreg"
            models_path = project_root / "out" / "models" / model_subdir
        models_path.mkdir(exist_ok=True, parents=True)
        id = 1
        # Generate model filename based on whether PCA is used
        # Include sector in filename only if PCA is active (sector data is used)
        if tick_name and (cfg.loader.dopca or cfg.train.pca_path):
            # PCA active: ticker + sector PCA components
            out_name = f"{cfg.tune.model}_{ind_name}({tick_name})_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pth"
        elif tick_name:
            # No PCA: ticker data only
            out_name = f"{cfg.tune.model}_{tick_name}_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pth"
        else:
            # Sector-level (no ticker)
            out_name = f"{cfg.tune.model}_{ind_name}_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pth"

        while Path(models_path / out_name).exists():
            id += 1
            if tick_name and (cfg.loader.dopca or cfg.train.pca_path):
                out_name = f"{cfg.tune.model}_{ind_name}({tick_name})_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pth"
            elif tick_name:
                out_name = f"{cfg.tune.model}_{tick_name}_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pth"
            else:
                out_name = f"{cfg.tune.model}_{ind_name}_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pth"
        mdl_path = models_path / out_name
    else:
        mdl_path = cfg.train.mdl_path

    if tick_name:
        tick_df, ind_df = df_industry_split(new_df, industry=ind_name, ticker=tick_name)
        ind_mean = df_industry_avg(ind_df)
        tick_df = tick_df.drop(["Company", "Industry"], axis=1)
        tick_df = tick_df.set_index("Date")
        base_feature_count = _count_feature_columns(tick_df)
    else:
        ind_mean_w_labels = df_industry_avg(new_df, 0)
        ind_mean_w_labels.Labels = ind_mean_w_labels.Labels.round()
        base_feature_count = _count_feature_columns(ind_mean_w_labels)

    if cfg.train.pca_path:
        from automar.shared.services.pca_service import load_pca, build_pca_df
        from warnings import warn

        pca0 = load_pca(cfg.train.pca_path)
        cfg.loader.dopca = False

        if tick_name:
            _, pca_df = build_pca_df(pca0, ind_df)
            tick_df = tick_df.join(pca_df, on="Date")
            actual_input_dim = tick_df.shape[1] - 1
        else:
            _, pca_df = build_pca_df(pca0, new_df[new_df["Industry"] == ind_name])
            ind_mean_w_labels = ind_mean_w_labels.join(pca_df, on="Date")
            actual_input_dim = ind_mean_w_labels.shape[1] - 1

        # Override input_dim in ray_results and warn user
        if cfg.tune.model in ["GRU", "transformer"]:
            if ray_results["model"]["input_dim"] != actual_input_dim:
                warn(
                    f"Overriding input_dim from hyperparameter config ({ray_results['model']['input_dim']}) "
                    f"with actual input dimension ({actual_input_dim}) due to loaded PCA transformation.",
                    UserWarning,
                )
            ray_results["model"]["input_dim"] = actual_input_dim

    if cfg.tune.model.lower() in ["gru", "transformer"]:
        from automar.shared.services.training_service import train_nn_model

        # Prepare loaders for neural networks
        if tick_name:
            full_loaders = prepare_loaders(cfg, tick_df, avg_df=ind_mean)
        else:
            full_loaders = prepare_loaders(cfg, ind_mean_w_labels)
        train_loader_seq, val_loader_seq, test_loader_seq = full_loaders

        # Train the neural network model
        training_results = train_nn_model(
            cfg,
            ray_results,
            train_loader_seq,
            val_loader_seq,
            test_loader_seq,
            progress_callback=progress_callback,
        )
        model_trained, model_avg_losses, model_val_auroc, model_val_lr = (
            training_results.values()
        )
    elif cfg.tune.model.lower() == "log-reg":
        from automar.core.preprocessing.loaders import vecs_to_dict
        from automar.shared.services.training_service import train_logreg_model

        # Prepare logistic regression data
        if tick_name:
            seq_vecs, pca_obj = prepare_loaders(
                cfg, tick_df, avg_df=ind_mean, mode="reg"
            )
        else:
            seq_vecs, pca_obj = prepare_loaders(cfg, ind_mean_w_labels, mode="reg")
        log_reg_data = vecs_to_dict(seq_vecs, pca=pca_obj)

        # Train the logistic regression model
        training_results = train_logreg_model(ray_results, log_reg_data)

    from torch import save as torch_save

    # Create parent directory if it doesn't exist
    if mdl_path.parent and str(mdl_path.parent) != ".":
        mdl_path.parent.mkdir(parents=True, exist_ok=True)

    # Compute synthesis statistics for multi-day forecasting
    from automar.core.models.forecast import compute_synthesis_statistics

    # Use the appropriate dataframe based on training mode
    if tick_name:
        synthesis_df = tick_df.copy()
        # Add Labels column back if it's not there (it was removed when setting Date as index)
        if "Labels" not in synthesis_df.columns and hasattr(tick_df, "index"):
            # Labels are part of the dataframe used for training
            synthesis_df = tick_df.reset_index()
    else:
        synthesis_df = ind_mean_w_labels.copy()

    try:
        synthesis_stats = compute_synthesis_statistics(synthesis_df)
    except Exception as e:
        # Fallback to None if synthesis stats computation fails
        print(f"Warning: Could not compute synthesis statistics: {e}")
        synthesis_stats = None

    # Compute test metrics to cache in checkpoint (avoids recomputation in visualizations)
    test_metrics = None
    if cfg.tune.model.lower() in ["gru", "transformer"]:
        try:
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

            # Compute predictions on test set
            prob_preds = prob_predictor(
                model_trained, test_loader_seq, device=cfg.loader.device
            )
            threshold = eval_roc_thresh(prob_preds, test_loader_seq)

            # Compute all metrics
            con_mat = confu_matrix(prob_preds, test_loader_seq, threshold)
            accuracy = pred_accuracy(prob_preds, test_loader_seq, threshold)
            precision = pred_precision(prob_preds, test_loader_seq, threshold)
            recall = pred_recall(prob_preds, test_loader_seq, threshold)
            fscore = pred_Fscore(prob_preds, test_loader_seq, threshold)
            auroc = eval_auroc(prob_preds, test_loader_seq)

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

            # Store metrics in format expected by visualization
            test_metrics = {
                "confusion_matrix": (
                    con_mat.tolist()
                    if hasattr(con_mat, "tolist")
                    else [[int(x) for x in row] for row in con_mat]
                ),
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "fscore": float(fscore),
                "auroc": float(auroc),
                "threshold": float(threshold),
            }
        except Exception as e:
            # If test metrics computation fails, continue without them (visualization will fall back to recomputation)
            print(f"Warning: Could not compute test metrics: {e}")
            test_metrics = None
    elif cfg.tune.model.lower() == "log-reg":
        # Compute test metrics for logistic regression
        try:
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

            # Compute predictions on test set
            prob_preds = prob_predictor(training_results["model"], log_reg_data, "test")
            threshold = eval_roc_thresh(prob_preds, log_reg_data, "test")

            # Compute all metrics
            con_mat = confu_matrix(prob_preds, log_reg_data, threshold, "test")
            accuracy = pred_accuracy(prob_preds, log_reg_data, threshold, "test")
            precision = pred_precision(prob_preds, log_reg_data, threshold, "test")
            recall = pred_recall(prob_preds, log_reg_data, threshold, "test")
            fscore = pred_Fscore(prob_preds, log_reg_data, threshold, "test")
            auroc = eval_auroc(prob_preds, log_reg_data, "test")

            # Store metrics in format expected by visualization
            test_metrics = {
                "confusion_matrix": (
                    con_mat.tolist()
                    if hasattr(con_mat, "tolist")
                    else [[int(x) for x in row] for row in con_mat]
                ),
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "fscore": float(fscore),
                "auroc": float(auroc),
                "threshold": float(threshold),
            }
        except Exception as e:
            # If test metrics computation fails, continue without them (visualization will fall back to recomputation)
            print(f"Warning: Could not compute test metrics for log-reg: {e}")
            test_metrics = None

    # Compute feature importance for synthesis weighting
    feature_names = None
    feature_importances = None

    if cfg.tune.model.lower() in ["gru", "transformer"]:
        try:
            from automar.core.models.feature_importance import (
                compute_permutation_importance_auroc,
                adjust_importance_for_feature_groups,
            )

            # Get feature names from the ACTUAL input tensor (includes PCA components if applicable)
            # This ensures feature_names matches the model's actual input dimension
            actual_n_features = val_loader_seq.dataset.tensors[0].shape[
                2
            ]  # (batch, seq, features)

            # Start with base feature names (before PCA)
            if tick_name:
                base_feature_names = [col for col in tick_df.columns if col != "Labels"]
            else:
                base_feature_names = [
                    col for col in ind_mean_w_labels.columns if col != "Labels"
                ]

            # Check if PCA components were added
            if actual_n_features > len(base_feature_names):
                # PCA was applied - add Industry component names
                n_pca_components = actual_n_features - len(base_feature_names)
                feature_names = base_feature_names + [
                    f"Industry{i+1}" for i in range(n_pca_components)
                ]
                print(
                    f"Detected PCA: {len(base_feature_names)} base features + {n_pca_components} PCA components = {actual_n_features} total"
                )
            elif actual_n_features == len(base_feature_names):
                # No PCA - use base names directly
                feature_names = base_feature_names
                print(f"No PCA detected: {actual_n_features} features")
            else:
                # This shouldn't happen - fall back to base names
                print(
                    f"Warning: Loader has fewer features ({actual_n_features}) than base dataframe ({len(base_feature_names)}). Using first {actual_n_features} feature names."
                )
                feature_names = base_feature_names[:actual_n_features]

            print("Computing feature importance (permutation method)...")
            # Use permutation-only importance (ensemble has issues with CuDNN RNN gradients in eval mode)
            raw_importance = compute_permutation_importance_auroc(
                model_trained, val_loader_seq, device=cfg.loader.device, n_repeats=5
            )

            print("Adjusting importance for feature correlation groups...")
            feature_importances = adjust_importance_for_feature_groups(
                raw_importance, feature_names
            )

            print(f"✓ Feature importance computed for {len(feature_names)} features")
        except Exception as e:
            # If importance computation fails, continue without it (forecasts will use uniform weighting)
            print(f"Warning: Could not compute feature importance: {e}")
            feature_names = None
            feature_importances = None

    elif cfg.tune.model.lower() == "log-reg":
        try:
            from automar.core.models.feature_importance import (
                compute_pca_auroc_hybrid,
                adjust_importance_for_feature_groups,
            )

            # Get feature names from dataframe
            if tick_name:
                feature_names = [col for col in tick_df.columns if col != "Labels"]
                data_for_importance = tick_df.drop(columns=["Labels"], errors="ignore")
                labels_for_importance = tick_df["Labels"].values
            else:
                feature_names = [
                    col for col in ind_mean_w_labels.columns if col != "Labels"
                ]
                data_for_importance = ind_mean_w_labels.drop(
                    columns=["Labels"], errors="ignore"
                )
                labels_for_importance = ind_mean_w_labels["Labels"].values

            # Check if we have PCA object from training
            has_pca = "pca" in log_reg_data

            if has_pca and log_reg_data["pca"] is not None:
                pca_obj = log_reg_data["pca"]
                if hasattr(pca_obj, "components_"):
                    print("Computing feature importance (PCA+AUROC hybrid method)...")
                    name_importance = compute_pca_auroc_hybrid(
                        pca_obj,
                        feature_names,
                        pca_obj.explained_variance_ratio_,
                        data_for_importance,
                        labels_for_importance,
                    )

                    # Convert to feature_idx -> score format
                    raw_importance = {
                        i: name_importance.get(name, 1.0 / len(feature_names))
                        for i, name in enumerate(feature_names)
                    }

                    # Adjust for feature correlation groups
                    print("Adjusting importance for feature correlation groups...")
                    feature_importances = adjust_importance_for_feature_groups(
                        raw_importance, feature_names
                    )

                    print(
                        f"✓ Feature importance computed for {len(feature_names)} features"
                    )
                else:
                    print(
                        "Warning: PCA object not available for log-reg importance computation"
                    )
                    feature_names = None
                    feature_importances = None
            else:
                print(
                    "Warning: PCA object not available for log-reg importance computation"
                )
                feature_names = None
                feature_importances = None

        except Exception as e:
            # If importance computation fails, continue without it
            print(f"Warning: Could not compute feature importance for log-reg: {e}")
            feature_names = None
            feature_importances = None

    # For neural networks, add training history to checkpoint
    if cfg.tune.model.lower() in ["gru", "transformer"]:
        epochs_list = list(range(1, len(model_avg_losses) + 1))
        total_input_dim = ray_results["model"].get("input_dim")
        if total_input_dim is not None and base_feature_count is not None:
            pca_component_count = max(0, total_input_dim - base_feature_count)
        else:
            pca_component_count = None

        checkpoint = {
            "model_state_dict": model_trained.state_dict(),
            "training_history": {
                "epochs": epochs_list,
                "train_loss": model_avg_losses,
                "val_auroc": model_val_auroc,
                "val_lr": model_val_lr,
            },
            "model_type": cfg.tune.model,
            "hyperparameters": ray_results,
            "loader_config": {
                "dopca": cfg.loader.dopca,
                "tsize": cfg.loader.tsize,
                "scaler": cfg.loader.scaler,
            },
            "training_context": {
                "ticker": tick_name,  # None for industry-level, ticker symbol for company-specific
                "industry": ind_name,
            },
            "synthesis_stats": synthesis_stats,  # For multi-day forecasting
            "test_metrics": test_metrics,  # Cache test metrics for instant visualization
            "feature_metadata": {
                "base_feature_count": base_feature_count,
                "pca_component_count": pca_component_count,
                "total_input_dim": total_input_dim,
            },
            "feature_names": feature_names,  # For importance-weighted synthesis
            "feature_importances": feature_importances,  # For importance-weighted synthesis
        }
        torch_save(checkpoint, mdl_path)
    else:
        # For log-reg, save model with metadata for compatibility with model selector
        checkpoint = {
            "model": training_results["model"],
            "model_type": cfg.tune.model,
            "hyperparameters": ray_results,
            "training_context": {
                "ticker": tick_name,  # None for industry-level, ticker symbol for company-specific
                "industry": ind_name,
            },
            "synthesis_stats": synthesis_stats,  # For multi-day forecasting
            "test_metrics": test_metrics,  # Cache test metrics including optimal threshold
            "feature_names": feature_names,  # For importance-weighted synthesis
            "feature_importances": feature_importances,  # For importance-weighted synthesis
        }
        torch_save(checkpoint, mdl_path)

    print(f"Model stored as {mdl_path}")

    # Return both path and training results for API to access AUROC
    return str(mdl_path), (
        training_results if cfg.tune.model.lower() == "log-reg" else None
    )
