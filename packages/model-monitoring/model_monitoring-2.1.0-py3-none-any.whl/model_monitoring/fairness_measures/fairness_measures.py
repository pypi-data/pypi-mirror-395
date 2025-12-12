from warnings import warn
import numpy as np

from sklearn.metrics import recall_score, precision_score
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression


class UndefinedMetricWarning(UserWarning):
    """Warning used when the metric is invalid."""


# ============================ GROUP FAIRNESS CLASSIFICATION ==================================
def statistical_parity_difference(y_true, y_pred, fair_attr, unpriv_group=0, multiclass_agg_mode="max", **kwargs):
    """Fairness metric for binary classification: it returns the difference between the computed PR (Positive Rate) between the two groups.

    Args:
        y_true (pd.Series/np.array): ground truth target values.
        y_pred (pd.Series/np.array): estimated targets.
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics.
        unpriv_group (int/float/str/list, optional): the label of the unprivileged group in the features fair_attr. Defaults to 0.
        multiclass_agg_mode (str, optional): mode of aggregating metric scores for multiclassification problem among 'max' and 'sum'. Defaults to 'max'.

    Returns:
        float: statistical parity difference metric score
    """
    multiclass = False
    # For multiclassifcation ML problem
    if len(np.unique(y_true)) > 2:
        if multiclass_agg_mode not in ["max", "sum"]:
            raise ValueError(f"{multiclass_agg_mode} is not a valid aggregation mode. Choose between ['max','sum'].")
        list_score = []
        for cl in np.unique(y_true):
            y_true_multi = np.where(y_true == cl, 1, 0)
            y_pred_multi = np.where(y_pred == cl, 1, 0)
            # One Fairness Attribute
            try:
                unpr_pr_group = positive_rate(
                    y_true_multi[fair_attr == unpriv_group], y_pred_multi[fair_attr == unpriv_group], **kwargs
                )
                pr_pr_group = positive_rate(
                    y_true_multi[fair_attr != unpriv_group], y_pred_multi[fair_attr != unpriv_group], **kwargs
                )
            # More Fairness Attributes
            except Exception:
                unpr_pr_group = positive_rate(
                    y_true_multi[(fair_attr == unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr == unpriv_group).all(axis=1)],
                    **kwargs,
                )
                pr_pr_group = positive_rate(
                    y_true_multi[(fair_attr != unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr != unpriv_group).all(axis=1)],
                    **kwargs,
                )
            list_score.append(unpr_pr_group - pr_pr_group)
        multiclass = True
    else:
        # One Fairness Attribute
        try:
            unpr_pr_group = positive_rate(
                y_true[fair_attr == unpriv_group], y_pred[fair_attr == unpriv_group], **kwargs
            )
            pr_pr_group = positive_rate(y_true[fair_attr != unpriv_group], y_pred[fair_attr != unpriv_group], **kwargs)
        # More Fairness Attributes
        except Exception:
            unpr_pr_group = positive_rate(
                y_true[(fair_attr == unpriv_group).all(axis=1)],
                y_pred[(fair_attr == unpriv_group).all(axis=1)],
                **kwargs,
            )
            pr_pr_group = positive_rate(
                y_true[(fair_attr != unpriv_group).all(axis=1)],
                y_pred[(fair_attr != unpriv_group).all(axis=1)],
                **kwargs,
            )
    if multiclass:
        if multiclass_agg_mode == "max":
            return max(list_score, key=abs)
        else:
            return sum(map(abs, list_score))
    else:
        return unpr_pr_group - pr_pr_group


def disparate_impact_ratio(y_true, y_pred, fair_attr, unpriv_group=0, **kwargs):
    """Fairness metric for binary classification: it returns the ratio between the computed PR (Positive Rate) between the two groups.

    Args:
        y_true (pd.Series/np.array): ground truth target values.
        y_pred (pd.Series/np.array): estimated targets.
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics.
        unpriv_group (int/float/str/list, optional): the label of the unprivileged group in the features fair_attr. Defaults to 0.

    Returns:
        float: disparate impact ratio metric score
    """
    # One Fairness Attribute
    try:
        unpr_pr_group = positive_rate(y_true[fair_attr == unpriv_group], y_pred[fair_attr == unpriv_group], **kwargs)
        pr_pr_group = positive_rate(y_true[fair_attr != unpriv_group], y_pred[fair_attr != unpriv_group], **kwargs)
    # More Fairness Attributes
    except Exception:
        unpr_pr_group = positive_rate(
            y_true[(fair_attr == unpriv_group).all(axis=1)], y_pred[(fair_attr == unpriv_group).all(axis=1)], **kwargs
        )
        pr_pr_group = positive_rate(
            y_true[(fair_attr != unpriv_group).all(axis=1)], y_pred[(fair_attr != unpriv_group).all(axis=1)], **kwargs
        )

    return unpr_pr_group / pr_pr_group


