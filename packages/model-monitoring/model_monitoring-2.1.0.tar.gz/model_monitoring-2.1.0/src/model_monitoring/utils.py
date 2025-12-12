import pandas as pd
import numpy as np
import warnings
from datetime import datetime, date
import time
from dateutil import parser


def check_size(data_1, data_2):
    """Check if two np.arrays/pd.DataFrames/pd.Series have the same length.

    Args:
        data_1 (np.array/pd.Series/pd.DataFrame): data 1
        data_2 (np.array/pd.Series/pd.DataFrame): data 2

    Returns:
        ValueError: ValueError if data_1 and data_2 do not have the same length
    """
    if len(data_1) != len(data_2):
        raise ValueError("input dataset do not have the same length ({0},{1})".format(len(data_1), len(data_2)))


def check_metrics_sets(metrics_1: dict, metrics_2: dict):
    """Check that metrics in set 1 are the same of those in set 2. If not raise a warning.

    Args:
        metrics_1 (dict): dictionary of metrics 1
        metrics_2 (dict): dictionary of metrics 2
    """
    metrics = set(metrics_1.keys())
    cnf_metrics = set(metrics_2.keys())

    if metrics ^ cnf_metrics != set():
        warnings.warn(f"unmatched metrics {metrics^cnf_metrics}")


def check_features_sets(features_1: list, features_2: list):
    """Check that features in set 1 are the same of those in set 2. If not raise a warning.

    Args:
        features_1 (list): list of features 1
        features_2 (list): list of features 2
    """
    features_base = set(features_1)
    features_compare = set(features_2)

    if features_base ^ features_compare != set():
        warnings.warn(f"unmatched features {features_base^features_compare}. Analysis is computed on common features.")


def get_categorical_features(df, feature_filter=None):
    """It gets a list of categorical features' names from a DataFrame excluding unwanted features' names.

    Args:

    df (pd.DataFrame): input dataframe
    feature_filter (list, optional): list of columns that will be filtered when extracting
        categorical features.

    Returns:
        list: the list of categorical feature names
    """
    if feature_filter is None:
        feature_filter = []

    categorical_feat = [
        var for var in df.columns if (df[var].dtype == "O" or df[var].dtype == "category") and var not in feature_filter
    ]

    return categorical_feat


def get_numerical_features(df, feature_filter=None):
    """It gets a list of numerical features' names from a DataFrame excluding unwanted features' names.

    Args:
        df (pd.DataFrame): input dataframe
        feature_filter (list, optional): list of columns that will be filtered when extracting
            numerical features.

    Returns:
        list: the list of numerical feature names
    """
    if feature_filter is None:
        feature_filter = []

    numerical_feat = [
        var
        for var in df.columns
        if (df[var].dtype != "O" and df[var].dtype != "category") and (var not in feature_filter)
    ]
    return numerical_feat


def merge_categorical_bins(df, feat, mapper, bin_min_pct=0.04):
    """Merge buckets that have low frequency.

    Args:
        df (pd.DataFrame): DataFrame to be used
        feat (str): feature to be bucketed
        mapper (dict): initial mapper to be used to bucket the feature feat
        bin_min_pct (float, optional): minimum percentage of observations per bucket. Defaults to 0.04.

    Returns:
        dict: mapper to be used to bucket the feature feat
    """
    db = df[[feat]].dropna().assign(bin=df[feat].dropna().map(mapper))

    freqs = db["bin"].value_counts(ascending=True, normalize=True)

    if freqs.iloc[0] < bin_min_pct:
        update = {x: freqs.index[1] for x, y in mapper.items() if y == freqs.index[0]}
        mapper.update(update)
        mapper = merge_categorical_bins(df, feat, mapper, bin_min_pct)

    return mapper


def retrieve_bin_numerical(df, feat, max_n_bins=1000):
    """Retrieve the bucket for a numerical feature.

    Args:
        df (pd.DataFrame): DataFrame to be used
        feat (str): feature to be bucketed
        max_n_bins (int, optional): number of bins into which the features will be bucketed (maximum) to compute psi
    Returns:
        list: the list of cuts to be used in pd.cut
    """
    if df[feat].dropna().nunique() > max_n_bins:
        db = (
            df[[feat]].dropna().assign(bucket=pd.qcut(df[feat].dropna(), q=max_n_bins, labels=False, duplicates="drop"))
        )
        cuts = list(db.groupby("bucket")[feat].max())
    else:
        cuts = list(df[feat].dropna().unique())

    cuts.sort()
    cuts = [-np.inf] + cuts
    cuts[-1] = np.inf

    return cuts


