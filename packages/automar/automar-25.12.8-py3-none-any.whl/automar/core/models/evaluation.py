# -*- coding: utf-8 -*-
"""
Metrics to evaluate and validate the forecasting models.
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
import torch
from torch.utils.data.dataloader import DataLoader
import torcheval.metrics


def apply_threshold(Y, threshold):
    """
    Given a (n x 2) tensor containig the results of a binary catogerization,
    apply a threshold to determine wether the result is positive or not.

    Args:
        Y (tensor): (n x 2) tensor containig the results of a binary
            catogerization.
        threshold (float): [0., 1.] value of the application threshold.

    Returns:
        Boolean tensor of dimension n with the computed results.
    """
    return torch.where(Y > threshold, torch.tensor(1), torch.tensor(0)).view(-1)


def select_apply_eval(loader_fn, generic_fn, Y, loader, threshold, set_type=None):
    """
    Given two evaluation functions, a predicted tensor, a loader and a
    threshold, select the appropiate evaluation function and apply it.

    Args:
        loader_fn (func): Function to apply if var:`loader` is an
            obj:`DataLoader`.
        generic_fn (func): Function to apply if var:`loader` is an
            obj:`DataLoader`.
        Y: Either a tensor or an array with predicted probabilities.
        loader: Either a tensor data loader or a dictionary of dataframes.
        threshold (float): Optimal threshold, based on the validation ROC.
        set_type (str): Determines the dataframe to be used in the case of.
            inputting a dictionary.

    Returns:
        Application of the evaluator to the data.

    Note:
        Due to the discrepancy in the order of the prediction and target value
        between torcheval and sklearn functions, loader_fn is assumed to take
        as input (pred, target) while generic funct is assumed to take as input
        (target, pred).
    """
    if type(loader) == DataLoader:
        predictions = apply_threshold(Y, threshold)
        real = loader.dataset.tensors[1].to(torch.int64)
        return loader_fn(predictions, real)
    else:
        predictions = np.where(Y >= threshold, 1, 0)
        return generic_fn(loader["Y"][set_type], predictions)


def prob_predictor(model, loader, set_type=None, device=None):
    """
    Generates probability predictions based on
    the trained models, different functions are
    applied to the logistic regression and to the RNNs.

    Args:
        model: Trained model, either the GRU, transformer or logistic
            regression.
        loader: either a tensor data loader or a dictionary of dataframes.
        device (str): Device where to store the generated tensor.
        set_type (str): Determines the dataframe to be used in the case of.
            inputting a dictionary.

    Returns:
        The predicted probability of the target having a value of 1.
    """
    if type(loader) == DataLoader:
        model.eval()
        results = []
        with torch.no_grad():
            for data, labels in loader:
                target = model(data.to(device).float())
                results.append(target)
            return torch.sigmoid(torch.cat(results, dim=0))
    else:
        return model.predict_proba(loader["X"][set_type])[:, 1]


def pred_accuracy(prob_preds, loader, threshold, set_type=None):
    """
    Calculates the accuracy of the model's prediction.

    Args:
        prob_preds: either a tensor or an array with predicted probabilities
        loader: either a tensor data loader or a dictionary of dataframes
        threshold (float): optimal threshold, based on the validation ROC
        set_type (str): determines the dataframe to be used in the case of
            inputting a dictionary.

    Returns:
        Either a tensor or a float with the accuracy of the model.
    """
    return select_apply_eval(
        loader_fn=torcheval.metrics.functional.binary_accuracy,
        generic_fn=accuracy_score,
        Y=prob_preds,
        loader=loader,
        threshold=threshold,
        set_type=set_type,
    )


def pred_precision(prob_preds, loader, threshold, set_type=None):
    """
    Calculates the precision of the model's prediction.

    Args:
        prob_preds: Either a tensor or an array with predicted probabilities.
        loader: Either a tensor data loader or a dictionary of dataframes.
        threshold (float): Optimal threshold, based on the validation ROC.
        set_type (str): Determines the dataframe to be used in the case of
            inputting a dictionary.

    Returns:
        Either a tensor or a float with the precision of the model.
    """
    return select_apply_eval(
        loader_fn=torcheval.metrics.functional.binary_precision,
        generic_fn=precision_score,
        Y=prob_preds,
        loader=loader,
        threshold=threshold,
        set_type=set_type,
    )


def pred_recall(prob_preds, loader, threshold, set_type=None):
    """
    Calculates the recall of the model's prediction.

    Args:
        prob_preds: Either a tensor or an array with predicted probabilities.
        loader: Either tensor data loader or a dictionary of dataframes.
        threshold (float): optimal threshold, based on the validation ROC.
        set_type (str): determines the dataframe to be used in the case of
            inputting a dictionary.

    Returns:
        Either a tensor or a float with the recall of the model.
    """
    return select_apply_eval(
        loader_fn=torcheval.metrics.functional.binary_recall,
        generic_fn=recall_score,
        Y=prob_preds,
        loader=loader,
        threshold=threshold,
        set_type=set_type,
    )


def pred_Fscore(prob_preds, loader, threshold, set_type=None):
    """
    Calculates the F-Score of the model's prediction.

    Args:
        prob_preds: Either a tensor or an array with predicted probabilities.
        loader: Either a tensor data loader or a dictionary of dataframes
        threshold (float): Optimal threshold, based on the validation ROC
        set_type (str): Determines the dataframe to be used in the case of
            inputting a dictionary.

    Returns:
        Either a tensor or a float with the recall of the model.
    """
    return select_apply_eval(
        loader_fn=torcheval.metrics.functional.binary_f1_score,
        generic_fn=f1_score,
        Y=prob_preds,
        loader=loader,
        threshold=threshold,
        set_type=set_type,
    )


def confu_matrix(prob_preds, loader, threshold, set_type=None):
    """
    Computes the confusion matrix based on the model's prediction.

    Args:
        prob_preds: Either a tensor or an array with predicted probabilities.
        loader: Either a tensor data loader or a dictionary of dataframes.
        threshold (float): Optimal threshold, based on the validation ROC.
        set_type (str): Determines the dataframe to be used in the case of.
            inputting a dictionary.

    Returns:
        Either a tensor or an array with the elements of the confusion matrix.
    """
    return select_apply_eval(
        loader_fn=torcheval.metrics.functional.binary_confusion_matrix,
        generic_fn=confusion_matrix,
        Y=prob_preds,
        loader=loader,
        threshold=threshold,
        set_type=set_type,
    )


def eval_Youden(fpr, tpr, thresh):
    """
    Calculates Youden's J statistic and applies it to identify the optimal
        threshold.

    Args:
        fpr (array): Specificity, false positive rates.
        tpr (array): Sensitivity, true positive rates.
        thresh (array): ROC thresholds.

    Returns:
        optimal_threshold (float): threshold with.  highest J.
    """
    J = tpr - fpr
    optimal_idx = np.argmax(J)
    optimal_threshold = thresh[optimal_idx]
    return optimal_threshold


def eval_roc_thresh(prob_preds, loader, set_type=None):
    """
    Calculates the optimal prediction threshold based on the model's ROC.

    Args:
        prob_preds: Either a tensor or an array of predicted probabilities.
        loader: Either a data loader or a dictionary of dataframes.
        set_type: Determines the dataframe to be used in the case of inputting
            a dictionary.

    Returns:
        threshold (float): see the output of :func: eval_Youden
    """
    if type(loader) == DataLoader:
        true_vals = []
        for _, target in loader:
            true_vals.append(target)
        true_vals = torch.concat(true_vals).detach().cpu().numpy()
        predictions = prob_preds.view(-1).cpu()
    else:
        true_vals = loader["Y"][set_type]
        predictions = prob_preds

    fpr, tpr, thresh = roc_curve(true_vals, predictions)
    threshold = eval_Youden(fpr, tpr, thresh)
    return threshold


def eval_auroc(prob_preds, loader, set_type=None):
    """
    Calculates the AUROC of the model's predictions.

    Args:
        prob_preds: Either a tensor or an array of predicted probabilities.
        loader: Either a data loader or a dictionary of dataframes.
        set_type: Determines the dataframe to be used in the case of inputting
            a dictionary.

    Returns:
        Either a tensor or a float of the area under the ROC curve.
    """
    if type(loader) == DataLoader:
        predictions = prob_preds.view(-1)
        real = loader.dataset.tensors[1].to(torch.int64)
        return torcheval.metrics.functional.binary_auroc(predictions, real)
    else:
        return roc_auc_score(loader["Y"][set_type], prob_preds)


def evaluate(model, loader, criterion, device):
    """
    Calculates the average value of the loss function.

    Args:
        model: The trained model, either the GRU, transformer
            or logistic regression.
        loader: Either a tensor data loader or a
            dictionary of dataframes.
        criterion (class): Loss function.
        device (str): Device where to store the generated tensor.

    Returns:
        Average valiue of the loss function.
    """
    model.eval()
    n_samples: int = 0
    avg_loss: float = 0.0
    with torch.no_grad():
        for data, labels in loader:
            n_samples = data.shape[0]
            target = model(data.to(device).float())
            loss = criterion(target.view(-1), labels.to(device).float())
            avg_loss += loss.item() / n_samples
    return avg_loss / len(loader)


def total_eval(model, loader, device, criterion=None, threshold=None):
    """
    Convenience function that runs all evaluation functions.

    Args:
        model: The trained model, either the GRU, transformer or logistic
            regression.
        loader: Either a tensor data loader or a dictionary of dataframes.
        device (str): Device where to store the generated tensor.
        criterion (class): Loss function.
        threshold (float): Optimal threshold, based on the validation ROC.

    Returns:
        prediction: See the output of :func: prob_predictor.
        accuracy: See the output of :func: pred_accuracy.
        auroc: See the output of :func: eval_auroc.
        recall: See the output of :func: pred_recall.
        fscore: See the output of :func: pred_Fscore.
        con_mat: See the output of :func: confu_matrix.
        precision: See the output of :func: pred_precision.
    """
    if type(loader) == DataLoader:
        prediction = prob_predictor(model, loader, device=device)

        if threshold is None:
            threshold = eval_roc_thresh(prediction, loader)

        arguments = {"prob_preds": prediction, "loader": loader, "threshold": threshold}
    else:
        prediction = prob_predictor(model, loader, "test", device=device)
        arguments = {
            "prob_preds": prediction,
            "loader": loader,
            "threshold": threshold,
            "set_type": "test",
        }

    accuracy = pred_accuracy(**arguments)
    recall = pred_recall(**arguments)
    fscore = pred_Fscore(**arguments)
    con_mat = confu_matrix(**arguments)
    precision = pred_precision(**arguments)

    del arguments["threshold"]
    auroc = eval_auroc(**arguments)

    if criterion:
        loss = evaluate(model, loader, criterion, device)
        return [prediction, accuracy, auroc, loss]
    return [prediction, accuracy, auroc, recall, fscore, con_mat, precision]
