import pandas as pd
import numpy as np
import numba
from numba import njit


def convert_columns_name(column_names):
    """Converts a list of column names to a mapping of names to numbers and vice versa.

    Args:
        column_names (list of str): A list of column names to be converted.

    Returns:
        (dict): A dictionary mapping each column name to a unique integer.
        (dict): A dictionary mapping each integer back to the original column name.
    """
    numbers = {name: str(i) for i, name in enumerate(column_names)}
    reverse_mapping = {v: k for k, v in numbers.items()}
    return numbers, reverse_mapping


def rename_columns_in_dataframe(df, column_mapping):
    """
    Renames columns in a DataFrame according to a specified mapping. The keys are the existing column names and the values are the new column names.

    Args:
        df (pandas.DataFrame): The DataFrame whose columns are to be renamed.
        column_mapping (dict): A dictionary mapping current column names to new column names.

    Returns:
        None: The function modifies the DataFrame in place.
    """
    df.rename(columns=column_mapping, inplace=True)


def cluster_imputing(data, labels, k=5, size=500):
    """Performs K-Nearest Neighbors (KNN) imputation on the input dataset, grouping by provided labels.

    Args:
        data (pd.DataFrame): The input dataset containing missing values.
        labels (pd.Series): A series used to group the data for imputation.
        k (int, optional): The number of nearest neighbors to consider for imputation. Defaults to 5.
        size (int, optional): The size of sample in which searching the k-neighbours. Defaults to 500.

    Returns:
        pd.DataFrame: The imputed dataset with missing values filled.
        np.ndarray: An array of cluster labels corresponding to the input data.
    """
    random_strings_dict, reverse_mapping = convert_columns_name(data.columns)
    rename_columns_in_dataframe(data, random_strings_dict)
    data_grouped = knn__dataset_prep(data, labels)

    imputed_data = knn_imputation(data, data_grouped, k, size)
    cluster_labels = np.asarray(imputed_data["cluster"].values)
    imputed_data = imputed_data.drop(columns=["cluster", "original_index_to_drop"])
    rename_columns_in_dataframe(imputed_data, reverse_mapping)
    return imputed_data, cluster_labels


def knn__dataset_prep(data, labels):
    """Applies KNN imputation on grouped data, handling missing values within each group.

    Args:
        data (pd.DataFrame): The original dataset containing missing values.
        labels (np.array): Dataset cluster labels.

    Returns:
        pd.core.groupby.generic.DataFrameGroupBy: The grouped dataset for imputation.
    """
    datanan = data.index[data.isnull().all(axis=1)]
    data["cluster"] = labels
    data["cluster"] = data["cluster"].astype(str)
    data = data.drop(datanan).reset_index(drop=True)
    data["original_index_to_drop"] = data.index.astype(int)

    data_grouped = data.groupby("cluster")
    return data_grouped


def knn_imputation(data, data_grouped, k=5, size=500):
    """Applies KNN imputation on grouped data, handling missing values within each group.

    Args:
        data (pd.DataFrame): The original dataset containing missing values.
        data_grouped (pd.core.groupby.generic.DataFrameGroupBy): The grouped dataset for imputation.
        k (int, optional): The number of nearest neighbors to consider for imputation. Defaults to 5.
        size (int, optional): The size of sample in which searching the k-neighbours. Defaults to 500.

    Returns:
        pd.DataFrame: The dataset with missing values imputed.
    """
    imputed_data = []
    for a, group in data_grouped:
        copy_group = group.copy()
        group = group.drop(columns=["cluster", "original_index_to_drop"])
        if group.isna().all().any():
            for col in group:
                if group[col].isna().all():
                    if not pd.api.types.is_numeric_dtype(group[col]):
                        mode = data[col].mode()[0] if not data[col].mode().empty else None
                        group[col].fillna(mode, inplace=True)
                    else:
                        group[col].fillna(data[col].median(), inplace=True)
        group = imputer_numba(group, k, size)
        group["cluster"] = copy_group["cluster"]
        group["original_index_to_drop"] = copy_group["original_index_to_drop"]
        imputed_data.append(group)

    imputed_data = pd.concat(imputed_data)
    imputed_data = imputed_data.sort_values("original_index_to_drop")
    return imputed_data