def predictive_parity_difference(
    y_true, y_pred, fair_attr, unpriv_group=0, multiclass_agg_mode="max", zero_division=0, **kwargs
):
    """Fairness metric for binary classification: it returns the difference between the computed precision between the two groups.

    Args:
        y_true (pd.Series/np.array): ground truth target values.
        y_pred (pd.Series/np.array): estimated targets.
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics.
        unpriv_group (int/float/str/list, optional): the label of the unprivileged group in the features fair_attr. Defaults to 0.
        multiclass_agg_mode (str, optional): mode of aggregating metric scores for multiclassification problem among 'max' and 'sum'. Defaults to 'max'.
        zero_division (int/str optional): it can be 0, 1 or 'warn'. It sets to a value when division with 0 in the denominator.
            When 'warn' it prints the warning and set the division to 0. Deafults to 0.

    Returns:
        float: predictive parity difference metric score
    """
    multiclass = False
    # For multiclassifcation ML problem
    if len(np.unique(y_true)) > 2:
        if multiclass_agg_mode not in ["max", "sum"]:
            raise ValueError(f"{multiclass_agg_mode} is not a valid aggregation mode. Choose between ['max','sum'].")
        list_score = []
        for cl in np.unique(y_true):
            y_true_multi = np.where(y_true == cl, 1, 0)
            y_pred_multi = np.where(y_pred == cl, 1, 0)
            # One Fairness Attribute
            try:
                unpr_pre_group = precision_score(
                    y_true_multi[fair_attr == unpriv_group],
                    y_pred_multi[fair_attr == unpriv_group],
                    zero_division=zero_division,
                    **kwargs,
                )
                pr_pre_group = precision_score(
                    y_true_multi[fair_attr != unpriv_group],
                    y_pred_multi[fair_attr != unpriv_group],
                    zero_division=zero_division,
                    **kwargs,
                )
            # More Fairness Attributes
            except Exception:
                unpr_pre_group = precision_score(
                    y_true_multi[(fair_attr == unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr == unpriv_group).all(axis=1)],
                    zero_division=zero_division,
                    **kwargs,
                )
                pr_pre_group = precision_score(
                    y_true_multi[(fair_attr != unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr != unpriv_group).all(axis=1)],
                    zero_division=zero_division,
                    **kwargs,
                )
            list_score.append(unpr_pre_group - pr_pre_group)
        multiclass = True
    else:
        # One Fairness Attribute
        try:
            unpr_pre_group = precision_score(
                y_true[fair_attr == unpriv_group],
                y_pred[fair_attr == unpriv_group],
                zero_division=zero_division,
                **kwargs,
            )
            pr_pre_group = precision_score(
                y_true[fair_attr != unpriv_group],
                y_pred[fair_attr != unpriv_group],
                zero_division=zero_division,
                **kwargs,
            )
        # More Fairness Attributes
        except Exception:
            unpr_pre_group = precision_score(
                y_true[(fair_attr == unpriv_group).all(axis=1)],
                y_pred[(fair_attr == unpriv_group).all(axis=1)],
                zero_division=zero_division,
                **kwargs,
            )
            pr_pre_group = precision_score(
                y_true[(fair_attr != unpriv_group).all(axis=1)],
                y_pred[(fair_attr != unpriv_group).all(axis=1)],
                zero_division=zero_division,
                **kwargs,
            )
    if multiclass:
        if multiclass_agg_mode == "max":
            return max(list_score, key=abs)
        else:
            return sum(map(abs, list_score))
    else:
        return unpr_pre_group - pr_pre_group


