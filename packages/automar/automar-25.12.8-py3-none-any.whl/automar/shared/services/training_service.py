# -*- coding: utf-8 -*-
from pathlib import Path


def train_nn_model(
    args, hyperparameters, train_data, val_data, test_data, progress_callback=None
):
    # Import inside function to avoid loading Ray at module import time
    from automar.core.models import tuning, nn

    if args.tune.model == "GRU":
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
        training=True,
        progress_callback=progress_callback,
    )

    return training(hyperparameters)


def train_logreg_model(hyperparameters, data):
    from sktime.classification.dictionary_based import MUSE
    from automar.core.models.evaluation import prob_predictor, eval_auroc

    hyperparameters["window_inc"] = int(hyperparameters["window_inc"])
    hyperparameters["alphabet_size"] = int(hyperparameters["alphabet_size"])

    log_reg_tuned = MUSE(**hyperparameters, support_probabilities=True)
    log_reg_trained = log_reg_tuned.fit(data["X"]["train"], data["Y"]["train"])

    # Calculate validation AUROC
    val_auroc = None
    try:
        val_pred_probs = prob_predictor(log_reg_trained, data, set_type="val")
        val_auroc = eval_auroc(val_pred_probs, data, set_type="val")
    except Exception as e:
        print(f"Warning: Could not calculate validation AUROC: {e}")

    return {"model": log_reg_trained, "val_auroc": val_auroc}
