# -*- coding: utf-8 -*-
"""
Module to parse the configuration.
"""

from pydantic import BaseModel, Field, model_validator
from typing import Callable, Literal, Optional, Self
import tomli
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler


scalers_dic = {
    "standard": StandardScaler(),
    "minmax": MinMaxScaler(),
    "robust": RobustScaler(),
}


class ExtractorConfig(BaseModel):
    tick_input: str = Field(
        default="MSFT", description="Symbol of the S&P 500 company to study"
    )
    hist_length: str = Field(
        default="10y", description="Length of data history to retrieve for the study"
    )
    industry: Optional[str] = Field(
        default=None, description="Industry to extract data from"
    )


class PCAConfig(BaseModel):
    def_comp: Optional[int] = Field(
        default=None,
        description="Maximum number of potential principal components from the industry average set",
    )
    cutoff_var: float = Field(
        default=0.05,
        description="Significance level for rejecting principal components",
    )


class DataConfig(BaseModel):
    n_split: int = Field(
        default=10, description="Number of batches the loader splits the data into"
    )
    sc_alg: Literal["standard", "minmax", "robust"] = Field(
        default="minmax", description="Scaling method"
    )
    sc: Optional[Callable] = None
    tsize: int = Field(
        default=20, description="Number of observations used to predict the next one"
    )
    batch_size: int = Field(
        default=50, description="Number of observations contained in each batch of data"
    )
    n_split_gw: int = Field(
        default=5, description="Number of batches for growing windows"
    )
    test_size: float = Field(
        default=0.15, description="Percentage of data allocated to test subset"
    )
    val_size: float = Field(
        default=0.15, description="Percentage of data allocated to validation subset"
    )

    @model_validator(mode="after")
    def fill_sc(self) -> Self:
        self.sc = scalers_dic[self.sc_alg]
        return self


class TrainingConfig(BaseModel):
    device: str = Field(default="cpu", description="Select device to use")
    tuning_epochs: int = Field(default=2, description="Number of tuning epochs")
    training_epochs: int = Field(default=2, description="Number of training epochs")
    samples: int = Field(default=5, description="Number of tuning samples")
    drop_prob: float = Field(default=0.5, description="Drop probability")
    cpu: int = Field(default=2, description="Number of CPUs used by raytune task")
    reset: bool = Field(
        default=False, description="Overwrite preexisting tuning and training results"
    )


class VisualizationConfig(BaseModel):
    inflation: bool = Field(
        default=True, description="If true, adjust prices for inflation"
    )


class Config(BaseModel):
    extractor: ExtractorConfig = Field(default_factory=ExtractorConfig)
    pca: PCAConfig = Field(default_factory=PCAConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    visualization: VisualizationConfig = Field(default_factory=VisualizationConfig)


def build_config(fn: Path | str) -> Config:
    fn_path = Path(fn)
    if fn_path.exists():
        with open(fn_path, "rb") as ff:
            config_dic = tomli.load(ff)
        config = Config(**config_dic)  # Unpack the dictionary into the Pydantic model
    else:
        config = Config()  # Use defaults
    return config