def equal_opportunity_difference(
    y_true, y_pred, fair_attr, unpriv_group=0, multiclass_agg_mode="max", zero_division=0, **kwargs
):
    """Fairness metric for binary classification: it returns the difference between the computed recall between two groups.

    Args:
        y_true (pd.Series/np.array): ground truth target values.
        y_pred (pd.Series/np.array): estimated targets.
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics.
        unpriv_group (int/float/str/list, optional): the label of the unprivileged group in the features fair_attr. Defaults to 0.
        multiclass_agg_mode (str, optional): mode of aggregating metric scores for multiclassification problem among 'max' and 'sum'. Defaults to 'max'.
        zero_division (int/str optional): it can be 0, 1 or 'warn'. It sets to a value when division with 0 in the denominator.
            When 'warn' it prints the warning and set the division to 0. Deafults to 0.

    Returns:
        float: equal opportunity difference metric score
    """
    multiclass = False
    # For multiclassifcation ML problem
    if len(np.unique(y_true)) > 2:
        if multiclass_agg_mode not in ["max", "sum"]:
            raise ValueError(f"{multiclass_agg_mode} is not a valid aggregation mode. Choose between ['max','sum'].")
        list_score = []
        for cl in np.unique(y_true):
            y_true_multi = np.where(y_true == cl, 1, 0)
            y_pred_multi = np.where(y_pred == cl, 1, 0)
            # One Fairness Attribute
            try:
                unpr_rec_group = recall_score(
                    y_true_multi[fair_attr == unpriv_group],
                    y_pred_multi[fair_attr == unpriv_group],
                    zero_division=zero_division,
                    **kwargs,
                )
                pr_rec_group = recall_score(
                    y_true_multi[fair_attr != unpriv_group],
                    y_pred_multi[fair_attr != unpriv_group],
                    zero_division=zero_division,
                    **kwargs,
                )
            # More Fairness Attributes
            except Exception:
                unpr_rec_group = recall_score(
                    y_true_multi[(fair_attr == unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr == unpriv_group).all(axis=1)],
                    zero_division=zero_division,
                    **kwargs,
                )
                pr_rec_group = recall_score(
                    y_true_multi[(fair_attr != unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr != unpriv_group).all(axis=1)],
                    zero_division=zero_division,
                    **kwargs,
                )
            list_score.append(unpr_rec_group - pr_rec_group)
        multiclass = True
    else:
        # One Fairness Attribute
        try:
            unpr_rec_group = recall_score(
                y_true[fair_attr == unpriv_group],
                y_pred[fair_attr == unpriv_group],
                zero_division=zero_division,
                **kwargs,
            )
            pr_rec_group = recall_score(
                y_true[fair_attr != unpriv_group],
                y_pred[fair_attr != unpriv_group],
                zero_division=zero_division,
                **kwargs,
            )
        # More Fairness Attributes
        except Exception:
            unpr_rec_group = recall_score(
                y_true[(fair_attr == unpriv_group).all(axis=1)],
                y_pred[(fair_attr == unpriv_group).all(axis=1)],
                zero_division=zero_division,
                **kwargs,
            )
            pr_rec_group = recall_score(
                y_true[(fair_attr != unpriv_group).all(axis=1)],
                y_pred[(fair_attr != unpriv_group).all(axis=1)],
                zero_division=zero_division,
                **kwargs,
            )
    if multiclass:
        if multiclass_agg_mode == "max":
            return max(list_score, key=abs)
        else:
            return sum(map(abs, list_score))
    else:
        return unpr_rec_group - pr_rec_group


