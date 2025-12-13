# -*- coding: utf-8 -*-
from automar.core.models.crossval import cross_validate_nn, cross_validate_log_reg
from automar.core.models import tuning, nn
from automar.core.preprocessing.tensor import growing_windows
from automar.core.preprocessing.loaders import vecs_to_series_loaders


def prepare_gw_loaders(gw_vecs, tsize, batch_size, device):
    """
    Prepares loaders for growing windows data.

    Args:
        gw_vecs (tuple): Tuple of datasets produced by growing windows.
        tsize (int): Length of the rolling time window fed to the network.
        batch_size (int): Number of windows per batch.
        device (str): Device where the tensors will be stored (e.g. 'cpu' or 'cuda:0').

    Returns:
        tuple: Contains train_loader, val_loader, and test_loader.
    """
    return tuple(
        map(
            lambda x: vecs_to_series_loaders(
                x, tsize=tsize, batch_size=batch_size, device=device
            ),
            gw_vecs,
        )
    )


def prepare_growing_windows(
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
    Prepares growing windows data loaders.

    Args:
        df_input (dataframe): Complete dataframe containing all data for training,
            validation, and testing.
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
    # Call the growing_windows function
    gw_loaders, lengths = growing_windows(
        df_input,
        n_split=n_split,
        sc=sc,
        test_size=test_size,
        val_size=val_size,
        df_pca=df_pca,
        def_comp=def_comp,
        cutoff_var=cutoff_var,
    )

    return gw_loaders, lengths


def crossval_nn(
    args,
    hyperparameters,
    train_data,
    val_data,
    test_data,
    gw_loaders,
    progress_callback=None,
):
    if args.tune.model.lower() == "gru":
        model = nn.GRUNet
    elif args.tune.model == "transformer":
        model = nn.Transnet

    training = tuning.train_model_builder(
        model=model,
        train_loader=train_data,
        val_loader=val_data,
        test_loader=test_data,
        device=args.loader.device,
        tuning=False,
        training=False,
    )

    crossval_results = cross_validate_nn(
        training,
        gw_loaders,
        hyperparameters,
        device=args.loader.device,
        progress_callback=progress_callback,
    )

    return crossval_results


def crossval_lr(log_reg_cross_data, log_reg_best, progress_callback=None):
    from sktime.classification.dictionary_based import MUSE

    # Convert string values to int for MUSE parameters
    config = log_reg_best.copy()
    config["window_inc"] = int(config["window_inc"])
    config["alphabet_size"] = int(config["alphabet_size"])

    return cross_validate_log_reg(
        MUSE, log_reg_cross_data, config, progress_callback=progress_callback
    )