def data_prep(df):
    """
    Prepares the data by converting categorical columns into dummy variables and handling NaN values.

    Args:
        df (pandas.DataFrame): The original DataFrame containing categorical data.

    Returns:
        df_dummies (pandas.DataFrame): The DataFrame with dummy columns added.
        original_categorical_columns (list): A list of the original categorical columns.
    """
    df_dummies = pd.get_dummies(df, dummy_na=False)
    original_categorical_columns = []
    for col in df.columns:
        dummy_cols = [dcol for dcol in df_dummies.columns if dcol.startswith(col + "_") and dcol not in df.columns]
        if dummy_cols:
            original_categorical_columns.append(col)
    nan_mask = df[original_categorical_columns].isna()

    for col in original_categorical_columns:
        dummy_cols = [col + "_" + str(val) for val in df[col].dropna().unique()]
        df_dummies[dummy_cols] = np.where(nan_mask[col].values[:, None], np.nan, df_dummies[dummy_cols].values)

    return df_dummies, original_categorical_columns


def revert_dummies(df_imputed, df, original_categorical_columns):
    """
    Converts dummy-encoded columns back to their original categorical format.

    Args:
        df_imputed (pandas.DataFrame): The DataFrame with dummy columns after imputation.
        df (pandas.DataFrame): The original DataFrame before dummy encoding.
        original_categorical_columns (list): A list of the original categorical columns.

    Returns:
        pandas.DataFrame: The DataFrame with the original categorical columns restored.
    """
    original_order = df.columns.tolist()
    for prefix in original_categorical_columns:
        dummy_cols = [col for col in df_imputed.columns if col.startswith(prefix + "_")]
        if dummy_cols:
            df_imputed[prefix] = df_imputed[dummy_cols].idxmax(axis=1)
            df_imputed[prefix] = df_imputed[prefix].apply(
                lambda x: x[len(prefix) + 1 :] if pd.notna(x) and "_" in x else np.nan
            )
            df_imputed = df_imputed.drop(columns=dummy_cols)

    df_imputed = df_imputed[original_order]

    return df_imputed


@numba.vectorize
def calc_mono_dist(val1, val2, max_val, min_val):
    """
    Calculates the normalized distance between two values, handling NaN values.

    Args:
        val1 (float): The first value.
        val2 (float): The second value.
        max_val (float): The maximum value of the variable.
        min_val (float): The minimum value of the variable.

    Returns:
        float: distance between two values.
    """
    if np.isnan(val1) or np.isnan(val2):
        return 1
    return abs(val1 - val2) / (max_val - min_val) if max_val != min_val else 0


@numba.jit(nopython=True)
def custom_distance_per_variable(point1, point2, max_vals, min_vals):
    """
    Computes the custom distance between two points across multiple variables.

    Args:
        point1 (np.ndarray): The first point as an array of values.
        point2 (np.ndarray): The second point as an array of values.
        max_vals (np.ndarray): Array of maximum values for each variable.
        min_vals (np.ndarray): Array of minimum values for each variable.

    Returns:
        float: The mean of the calculated distances across all variables.
    """
    distances = np.zeros(len(point1))
    for i in range(len(point1)):
        distances[i] = calc_mono_dist(point1[i], point2[i], max_vals[i], min_vals[i])
    return distances


@numba.jit(nopython=True)
def calculate_distance_for_point(k_point, random_points, max_vals, min_vals):
    """
    Compute distances between a point and an array of points.

    Args:
        punto_k (np.ndarray): Point of which distances will be calculated.
        punti_casuali (np.ndarray): Random point matrix.
        max_vals (np.ndarray): Maximum values array.
        min_vals (np.ndarray): Minimum values array.

    Returns:
        np.ndarray: Distance array between a point and each sampled points of dataset.
    """
    n_points = random_points.shape[0]
    n_variables = k_point.shape[0]

    distances = np.empty((n_points, n_variables))

    for i in range(n_points):
        distances[i, :] = custom_distance_per_variable(k_point, random_points[i], max_vals, min_vals)

    return distances


@njit
def fix_std(std_dev):
    """
    Changes std value to 1 if the real value is 0.

    Args:
        std_dev (np.ndarray): array of std of a set of variables.

    Return:
        np.ndarray: array of fixed std's.
    """
    fixed_std_dev = std_dev.copy()
    for i in range(len(fixed_std_dev)):
        if fixed_std_dev[i] == 0:
            fixed_std_dev[i] = 1
    return fixed_std_dev


