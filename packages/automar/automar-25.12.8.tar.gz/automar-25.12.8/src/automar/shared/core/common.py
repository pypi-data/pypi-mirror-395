"""
Common business logic shared between CLI (main.py) and API (api.py).

This module contains the core functionality for:
- Hyperparameter tuning
- Cross-validation
- Model training

The CLI and API layers handle only:
- CLI: argparse and command execution
- API: FastAPI endpoints and HTTP handling
"""

from pathlib import Path
from typing import Optional, Callable, Any
import tomli
import tomli_w
import pickle

from automar.core.preprocessing.extractor import df_industry_split, df_industry_avg
from automar.core.preprocessing.loaders import vecs_to_dict
from automar.core import models
from automar.shared.persistence.library import read_df


def build_final_df(cfg):
    """
    Build the final dataframe either by loading an existing dataset or extracting new data.

    Args:
        cfg: GlobalConfig object with extract and pca options

    Returns:
        tuple: (extract_df, ind_name) - The dataframe and industry name
    """
    from automar.shared.runners.extract_runner import run_extraction
    from automar.shared.persistence.library import (
        create_connection,
        load_df_from_sqlite,
        TABLE_NAME,
    )

    if cfg.pca.data_file:
        extract_df = read_df(cfg.pca.data_file)
        extract_df = extract_df.dropna(ignore_index=True)
    else:
        # Check if we should use an existing dataset instead of extracting new data
        if (
            hasattr(cfg, "pca")
            and hasattr(cfg.pca, "dataset_path")
            and cfg.pca.dataset_path
        ):
            dataset_path = Path(cfg.pca.dataset_path)

            # Check if this is a SQLite database
            if dataset_path.suffix.lower() in [".sqlite", ".sqlite3", ".db"]:
                # Load SQLite data with proper filtering
                conn = create_connection(dataset_path, mkfolder=False)
                try:
                    extract_df = load_df_from_sqlite(
                        TABLE_NAME,
                        conn,
                        comp_name=cfg.extract.ticker,
                        ind_name=cfg.extract.industry,
                        start_date=(
                            str(cfg.extract.datest) if cfg.extract.datest else None
                        ),
                        end_date=(
                            str(cfg.extract.datend) if cfg.extract.datend else None
                        ),
                        validate_continuity=True,  # Enable gap detection for non-Extract jobs
                    )
                except Exception as e:
                    conn.close()
                    # Re-raise with context about what operation was being performed
                    operation_context = (
                        f"loading data for {cfg.extract.industry or cfg.extract.ticker}"
                    )
                    raise ValueError(
                        f"Cannot complete {operation_context}: {str(e)}"
                    ) from e
                conn.close()
                extract_df = extract_df.dropna(ignore_index=True)
            else:
                # Regular file formats (feather, parquet, csv, etc.)
                extract_df = read_df(dataset_path)
                extract_df = extract_df.dropna(ignore_index=True)

            # Clean up if needed
            if "Unnamed: 0" in extract_df.columns:
                extract_df = extract_df.drop(["Unnamed: 0"], axis=1)
        else:
            # Extract new data (original behavior)
            extract_df = run_extraction(cfg.extract).dropna(ignore_index=True)

    if "Unnamed: 0" in extract_df.columns:
        extract_df = extract_df.drop(["Unnamed: 0"], axis=1)

    ind_name = extract_df["Industry"].value_counts().idxmax()

    return extract_df, ind_name


