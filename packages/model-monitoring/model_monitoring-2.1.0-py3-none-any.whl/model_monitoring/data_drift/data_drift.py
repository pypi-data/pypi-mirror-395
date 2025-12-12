import numpy as np
import pandas as pd
from tqdm import tqdm
import sys
import warnings
from scipy import stats

from model_monitoring.utils import (
    get_categorical_features,
    retrieve_bin_numerical,
    merge_numerical_bins,
    merge_categorical_bins,
)


def stat_report(
    base_df,
    compare_df,
    type_data="data",
    feat_to_check=None,
    stat="psi",
    alpha=0.05,
    max_psi=0.2,
    mid_psi=0.1,
    psi_nbins=1000,
    psi_bin_min_pct=0.04,
    return_meta_ref=False,
    dim_threshold=5000,
):
    """Retrieve the dataframe with psis or pval for each feature and a `Warning` if the psi exceeds thresholds or if the pval doesn't exceeds alpha.

    Args:
        base_df (pd.DataFrame/dict): reference dataset, usually the train set.
        compare_df (pd.DataFrame/dict): comparison dataset, usually the test set.
        type_data (str, optional): indicates the type of input data among "data" (pd.DataFrame), "metadata" (dict of metadata containing for each feature the bin mapping). Defaults to "data".
        feat_to_check (list, optional): list of features to be checked.
        stat (str, optional): indicates the type of test between "psi" and "pval" (Kolmogorov-Smirnov Test for numerical features and Chi-Squared Test for categorical features). Defaults to "psi".
        alpha (float, optional): level of significance for the test. Defaults to 0.05.
        max_psi (float, optional): maximum psi acceptable. Defaults to 0.2.
        mid_psi (float, optional): medium psi acceptable. Defaults to 0.1.
        psi_nbins (int, optional): number of bins into which the features will be bucketed (maximum) to compute psi. Deafults to 1000.
        psi_bin_min_pct (float, optional): minimum percentage of observations per bucket. Defaults to 0.04.
        return_meta_ref (bool, optional): boolean to save the reference metadata dictionary. Defaults to False.
        dim_threshold (int,optional): maximum significant size of the test set for Chi-Square test. Defaults to 5000.

    Returns:
        pd.DataFrame: report containing psis, features and warnings
        dict () : reference metadata dictionary
    """
    if feat_to_check is None:
        feat_to_check = []
    stat_results, meta_ref = retrieve_stat(
        base_df,
        compare_df,
        stat,
        feat_to_check,
        type_data=type_data,
        psi_nbins=psi_nbins,
        psi_bin_min_pct=psi_bin_min_pct,
        return_meta_ref=return_meta_ref,
        dim_threshold=dim_threshold,
    )

    report_df = pd.DataFrame.from_dict(stat_results, orient="index").reset_index()

    if stat == "psi":
        report_df.columns = [
            "feature",
            "common_psi",
            "total_psi",
            "proportion_new_data",
            "proportion_old-fashioned_data",
            "validity_warning",
            "warning_constant",
        ]
        warning = pd.Series(
            [
                "Red Alert" if i > max_psi else "Yellow Alert" if (i > mid_psi and i <= max_psi) else None
                for i in report_df["common_psi"].values
            ]
        )
    else:
        report_df.columns = [
            "feature",
            "common_pval",
            "total_pval",
            "proportion_new_data",
            "proportion_old-fashioned_data",
            "validity_warning",
            "warning_constant",
        ]
        warning = pd.Series(["Red Alert" if i < alpha else None for i in report_df["common_pval"].values])

    report_df.insert(2, "warning", warning)
    report_df.loc[~report_df["warning_constant"].isnull(), "warning"] = report_df.loc[
        ~report_df["warning_constant"].isnull(), "warning_constant"
    ]
    report_df.drop(columns="warning_constant", inplace=True)

    return report_df, meta_ref


