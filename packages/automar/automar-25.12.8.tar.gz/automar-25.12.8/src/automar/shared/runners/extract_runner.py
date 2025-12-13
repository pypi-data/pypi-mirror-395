# -*- coding: utf-8 -*-
"""
Data extraction runner for Automar

Handles loading or extracting financial data from Yahoo Finance
"""


def run_extraction(cfg):
    """
    Extract financial data based on configuration

    Args:
        cfg: Configuration object with extraction parameters

    Returns:
        DataFrame with extraction_status stored in attrs
    """
    from automar.shared.services.extraction_service import load_or_extract

    # Convert force to skip (inverted logic)
    skip = not cfg.force

    # load_or_extract now returns (df, FinderSt status)
    df, status = load_or_extract(
        datest=cfg.datest,
        datend=cfg.datend,
        ticker=cfg.ticker,
        industry=cfg.industry,
        history=cfg.history,
        skip=skip,
        file_path=cfg.extract_file,
        dir_path=cfg.dir_path,
        format=cfg.format,
        ensure_combined_dataset=getattr(cfg, "ensure_combined_dataset", False),
    )

    # For backward compatibility, store status in df.attrs
    df.attrs["extraction_status"] = status

    return df
