# -*- coding: utf-8 -*-
"""
PCA analysis runner for Automar

Handles PCA transformation of financial datasets
"""

from pathlib import Path
from functools import partial


def run_pca(cfg, dataset=None, skip=None):
    """
    Run PCA analysis on financial data

    Args:
        cfg: Configuration object with PCA and extraction parameters
        dataset: Optional pre-loaded dataset
        skip: Skip mode (1 = load existing, None/0 = error if exists)

    Returns:
        Tuple of (pca_object, transformed_df, pca_file_path, df_file_path)
    """
    from automar.shared.services.pca_service import (
        build_pca_df,
        gen_pca_filename,
        prcoan,
        save_pca,
        load_pca,
    )
    from automar.shared.persistence.library import read_df, write_df, date_ender
    from automar.shared.runners.extract_runner import run_extraction

    if cfg.pca.data_file:
        dataset = read_df(cfg.pca.data_file)

    if (dataset is None) or (dataset.empty):
        dataset = run_extraction(cfg.extract)

    if cfg.extract.industry is not None:
        ind_name = cfg.extract.industry
    else:
        ind_name = dataset["Industry"].value_counts().idxmax()

    pca_fname_build = partial(
        gen_pca_filename,
        industry=ind_name,
        dir_path=cfg.extract.dir_path,
        history=cfg.extract.history,
    )

    guess_name = pca_fname_build(
        datest=cfg.extract.datest and dataset["Date"].min(),
        datend=date_ender(cfg.extract.datend),
    )

    if guess_name.is_file() and not cfg.pca.pca_force:
        if skip == 1:
            # CLI mode with skip=1: load existing file
            pca = load_pca(guess_name)
            _, pca_df = build_pca_df(pca, dataset.dropna())
            return pca, pca_df, str(guess_name), None
        else:
            # API mode or CLI without skip: error if file exists
            raise FileExistsError(
                f"PCA analysis already exists at {guess_name}. Enable 'Force recompute PCA' option to overwrite and recompute."
            )

    out_file = cfg.pca.pca_file
    if not out_file:
        # Use custom directory if provided, otherwise use default
        if cfg.pca.pca_obj_dir:
            from automar.shared.config.path_resolver import resolve_path

            pca_dir = resolve_path(cfg.pca.pca_obj_dir, relative_to_project=True)
        else:
            pca_dir = None

        out_file = pca_fname_build(
            datest=cfg.extract.datest and dataset["Date"].min(),
            datend=dataset["Date"].max(),
        )

        # Replace directory if custom one provided
        if pca_dir:
            out_file = pca_dir / Path(out_file).name

    ind_data = dataset[dataset["Industry"] == ind_name]
    pca, feature_names = prcoan(
        ind_data.dropna(),
        default=cfg.pca.n_components,
        alpha=cfg.pca.alpha,
        drop=cfg.pca.drop,
    )
    out_file_path = Path(out_file)
    if out_file_path.parent and str(out_file_path.parent) != ".":
        out_file_path.parent.mkdir(parents=True, exist_ok=True)
    save_pca(pca, out_file, feature_names=feature_names)
    print(f"Saved fitted PCA at {out_file}")

    df = None
    df_file_path_str = None
    if not cfg.pca.notdf:
        df_file = cfg.pca.pca_df_file
        if not df_file:
            # Use custom directory if provided, otherwise use default
            if cfg.pca.pca_df_dir:
                from automar.shared.config.path_resolver import resolve_path

                df_dir = resolve_path(cfg.pca.pca_df_dir, relative_to_project=True)
            else:
                df_dir = None

            df_file = pca_fname_build(
                datest=cfg.extract.datest and dataset["Date"].min(),
                datend=dataset["Date"].max(),
                format=cfg.extract.format,
            )

            # Replace directory if custom one provided
            if df_dir:
                df_file = df_dir / Path(df_file).name

        _, df = build_pca_df(pca, dataset.dropna())
        df_file_path = Path(df_file)
        if df_file_path.parent and str(df_file_path.parent) != ".":
            df_file_path.parent.mkdir(parents=True, exist_ok=True)
        write_df(df, df_file)
        print(f"Saved data transformed by fitted PCA at {df_file}")
        df_file_path_str = str(df_file)
    return (pca, df, str(out_file), df_file_path_str)
