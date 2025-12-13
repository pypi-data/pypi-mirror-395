# -*- coding: utf-8 -*-
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from ray.tune.schedulers import ASHAScheduler
from pathlib import Path
import ray
from ray.tune.search import optuna
from automar.core.models import tuning
from automar.shared.persistence.library import get_dirs
from automar.shared.config.path_resolver import get_hpt_defaults_dir

SCALERS = {"standard": StandardScaler, "minmax": MinMaxScaler, "robust": RobustScaler}

# Use path_resolver to find assets directory (works in both repository and installed package)
PATH_TO_CFG = get_hpt_defaults_dir()


def gen_hpt_filename(
    model,
    root_path=None,
    end_path=None,
):
    if root_path is None:
        end_path = PATH_TO_CFG

    if model == "gru":
        file_name = "gru"
    elif model == "log-reg":
        file_name = "logreg"
    elif model == "transformer":
        file_name = "transformer"

    return get_dirs(root=root_path, create_dirs=False, end=end_path) / f"{file_name}.py"


def prepare_loaders(cfg, new_df, avg_df=None, mode="nn"):
    from automar.core.preprocessing.loaders import vecs_to_series_loaders
    from automar.core.preprocessing.tensor import (
        sequential_split,
        sequential_split_no_pca,
    )

    # Assuming new_df is already split into train, validation, and test sets
    pca_obj = None
    if cfg.loader.dopca:
        result = sequential_split(
            new_df,
            sc=SCALERS[cfg.loader.scaler](),
            val_size=cfg.loader.val_size,
            test_size=cfg.loader.test_size,
            df_pca=avg_df,
            def_comp=cfg.pca.n_components,
            cutoff_var=cfg.pca.alpha,
        )
        # sequential_split now returns (train_t, val_t, test_t, pca_obj)
        seq_vecs = result[:3]
        pca_obj = result[3] if len(result) > 3 else None
    else:
        seq_vecs = sequential_split_no_pca(
            new_df,
            sc=SCALERS[cfg.loader.scaler](),
            val_size=cfg.loader.val_size,
            test_size=cfg.loader.test_size,
        )

    if mode == "reg":
        # For log-reg mode, return both vectors and PCA object
        return seq_vecs, pca_obj

    elif mode == "nn":
        # Create loaders using the new function
        train_loader_seq, val_loader_seq, test_loader_seq = vecs_to_series_loaders(
            seq_vecs,
            tsize=cfg.loader.tsize,
            batch_size=cfg.loader.batch_size,
            device=cfg.loader.device,
        )
        return train_loader_seq, val_loader_seq, test_loader_seq


def GRU_super_tuner(
    module, model, cfg, train_loader_seq, val_loader_seq, test_loader_seq, ray_dir=None
):
    # Lazy-load device if not set (avoids PyTorch import at API startup)
    if cfg.loader.device is None:
        from .device_utils import _available_device_types

        cfg.loader.device = _available_device_types()[0]

    GRU_search_space = module.get_search_space(
        train_loader_seq.dataset.tensors[0].shape[2]
    )
    GRU_search_space["epochs"] = cfg.tune.epochs

    train_GRU = tuning.train_model_builder(
        model=model,
        train_loader=train_loader_seq,
        val_loader=val_loader_seq,
        test_loader=test_loader_seq,
        device=cfg.loader.device,
        tuning=True,
    )

    ### GRU tuning
    if cfg.loader.device == "cuda":
        GRU_trainable = ray.tune.with_resources(
            train_GRU, {"gpu": cfg.tune.gpu_per_trial}
        )
    elif cfg.loader.device == "cpu":
        GRU_trainable = ray.tune.with_resources(train_GRU, {"cpu": cfg.loader.cores})
    GRU_tuner = ray.tune.Tuner(
        GRU_trainable,
        param_space=GRU_search_space,
        tune_config=ray.tune.TuneConfig(
            scheduler=ASHAScheduler(),
            metric="AUROC",
            mode="max",
            num_samples=cfg.tune.num_samples,
            search_alg=ray.tune.search.optuna.OptunaSearch(),
            trial_dirname_creator=tuning.custom_trial_dirname_creator,
        ),
        run_config=ray.tune.RunConfig(storage_path=ray_dir),
    )
    GRU_analysis = GRU_tuner.fit()
    GRU_ray_results = GRU_analysis.get_best_result()

    # Attach metrics_dataframe from analysis to the best result for stats saving
    GRU_ray_results.metrics_dataframe = GRU_analysis.get_dataframe()

    return GRU_ray_results


