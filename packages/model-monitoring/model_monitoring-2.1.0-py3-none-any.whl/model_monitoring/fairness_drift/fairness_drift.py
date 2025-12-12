import pandas as pd
import numpy as np
from functools import reduce
import warnings


def check_fairness_groups(df_1, df_2, multiindex=True):
    """Check if two DataFrames have different group of fairness or if Multiindex Dataframes have different columns until level 1 and retrieves the list of unmatched fairness groups.

    Args:
        df_1 (pd.DataFrame): Multiindex DataFrame 1
        df_2 (pd.DataFrame): Multiindex DataFrame 2
        multiindex (bool, optional): determines if args are Multiindex Dataframes or DataFrames. Default to True.

    Returns:
        list: list of unmatched fairness groups unmatched.
    """
    if multiindex:
        col_2_train = reduce(
            lambda l, y: l.append(y) or l if y not in l else l, [(x[0], x[1]) for x in df_1.columns], []
        )
        col_2_test = reduce(
            lambda l, y: l.append(y) or l if y not in l else l, [(x[0], x[1]) for x in df_2.columns], []
        )
        list_no_join = list(set(col_2_train) ^ set(col_2_test))
    else:
        list_no_join = list(set(df_1.groups) ^ set(df_2.groups))
    if len(list_no_join) != 0:
        warnings.warn(f"unmatched fairness groups {list_no_join}")

    return list_no_join


def bg_red_yellow(df):
    """Color report of Class Fairness Drift based on Alert.

    Args:
        df (pd.DataFrame): report in input

    Returns:
        pd.DataFrame: color-mapping report
    """
    ret = pd.DataFrame("", index=df.index, columns=df.columns)
    for x in np.unique([x for x in df.columns.levels[0] if x != "metric"]):
        for y in np.unique(df[x].columns.get_level_values(0)):
            if "absolute_warning" in df[x][y].columns:
                ret.loc[
                    df[x][y].absolute_warning == "Red Alert", [(x, y, "curr_perf"), (x, y, "absolute_warning")]
                ] = "background-color: red"
                ret.loc[
                    df[x][y].absolute_warning == "Yellow Alert", [(x, y, "curr_perf"), (x, y, "absolute_warning")]
                ] = "background-color: yellow"

            ret.loc[
                df[x][y].relative_warning == "Red Alert", [(x, y, "drift_perc"), (x, y, "relative_warning")]
            ] = "background-color: red"
            ret.loc[
                df[x][y].relative_warning == "Yellow Alert", [(x, y, "drift_perc"), (x, y, "relative_warning")]
            ] = "background-color: yellow"
    return ret