@numba.njit
def standardize_distances(distances, mean_dist, std_dist):
    """
    Standardizes distances using the mean and standard deviation.

    Args:
        distances (np.ndarray): Array of distances to standardize.
        mean_dist (float): Mean of the distances.
        std_dist (float): Standard deviation of the distances.

    Returns:
        np.ndarray: Array of standardized distances.
    """
    standardized_distances = np.empty_like(distances)
    std_dist = fix_std(std_dist)
    for i in range(distances.shape[0]):
        standardized_distances[i] = (distances[i] - mean_dist) / std_dist
    return standardized_distances


@numba.njit
def row_means(matrix):
    """
    Computes the mean of each row in a matrix.

    Args:
        matrix (np.ndarray): 2D array from which to compute row means.

    Returns:
        np.ndarray: 1D array of row means.
    """
    n_rows = matrix.shape[0]
    row_means = np.empty(n_rows)

    for i in range(n_rows):
        row_means[i] = np.mean(matrix[i, :])

    return row_means


def create_distance_array(index, df_values, max_vals, min_vals, size=500):
    """
    Creates an array of standardized distances for a specific point in the DataFrame.

    Args:
        index (int): Index of the point in the DataFrame.
        df_values (np.ndarray): Array of DataFrame values.
        max_vals (np.ndarray): Array of maximum values for each variable.
        min_vals (np.ndarray): Array of minimum values for each variable.
        size (int, optional): Number of random points to sample (default is 500).

    Returns:
        np.ndarray: Array of standardized distances.
        np.ndarray: Array of sampled points.
    """
    k_point = df_values[index]
    if df_values.shape[0] > 5000:
        random_indices = np.random.choice(df_values.shape[0], size=size, replace=False)
    else:
        random_indices = np.arange(df_values.shape[0])
    random_points = df_values[random_indices]

    distances = calculate_distance_for_point(k_point, random_points, max_vals, min_vals)
    mean_dist = np.nanmean(distances, axis=0)
    std_dist = np.nanstd(distances, axis=0)
    standardized_distances = standardize_distances(distances, mean_dist, std_dist)
    standardized_distances = row_means(standardized_distances)
    return standardized_distances, random_points


@numba.jit(nopython=True)
def find_k_nearest(distances, k):
    """
    Finds the indices of the k-nearest points based on the distances.

    Args:
        distances (np.ndarray): Array of distances.
        k (int): Number of nearest points to find.

    Returns:
        np.ndarray: Indices of the k-nearest points.
    """
    return np.argsort(distances)[:k]


@numba.jit(nopython=True)
def impute_missing_values(row, nearest_rows, df_mean):
    """
    Imputes missing values in a row using the mean of the nearest rows.

    Args:
        row (np.ndarray): The row with missing values.
        nearest_rows (np.ndarray): Array of nearest rows.
        df_mean (np.ndarray): Mean values for each column in the DataFrame.

    Returns:
        np.ndarray: The row with imputed values.
    """
    for i in range(len(row)):
        if np.isnan(row[i]):
            row[i] = np.nanmean(nearest_rows[:, i])
        if np.isnan(row[i]):
            row[i] = df_mean[i]
    return row


def imputer_numba(df, k=5, size=500):
    """
    Imputes missing values in a DataFrame using a custom distance metric and Numba for optimization.

    Args:
        df (pd.DataFrame): The DataFrame with missing values.
        k (int, optional): The number of nearest neighbors to consider for imputation. Defaults to 5.
        size (int, optional): The size of sample in which searching the k-neighbours. Defaults to 500.

    Returns:
        pd.Dataframe: the imputed DataFrame
    """
    df2 = df.copy()
    df = df.dropna(how="all")
    df, original_categorical = data_prep(df)
    max_vals = df.max().values
    min_vals = df.min().values
    df_mean = np.nanmean(df.values, axis=0)
    nan_mask = df.isna().any(axis=1).values
    nan_row_indices = np.where(nan_mask)[0]
    df_values = df.values
    # imputation
    for index in nan_row_indices:
        distance_array, sample_array = create_distance_array(index, df_values, max_vals, min_vals, size)
        k_nearest = find_k_nearest(distance_array, k)
        df_values[index] = impute_missing_values(df_values[index], sample_array[k_nearest], df_mean)
    df = pd.DataFrame(df_values, columns=df.columns, index=df.index)
    # revert filled dataset
    df = revert_dummies(df, df2, original_categorical)

    return df
