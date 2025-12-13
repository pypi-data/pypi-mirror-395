import pandas as pd
import joblib
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from automar.shared.persistence.library import (
    DataKind,
    gen_filename,
    get_dirs,
    Periods,
)

OUTPUT_FORMAT = "joblib"
PATH_TO_PCA = "out/pca"  # PCA objects (.pkl)
PATH_TO_PCA_DATA = "out/pca/data"  # PCA transformed dataframes


def load_pca(pca_path):
    """
    Load PCA object, handling both old format (direct PCA) and new format (dict with feature names).

    Returns:
        PCA object (for backward compatibility)
    """
    with open(pca_path, "rb") as fn:
        data = joblib.load(fn)

    # Handle both old and new formats
    if isinstance(data, dict) and "pca" in data:
        return data["pca"]
    else:
        return data


def save_pca(pca, pca_path, feature_names=None):
    """
    Save PCA object with optional feature names for visualization.

    Args:
        pca: Fitted PCA object
        pca_path: Path to save the PCA
        feature_names: Optional list of feature names for better visualization
    """
    # Store as dictionary if feature names provided, otherwise just the PCA
    if feature_names is not None:
        data = {"pca": pca, "feature_names": feature_names}
    else:
        data = pca
    joblib.dump(data, pca_path)


def gen_pca_filename(
    industry,
    dir_path=None,
    history=Periods.Y10,
    datest=None,
    datend=None,
    format=OUTPUT_FORMAT,
):
    # Handle datest: convert date object to string, leave string as-is
    if datest and not isinstance(datest, str):
        datest = datest.strftime("%Y-%m-%d")
    # Handle datend: convert date object to string, leave string as-is
    if datend and not isinstance(datend, str):
        datend = datend.strftime("%Y-%m-%d")
    return get_dirs(root=dir_path, create_dirs=True, end=PATH_TO_PCA) / gen_filename(
        industry=industry,
        history=history,
        datest=datest,
        date=datend,
        kind=DataKind.PCA,
        ticker=None,
        format=format,
    )


def prepare_data(dataset):
    return (
        dataset.drop(columns=["Labels"])
        .select_dtypes(include=["number"])
        .groupby(dataset["Date"])
        .mean()
    )


def prcoan(dataset, default=0, alpha=0.05, drop=True):
    if default == 0:
        default = None

    pca_ = PCA(default)
    data_prepared = prepare_data(dataset)
    data_scaled = StandardScaler().fit_transform(data_prepared)
    pca_.fit(data_scaled)

    pca_num = len(
        pca_.explained_variance_ratio_[pca_.explained_variance_ratio_ > alpha]
    )

    if len(pca_.components_) > pca_num and drop == True:
        pca_ = PCA(pca_num)
        pca_.fit(data_scaled)

    # Return PCA and feature names for visualization
    feature_names = list(data_prepared.columns)
    return pca_, feature_names


def build_pca_df(pca, input_df):
    data_prepared = prepare_data(input_df)
    pca_results = pca.transform(StandardScaler().fit_transform(data_prepared))
    return data_prepared, pd.DataFrame(
        pca_results,
        index=data_prepared.index,
        columns=[f"Industry{ii+1}" for ii in range(pca.n_components)],
    )