def retrieve_stat(
    base_df,
    compare_df,
    stat,
    features,
    type_data="data",
    psi_nbins=1000,
    psi_bin_min_pct=0.04,
    return_meta_ref=False,
    dim_threshold=5000,
):
    """Retrieve stat for all the features.

    Args:
        base_df (pd.DataFrame/dict): reference dataset, usually the train set.
        compare_df (pd.DataFrame/dict): comparison dataset, usually the test set.
        stat (str): indicates the type of test between "psi" and "pval" (Kolmogorov-Smirnov Test for numerical features and Chi-Squared Test for categorical features). Default to "psi".
        features (list): list of features to be checked
        type_data (str, optional): indicates the type of input data among "data" (pd.DataFrame), "metadata" (dict of metadata containing for each feature the bin mapping). Defaults to "data".
        psi_nbins (int, optional): number of bins into which the features will be bucketed (maximum) to compute psi. Deafults to 1000.
        psi_bin_min_pct (float, optional): minimum percentage of observations per bucket. Defaults to 0.04.
        return_meta_ref (bool, optional): boolean to save the reference metadata dictionary. Defaults to False.
        dim_threshold (int,optional): maximum significant size of the test set for Chi-Square test. Defaults to 5000.

    Returns:
        dict: dictionary reporting for each feature (key) the psi value (value)
        dict (optional) : reference metadata dictionary
    """
    if len(features) == 0:
        if type_data == "data":
            features = base_df.columns
        else:
            features = base_df.keys()
    if isinstance(features, str):
        features = [features]

    statt = dict()
    if return_meta_ref:
        meta_ref_dict = dict()
    else:
        meta_ref_dict = None

    if type_data == "data":
        categorical_features = get_categorical_features(base_df)
    else:
        categorical_features = [x for x in base_df.keys() if base_df[x]["type"] == "categorical"]

    if stat == "psi":
        features_pb = tqdm(features, file=sys.stdout, desc="Performing psi drift", ncols=100, leave=True)
    else:
        features_pb = tqdm(features, file=sys.stdout, desc="Performing p-value", ncols=100, leave=True)

    for ix, col in enumerate(features_pb):
        validity_warning = None
        warning = None
        if return_meta_ref:
            col_dict = dict()
        if stat == "pval":
            if type_data == "data":
                n = (len(base_df[col])) - base_df[col].isnull().sum()
                m = (len(compare_df[col])) - compare_df[col].isnull().sum()
            else:
                n = base_df[col]["not_missing_values"]
                m = compare_df[col]["not_missing_values"]
        # categorical bins generation
        if col in categorical_features:
            categorical_data = True
            # original data
            if type_data == "data":
                mapper = {x: x for x in base_df[col].dropna().unique()}
                mapper = merge_categorical_bins(base_df, col, mapper, bin_min_pct=psi_bin_min_pct)
                base_bin = base_df[col].dropna().map(mapper)
                if base_bin.nunique() == 1:
                    warning = f"Information - one bucket in reference data with more than {(1-psi_bin_min_pct)*100}% of information"
                if return_meta_ref:
                    col_dict["type"] = "categorical"
                    for y in list(dict.fromkeys(mapper.values())):
                        col_dict[y] = {
                            "labels": [k for k, v in mapper.items() if v == y],
                            "freq": base_bin.value_counts(normalize=True)[y],
                        }
                if set(compare_df[col].dropna().unique()) - set(base_df[col].dropna().unique()) != set():
                    only_comp = {
                        x: "_other_"
                        for x in list(set(compare_df[col].dropna().unique()) - set(base_df[col].dropna().unique()))
                    }
                    mapper.update(only_comp)
                comp_bin = compare_df[col].dropna().map(mapper)
                if (set(base_bin.unique()) - set(comp_bin.unique()) != set()) and (
                    set(comp_bin.unique()) - set(base_bin.unique()) != set()
                ):
                    validity_warning = "Red Alert - new and old-fashioned categorical data"
                else:
                    if set(base_bin.unique()) - set(comp_bin.unique()) != set():
                        validity_warning = "Yellow Alert - old-fashioned categorical data"
                    if set(comp_bin.unique()) - set(base_bin.unique()) != set():
                        validity_warning = "Red Alert - new categorical data"
            # metadata
            else:
                base_bin = {
                    x: base_df[col][x]
                    for x in base_df[col].keys()
                    if x not in ["type", "missing_values", "not_missing_values"]
                }
                if len(base_bin.keys()) == 1:
                    warning = f"Information - one bucket in reference data with more than {(1-psi_bin_min_pct)*100}% of information"
                comp_bin = {
                    x: compare_df[col][x]
                    for x in compare_df[col].keys()
                    if x not in ["type", "missing_values", "not_missing_values"]
                }
                if (set(base_bin.keys()) - set(comp_bin.keys()) != set()) and (
                    set(comp_bin.keys()) - set(base_bin.keys()) != set()
                ):
                    validity_warning = "Red Alert - new and old-fashioned categorical data"
                else:
                    if set(base_bin.keys()) - set(comp_bin.keys()) != set():
                        validity_warning = "Yellow Alert - old-fashioned categorical data"
                    if set(comp_bin.keys()) - set(base_bin.keys()) != set():
                        validity_warning = "Red Alert - new categorical data"

        # numerical bins generation
        else:
            categorical_data = False
            # original data
            if type_data == "data":
                cuts = retrieve_bin_numerical(base_df, col, max_n_bins=psi_nbins)
                cuts = merge_numerical_bins(base_df, col, cuts, bin_min_pct=psi_bin_min_pct)
                base_bin = pd.cut(base_df[col].dropna(), cuts, right=True, precision=25, duplicates="drop")
                if len(cuts) == 2:
                    warning = f"Information - one bucket in reference data with more than {(1-psi_bin_min_pct)*100}% of information"
                comp_bin = pd.cut(
                    compare_df[col].dropna().astype("float"), cuts, right=True, precision=25, duplicates="drop"
                )
                if (compare_df[col].max() > base_df[col].max()) and (compare_df[col].min() < base_df[col].min()):
                    validity_warning = "Information - values outside the min-max range in the new data"
                else:
                    if compare_df[col].min() < base_df[col].min():
                        validity_warning = "Information - values below lower bound in the new data"
                    if compare_df[col].max() > base_df[col].max():
                        validity_warning = "Information - values above the upper bound in the new data"
                if return_meta_ref:
                    col_dict["type"] = "numerical"
                    col_dict["min_val"] = base_df[col].min()
                    col_dict["max_val"] = base_df[col].max()
                    col_dict["not_missing_values"] = len(base_df[col]) - base_df[col].isnull().sum()
                    for i, y in enumerate(base_bin.value_counts(normalize=True).sort_index().index):
                        col_dict[f"bin_{i}"] = {
                            "min": y.left,
                            "max": y.right,
                            "freq": base_bin.value_counts(normalize=True)[y],
                        }
            # metadata
            else:
                base_bin = {
                    x: base_df[col][x]
                    for x in base_df[col].keys()
                    if x not in ["type", "missing_values", "min_val", "max_val", "not_missing_values"]
                }
                if len(base_bin.keys()) == 1:
                    warning = f"Information - one bucket in reference data with more than {(1-psi_bin_min_pct)*100}% of information"
                comp_bin = {
                    x: compare_df[col][x]
                    for x in compare_df[col].keys()
                    if x not in ["type", "missing_values", "min_val", "max_val", "not_missing_values"]
                }
                if (compare_df[col]["max_val"] > base_df[col]["max_val"]) and (
                    compare_df[col]["min_val"] < base_df[col]["min_val"]
                ):
                    validity_warning = "Information - values outside the min-max range in the new data"
                else:
                    if compare_df[col]["min_val"] < base_df[col]["min_val"]:
                        validity_warning = "Information - values below lower bound in the new data"
                    if compare_df[col]["max_val"] > base_df[col]["max_val"]:
                        validity_warning = "Information - values above the upper bound in the new data"

        if return_meta_ref:
            meta_ref_dict[col] = col_dict
        if (stat == "psi") and (ix == len(features) - 1):
            features_pb.set_description("Completed psi drift", refresh=True)
        elif (stat == "pval") and (ix == len(features) - 1):
            features_pb.set_description("Completed p-value", refresh=True)

        if stat == "psi":
            # drift indicators generation for psi
            common_psi, total_psi, prop_new_data, prop_oldfash_data = stat_value(
                base_bin, comp_bin, stat=stat, type_data=type_data, categorical=categorical_data
            )
            statt[col] = [common_psi, total_psi, prop_new_data, prop_oldfash_data, validity_warning, warning]
        else:
            # drift indicators generation for pval
            common_pval, total_pval, prop_new_data, prop_oldfash_data = stat_value(
                base_bin, comp_bin, stat=stat, n=n, m=m, type_data=type_data, categorical=categorical_data
            )
            statt[col] = [common_pval, total_pval, prop_new_data, prop_oldfash_data, validity_warning, warning]

    if return_meta_ref:
        if type_data == "metadata":
            meta_ref_dict = base_df

    if (stat == "pval") and (len(compare_df) > dim_threshold):
        warnings.warn(
            "Test chi quadro per le variabili categoriche potrebbe non essere affidabile se la dimensione del test set è maggiore di 5000"
        )

    return statt, meta_ref_dict


