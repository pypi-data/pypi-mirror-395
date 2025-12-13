# -*- coding: utf-8 -*-
"""Tensor generator module"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import TensorDataset, DataLoader
from automar.core.preprocessing.stats import PCA_func
from sklearn.preprocessing import StandardScaler


def pre_tensor_func(input_df, sc, fit=True):
    """
    Prepares a datarame to be formatted into tensors by turning it into an
    array with scaled data.

    Args:
        input_df (dataframe): contains all data that will be used to train,
            validate and test the models.
        sc (class): scikit-learn scaling method applied to the data.
        fit (bool, optional): If True, it will fit the scaler with the
            provided df before performing the transformation. Defaults to
            True.

    Returns:
        stacked (array): the output data is rearranged so that the target
        variable (column 'Labels' in the input dataframe) is positioned at the
        end in the y axis.
    """
    if fit:
        data = sc.fit_transform(input_df.drop(["Labels"], axis=1).values)
    else:
        data = sc.transform(input_df.drop(["Labels"], axis=1).values)
    target = np.asarray(input_df["Labels"].values, dtype=float)
    stacked = np.column_stack((data, target))
    return stacked


def group_batch(tsize, batch_size, shuffleBool, ds, device, generator=None):
    """
    Builds tensors and batches them into a data loader.

    Args:
        tsize (float): window size.
        batch_size (float): batch size.
        shuffleBool (bool): if True, the data loader will shuffle the batches.
        ds (array): input dataset (see the output of :func: pre_tensor_func).
        device (str): Where to store the dataset. Defaults to cpu.

    Returns:
      Data loader of batched tensors.
    """
    x_vals = []
    y_vals = []

    for idx in range(tsize + 1, ds.shape[0] - 1):
        sp = ds[idx - tsize - 1 : idx]
        x_vals.append(torch.tensor(sp[:-1, :-1], device=device))
        y_vals.append(torch.tensor(sp[-1, -1], device=device))

    try:
        return DataLoader(
            TensorDataset(torch.stack(x_vals, dim=0), torch.stack(y_vals, dim=0)),
            shuffle=shuffleBool,
            batch_size=batch_size,
            generator=generator,
        )
    except:
        raise ValueError(
            "Insufficient amount of observations to complete the requested number of growing windows."
            + f"Please lower either the number of growing windows with the argument 'n_split' or the set of historical observations per prediction with 'tsize'."
            + f"Alternatively, a larger dataset would avoid the issue altogether and could be acquired by increasing the number of periods downloaded with the argument 'history'."
        )


def build_pca_df(train_df, val_df, test_df, def_comp=0, cutoff_var=None):
    """
    Applies PCA transformation to train, validation, and test dataframes.

    Fits PCA on the training data and transforms all three datasets using the
    fitted PCA model. This ensures consistent dimensionality reduction across
    all datasets without data leakage.

    Args:
        train_df (dataframe): Training dataframe to fit PCA on.
        val_df (dataframe): Validation dataframe to transform.
        test_df (dataframe): Test dataframe to transform.
        def_comp (int, optional): Default number of principal components to retain.
            If 0, number is determined automatically. Defaults to 0.
        cutoff_var (float, optional): Variance threshold for selecting components.
            Components are selected to retain this proportion of total variance.
            Defaults to None.

    Returns:
        tuple: A tuple containing:
            - pca (PCA): Fitted PCA model.
            - (train_pca_df, val_pca_df, test_pca_df) (tuple): Tuple of
              transformed dataframes with PCA components as columns.
    """
    pca_sc = StandardScaler()
    pca_sc.fit(train_df)
    train_pca_df, _, pca = PCA_func(
        train_df, default_components=def_comp, cutoff_var=cutoff_var, scaler=pca_sc
    )
    val_pca_df = pca.transform(pca_sc.transform(val_df))
    val_pca_df = pd.DataFrame(
        val_pca_df, index=val_df.index, columns=train_pca_df.columns
    )
    test_pca_df = pca.transform(pca_sc.transform(test_df))
    test_pca_df = pd.DataFrame(
        test_pca_df, index=test_df.index, columns=train_pca_df.columns
    )

    return (pca, (train_pca_df, val_pca_df, test_pca_df))


def dataset_to_tensors(train_df, val_df, test_df, sc):
    """
    Converts train, validation, and test dataframes to preprocessed tensors.

    Applies scaling and preprocessing to convert dataframes into tensor format
    suitable for neural network training. The scaler is fitted only on training
    data to prevent data leakage.

    Args:
        train_df (dataframe): Training dataframe to fit scaler on and transform.
        val_df (dataframe): Validation dataframe to transform.
        test_df (dataframe): Test dataframe to transform.
        sc (class): Scikit-learn scaling method to apply to the data.

    Returns:
        tuple: A tuple containing:
            - train_tensor: Preprocessed training data as tensors.
            - val_tensor: Preprocessed validation data as tensors.
            - test_tensor: Preprocessed test data as tensors.
    """
    return (
        pre_tensor_func(train_df, sc, fit=True),
        pre_tensor_func(val_df, sc, fit=False),
        pre_tensor_func(test_df, sc, fit=False),
    )


def growing_windows(
    df_input,
    n_split,
    sc,
    test_size,
    val_size,
    df_pca=None,
    def_comp=None,
    cutoff_var=None,
):
    """
    Creates multiple sets of data dataframes using the growing windows method.

    This method generates n_split sets of data dataframes, where each subsequent set
    uses a larger portion of the training data. The test set remains constant
    throughout all splits, while training and validation sets grow progressively.
    This is useful for analyzing model performance with varying amounts of training data.

    Args:
        df_input (dataframe): Complete dataframe containing all data for training,
            validation and testing.
        n_split (int): Number of growing windows (progressive data slices).
        sc (class): Scikit-learn scaling method to apply to the data.
        test_size (float): Proportion of the test set over the total data length.
        val_size (float): Proportion of the validation set over the total data length.
        df_pca (dataframe, optional): PCA dataframe for dimensionality reduction.
            Must have same length as df_input. Defaults to None.
        def_comp (int, optional): Number of principal components to use. If 0,
            automatically determined from first window. Defaults to None.
        cutoff_var (float, optional): Variance cutoff for PCA. Defaults to None.

    Returns:
        tuple: A tuple containing:
            - loaders (list): List of tuples, each containing (train_loader,
              val_loader, test_loader) for each growing window.
            - lengths (list): Length of data used in each growing window
              (excluding the fixed test set).
    """
    # Split the data into training and test sets
    test_size_int = int(len(df_input) * test_size)
    train_data = df_input[:-test_size_int]
    test_data = df_input[-test_size_int:]

    # Adjust sizes
    val_size_adj = val_size / (1 - test_size)
    train_size_adj = (1 - test_size - val_size) / (1 - test_size)

    dfs = []
    lengths = []

    for idx in range(1, n_split + 1):
        # Calculate the size of the current training set
        current_total_size = int(len(train_data) * (idx / n_split))
        current_total_data = train_data[:current_total_size]

        train_end = int(current_total_size * train_size_adj)
        val_end = int(current_total_size * (train_size_adj + val_size_adj))

        current_train_data = current_total_data[:train_end]
        current_val_data = current_total_data[train_end:val_end]

        if (None not in (def_comp, cutoff_var)) and (df_pca is not None):
            (pca, (train_pca, val_pca, test_pca)) = build_pca_df(
                df_pca.iloc[:current_total_size].iloc[:train_end],
                df_pca.iloc[:current_total_size].iloc[train_end:val_end],
                df_pca.iloc[-test_size_int:],
                def_comp=def_comp,
                cutoff_var=cutoff_var,
            )
            # If def_comp is equal to 0, its number should be fixed by the first PCA to the training set
            def_comp = pca.n_components_

            current_train_data = pd.DataFrame({**current_train_data, **train_pca})
            current_val_data = pd.DataFrame({**current_val_data, **val_pca})
            current_test_data = pd.DataFrame({**test_data, **test_pca})
        else:
            current_test_data = test_data

        current_train_data, current_val_data, current_test_data = dataset_to_tensors(
            current_train_data, current_val_data, current_test_data, sc
        )

        # Append the loaders (train, val, test)
        dfs.append((current_train_data, current_val_data, current_test_data))

        # Store the lengths of the training and validation sets
        lengths.append(current_total_size)

    return dfs, lengths


def growing_windows_no_pca(
    df_input,
    n_split,
    sc,
    test_size,
    val_size,
):
    """
    Creates multiple sets of data using growing windows WITHOUT PCA.

    Simpler version that skips PCA dimensionality reduction.

    Args:
        df_input (dataframe): Complete dataframe.
        n_split (int): Number of growing windows.
        sc (class): Scikit-learn scaling method.
        test_size (float): Proportion of test set.
        val_size (float): Proportion of validation set.

    Returns:
        tuple: (loaders, lengths) - List of tensor tuples and their lengths
    """
    # Split the data into training and test sets
    test_size_int = int(len(df_input) * test_size)
    train_data = df_input[:-test_size_int]
    test_data = df_input[-test_size_int:]

    # Adjust sizes
    val_size_adj = val_size / (1 - test_size)
    train_size_adj = (1 - test_size - val_size) / (1 - test_size)

    dfs = []
    lengths = []

    for idx in range(1, n_split + 1):
        # Calculate the size of the current training set
        current_total_size = int(len(train_data) * (idx / n_split))
        current_total_data = train_data[:current_total_size]

        train_end = int(current_total_size * train_size_adj)
        val_end = int(current_total_size * (train_size_adj + val_size_adj))

        current_train_data = current_total_data[:train_end]
        current_val_data = current_total_data[train_end:val_end]
        current_test_data = test_data  # No PCA, just use test data directly

        # Skip PCA - go straight to tensor conversion
        current_train_data, current_val_data, current_test_data = dataset_to_tensors(
            current_train_data, current_val_data, current_test_data, sc
        )

        dfs.append((current_train_data, current_val_data, current_test_data))
        lengths.append(current_total_size)

    return dfs, lengths


def sequential_split(
    df_input,
    sc,
    val_size,
    test_size,
    df_pca=None,
    def_comp=None,
    cutoff_var=None,
):
    """
    Generates data loaders used to train, validate and test the RNN.

    Args:
        df_input (dataframe): The complete dataframe with the target and all features.
        sc (class): Scikit-learn scaling method applied to the data.
        tsize (int): Window size.
        batch_size (int): Batch size.
        val_size (float): Proportion of the validation set length over the
            total available data length.
        test_size (float): Proportion of the test set length over the
            total available data length.
        device (str): Device where to store the dataset (e.g., 'cuda', 'cpu').
        df_pca (dataframe, optional): PCA dataframe for dimensionality reduction.
            Defaults to None.
        def_comp (int, optional): Number of principal components to use.
            Defaults to None.
        cutoff_var (float, optional): Variance cutoff for PCA. Defaults to None.

    Returns:
        tuple: A tuple containing:
            - train_loader (DataLoader): Manages batches of training tensors.
            - val_loader (DataLoader): Manages batches of validation tensors.
            - test_loader (DataLoader): Manages batches of test tensors.
            - pca_obj (PCA or None): Fitted PCA object if PCA was applied, None otherwise.
    """
    total_size = len(df_input)
    train_size = 1 - (val_size + test_size)

    train_end = int(total_size * train_size)
    val_end = int(total_size * (train_size + val_size))

    train_df = df_input.iloc[:train_end].copy()
    val_df = df_input.iloc[train_end:val_end].copy()
    test_df = df_input.iloc[val_end:].copy()

    pca_obj = None
    if (None not in (def_comp, cutoff_var)) and (df_pca is not None):
        (pca_obj, (train_pca, val_pca, test_pca)) = build_pca_df(
            df_pca.iloc[:train_end],
            df_pca.iloc[train_end:val_end],
            df_pca.iloc[val_end:],
            def_comp=def_comp,
            cutoff_var=cutoff_var,
        )

        train_df = pd.DataFrame({**train_df, **train_pca})
        val_df = pd.DataFrame({**val_df, **val_pca})
        test_df = pd.DataFrame({**test_df, **test_pca})

    train_t, val_t, test_t = dataset_to_tensors(train_df, val_df, test_df, sc)

    return (train_t, val_t, test_t, pca_obj)


def sequential_split_no_pca(
    df_input,
    sc,
    val_size,
    test_size,
):
    """
    Generates train/val/test tensors WITHOUT PCA - simpler version.

    Args:
        df_input (dataframe): The complete dataframe with target and features.
        sc (class): Scikit-learn scaling method applied to the data.
        val_size (float): Proportion of validation set.
        test_size (float): Proportion of test set.

    Returns:
        tuple: (train_t, val_t, test_t) - tensors ready for loaders
    """
    total_size = len(df_input)
    train_size = 1 - (val_size + test_size)

    train_end = int(total_size * train_size)
    val_end = int(total_size * (train_size + val_size))

    train_df = df_input.iloc[:train_end].copy()
    val_df = df_input.iloc[train_end:val_end].copy()
    test_df = df_input.iloc[val_end:].copy()

    # Skip PCA entirely - go straight to tensor conversion
    train_t, val_t, test_t = dataset_to_tensors(train_df, val_df, test_df, sc)

    return (train_t, val_t, test_t)


def data_splitter(df_input, scaler, test):
    """
    Builds a dictionary containing training, validation and test dataframes for
    both the target and independent variables.

    Args:
        df_input (dataframe): contains all data that will be used to train,
            validate and test the models.
        scaler (class): scikit-learn scaling method applied to the data
        test (float): proportion of the length of the test set over the length
            of the whole available data.

    Returns:
        log_reg_data (dictionary): contains all data for the independent variables
        under the 'X' key and all for the target under 'Y', each of these keys being
        subdivided in the keys 'train', 'val' and 'test' each containing training,
        validation and test sets respectively.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        scaler.fit_transform(df_input.drop(["Labels"], axis=1)),
        df_input["Labels"],
        test_size=test,
    )
    train_size = int((1 - test * 2) * len(X_train))
    X_val, y_val = X_train[train_size:], y_train[train_size:]
    X_train, y_train = X_train[:train_size], y_train[:train_size]

    log_reg_data = {
        "X": {"train": X_train, "val": X_val, "test": X_test},
        "Y": {"train": y_train, "val": y_val, "test": y_test},
    }

    return log_reg_data