def run_tuning_common(cfg, progress_callback: Optional[Callable] = None):
    """
    Run hyperparameter tuning with optional progress callback.

    Args:
        cfg: GlobalConfig object
        progress_callback: Optional callback function for progress updates (for API)

    Returns:
        tuple: (results, config_file_path) - Ray results and path to saved config
    """
    # Lazy-load device if not set (avoids PyTorch import at API startup)
    if cfg.loader.device is None:
        from automar.shared.services.device_utils import _available_device_types

        cfg.loader.device = _available_device_types()[0]

    from automar.shared.services.tuning_service import gen_hpt_filename, prepare_loaders
    from automar.shared.services.file_utils import load_module_with_functions
    from automar.shared.config.path_resolver import get_project_root, resolve_path

    project_root = get_project_root()
    # Use custom output_dir if provided (absolute or relative to project root), otherwise use param_path
    if cfg.tune.output_dir:
        test_path = resolve_path(cfg.tune.output_dir, relative_to_project=True)
    else:
        # Use model-specific subdirectory
        model_subdir = cfg.tune.model.lower()  # gru, transformer, or log-reg -> logreg
        if model_subdir == "log-reg":
            model_subdir = "logreg"
        test_path = project_root / cfg.tune.param_path / model_subdir
    test_path.mkdir(exist_ok=True, parents=True)

    new_df, ind_name = build_final_df(cfg)
    tick_name = cfg.extract.ticker if cfg.extract.ticker else None

    if tick_name:
        tick_df, ind_df = df_industry_split(new_df, industry=ind_name, ticker=tick_name)
        ind_mean = df_industry_avg(ind_df)
        tick_df = tick_df.drop(["Company", "Industry"], axis=1)
        tick_df = tick_df.set_index("Date")
    else:
        ind_mean_w_labels = df_industry_avg(new_df, 0)
        ind_mean_w_labels.Labels = ind_mean_w_labels.Labels.round()

    # Load search space module (custom or default)
    if cfg.tune.search_space_path:
        # Use custom search space
        custom_path = resolve_path(cfg.tune.search_space_path, relative_to_project=True)
        module = load_module_with_functions(str(custom_path), ["get_search_space"])
    else:
        # Use default search space from hpt_defaults
        module = load_module_with_functions(
            gen_hpt_filename(cfg.tune.model.lower(), root_path=cfg.tune.tuning_path),
            ["get_search_space"],
        )

    ray_folder = project_root / "out" / "ray"
    ray_folder.mkdir(exist_ok=True, parents=True)

    if cfg.tune.model.lower() in ["gru", "transformer"]:
        from automar.shared.services.tuning_service import (
            GRU_super_tuner,
            transformer_super_tuner,
        )

        if tick_name:
            full_loaders = prepare_loaders(cfg, tick_df, avg_df=ind_mean)
        else:
            full_loaders = prepare_loaders(cfg, ind_mean_w_labels)
        train_loader_seq, val_loader_seq, test_loader_seq = full_loaders

        if cfg.tune.model.lower() == "gru":
            model = models.nn.GRUNet
            if progress_callback:
                results = _nn_super_tuner_with_callback(
                    module,
                    model,
                    cfg,
                    train_loader_seq,
                    val_loader_seq,
                    test_loader_seq,
                    ray_folder,
                    progress_callback,
                    model_name="GRU",
                )
            else:
                results = GRU_super_tuner(
                    module,
                    model,
                    cfg,
                    train_loader_seq,
                    val_loader_seq,
                    test_loader_seq,
                    ray_folder,
                )
        elif cfg.tune.model.lower() == "transformer":
            model = models.nn.Transnet
            if progress_callback:
                results = _nn_super_tuner_with_callback(
                    module,
                    model,
                    cfg,
                    train_loader_seq,
                    val_loader_seq,
                    test_loader_seq,
                    ray_folder,
                    progress_callback,
                    model_name="Transformer",
                )
            else:
                results = transformer_super_tuner(
                    module,
                    model,
                    cfg,
                    train_loader_seq,
                    val_loader_seq,
                    test_loader_seq,
                    ray_folder,
                )
    elif cfg.tune.model.lower() == "log-reg":
        from automar.shared.services.tuning_service import logreg_super_tuner

        if tick_name:
            seq_vecs, pca_obj = prepare_loaders(
                cfg, tick_df, avg_df=ind_mean, mode="reg"
            )
        else:
            seq_vecs, pca_obj = prepare_loaders(cfg, ind_mean_w_labels, mode="reg")
        log_reg_data = vecs_to_dict(seq_vecs, pca=pca_obj)

        # Pass callback to log-reg tuner for progress tracking
        results = logreg_super_tuner(
            module, log_reg_data, cfg, ray_dir=ray_folder, callback=progress_callback
        )

    # Generate output filename
    # Include sector in filename only if PCA is active (sector data is used)
    id = 1
    if tick_name and cfg.loader.dopca:
        # PCA active: ticker + sector PCA components
        out_name = f"{ind_name}({tick_name})_{cfg.tune.model}_hyperparameters_{id}.toml"
    elif tick_name:
        # No PCA: ticker data only
        out_name = f"{tick_name}_{cfg.tune.model}_hyperparameters_{id}.toml"
    else:
        # Sector-level (no ticker)
        out_name = f"{ind_name}_{cfg.tune.model}_hyperparameters_{id}.toml"

    while Path(test_path / out_name).exists():
        id += 1
        if tick_name and cfg.loader.dopca:
            out_name = (
                f"{ind_name}({tick_name})_{cfg.tune.model}_hyperparameters_{id}.toml"
            )
        elif tick_name:
            out_name = f"{tick_name}_{cfg.tune.model}_hyperparameters_{id}.toml"
        else:
            out_name = f"{ind_name}_{cfg.tune.model}_hyperparameters_{id}.toml"

    config_file_path = test_path / out_name
    with open(config_file_path, "wb") as ff:
        tomli_w.dump(results.config, ff)

    # Save tuning statistics for visualization
    if hasattr(results, "metrics_dataframe") and results.metrics_dataframe is not None:
        try:
            import json

            stats_file_path = config_file_path.with_suffix(".stats.json")
            df = results.metrics_dataframe

            # IMPORTANT: Ray Tune's metrics_dataframe is ALREADY in execution order
            # DO NOT SORT - that would mess up the chronological order
            # Each row corresponds to a trial in the order it was executed

            trial_numbers = list(range(1, len(df) + 1))

            stats_data = {
                "iterations": trial_numbers,
                "num_trials": len(df),
            }

            # Get AUROC if available (in execution order - as is)
            if "AUROC" in df.columns:
                auroc_list = df["AUROC"].tolist()
                stats_data["auroc"] = auroc_list
                stats_data["best_score"] = float(max(auroc_list))

                # Calculate AUROC_smooth (cumulative maximum)
                # This shows the best AUROC found so far at each iteration
                auroc_smooth = []
                max_so_far = 0
                for auroc in auroc_list:
                    max_so_far = max(max_so_far, auroc)
                    auroc_smooth.append(max_so_far)
                stats_data["auroc_smooth"] = auroc_smooth

            # Get top trials (sorted by AUROC)
            if "AUROC" in df.columns:
                # Sort by AUROC descending and get top 10
                top_10 = df.nlargest(10, "AUROC").copy()

                # Build trial info - match what's shown in the plot
                stats_data["top_trials"] = []
                for i, (idx, row) in enumerate(top_10.iterrows()):
                    trial_info = {
                        "rank": i + 1,  # 1st, 2nd, 3rd, etc.
                        "trial_id": str(idx),  # Trial ID from Ray Tune
                        "auroc": float(row.get("AUROC", 0)),
                    }

                    # Add training iteration if available
                    if "training_iteration" in df.columns:
                        trial_info["iteration"] = int(row.get("training_iteration", 0))

                    stats_data["top_trials"].append(trial_info)

            with open(stats_file_path, "w") as f:
                json.dump(stats_data, f, indent=2)

        except Exception as e:
            # Don't fail the whole tuning if stats saving fails
            print(f"Warning: Failed to save tuning statistics: {e}")

    return results, config_file_path


