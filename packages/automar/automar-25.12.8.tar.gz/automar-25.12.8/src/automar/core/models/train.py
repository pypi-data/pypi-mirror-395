# -*- coding: utf-8 -*-
"""
Helper functions for model training.
"""

import ray
from .evaluation import total_eval
from tqdm import tqdm


def train(model, train_loader, optimizer, criterion, device):
    """
    Given a model and a train loader, perform an a training step and return the
    loss average.

    Args:
        model: Model that will be trained.
        train_loader: Loader that will be used to train the model.
        optimizer: Optimizer to be used for the training step.
        criterion: Criterion to be applied to compute the loss.
        device (str): Device where to store the produced tensors.

    Returns:
        float: Computed loss average for the training set.
    """
    model.train()
    total_loss = 0.0
    total_n = 0

    for x, label in train_loader:
        n = x.shape[0]
        optimizer.zero_grad(set_to_none=True)
        out = model(x.to(device).float())
        loss = criterion(out.view(-1), label.to(device).float())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * n
        total_n += n

    return total_loss / total_n


def epoch(
    model,
    train_loader,
    val_loader,
    optimizer,
    criterion,
    scheduler,
    device,
    tuning=False,
    avg_losses=None,
    val_auroc=None,
    val_lr=None,
):
    """
    Perform a train + evaluation epoch.

    Args:
        model: Model that will be trained and evaluated.
        train_loader: Loader that will be used to train the model.
        val_loader: Loader that will be used to evaluate the model.
        optimizer: Optimizer to be used for the training step.
        criterion: Criterion to be applied to compute the loss.
        scheduler: Scheduler to be used during the epoch.
        device (str): Device where to store the produced tensors.
        tuning (bool, optional): Wether to report or not the AUROC to Ray Tune.
    """
    train_avg_loss = train(
        model=model,
        train_loader=train_loader,
        optimizer=optimizer,
        criterion=criterion,
        device=device,
    )
    vals = total_eval(
        model=model, loader=val_loader, criterion=criterion, device=device
    )
    val_avg_loss = vals[3]
    scheduler.step(val_avg_loss)
    lr = optimizer.param_groups[0]["lr"]
    preds = vals[0]
    acc = vals[1]
    auc = vals[2]
    if type(avg_losses) == list:
        avg_losses.append(train_avg_loss)
    if type(val_auroc) == list:
        val_auroc.append(auc.item())
    if type(val_lr) == list:
        val_lr.append(lr)
    if tuning:
        ray.tune.report({"AUROC": float(auc)})
    else:
        return train_avg_loss
