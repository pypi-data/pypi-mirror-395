# -*- coding: utf-8 -*-
"""
Functions to cross validate the models
"""

from .evaluation import (
    eval_roc_thresh,
    eval_auroc,
    pred_accuracy,
    pred_recall,
    pred_Fscore,
    pred_precision,
    prob_predictor,
    prob_predictor,
    total_eval,
)


def cross_validate_nn(train_fn, cv_loaders, config, device, progress_callback=None):
    report = []
    total_folds = len(cv_loaders)
    for chunk_num, (trl, val, tel) in enumerate(cv_loaders, start=1):
        trained_model = train_fn(
            config,
            train_loader=trl,
            val_loader=val,
            tuning=False,
            chunk_num=chunk_num,
            num_chunks=len(cv_loaders),
        )["model"]
        vals = total_eval(trained_model, tel, device=device)
        # To CPU for better handling
        acc = vals[1].cpu()
        auc = vals[2].cpu()
        rec = vals[3].cpu()
        fsc = vals[4].cpu()
        prec = vals[6].cpu()
        report.append((acc, auc, rec, fsc, prec))

        # Call progress callback after each fold
        if progress_callback:
            progress_callback(
                fold_num=chunk_num,
                total_folds=total_folds,
                fold_auroc=float(auc.item()),
            )

    return report


def cross_validate_log_reg(train_fn, cv_loaders, config, progress_callback=None):
    report = []
    total_folds = len(cv_loaders)
    for window in range(0, len(cv_loaders)):
        best_model = train_fn(**config, support_probabilities=True)
        fitted_model = best_model.fit(
            cv_loaders[window]["X"]["train"], cv_loaders[window]["Y"]["train"]
        )
        val_predprob = prob_predictor(fitted_model, cv_loaders[window], "val")
        threshold = eval_roc_thresh(val_predprob, cv_loaders[window], "val")
        test_predprob = prob_predictor(fitted_model, cv_loaders[window], "test")

        arguments = {
            "prob_preds": test_predprob,
            "loader": cv_loaders[window],
            "set_type": "test",
        }

        auc = eval_auroc(**arguments)

        arguments["threshold"] = threshold

        acc = pred_accuracy(**arguments)
        rec = pred_recall(**arguments)
        prec = pred_precision(**arguments)
        fsc = pred_Fscore(**arguments)
        report.append([acc, auc, rec, fsc, prec])

        # Call progress callback after each fold
        if progress_callback:
            progress_callback(
                fold_num=window + 1,
                total_folds=total_folds,
                fold_auroc=float(auc),
            )

    return report