def run_crossvalidation_common(cfg, progress_callback: Optional[Callable] = None):
    """
    Run cross-validation with optional progress callback.

    Args:
        cfg: GlobalConfig object
        progress_callback: Optional callback function for progress updates (for API)

    Returns:
        tuple: (crossval_results, out_path) - Cross-validation results and output path
    """
    # Lazy-load device if not set (avoids PyTorch import at API startup)
    if cfg.loader.device is None:
        from automar.shared.services.device_utils import _available_device_types

        cfg.loader.device = _available_device_types()[0]

    from automar.shared.services.tuning_service import SCALERS
    from automar.core.preprocessing.tensor import (
        growing_windows,
        growing_windows_no_pca,
    )
    from automar.shared.persistence.library import date_ender

    if cfg.crossvalidate.n_split == 1:
        raise ValueError("Please increase the number of 'n_split'")

    from automar.shared.config.path_resolver import get_project_root, resolve_path

    project_root = get_project_root()

    new_df, ind_name = build_final_df(cfg)
    tick_name = cfg.extract.ticker if cfg.extract.ticker else None

    if tick_name:
        tick_df, ind_df = df_industry_split(new_df, industry=ind_name, ticker=tick_name)
        ind_mean = df_industry_avg(ind_df)
        tick_df = tick_df.drop(["Company", "Industry"], axis=1)
        tick_df = tick_df.set_index("Date")
    else:
        ind_mean_w_labels = df_industry_avg(new_df, 0)
        ind_mean_w_labels.Labels = ind_mean_w_labels.Labels.round()

    scaler = SCALERS[cfg.loader.scaler]()

    # Generate hyperparameter filename based on whether PCA is used
    # Include sector in filename only if PCA is active (sector data is used)
    if tick_name and cfg.loader.dopca:
        # PCA active: ticker + sector PCA components
        file_name = f"{ind_name}({tick_name})_{cfg.tune.model}_hyperparameters_{cfg.train.id}.toml"
    elif tick_name:
        # No PCA: ticker data only
        file_name = f"{tick_name}_{cfg.tune.model}_hyperparameters_{cfg.train.id}.toml"
    else:
        # Sector-level (no ticker)
        file_name = f"{ind_name}_{cfg.tune.model}_hyperparameters_{cfg.train.id}.toml"

    # Check if manual TOML is provided
    if cfg.crossvalidate.manual_hyperparams_toml:
        # Use manual TOML directly
        import tomllib

        ray_results = tomllib.loads(cfg.crossvalidate.manual_hyperparams_toml)
        # Set epochs for neural network models (GRU, transformer) only - log-reg doesn't use epochs
        if cfg.tune.model.lower() in ["gru", "transformer"]:
            ray_results["epochs"] = cfg.tune.epochs
    else:
        # Determine config path
        # Check both train.cfg_path and tune.tuning_path (frontend sends to tune.tuning_path)
        if cfg.train.cfg_path is not None:
            cfg_path = Path(cfg.train.cfg_path)
        elif hasattr(cfg.tune, "tuning_path") and cfg.tune.tuning_path is not None:
            cfg_path = Path(cfg.tune.tuning_path)
        else:
            # Include model-specific subdirectory (same as tuning)
            model_subdir = cfg.tune.model.lower()
            if model_subdir == "log-reg":
                model_subdir = "logreg"
            cfg_path = project_root / cfg.tune.param_path / model_subdir / file_name

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
            raise FileNotFoundError(f"Configuration file not found: {cfg_path}")

    if cfg.crossvalidate.out_path is None:
        # Use custom results_dir if provided (absolute or relative to project root), otherwise use "out/cross"
        if cfg.crossvalidate.results_dir:
            models_path = resolve_path(
                cfg.crossvalidate.results_dir, relative_to_project=True
            )
        else:
            # Use model-specific subdirectory
            model_subdir = cfg.tune.model.lower()
            if model_subdir == "log-reg":
                model_subdir = "logreg"
            models_path = project_root / "out" / "cross" / model_subdir
        models_path.mkdir(exist_ok=True, parents=True)
        id = 1
        # Generate cross-validation output filename based on whether PCA is used
        # Include sector in filename only if PCA is active (sector data is used)
        if tick_name and cfg.loader.dopca:
            # PCA active: ticker + sector PCA components
            out_name = f"val_{cfg.tune.model}_{ind_name}({tick_name})_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pkl"
        elif tick_name:
            # No PCA: ticker data only
            out_name = f"val_{cfg.tune.model}_{tick_name}_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pkl"
        else:
            # Sector-level (no ticker)
            out_name = f"val_{cfg.tune.model}_{ind_name}_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pkl"

        while Path(models_path / out_name).exists():
            id += 1
            if tick_name and cfg.loader.dopca:
                out_name = f"val_{cfg.tune.model}_{ind_name}({tick_name})_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pkl"
            elif tick_name:
                out_name = f"val_{cfg.tune.model}_{tick_name}_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pkl"
            else:
                out_name = f"val_{cfg.tune.model}_{ind_name}_{date_ender(cfg.extract.datend)}_{cfg.train.id}_{id}.pkl"
        out_path = models_path / out_name
    else:
        out_path = cfg.crossvalidate.out_path

    if cfg.loader.dopca:
        if tick_name:
            # For neural networks, calculate num_pc from model input_dim
            # For log-reg, PCA will be determined automatically by growing_windows
            if cfg.tune.model.lower() in ["gru", "transformer"]:
                num_pc = ray_results["model"]["input_dim"] - len(ind_mean.columns)
                gw_vecs, lengths = growing_windows(
                    tick_df,
                    n_split=cfg.crossvalidate.n_split,
                    sc=scaler,
                    test_size=cfg.loader.test_size,
                    val_size=cfg.loader.val_size,
                    df_pca=ind_mean,
                    def_comp=num_pc,
                    cutoff_var=cfg.pca.alpha,
                )
            else:  # log-reg
                # For log-reg, let growing_windows determine PCA components automatically
                gw_vecs, lengths = growing_windows(
                    tick_df,
                    n_split=cfg.crossvalidate.n_split,
                    sc=scaler,
                    test_size=cfg.loader.test_size,
                    val_size=cfg.loader.val_size,
                    df_pca=ind_mean,
                    def_comp=None,  # Let it determine automatically
                    cutoff_var=cfg.pca.alpha,
                )
        else:
            gw_vecs, lengths = growing_windows(
                ind_mean_w_labels,
                n_split=cfg.crossvalidate.n_split,
                sc=scaler,
                test_size=cfg.loader.test_size,
                val_size=cfg.loader.val_size,
                cutoff_var=cfg.pca.alpha,
            )
    else:
        if tick_name:
            gw_vecs, lengths = growing_windows_no_pca(
                tick_df,
                n_split=cfg.crossvalidate.n_split,
                sc=scaler,
                test_size=cfg.loader.test_size,
                val_size=cfg.loader.val_size,
            )
        else:
            gw_vecs, lengths = growing_windows_no_pca(
                ind_mean_w_labels,
                n_split=cfg.crossvalidate.n_split,
                sc=scaler,
                test_size=cfg.loader.test_size,
                val_size=cfg.loader.val_size,
            )

    if cfg.tune.model.lower() in ["gru", "transformer"]:
        from automar.shared.services.crossvalidation_service import (
            crossval_nn,
            prepare_gw_loaders,
        )

        # Prepare loaders using the new function
        gw_loaders = prepare_gw_loaders(
            gw_vecs,
            tsize=cfg.loader.tsize,
            batch_size=cfg.loader.batch_size,
            device=cfg.loader.device,
        )

        # Cross-validation for neural networks
        crossval_results = crossval_nn(
            cfg,
            ray_results,
            gw_loaders[0],  # train_loader_seq
            gw_loaders[1],  # val_loader_seq
            gw_loaders[2],  # test_loader_seq
            gw_loaders,
            progress_callback=progress_callback,
        )
    elif cfg.tune.model.lower() == "log-reg":
        from automar.shared.services.crossvalidation_service import crossval_lr

        # Prepare logistic regression data using the new function
        log_reg_cross_data = tuple(map(vecs_to_dict, gw_vecs))
        crossval_results = crossval_lr(
            log_reg_cross_data, ray_results, progress_callback=progress_callback
        )

    # Create parent directory if it doesn't exist
    out_path_obj = Path(out_path)
    if out_path_obj.parent and str(out_path_obj.parent) != ".":
        out_path_obj.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "wb") as ff:
        pickle.dump(crossval_results, ff)

    # Get total dataset size from lengths (last fold uses all available data)
    total_samples = lengths[-1] if lengths else None

    print(f"Cross-validation results stored as {out_path}")
    print(f"Total dataset size: {total_samples} samples")
    return crossval_results, out_path, total_samples


