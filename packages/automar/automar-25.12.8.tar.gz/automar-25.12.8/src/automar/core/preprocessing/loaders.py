# -*- coding: utf-8 -*-
"""Module to build the pertinent datasets"""

from functools import partial
import pickle
import torch

import pandas as pd

from .extractor import ind_avg_func, GICStoYF, symbols_func, tick_func
from .stats import PCA_func, total_dic_func
from .tensor import group_batch, data_splitter


def vecs_to_series_loaders(vecs, tsize, batch_size, device, generator=None):
    """
    Builds the three ``DataLoader`` objects used to train, validate and
    test the model from already-split vectors.

    Args:
        vecs (tuple): tuple of three datasets ``(train_vecs, val_vecs,
            test_vecs)`` produced by the data-splitting utilities.
        tsize (int): length of the rolling time window fed to the network.
        batch_size (int): number of windows per batch.
        device (str): device where the tensors will be stored
            (e.g. ``'cpu'`` or ``'cuda:0'``).
        generator (torch.Generator, optional): random generator that
            controls shuffling of the training loader. If ``None`` (default),
            a new generator is created.

    Returns:
        train_loader (DataLoader): manages shuffled training batches.
        val_loader (DataLoader): manages validation batches (no shuffle).
        test_loader (DataLoader): manages test batches (no shuffle).
    """
    if generator is None:
        generator = torch.Generator()

    f = partial(
        group_batch,
        tsize=tsize,
        batch_size=batch_size,
        device=device,
        generator=generator,
    )
    return (
        f(shuffleBool=True, ds=vecs[0]),
        f(shuffleBool=False, ds=vecs[1]),
        f(shuffleBool=False, ds=vecs[2]),
    )


def vecs_to_dict(vecs, pca=None):
    """
    Builds nested feature/target dictionaries from already-split vectors.

    Args:
        vecs (tuple): tuple ``(train_vecs, val_vecs, test_vecs)``; each
            tensor has shape ``(n_samples, n_features + 1)`` with the
            last column holding the target.
        pca (PCA, optional): Fitted PCA object if PCA was applied during
            data preparation. Defaults to None.

    Returns:
        dict: ``{'X': {'train', 'val', 'test'}, 'Y': {'train', 'val',
            'test'}, 'pca': pca_obj}`` where ``X`` contains feature tensors
            ``[..., :-1]``, ``Y`` contains target tensors ``[..., -1]``,
            and ``pca`` contains the fitted PCA object (if provided).
    """
    result = {
        "X": {
            "train": vecs[0][:, :-1],
            "val": vecs[1][:, :-1],
            "test": vecs[2][:, :-1],
        },
        "Y": {"train": vecs[0][:, -1], "val": vecs[1][:, -1], "test": vecs[2][:, -1]},
    }

    # Add PCA object if provided
    if pca is not None:
        result["pca"] = pca

    return result


def data_collector(tick_input, hist_length, folder, current_date):
    """
    If there exists already a file with query data of the requested industry
    obtained on the current date, this function will extract the requested data
    out of it; if there isn't such file, it will run Yahoo Finance queries to
    obtain data for the requested industry. In either case, it applies all the
    functions necessary to obtain the basic dataframes.

    Args:
        tick_input (str): ticker of the requested company.
        hist_length (str): number and type of requested periods
        folder (str): folder where the data will be stored.
        current_date (str): Current date to name the output folder.

    Returns:
        htdf (dataframe): data obtained from the query for the requested
            company (opening, closing, lowest and highest price and volume of
            stock)
        spdata (dict): contains dataframes for each S&P 500 company in the
            requested industry describing the same variables obtained from
            queries as for the target company.
        ind_name (str): name of the industry
    """
    htdf = None
    spdata = None
    indname = None

    for ind in GICStoYF.keys():
        ind = ind.replace(" ", "_")
        PATH_DATA = folder / f"data_{ind}_{hist_length}_{current_date}.pkl"
        if PATH_DATA.exists():
            with open(PATH_DATA, "rb") as ff:
                data_dic = pickle.load(ff)
            if tick_input in data_dic["data"]:
                htdf = data_dic["data"][tick_input]
                spdata = data_dic["data"]
                indname = data_dic["name"]

    if htdf is None:
        htdf = tick_func(tick_input, hist_length)
        data_dic = symbols_func(tick_input, hist_length)
        spdata = data_dic["data"]
        indname = data_dic["name"]
        ind = indname.replace(" ", "_")
        PATH_DATA = folder / f"data_{ind}_{hist_length}_{current_date}.pkl"
        with open(PATH_DATA, "wb") as ff:
            pickle.dump(data_dic, ff)

    return htdf, spdata, indname


def df_builder(tick_input, hist_length, def_comp, cutoff_var, folder, current_date):
    """
    Generates the complete dataframe including the proper target variable and
    all individual features plus the principal components of the industry wide
    average variables that will be used for training, validating and testing
    the models.

    Args:
        tick_input (str): ticker of the requested company.
        hist_length (str): number and type of requested periods.
        def_comp (float): number of principal components the analysis extracts.
        cutoff_var (float): significance criterion to decide which principal
            components must be kept after the reduction.
        folder (str): folder where the data will be stored.
        current_date (str): Current date to name the output folder.

    Results:
        output (dict): contains the key 'dataframe' whose value is the definitive
        dataframe as described above, 'inudstry dataframe' whose value is the dataframe of
        industry averages, the key 'industry name' whose value is the name of the industry,
        'pca1' whose value is the PCA containing all components the analysis and 'pca2'
        whose value is the PCA only containing the principal components that comply with the
        cutoff value.
    """
    htdf, spdata, indname = data_collector(
        tick_input, hist_length, folder, current_date
    )

    MeansDF = ind_avg_func(spdata, htdf)
    df1, df2 = total_dic_func(htdf, MeansDF)
    dfpca, pca1, pca2 = PCA_func(
        df2, default_components=def_comp, cutoff_var=cutoff_var
    )
    df3 = pd.DataFrame({**df1, **dfpca})
    output = {
        "raw dataframe": df1,
        "dataframe": df3,
        "industry dataframe": df2,
        "industry dictionary": spdata,
        "industry name": indname,
        "pca1": pca1,
        "pca2": pca2,
    }
    return output


def logreg_builder(df_input, scaler, num_chunks, val_size, test_size):
    """
    Formats data as required to be inputted in the functions related to the
    WEASEL-MUSE and logistic regression model.

    Args:
        df_input (dataframe): the complete dataframe with the target and all
            features.
        scaler (class): scikit-learn scaling method applied to the data
        num_chunks (int): number of growing windows, of data slices with
            increasing length.
        val_size (float): proportion of the length of the validation set over
            the length of the whole available data.
        test_size (float): proportion of the length of the test set over the
            length of the whole available data.

    Returns:
        lr_dic (dict): see the output of :func: data_splitter
        lr_list (list): see the output of :func: growing_window_split
        lr_len (list): see the output of :func: growing_window_split
    """
    lr_dic = data_splitter(df_input, scaler=scaler, test=test_size)
    lr_list, lr_len = growing_window_split(
        df_input,
        scaler=scaler,
        num_chunks=num_chunks,
        val_size=val_size,
        test_size=test_size,
    )
    return lr_dic, lr_list, lr_len