def stat_value(ref, new, stat, n=None, m=None, type_data="data", categorical=True):
    """Retrieve the stat and proportion of new and old-fashioned data.

    Args:
        ref (pd.Series/dict): series of the bins in the base/reference feature.
        new (pd.Series/dict): series of the bins in the new/comparison feature.
        stat (str): indicates the type of test between "psi" and "pval" (Kolmogorov-Smirnov Test for numerical features and Chi-Squared Test for categorical features). Default to "psi".
        n (int, optional): numbers of non missing values in the base/reference feature. Defaults to None.
        m (int, optional): numbers of non missing values in the new/comparison feature. Defaults to None.
        type_data (str, optional): indicates the type of input data among "data" (pd.DataFrame), "metadata" (dict of metadata containing for each feature the bin mapping). Defaults to "data".
        categorical (bool, optional): indicates whether the bins come from a categorical or numerical variable. Defaults to True.

    Returns:
        float: the common stat
        float: the total stat
        float: the proportion of new data
        float: the proportion of old-fashioned data
    """
    if type_data == "data":
        ref_count = pd.DataFrame(ref.value_counts(normalize=True))
        ref_count.columns = ["ref"]
        new_count = pd.DataFrame(new.value_counts(normalize=True))
        new_count.columns = ["new"]
    else:
        if categorical:
            _cols = ["labels", "freq"]
        else:
            _cols = ["min", "max", "freq"]
        ref_count = pd.DataFrame.from_dict(ref, orient="index", columns=_cols).rename(columns={"freq": "ref"})
        new_count = pd.DataFrame.from_dict(new, orient="index", columns=_cols).rename(columns={"freq": "new"})

    # common stat
    merged_common = create_stat_table(ref_count, new_count, stat, n, m, "inner", categorical, type_data)

    # total stat
    merged_total = create_stat_table(ref_count, new_count, stat, n, m, "outer", categorical, type_data)

    # proportion old-fashioned data
    prop_oldfash_data = merged_total.loc[
        [x for x in list(ref_count.index) if x not in list(new_count.index)], "ref"
    ].sum()

    # proportion new data
    prop_new_data = merged_total.loc[[x for x in list(new_count.index) if x not in list(ref_count.index)], "new"].sum()

    if stat == "psi":
        return merged_common["psi"].sum(), merged_total["psi"].sum(), prop_new_data, prop_oldfash_data
    else:
        # Chi-Square p-value for categorical features
        if categorical:
            stat_cat_c = merged_common["pval"].sum()
            stat_cat_t = merged_total["pval"].sum()
            return (
                stats.chi2.sf(stat_cat_c, len(merged_common["pval"]) - 1),
                stats.chi2.sf(stat_cat_t, len(merged_total["pval"]) - 1),
                prop_new_data,
                prop_oldfash_data,
            )
        # KS p-value for numerical features
        else:
            stat_num_c = max(merged_common["pval"])
            stat_num_t = max(merged_total["pval"])
            # degrees of freedom for KS Test
            en = np.round((n * m) / (n + m))
            return stats.kstwo.sf(stat_num_c, en), stats.kstwo.sf(stat_num_t, en), prop_new_data, prop_oldfash_data