def average_odds_difference(
    y_true, y_pred, fair_attr, unpriv_group=0, multiclass_agg_mode="max", zero_division=0, **kwargs
):
    """Fairness metric for binary classification: it returns the average of the differences between the computed recall and FPR (False Positive Rate) between two groups.

    Args:
        y_true (pd.Series/np.array): ground truth target values.
        y_pred (pd.Series/np.array): estimated targets.
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics.
        unpriv_group (int/float/str/list, optional): the label of the unprivileged group in the features fair_attr. Defaults to 0.
        multiclass_agg_mode (str, optional): mode of aggregating metric scores for multiclassification problem among 'max' and 'sum'. Defaults to 'max'.
        zero_division (int/str optional): it can be 0, 1 or 'warn'. It sets to a value when division with 0 in the denominator.
            When 'warn' it prints the warning and set the division to 0. Deafults to 0.

    Returns:
        float: average odd difference metric score
    """
    multiclass = False
    # For multiclassifcation ML problem
    if len(np.unique(y_true)) > 2:
        if multiclass_agg_mode not in ["max", "sum"]:
            raise ValueError(f"{multiclass_agg_mode} is not a valid aggregation mode. Choose between ['max','sum'].")
        list_score = []
        for cl in np.unique(y_true):
            y_true_multi = np.where(y_true == cl, 1, 0)
            y_pred_multi = np.where(y_pred == cl, 1, 0)
            # One Fairness Attribute
            try:
                unpr_fpr_group = false_positive_rate(
                    y_true_multi[fair_attr == unpriv_group],
                    y_pred_multi[fair_attr == unpriv_group],
                    zero_division=zero_division,
                    **kwargs,
                )
                pr_fpr_group = false_positive_rate(
                    y_true_multi[fair_attr != unpriv_group],
                    y_pred_multi[fair_attr != unpriv_group],
                    zero_division=zero_division,
                    **kwargs,
                )
                unpr_rec_group = recall_score(
                    y_true_multi[fair_attr == unpriv_group],
                    y_pred_multi[fair_attr == unpriv_group],
                    zero_division=zero_division,
                    **kwargs,
                )
                pr_rec_group = recall_score(
                    y_true_multi[fair_attr != unpriv_group],
                    y_pred_multi[fair_attr != unpriv_group],
                    zero_division=zero_division,
                    **kwargs,
                )
            # More Fairness Attributes
            except Exception:
                unpr_fpr_group = false_positive_rate(
                    y_true_multi[(fair_attr == unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr == unpriv_group).all(axis=1)],
                    zero_division=zero_division,
                    **kwargs,
                )
                pr_fpr_group = false_positive_rate(
                    y_true_multi[(fair_attr != unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr != unpriv_group).all(axis=1)],
                    zero_division=zero_division,
                    **kwargs,
                )
                unpr_rec_group = recall_score(
                    y_true_multi[(fair_attr == unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr == unpriv_group).all(axis=1)],
                    zero_division=zero_division,
                    **kwargs,
                )
                pr_rec_group = recall_score(
                    y_true_multi[(fair_attr != unpriv_group).all(axis=1)],
                    y_pred_multi[(fair_attr != unpriv_group).all(axis=1)],
                    zero_division=zero_division,
                    **kwargs,
                )
            list_score.append(((unpr_fpr_group - pr_fpr_group) + (unpr_rec_group - pr_rec_group)) / 2)
        multiclass = True
    else:
        # One Fairness Attribute
        try:
            unpr_fpr_group = false_positive_rate(
                y_true[fair_attr == unpriv_group],
                y_pred[fair_attr == unpriv_group],
                zero_division=zero_division,
                **kwargs,
            )
            pr_fpr_group = false_positive_rate(
                y_true[fair_attr != unpriv_group],
                y_pred[fair_attr != unpriv_group],
                zero_division=zero_division,
                **kwargs,
            )
            unpr_rec_group = recall_score(
                y_true[fair_attr == unpriv_group],
                y_pred[fair_attr == unpriv_group],
                zero_division=zero_division,
                **kwargs,
            )
            pr_rec_group = recall_score(
                y_true[fair_attr != unpriv_group],
                y_pred[fair_attr != unpriv_group],
                zero_division=zero_division,
                **kwargs,
            )
        # More Fairness Attributes
        except Exception:
            unpr_fpr_group = false_positive_rate(
                y_true[(fair_attr == unpriv_group).all(axis=1)],
                y_pred[(fair_attr == unpriv_group).all(axis=1)],
                zero_division=zero_division,
                **kwargs,
            )
            pr_fpr_group = false_positive_rate(
                y_true[(fair_attr != unpriv_group).all(axis=1)],
                y_pred[(fair_attr != unpriv_group).all(axis=1)],
                zero_division=zero_division,
                **kwargs,
            )
            unpr_rec_group = recall_score(
                y_true[(fair_attr == unpriv_group).all(axis=1)],
                y_pred[(fair_attr == unpriv_group).all(axis=1)],
                zero_division=zero_division,
                **kwargs,
            )
            pr_rec_group = recall_score(
                y_true[(fair_attr != unpriv_group).all(axis=1)],
                y_pred[(fair_attr != unpriv_group).all(axis=1)],
                zero_division=zero_division,
                **kwargs,
            )
    if multiclass:
        if multiclass_agg_mode == "max":
            return max(list_score, key=abs)
        else:
            return sum(map(abs, list_score))
    else:
        return ((unpr_fpr_group - pr_fpr_group) + (unpr_rec_group - pr_rec_group)) / 2