def transformer_super_tuner(
    module, model, cfg, train_loader_seq, val_loader_seq, test_loader_seq, ray_dir=None
):
    # Lazy-load device if not set (avoids PyTorch import at API startup)
    if cfg.loader.device is None:
        from .device_utils import _available_device_types

        cfg.loader.device = _available_device_types()[0]

    transformer_search_space = module.get_search_space(
        train_loader_seq.dataset.tensors[0].shape[2]
    )
    transformer_search_space["epochs"] = cfg.tune.epochs

    train_transformer = tuning.train_model_builder(
        model=model,
        train_loader=train_loader_seq,
        val_loader=val_loader_seq,
        test_loader=test_loader_seq,
        device=cfg.loader.device,
        tuning=True,
    )

    ### Transformer tuning
    if cfg.loader.device == "cuda":
        transformer_trainable = ray.tune.with_resources(
            train_transformer, {"gpu": cfg.tune.gpu_per_trial}
        )
    elif cfg.loader.device == "cpu":
        transformer_trainable = ray.tune.with_resources(
            train_transformer, {"cpu": cfg.loader.cores}
        )
    transformer_tuner = ray.tune.Tuner(
        transformer_trainable,
        param_space=transformer_search_space,
        tune_config=ray.tune.TuneConfig(
            scheduler=ASHAScheduler(),
            metric="AUROC",
            mode="max",
            num_samples=cfg.tune.num_samples,
            search_alg=ray.tune.search.optuna.OptunaSearch(),
            trial_dirname_creator=tuning.custom_trial_dirname_creator,
        ),
        run_config=ray.tune.RunConfig(storage_path=ray_dir),
    )
    transformer_analysis = transformer_tuner.fit()
    transformer_ray_results = transformer_analysis.get_best_result()

    # Attach metrics_dataframe from analysis to the best result for stats saving
    transformer_ray_results.metrics_dataframe = transformer_analysis.get_dataframe()

    return transformer_ray_results


def logreg_super_tuner(module, log_reg_data, cfg, ray_dir=None, callback=None):
    logreg_search_space = module.get_search_space(log_reg_data)
    log_reg_trainable = ray.tune.with_resources(
        tuning.train_log_reg_builder(log_reg_data), {"cpu": cfg.loader.cores}
    )

    # Build run config with optional callback
    run_config_kwargs = {"storage_path": ray_dir}
    if callback:
        run_config_kwargs["callbacks"] = [callback]

    log_reg_tuner = ray.tune.Tuner(
        log_reg_trainable,
        param_space=logreg_search_space,
        tune_config=ray.tune.TuneConfig(
            scheduler=ASHAScheduler(),
            metric="AUROC",
            mode="max",
            num_samples=cfg.tune.num_samples,
            search_alg=ray.tune.search.optuna.OptunaSearch(),
        ),
        run_config=ray.tune.RunConfig(**run_config_kwargs),
    )

    logreg_analysis = log_reg_tuner.fit()
    logreg_ray_results = logreg_analysis.get_best_result()

    # Attach metrics_dataframe from analysis to the best result for stats saving
    logreg_ray_results.metrics_dataframe = logreg_analysis.get_dataframe()

    return logreg_ray_results