def dd_red_yellow(df, missing_alert=False, missing_max_thresholds=10, missing_mid_thresholds=5):
    """Color report of Class Data Drift based on Alert.

    Args:
        df (pd.DataFrame): report in input.
        missing_alert (bool, optional): boolean to color report based on alert on missing values. Defaults to False.
        missing_max_thresholds (float, optional): maximun percentage of new missing values threshold, computed if missing_alert is set to True. Defaults to 10.
        missing_mid_thresholds (float, optional): medium percentage of new missing values threshold, computed if missing_alert is set to True. Defaults to 5.

    Returns:
        pd.DataFrame: color-mapping report
    """
    ret = pd.DataFrame("", index=df.index, columns=df.columns)

    ret.loc[df.warning == "Red Alert", ["common_psi", "warning"]] = "background-color: red"
    ret.loc[df.warning == "Yellow Alert", ["common_psi", "warning"]] = "background-color: yellow"
    ret.loc[
        df["validity_warning"].fillna("Missing").str.startswith("Red Alert"), "validity_warning"
    ] = "background-color: red"
    ret.loc[
        df["validity_warning"].fillna("Missing").str.startswith("Yellow Alert"), "validity_warning"
    ] = "background-color: yellow"
    if missing_alert:
        ret.loc[df["drift_perc_missing"] > missing_max_thresholds, "drift_perc_missing"] = "background-color: red"
        ret.loc[
            df["drift_perc_missing"] <= missing_max_thresholds and df["drift_perc_missing"] > missing_mid_thresholds,
            "drift_perc_missing",
        ] = "background-color: yellow"

    return ret


