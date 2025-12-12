import pandas as pd
import numpy as np
from sklearn.metrics import recall_score, balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold, KFold
from model_monitoring.performance_measures import compute_unsupervised_metric
import lightgbm as lgb


def lift_score(y_true, y_prob, method: str = "percentile", percentile: float = 0.2, threshold: float = 0.5):
    """Calculates the lift score which compares the model true positive rate versus a random choice.

    Args:
        y_true (np.array, pd.Series): real value of target
        y_prob (np.array, pd.Series): predicted probability of the target
        method (str, optional): 'percentile' or 'threshold'. If percentile it uses the defined percentiles to set the cutoff.
            If threshold it uses the defined threshold as cutoff. Default percentile
        percentile (float, optional): Percentile to use to get the cutoff. Defaults to 0.2.
        threshold (float, optional): Threshold to use as cutoff. Defaults to 0.5.

    Returns:
        float: lift score
    """
    checker_te = pd.DataFrame({"events": y_true, "prob": y_prob})
    if method == "percentile":
        cutoff = checker_te.prob.quantile(q=1 - percentile)
    else:
        cutoff = threshold
    if checker_te["events"].sum() == 0:
        raise ValueError("y_true always 0")

    tpr_db = checker_te.loc[checker_te.prob > cutoff]
    tpr_model = tpr_db["events"].sum() / tpr_db.shape[0]
    tpr_random = checker_te["events"].sum() / checker_te.shape[0]

    return tpr_model / tpr_random


def gain_score(y_true, y_prob, method: str = "percentile", percentile: float = 0.2, threshold: float = 0.5):
    """Calculates the gain score which identifies the recall at a cutoff.

    Args:
        y_true (np.array, pd.Series): real value of target
        y_prob (np.array, pd.Series): predicted probability of the target
        method (str, optional): 'percentile' or 'threshold'. If percentile it uses the defined percentiles to set the cutoff.
            If threshold it uses the defined threshold as cutoff. Default percentile
        percentile (float, optional): Percentile to use to get the cutoff. Defaults to 0.2.
        threshold (float, optional): Threshold to use as cutoff. Defaults to 0.5.

    Returns:
        float: gain score
    """
    checker_te = pd.DataFrame({"events": y_true, "prob": y_prob})
    if method == "percentile":
        cutoff = checker_te.prob.quantile(q=1 - percentile)
    else:
        cutoff = threshold
    if checker_te["events"].sum() == 0:
        raise ValueError("y_true always 0")
    return recall_score(y_true, np.where(checker_te.prob > cutoff, 1, 0))


def classification_clustering(
    data, labels, n_splits=5, classification_clustering_metric=balanced_accuracy_score, **kwargs
):
    """Train model for classification clustering method and compute classification clustering metric.

    Args:
        data: (pd.Dataframe): original data matrix
        labels: (pd.series/np.array): cluster labels
        test_size (float, optional): ratio between original dataset and test set dimensions. Defaults to 0.3
        classification_clustering_metric (func, optional): classification clustering metric to compute

    Returns:
        float: classification_clustering_metric
    """
    model = lgb.LGBMClassifier(class_weight="balanced")
    kf = KFold(n_splits=n_splits, shuffle=True)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True)
    lst_perf = []
    try:
        for train_index, test_index in skf.split(data, labels):
            x_train_fold = data.loc[train_index]
            x_test_fold = data.loc[test_index]
            y_train_fold, y_test_fold = labels[train_index], labels[test_index]
            model.fit(x_train_fold, y_train_fold)
            predicted_labels = model.predict(x_test_fold)
            metric = compute_unsupervised_metric(
                y_test_fold, predicted_labels, classification_clustering_metric, **kwargs
            )
            lst_perf.append(metric)
    except Exception:
        for train_index, test_index in kf.split(data, labels):
            x_train_fold = data.loc[train_index]
            x_test_fold = data.loc[test_index]
            y_train_fold, y_test_fold = labels[train_index], labels[test_index]
            model.fit(x_train_fold, y_train_fold)
            predicted_labels = model.predict(x_test_fold)
            metric = compute_unsupervised_metric(
                y_test_fold, predicted_labels, classification_clustering_metric, **kwargs
            )
            lst_perf.append(metric)
    return np.median(lst_perf)
