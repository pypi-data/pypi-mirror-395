# schemas.py
from __future__ import annotations
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional, Literal, List

from pydantic import BaseModel, Field, model_validator

from automar.shared.persistence.library import Periods, ValidFormats, VALID_INDUSTRY

# Define SCALERS here to avoid importing tuning.py (which imports Ray and PyTorch at module level)
SCALERS_KEYS = ["standard", "minmax", "robust"]


class ExtractOptions(BaseModel):
    ticker: Optional[str] = Field(None, description="Ticker symbol (e.g. AAPL)")
    industry: Optional[str] = Field(
        None, description=f"Industry name ∈ {{{', '.join(VALID_INDUSTRY)}}}"
    )
    history: Periods = Field(Periods.Y10)
    force: bool = Field(
        False, description="Force re-download even if data already exists"
    )
    dir_path: Optional[Path] = None
    extract_file: Optional[Path] = None
    format: ValidFormats = Field(ValidFormats.FEATHER)
    datest: Optional[date] = None
    datend: Optional[date] = Field(
        default_factory=lambda: (datetime.today() - timedelta(days=1)).date()
    )
    ensure_combined_dataset: bool = Field(
        False,
        description=(
            "When true, always persist a combined industry+ticker file even if the ticker"
            " already exists in another dataset. Frontend uses this to guarantee that"
            " each extraction requested from the UI materializes as a standalone file."
        ),
    )


class PCAOptions(BaseModel):
    n_components: int = 0
    alpha: float = 0.05
    drop: bool = True
    data_file: Optional[Path] = None
    pca_file: Optional[Path] = None
    pca_force: bool = False
    notdf: bool = False
    pca_df_file: Optional[Path] = None
    dataset_path: Optional[str] = Field(
        None, description="Path to dataset file to use for PCA"
    )
    pca_obj_dir: Optional[Path] = (
        None  # Custom directory for auto-generated PCA object files
    )
    pca_df_dir: Optional[Path] = (
        None  # Custom directory for auto-generated PCA dataframe files
    )


class LoaderOptions(BaseModel):
    tsize: int = 20
    batch_size: int = 50
    dopca: bool = True
    val_size: float = 0.15
    test_size: float = 0.15
    device: Optional[str] = None  # Lazy-loaded to avoid PyTorch import at startup
    cores: int = 4
    gpu_fraction: float = 0.25
    seed: int = 2
    scaler: str = Field("standard", pattern="|".join(SCALERS_KEYS))


class TuningOptions(BaseModel):
    tuning_path: Optional[Path] = None
    output_dir: Optional[Path] = (
        None  # Custom directory for auto-generated tuning files
    )
    param_path: str = (
        "out/hyper"  # Base path, model-specific subdirectory added automatically
    )
    num_samples: int = 50
    epochs: int = 50
    gpu_per_trial: float = 1.0
    model: Literal["GRU", "transformer", "log-reg"] = "GRU"
    search_space_path: Optional[str] = None  # Path to custom search space file


class TrainingOptions(BaseModel):
    cfg_path: Optional[Path] = None
    pca_path: Optional[Path] = None
    mdl_path: Optional[Path] = None
    save_dir: Optional[Path] = None  # Custom directory for auto-generated model files
    id: int = 1
    manual_hyperparams_toml: Optional[str] = None  # Manual TOML content


class CrossvalidateOptions(BaseModel):
    out_path: Optional[Path] = None
    results_dir: Optional[Path] = (
        None  # Custom directory for auto-generated output files
    )
    n_split: int = 5
    manual_hyperparams_toml: Optional[str] = None  # Manual TOML content


class PredictionOptions(BaseModel):
    """Options for model prediction/inference"""

    model_path: str = Field(..., description="Path to trained model .pth file")
    pca_path: Optional[str] = Field(
        None,
        description="Optional path to PCA .joblib file if model was trained with PCA",
    )
    model_type: Optional[Literal["GRU", "transformer", "log-reg"]] = Field(
        None, description="Model type (auto-detected from checkpoint if not specified)"
    )
    save_dir: Optional[Path] = Field(
        None,
        description="Custom directory for saving predictions (default: out/preds/)",
    )
    mode: Literal["eval", "forecast"] = Field(
        "eval",
        description="Prediction mode: 'eval' for test set evaluation, 'forecast' for future predictions",
    )
    forecast_days: Optional[int] = Field(
        1,
        ge=1,
        le=30,
        description="Number of future business days to forecast (forecast mode only, default: 1)",
    )


from enum import Enum


class ModelName(str, Enum):
    GRU = "GRU"
    TRANSFORMER = "transformer"
    LOG_REG = "log-reg"


class APIOptions(BaseModel):
    host: str = Field("127.0.0.1", description="Host to bind the server to")
    port: int = Field(8000, description="Port to bind the server to")
    reload: bool = Field(False, description="Enable auto-reload for development")
    workers: int = Field(1, description="Number of worker processes")


def _create_extract_options():
    """Create default ExtractOptions without triggering validation"""
    return ExtractOptions.model_construct()


def _create_pca_options():
    """Create default PCAOptions"""
    return PCAOptions()


def _create_loader_options():
    """Create default LoaderOptions"""
    return LoaderOptions()


def _create_tuning_options():
    """Create default TuningOptions"""
    return TuningOptions()


def _create_training_options():
    """Create default TrainingOptions"""
    return TrainingOptions()


def _create_crossvalidate_options():
    """Create default CrossvalidateOptions"""
    return CrossvalidateOptions()


def _create_prediction_options():
    """Create default PredictionOptions"""
    return PredictionOptions(model_path="")  # Required field, empty default


def _create_api_options():
    """Create default APIOptions"""
    return APIOptions()


class GlobalConfig(BaseModel):
    command: Literal[
        "extract", "pca", "tune", "train", "crossvalidate", "predict", "api", "gui"
    ]
    extract: ExtractOptions = Field(default_factory=_create_extract_options)
    pca: PCAOptions = Field(default_factory=_create_pca_options)
    loader: LoaderOptions = Field(default_factory=_create_loader_options)
    tune: TuningOptions = Field(default_factory=_create_tuning_options)
    train: TrainingOptions = Field(default_factory=_create_training_options)
    crossvalidate: CrossvalidateOptions = Field(
        default_factory=_create_crossvalidate_options
    )
    predict: PredictionOptions = Field(default_factory=_create_prediction_options)
    api: APIOptions = Field(default_factory=_create_api_options)

    @model_validator(mode="after")
    def check_ticker_or_industry_or_datafile(self):
        if self.command in [
            "extract",
            "pca",
            "tune",
            "train",
            "crossvalidate",
            "predict",
        ]:
            if not (
                self.extract.ticker
                or self.extract.industry
                or self.pca.data_file
                or self.pca.dataset_path
            ):
                raise ValueError(
                    "Must specify either 'ticker', 'industry', 'data_file', or 'dataset_path'"
                )
        return self
