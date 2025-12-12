import pandas as pd

from model_monitoring.utils import (
    get_categorical_features,
    retrieve_bin_numerical,
    merge_numerical_bins,
    merge_categorical_bins,
)


def retrieve_bins_dict(df, features, nbins=1000, bin_min_pct=0.04):
    """Retrieve metadata bins mapping for all the features.

    Args:
        df (pd.DataFrame): input dataframe.
        features (list): list of features to be checked.
        nbins (int, optional): number of bins into which the features will be bucketed (maximum). Defaults to 1000.
        bin_min_pct (float, optional): minimum percentage of observations per bucket. Defaults to 0.04.

    Returns:
        dict: dictionary reporting for each feature the metadata bin mapping
    """
    if len(features) == 0:
        features = df.columns
    if isinstance(features, str):
        features = [features]

    bins_dict = dict()

    for col in features:
        bin_col = dict()
        # categorical bins generation
        if col in get_categorical_features(df):
            mapper = {x: x for x in df[col].dropna().unique()}
            mapper = merge_categorical_bins(df, col, mapper, bin_min_pct=bin_min_pct)
            base_bin = df[col].dropna().map(mapper)
            for y in list(dict.fromkeys(mapper.values())):
                bin_col[y] = {
                    "labels": [k for k, v in mapper.items() if v == y],
                    "freq": base_bin.value_counts(normalize=True)[y],
                }
        # numerical bins generation
        else:
            cuts = retrieve_bin_numerical(df, col, max_n_bins=nbins)
            cuts = merge_numerical_bins(df, col, cuts, bin_min_pct=bin_min_pct)
            base_bin = pd.cut(df[col].dropna(), cuts, right=True, precision=25, duplicates="drop")
            for i, y in enumerate(base_bin.value_counts(normalize=True).sort_index().index):
                bin_col[f"bin_{i}"] = {"min": y.left, "max": y.right, "freq": base_bin.value_counts(normalize=True)[y]}

        bins_dict[col] = bin_col

    return bins_dict


def map_bins_dict(df, meta_dict, features):
    """Apply metadata mapping to an input dataset.

    Args:
        df (pd.DataFrame): input dataframe.
        meta_dict (dict): reference metadata dictionary.
        features (list): list of features to be checked.

    Returns:
        dict: dictionary reporting for each feature the metadata bin mapping
    """
    if len(features) == 0:
        features = df.columns
    if isinstance(features, str):
        features = [features]

    bins_dict = dict()

    for col in features:
        bin_col = dict()

        # numerical bins generation
        if meta_dict[col]["type"] == "numerical":
            for x in [
                y
                for y in meta_dict[col].keys()
                if y not in ["type", "min_val", "max_val", "missing_values", "not_missing_values"]
            ]:
                min_bin = meta_dict[col][x]["min"]
                max_bin = meta_dict[col][x]["max"]
                bin_col.update(
                    {
                        x: {
                            "min": min_bin,
                            "max": max_bin,
                            "freq": df.loc[(df[col] > min_bin) & (df[col] <= max_bin), col].dropna().shape[0]
                            / df.dropna().shape[0],
                        }
                    }
                )

        # categorical bins generation
        if meta_dict[col]["type"] == "categorical":
            for x in [y for y in meta_dict[col].keys() if y not in ["type", "missing_values", "not_missing_values"]]:
                list_new_labels = [k for k in meta_dict[col][x]["labels"] if k in df[col].dropna().unique()]
                if list_new_labels != []:
                    bin_col.update(
                        {
                            x: {
                                "labels": list_new_labels,
                                "freq": df[col].dropna().value_counts(normalize=True)[list_new_labels].sum(),
                            }
                        }
                    )
            new_data = set(df[col].dropna().unique()) - set(sum([bin_col[x]["labels"] for x in bin_col.keys()], []))
            if new_data != set():
                bin_col.update(
                    {
                        "_other_": {
                            "labels": list(new_data),
                            "freq": df[col].dropna().value_counts(normalize=True)[list(new_data)].sum(),
                        }
                    }
                )

        bins_dict[col] = bin_col

    return bins_dict