# ============================================================================
# Callback wrapper function for API progress tracking
# ============================================================================


def _nn_super_tuner_with_callback(
    module,
    model,
    cfg,
    train_loader_seq,
    val_loader_seq,
    test_loader_seq,
    ray_dir,
    callback,
    model_name="NN",
):
    """
    Generic neural network tuner with progress callback integration.
    Works for GRU, Transformer, and other neural network models.

    Args:
        module: Module containing get_search_space function
        model: Model class (e.g., models.nn.GRUNet or models.nn.Transnet)
        cfg: GlobalConfig object
        train_loader_seq: Training data loader
        val_loader_seq: Validation data loader
        test_loader_seq: Test data loader
        ray_dir: Directory for Ray Tune results
        callback: Progress callback object
        model_name: Name of the model (for debugging)

    Returns:
        Best result from Ray Tune
    """
    import ray
    from ray.tune.schedulers import ASHAScheduler
    from automar.core.models import tuning

    # Get search space from module
    search_space = module.get_search_space(train_loader_seq.dataset.tensors[0].shape[2])
    search_space["epochs"] = cfg.tune.epochs

    # Build training function
    train_fn = tuning.train_model_builder(
        model=model,
        train_loader=train_loader_seq,
        val_loader=val_loader_seq,
        test_loader=test_loader_seq,
        device=cfg.loader.device,
        tuning=True,
    )

    # Configure resources based on device
    if cfg.loader.device == "cuda":
        trainable = ray.tune.with_resources(train_fn, {"gpu": cfg.tune.gpu_per_trial})
    elif cfg.loader.device == "cpu":
        trainable = ray.tune.with_resources(train_fn, {"cpu": cfg.loader.cores})
    else:
        trainable = train_fn

    # Create Ray Tune callback adapter
    class RayTuneCallbackAdapter(ray.tune.Callback):
        """Adapts our callback interface to Ray Tune's callback interface"""

        def __init__(self, progress_callback):
            self.progress_callback = progress_callback

        def on_trial_start(self, iteration, trials, trial, **info):
            # Pass all arguments to match new callback signature
            self.progress_callback.on_trial_start(iteration, trials, trial, **info)

        def on_trial_result(self, iteration, trials, trial, result, **info):
            # Pass all arguments to match new callback signature
            self.progress_callback.on_trial_result(
                iteration, trials, trial, result, **info
            )

    # Create and run tuner
    if tuning:
        module = ray.tune
    else:
        module = ray.air
    tuner = ray.tune.Tuner(
        trainable,
        param_space=search_space,
        tune_config=ray.tune.TuneConfig(
            scheduler=ASHAScheduler(),
            metric="AUROC",
            mode="max",
            num_samples=cfg.tune.num_samples,
            search_alg=ray.tune.search.optuna.OptunaSearch(),
            trial_dirname_creator=tuning.custom_trial_dirname_creator,
        ),
        run_config=module.RunConfig(
            storage_path=ray_dir, callbacks=[RayTuneCallbackAdapter(callback)]
        ),
    )

    analysis = tuner.fit()
    best_result = analysis.get_best_result()

    # Attach metrics_dataframe from analysis to the best result for stats saving
    best_result.metrics_dataframe = analysis.get_dataframe()

    return best_result


