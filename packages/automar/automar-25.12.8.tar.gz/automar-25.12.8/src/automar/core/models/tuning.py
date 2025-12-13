# -*- coding: utf-8 -*-
"""
Helper functions for the hyperparameter tuning.
"""

from collections import deque
from tqdm import tqdm
import torch
import ray
from sktime.classification.dictionary_based import MUSE

from .train import epoch
from .evaluation import prob_predictor, eval_auroc


def custom_trial_dirname_creator(trial):
    # Create a shorter name based on trial parameters
    return f"trial_{trial.trial_id}"


def train_model_builder(
    model,
    train_loader,
    val_loader,
    test_loader,
    device,
    tuning,
    optimizer=torch.optim.Adam,
    criterion=torch.nn.BCEWithLogitsLoss,
    scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau,
    training=False,
    chunk_num=None,
    num_chunks=None,
    progress_callback=None,
):
    def proxy(
        config,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        tuning=tuning,
        training=training,
        chunk_num=chunk_num,
        num_chunks=num_chunks,
    ):
        return train_model(
            model=model,
            config=config,
            train_loader=train_loader,
            val_loader=val_loader,
            test_loader=test_loader,
            device=device,
            tuning=tuning,
            optimizer=optimizer,
            criterion=criterion,
            scheduler=scheduler,
            training=training,
            chunk_num=chunk_num,
            num_chunks=num_chunks,
            progress_callback=progress_callback,
        )

    return proxy


def train_model(
    model,
    config,
    train_loader,
    val_loader,
    test_loader,
    device,
    tuning=True,
    optimizer=torch.optim.Adam,
    criterion=torch.nn.BCEWithLogitsLoss,
    scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau,
    training=False,
    chunk_num=None,
    num_chunks=None,
    progress_callback=None,
):
    model = model(**config["model"])
    model = model.to(device)

    optimizer = optimizer(model.parameters(), **config["optimizer"])
    criterion = criterion(**config["criterion"])
    scheduler = scheduler(optimizer, **config["scheduler"])

    avg_losses = []
    val_auroc = []
    val_lr = []

    epoch_args = [
        model,
        train_loader,
        val_loader,
        optimizer,
        criterion,
        scheduler,
        device,
        tuning,
        avg_losses,
        val_auroc,
        val_lr,
    ]

    total_epochs = config["epochs"]

    if training:
        for epoch_index in tqdm(range(total_epochs), desc="Training epochs"):
            _ = epoch(*epoch_args)
            # Call progress callback after each epoch (for web API progress tracking)
            if progress_callback:
                progress_callback(
                    epoch_num=epoch_index + 1,
                    total_epochs=total_epochs,
                    avg_losses=avg_losses,
                    val_auroc=val_auroc,
                    val_lr=val_lr,
                )
    elif chunk_num and num_chunks:
        for epoch_index in tqdm(
            range(total_epochs),
            desc=f"Training epochs (chunk {chunk_num} of {num_chunks})",
        ):
            _ = epoch(*epoch_args)
            # Call progress callback after each epoch
            if progress_callback:
                progress_callback(
                    epoch_num=epoch_index + 1,
                    total_epochs=total_epochs,
                    avg_losses=avg_losses,
                    val_auroc=val_auroc,
                    val_lr=val_lr,
                )
    else:
        _ = deque(map(lambda x: epoch(*epoch_args), range(total_epochs)))

    if tuning:
        return None
    return {"model": model, "loss": avg_losses, "aouroc": val_auroc, "lr": val_lr}


def train_log_reg(config, data_dic):
    model = MUSE(
        support_probabilities=True,
        window_inc=int(config["window_inc"]),
        alphabet_size=int(config["alphabet_size"]),
        feature_selection=config["feature_selection"],
        anova=False,
        variance=True,
    )
    model.fit(data_dic["X"]["train"], data_dic["Y"]["train"])

    # Calculate the AUROC
    prob_preds = prob_predictor(model, data_dic, set_type="val")
    auroc = eval_auroc(prob_preds, data_dic, set_type="val")

    # Report the AUROC value to Ray Tune
    ray.tune.report({"AUROC": auroc})


def train_log_reg_builder(data_dic):
    def proxy(config):
        train_log_reg(config, data_dic)

    return proxy