# ============================ GROUP FAIRNESS REGRESSION ==================================


def ddre_independence(
    y_true,
    y_pred,
    fair_attr,
    unpriv_group=0,
):
    """It computes the Direct Density Ratio Estimation (DDRE) of the independence density ratio score.

    Args:
        y_true (pd.Series): ground truth target values (not used for the metrics). It is set for compatibility.
        y_pred (pd.Series): estimated targets.
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics.
        unpriv_group (int/float/str/list, optional): the label of the unprivileged group in the features fair_attr. Defaults to 0.

    Returns:
        float: independence DDRE score
    """
    # normalization
    s_u = ((y_pred - y_pred.mean()) / y_pred.std()).values.reshape(-1, 1)

    # One Fairness Attribute
    if (len(fair_attr.shape) == 1) | ((fair_attr.shape[-1]) == 1):
        a = np.where(fair_attr == unpriv_group, 1, 0)
    # More Fairness Attributes
    else:
        a = np.where((fair_attr == unpriv_group).all(axis=1), 1, 0)

    n = len(a)

    # density ratio approximation with probabilistic classifier
    p_s = LogisticRegression()
    p_s.fit(s_u, a.ravel())
    pred_p_s = p_s.predict_proba(s_u.reshape(-1, 1))[:, 1]

    # independence metric score
    r_ind = ((n - a.sum()) / a.sum()) * (pred_p_s / (1 - pred_p_s)).mean()

    return r_ind


def ddre_separation(y_true, y_pred, fair_attr, unpriv_group=0):
    """It computes the Direct Density Ratio Estimation (DDRE) of the separation density ratio score.

    Args:
        y_true (pd.Series): ground truth target values.
        y_pred (pd.Series): estimated targets.
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics.
        unpriv_group (int/float/str/list, optional): the label of the unprivileged group in the features fair_attr. Defaults to 0.

    Returns:
        float: separation DDRE score
    """
    # normalization
    y_u = ((y_true - y_true.mean()) / y_true.std()).values.reshape(-1, 1)
    s_u = ((y_pred - y_pred.mean()) / y_pred.std()).values.reshape(-1, 1)

    # One Fairness Attribute
    if (len(fair_attr.shape) == 1) | ((fair_attr.shape[-1]) == 1):
        a = np.where(fair_attr == unpriv_group, 1, 0)
    # More Fairness Attributes
    else:
        a = np.where((fair_attr == unpriv_group).all(axis=1), 1, 0)

    # density ratios approximation with probabilistic classifier
    p_ys = LogisticRegression()
    p_y = LogisticRegression()
    p_y.fit(y_u, a.ravel())
    p_ys.fit(np.c_[y_u, s_u], a.ravel())
    pred_p_y = p_y.predict_proba(y_u.reshape(-1, 1))[:, 1]
    pred_p_ys = p_ys.predict_proba(np.c_[y_u, s_u])[:, 1]

    # separation metric score
    r_sep = ((pred_p_ys / (1 - pred_p_ys) * (1 - pred_p_y) / pred_p_y)).mean()

    return r_sep