def create_stat_table(
    ref_count, new_count, stat, n=None, m=None, merge_type="inner", categorical=True, type_data="data"
):
    """Create stat table using normalized frequency on bins of a feature in reference and new datasets.

    Args:
        ref_count (pd.DataFrame): dataframe counting relative frequency on bins of a feature in the reference dataset.
        new_count (pd.DataFrame): dataframe counting relative frequency on bins of a feature in the new dataset.
        stat (str): indicates the type of test between "psi" and "pval" (Kolmogorov-Smirnov Test for numerical features and Chi-Squared Test for categorical features). Default to "psi".
        n (int, optional): numbers of non missing values in the base/reference feature. Defaults to None.
        m (int, optional): numbers of non missing values in the new/comparison feature. Defaults to None.
        merge_type (str): type of merge to be performed between "left", "right", "outer", "inner" and "cross". Defaults to "inner".
        categorical (bool, optional): indicates whether the bins come from a categorical or numerical variable. Defaults to True.
        type_data (str, optional): indicates the type of input data among "data" (pd.DataFrame), "metadata" (dict of metadata containing for each feature the bin mapping). Defaults to "data".

    Returns:
        pd.DataFrame: stat table
    """
    if type_data == "data":
        merged = ref_count.merge(new_count, how=merge_type, left_index=True, right_index=True).fillna(0).sort_index()
    else:
        if not categorical:
            ref_count = ref_count.sort_values(by="min")
            merged = ref_count.merge(new_count, how=merge_type, left_index=True, right_index=True).fillna(0)
        else:
            merged = (
                ref_count.merge(new_count, how=merge_type, left_index=True, right_index=True).fillna(0).sort_index()
            )

    if stat == "psi":
        merged[["ref", "new"]] = merged[["ref", "new"]].fillna(0).clip(lower=0.000001)
        merged["psi"] = (merged["new"] - merged["ref"]) * (np.log(merged["new"] / merged["ref"]))
    else:
        # Chi-Square statistic for categorical features
        if categorical:
            merged["ref"] = np.round(merged["ref"] * n)
            merged["new"] = np.round(merged["new"] * m)
            merged["ref"] = np.round((merged["ref"] / n) * m)
            merged["pval"] = ((merged["new"] - merged["ref"]) ** 2) / (merged["ref"])
        # KS statistic for numerical features
        else:
            merged["ref"] = np.cumsum(merged["ref"])
            merged["new"] = np.cumsum(merged["new"])
            merged["pval"] = [np.abs(x - y) for x, y in zip(merged["ref"], merged["new"])]

    return merged