def run_prediction_common(cfg, progress_callback: Optional[Callable] = None):
    """
    Run model inference/forecasting with optional progress callback.

    Args:
        cfg: GlobalConfig object with predict, extract, pca, loader options
        progress_callback: Optional callback function for progress updates (for API)

    Returns:
        Dictionary with predictions, metrics, and metadata
    """
    import torch
    from automar.shared.config.path_resolver import get_project_root
    from automar.shared.services.tuning_service import prepare_loaders

    def _count_feature_columns(df):
        if df is None:
            return 0
        return len([col for col in df.columns if col != "Labels"])

    def _determine_pca_components(feature_meta, hyperparams, fallback_base):
        feature_meta = feature_meta or {}
        stored_components = feature_meta.get("pca_component_count")
        if stored_components is not None:
            return stored_components

        total_dim = feature_meta.get("total_input_dim")
        if total_dim is None and hyperparams and "model" in hyperparams:
            total_dim = hyperparams["model"].get("input_dim")

        if total_dim is None:
            return None

        base_count = feature_meta.get("base_feature_count")
        if base_count is None:
            base_count = fallback_base

        if base_count is None:
            return None

        return max(0, total_dim - base_count)

    # Lazy-load device if not set
    if cfg.loader.device is None:
        from automar.shared.services.device_utils import _available_device_types

        cfg.loader.device = _available_device_types()[0]

    project_root = get_project_root()

    # 1. Load model checkpoint
    model_path = Path(cfg.predict.model_path)
    if not model_path.is_absolute():
        model_path = project_root / model_path

    if not model_path.exists():
        raise ValueError(f"Model file not found: {model_path}")

    checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)

    # Extract model metadata
    if isinstance(checkpoint, dict) and "model_type" in checkpoint:
        model_type = checkpoint["model_type"]
        feature_metadata = checkpoint.get("feature_metadata") or {}

        # For neural networks, extract model_state_dict and hyperparameters
        # For log-reg, extract model object
        if model_type.lower() in ["gru", "transformer"]:
            state_dict = checkpoint["model_state_dict"]
            hyperparameters = checkpoint["hyperparameters"]
        else:  # log-reg
            state_dict = checkpoint.get(
                "model", checkpoint
            )  # Fallback to checkpoint if "model" key missing
            hyperparameters = checkpoint.get("hyperparameters")

        if "loader_config" in checkpoint:
            loader_config = checkpoint["loader_config"]
            cfg.loader.dopca = loader_config.get("dopca", False)
            if "tsize" in loader_config:
                cfg.loader.tsize = loader_config["tsize"]
            if "scaler" in loader_config:
                cfg.loader.scaler = loader_config["scaler"]
    else:
        # Old format (MUSE object without dict wrapper)
        model_type = "log-reg"
        state_dict = checkpoint
        hyperparameters = None
        feature_metadata = {}

    if cfg.predict.model_type:
        model_type = cfg.predict.model_type

    # 2. Load dataset and prepare data
    new_df, ind_name = build_final_df(cfg)
    tick_name = cfg.extract.ticker if cfg.extract.ticker else None

    if tick_name:
        tick_df, ind_df = df_industry_split(new_df, industry=ind_name, ticker=tick_name)
        ind_mean = df_industry_avg(ind_df)
        tick_df = tick_df.drop(["Company", "Industry"], axis=1)
        tick_df = tick_df.set_index("Date")
        base_feature_count_current = _count_feature_columns(tick_df)
    else:
        ind_mean_w_labels = df_industry_avg(new_df, 0)
        ind_mean_w_labels.Labels = ind_mean_w_labels.Labels.round()
        ind_mean = df_industry_avg(new_df)
        base_feature_count_current = _count_feature_columns(ind_mean_w_labels)

    # 3. Apply PCA if needed
    if cfg.predict.pca_path or cfg.train.pca_path:
        from automar.shared.services.pca_service import load_pca, build_pca_df

        pca_path = Path(cfg.predict.pca_path or cfg.train.pca_path)
        if not pca_path.is_absolute():
            pca_path = project_root / pca_path

        pca0 = load_pca(str(pca_path))
        cfg.loader.dopca = False

        if tick_name:
            _, pca_df = build_pca_df(pca0, ind_df)
            tick_df = tick_df.join(pca_df, on="Date")
            ind_mean_temp = df_industry_avg(ind_df)
            ind_mean = ind_mean_temp.join(pca_df, on="Date")
        else:
            _, pca_df = build_pca_df(pca0, new_df[new_df["Industry"] == ind_name])
            ind_mean_w_labels = ind_mean_w_labels.join(pca_df, on="Date")

    # 4. Prepare loaders
    if hyperparameters and "loader" in hyperparameters:
        saved_loader = hyperparameters["loader"]
        cfg.loader.tsize = saved_loader.get("tsize", cfg.loader.tsize)
        cfg.loader.batch_size = saved_loader.get("batch_size", cfg.loader.batch_size)
        cfg.loader.val_size = saved_loader.get("val_size", cfg.loader.val_size)
        cfg.loader.test_size = saved_loader.get("test_size", cfg.loader.test_size)
        cfg.loader.scaler = saved_loader.get("scaler", cfg.loader.scaler)

    if model_type.lower() in ["gru", "transformer"]:
        # Apply dynamic PCA if dopca=True (critical for models trained with on-the-fly PCA)
        if tick_name:
            if cfg.loader.dopca and ind_mean is not None:
                import pandas as pd
                from automar.core.preprocessing.tensor import build_pca_df as bpd

                fallback_base = feature_metadata.get("base_feature_count")
                if fallback_base is None:
                    fallback_base = len(ind_mean.columns)

                stored_base = feature_metadata.get("base_feature_count")
                if (
                    stored_base is not None
                    and base_feature_count_current is not None
                    and stored_base != base_feature_count_current
                ):
                    print(
                        "Warning: Base feature count differs between training and prediction datasets. "
                        "Proceeding with stored metadata."
                    )

                # Determine number of PCA components from saved metadata (preferred) or fallback logic
                num_pc = _determine_pca_components(
                    feature_metadata, hyperparameters, fallback_base
                )

                if num_pc is None or num_pc <= 0:
                    # Final fallback to legacy behavior to avoid breaking older checkpoints
                    num_pc = hyperparameters["model"]["input_dim"] - len(
                        ind_mean.columns
                    )

                if num_pc <= 0:
                    raise ValueError(
                        "Could not determine a valid number of PCA components for prediction. "
                        "Ensure the model checkpoint includes feature metadata or provide an explicit PCA file."
                    )

                # Split data to match what sequential_split does
                n_total = len(tick_df)
                train_size_pca = int(
                    n_total * (1 - cfg.loader.val_size - cfg.loader.test_size)
                )

                # Compute PCA on industry average (training portion)
                # Use def_comp to enforce exact number of components from checkpoint
                _, (train_pca, val_pca, test_pca) = bpd(
                    ind_mean.iloc[:train_size_pca],
                    ind_mean.iloc[
                        train_size_pca : int(n_total * (1 - cfg.loader.test_size))
                    ],
                    ind_mean.iloc[int(n_total * (1 - cfg.loader.test_size)) :],
                    def_comp=num_pc,
                    cutoff_var=None,  # Ignored when def_comp is set
                )

                # Concatenate PCA components to ticker data
                full_pca = pd.concat([train_pca, val_pca, test_pca])
                tick_df = pd.DataFrame({**tick_df, **full_pca})

            data_df = tick_df
            full_loaders = prepare_loaders(cfg, tick_df, avg_df=ind_mean)
        else:
            data_df = ind_mean_w_labels
            full_loaders = prepare_loaders(cfg, ind_mean_w_labels)

        _, _, test_loader = full_loaders

        # Load model
        if model_type.lower() == "gru":
            model = models.nn.GRUNet(**hyperparameters["model"])
        else:
            model = models.nn.Transnet(**hyperparameters["model"])

        model.load_state_dict(state_dict)
        model.eval()
        device = torch.device(cfg.loader.device)
        model.to(device)

        # Run inference using existing evaluation functions
        from automar.core.models.evaluation import (
            prob_predictor,
            eval_auroc,
            eval_roc_thresh,
        )
        from sklearn.metrics import (
            accuracy_score,
            confusion_matrix,
            precision_score,
            recall_score,
            f1_score,
        )

        if cfg.predict.mode == "eval":
            # Use existing evaluation functions
            prob_preds = prob_predictor(model, test_loader, device=device)

            # Extract optimal threshold from checkpoint, or compute it if not available
            threshold = None
            if checkpoint and isinstance(checkpoint, dict):
                test_metrics = checkpoint.get("test_metrics")
                if test_metrics and isinstance(test_metrics, dict):
                    threshold = test_metrics.get("threshold")

            # Fallback: compute threshold from current predictions if not in checkpoint
            if threshold is None:
                threshold = eval_roc_thresh(prob_preds, test_loader)
                print(
                    f"Warning: Threshold not found in checkpoint, computed from data: {threshold:.4f}"
                )

            # Apply optimal threshold for predictions
            preds = (prob_preds > threshold).long().cpu().numpy()
            probs = prob_preds.cpu().numpy()
            labels = test_loader.dataset.tensors[1].cpu().numpy()

            # Compute all classification metrics
            auroc = eval_auroc(prob_preds, test_loader).item()
            accuracy = accuracy_score(labels, preds)
            precision = precision_score(labels, preds, zero_division=0)
            recall = recall_score(labels, preds, zero_division=0)
            fscore = f1_score(labels, preds, zero_division=0)
            cm = confusion_matrix(labels, preds)

            # Extract test dates from data_df
            n_total = len(data_df)
            train_size = int(n_total * (1 - cfg.loader.val_size - cfg.loader.test_size))
            val_size = int(n_total * cfg.loader.val_size)
            test_start_idx = train_size + val_size
            test_dates = data_df.index[test_start_idx + cfg.loader.tsize :].tolist()

            results = {
                "predictions": preds.tolist(),
                "probabilities": (probs * 100).tolist(),
                "labels": labels.tolist(),
                "metrics": {
                    "auroc": float(auroc),
                    "accuracy": float(accuracy),
                    "precision": float(precision),
                    "recall": float(recall),
                    "fscore": float(fscore),
                    "threshold": float(
                        threshold
                    ),  # Keep as 0-1 range (frontend will convert to %)
                },
                "confusion_matrix": cm.tolist(),
                "dates": test_dates,
            }
        else:
            # Forecast mode - delegate to forecast module
            from automar.core.models.forecast import run_forecast

            results = run_forecast(
                model=model,
                device=device,
                data_df=data_df,
                ind_mean=ind_mean,
                cfg=cfg,
                checkpoint=checkpoint,
            )

    elif model_type.lower() == "log-reg":
        if tick_name:
            data_df = tick_df
            seq_vecs, pca_obj = prepare_loaders(
                cfg, tick_df, avg_df=ind_mean, mode="reg"
            )
        else:
            data_df = ind_mean_w_labels
            seq_vecs, pca_obj = prepare_loaders(cfg, ind_mean_w_labels, mode="reg")

        log_reg_data = vecs_to_dict(seq_vecs, pca=pca_obj)
        model = state_dict

        if cfg.predict.mode == "eval":
            from automar.core.models.evaluation import (
                prob_predictor,
                eval_auroc,
                eval_roc_thresh,
            )
            from sklearn.metrics import (
                accuracy_score,
                confusion_matrix,
                precision_score,
                recall_score,
                f1_score,
            )

            prob_preds = prob_predictor(model, log_reg_data, "test")

            # Extract optimal threshold from checkpoint, or compute it if not available
            threshold = None
            if checkpoint and isinstance(checkpoint, dict):
                test_metrics = checkpoint.get("test_metrics")
                if test_metrics and isinstance(test_metrics, dict):
                    threshold = test_metrics.get("threshold")

            # Fallback: compute threshold from current predictions if not in checkpoint
            if threshold is None:
                threshold = eval_roc_thresh(prob_preds, log_reg_data, "test")
                print(
                    f"Warning: Threshold not found in checkpoint, computed from data: {threshold:.4f}"
                )

            # Apply optimal threshold for predictions
            preds = (prob_preds > threshold).astype(int)
            labels = log_reg_data["Y"]["test"]

            # Compute all classification metrics
            auroc = eval_auroc(prob_preds, log_reg_data, "test")
            accuracy = accuracy_score(labels, preds)
            precision = precision_score(labels, preds, zero_division=0)
            recall = recall_score(labels, preds, zero_division=0)
            fscore = f1_score(labels, preds, zero_division=0)
            cm = confusion_matrix(labels, preds)

            # Extract test dates from data_df (log-reg doesn't use sliding window offset)
            n_total = len(data_df)
            train_size = int(n_total * (1 - cfg.loader.val_size - cfg.loader.test_size))
            val_size = int(n_total * cfg.loader.val_size)
            test_start_idx = train_size + val_size
            test_dates = data_df.index[test_start_idx:].tolist()

            results = {
                "predictions": preds.tolist(),
                "probabilities": (prob_preds * 100).tolist(),
                "labels": labels.tolist(),
                "metrics": {
                    "auroc": float(auroc),
                    "accuracy": float(accuracy),
                    "precision": float(precision),
                    "recall": float(recall),
                    "fscore": float(fscore),
                    "threshold": float(
                        threshold
                    ),  # Keep as 0-1 range (frontend will convert to %)
                },
                "confusion_matrix": cm.tolist(),
                "dates": test_dates,
            }
        else:
            # Forecast mode
            from automar.core.models.forecast import run_forecast_logreg

            results = run_forecast_logreg(
                model=model,
                data_df=data_df,
                ind_mean=ind_mean,
                cfg=cfg,
                checkpoint=checkpoint,
            )

    # Add metadata
    results["model_type"] = model_type
    results["model_path"] = str(model_path)
    results["dataset"] = {"industry": ind_name, "ticker": tick_name}

    # 5. Save predictions
    from ..runners.predict_runner import save_predictions_to_disk

    save_predictions_to_disk(cfg, results, model_path, ind_name, tick_name)

    return results