def ddre_sufficiency(y_true, y_pred, fair_attr, unpriv_group=0):
    """It computes the Direct Density Ratio Estimation (DDRE) of the sufficiency density ratio score.

    Args:
        y_true (pd.Series): ground truth target values.
        y_pred (pd.Series): estimated targets.
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics.
        unpriv_group (int/float/str/list, optional): the label of the unprivileged group in the features fair_attr. Defaults to 0.

    Returns:
        float: sufficiency DDRE score
    """
    # normalization
    y_u = ((y_true - y_true.mean()) / y_true.std()).values.reshape(-1, 1)
    s_u = ((y_pred - y_pred.mean()) / y_pred.std()).values.reshape(-1, 1)

    # One Fairness Attribute
    if (len(fair_attr.shape) == 1) | ((fair_attr.shape[-1]) == 1):
        a = np.where(fair_attr == unpriv_group, 1, 0)
    # More Fairness Attributes
    else:
        a = np.where((fair_attr == unpriv_group).all(axis=1), 1, 0)

    # density ratios approximation with probabilistic classifier
    p_s = LogisticRegression()
    p_ys = LogisticRegression()
    p_s.fit(s_u, a.ravel())
    p_ys.fit(np.c_[y_u, s_u], a.ravel())
    pred_p_s = p_s.predict_proba(s_u.reshape(-1, 1))[:, 1]
    pred_p_ys = p_ys.predict_proba(np.c_[y_u, s_u])[:, 1]

    # sufficiency metric score
    r_suf = ((pred_p_ys / (1 - pred_p_ys)) * ((1 - pred_p_s) / pred_p_s)).mean()

    return r_suf


# ================================ USEFUL METRICS =========================================


def specificity_score(y_true, y_pred, zero_division=0, **kwargs):
    """Retrieve the specificity metric for a binary classification ML problem.

    Args:
        y_true (pandas.Series/np.array): ground truth target values.
        y_pred (pandas.Series/np.array): estimated targets.
        zero_division (int/str optional): it can be 0, 1 or 'warn'. It sets to a value when division with 0 in the denominator.
            When 'warn' it prints the warning and set the division to 0. Deafults to 0.

    Returns:
        float: specificity metric score
    """
    try:
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1], **kwargs).ravel()
    except Exception:
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[-1, 1], **kwargs).ravel()

    if (tn == 0) and (fp == 0):
        if zero_division not in ["warn", 0, 1]:
            raise ValueError(
                f"{zero_division} not valid logic for division with 0 in the denominator. It should be one of the following : ['warn',0,1]"
            )
        elif zero_division == "warn":
            warn("Specificity is ill-defined and being set to 0.0 due to no false samples.", UndefinedMetricWarning)
            specificity = 0
        else:
            specificity = zero_division
    else:
        specificity = tn / (tn + fp)
    return specificity


def positive_rate(y_true, y_pred, **kwargs):
    """Retrieve the PR (Positive Rate) metric for a binary classification ML problem.

    Args:
        y_true (pandas.Series/np.array): ground truth target values.
        y_pred (pandas.Series/np.array): estimated targets.

    Returns:
        float: PR metric score
    """
    try:
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1], **kwargs).ravel()
    except Exception:
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[-1, 1], **kwargs).ravel()

    pr = (tp + fp) / len(y_true)

    return pr


def false_positive_rate(y_true, y_pred, zero_division=0, **kwargs):
    """Retrieve the FPR (False Positive Rate) for a binary classification ML problem.

    Args:
        y_true (pandas.Series/np.array): ground truth target values.
        y_pred (pandas.Series/np.array): estimated targets.
        zero_division (int/str optional): it can be 0, 1 or 'warn'. It sets to a value when division with 0 in the denominator.
            When 'warn' it prints the warning and set the division to 0. Deafults to 0.

    Returns:
        float: FPR metric score
    """
    return 1 - specificity_score(y_true, y_pred, zero_division=zero_division, **kwargs)


# ================================ USEFUL FUNCTION =========================================


def compute_metric_fairness(y_true, y_pred, metric, fair_attr, unpriv_group, **kwargs):
    """Compute the supervised fairness metric scoring.

    Args:
        y_pred (pd.Series/np.array): predictions/scores of target
        metric (function): fairness metric function
        fair_attr (pd.DataFrame/pd.Series): attributes to be analyzed for fairness metrics
        unpriv_group (int/float/str/list): the label of the unprivileged group in the features fair_attr
        y_true (pd.Series/np.array, optional): true values of target. Defaults to None.

    Returns:
        fairness metric scoring performance
    """
    return metric(y_true, y_pred, fair_attr, unpriv_group, **kwargs)