def merge_numerical_bins(df, feat, cuts, bin_min_pct=0.04):
    """Merge buckets that have low frequency.

    Args:
        df (pd.DataFrame): DataFrame to be used
        feat (str): feature to be bucketed
        cuts (list): initial cuts to be used to bucket the feature feat
        bin_min_pct (float, optional): minimum percentage of observations per bucket

    Returns:
        dict: mapper to be used to bucket the feature feat
    """
    db = df[[feat]].dropna().assign(bin=pd.cut(df[feat].dropna(), bins=cuts, labels=False, right=True))
    freqs = db["bin"].value_counts(ascending=True, normalize=True).sort_index()

    n = freqs.index[-1]
    j = 0
    for i in range(n + 1):
        if freqs.iloc[i - j] < bin_min_pct:
            j += 1
            if (i + 1 - j) == freqs.index[-1]:
                remove_cut = cuts[-2]
            else:
                remove_cut = cuts[i + 2 - j]
            cuts.remove(remove_cut)
            db = df[[feat]].dropna().assign(bin=pd.cut(df[feat].dropna(), bins=cuts, labels=False, right=True))
            freqs = db["bin"].value_counts(ascending=True, normalize=True).sort_index()

    return cuts


def convert_Int_dataframe(db):
    """Converts feature "Int" format into "float" format of the dataset in input.

    Args:
        db (pd.DataFrame): dataset for integer converting mapping

    Returns:
        pd.DataFrame: dataframe with converted int types features
    """
    return db.astype(
        {
            **{col: "float64" for col in db.columns if db[col].dtype == "Int64"},
            **{col: "float32" for col in db.columns if db[col].dtype == "Int32"},
        }
    )


def convert_Int_series(db):
    """Converts feature "Int" format into "float" format of the dataset in input.

    Args:
        db (pd.Series): pd.Series for integer converting mapping

    Returns:
        pd.Series: series with converted int types features
    """
    return db.astype("float64") if db.dtype == "Int64" else db.astype("float32") if db.dtype == "Int32" else db


def absmax(a, axis=0):
    """Retrieve the maximum values in absolute value along an axis from a numpy ndarray.

    Args:
        a (np.ndarray): numpy ndarray from which we get the maximum in absolute value
        axis (int): determines the axis along which we calculate the maximum in absolute value

    Returns:
        np.array: np.array with the maximum values in asbolute value along an axis
    """
    s = np.array(a.shape)
    s[axis] = -1
    return np.take_along_axis(a, np.abs(a).argmax(axis).reshape(s), axis=axis)[0]


def to_seconds(obj):
    """
    Converts various types of date and time representations to Unix timestamp (seconds since epoch).

    Args:
        obj (datetime.datetime / datetime.date / pandas.Timestamp / numpy.datetime64 / str / time.struct_time / float): The date or time representation to be converted.

    Returns:
        float: The Unix timestamp (seconds since 1970/01/01 00:00) corresponding to the input object.
        np.nan: If the input is NaN or cannot be converted to a valid timestamp.
    """
    if pd.isna(obj):
        return np.nan
    if isinstance(obj, datetime):
        return obj.timestamp()
    elif isinstance(obj, date):
        dt = datetime.combine(obj, datetime.min.time())
        return dt.timestamp()
    elif isinstance(obj, pd.Timestamp):
        return obj.timestamp()
    elif isinstance(obj, np.datetime64):
        dt = obj.astype("datetime64[s]").astype(datetime)
        return dt.timestamp()
    elif isinstance(obj, str):
        try:
            dt = parser.parse(obj)
            return dt.timestamp()
        except (ValueError, TypeError):
            return np.nan
    elif isinstance(obj, time.struct_time):
        dt = datetime(*obj[:6])
        return dt.timestamp()
    else:
        raise TypeError(f"This type is not supported for conversion to float from date: {type(obj)}")


def convert_date_columns_to_seconds(df):
    """
    Converts all columns with date or datetime types in a DataFrame to Unix timestamps (seconds since 1970/01/01 00:00).

    Args:
        df (pandas.DataFrame): The DataFrame containing columns with date or datetime types to be converted.

    Returns:
        pandas.DataFrame: The DataFrame with date or datetime columns converted to Unix timestamps.
    """
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                df[col] = df[col].apply(to_seconds)
            except Exception as e:
                raise ValueError(f"An error occured while converting '{col}' from date to float: {e}")
    return df


def convert_cluster_labels(cluster_labels, vals):
    """
    Converts cluster labels into a range of integers from 0 to `vals - 1`.

    Args:
        cluster_labels (pandas.Series / list / np.ndarray): The cluster labels to be converted. This can be a pandas Series, a list, or a NumPy array.
        vals (int): The number of distinct cluster labels.

    Returns:
        pandas.Series: A pandas Series with cluster labels mapped to integers from 0 to `vals - 1`.
    """
    if not isinstance(cluster_labels, pd.Series):
        cluster_labels = pd.Series(cluster_labels)
    if not cluster_labels.apply(lambda x: isinstance(x, int)).all():
        if not cluster_labels.apply(lambda x: x in range(vals)).all():
            unique_labels = list(set(cluster_labels))
            map_value = {value: index for index, value in enumerate(unique_labels)}
            cluster_labels = cluster_labels.map(map_value)
    return cluster_labels
