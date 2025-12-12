def compute_metric(y_true, y_pred, metric, **kwargs):
    """Compute the supervised metric scoring.

    Args:
        y_true (pd.Series/np.array): true values of target
        y_pred (pd.Series/np.array): predictions/scores of target
        metric (function): metric function

    Returns:
        float: metric scoring performance
    """
    return metric(y_true, y_pred, **kwargs)


def compute_unsupervised_metric(data, labels, metric, **kwargs):
    """Compute the unsupervised metric scoring.

    Args:
        data (pd.Dataframe): original data matrix
        labels (pd.series/np.array): cluster labels
        metric (function): metric function

    Returns:
        float: metric scoring performance
    """
    return metric(data, labels, **kwargs)
