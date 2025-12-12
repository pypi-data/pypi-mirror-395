import pandas as pd


def bg_red_yellow(df):
    """Color report of Class Performance Drift based on Alert.

    Args:
        df (pd.DataFrame): report in input

    Returns:
        pd.DataFrame: color-mapping report
    """
    ret = pd.DataFrame("", index=df.index, columns=df.columns)
    if "absolute_warning" in df.columns:
        ret.loc[df.absolute_warning == "Red Alert", ["curr_perf", "absolute_warning"]] = "background-color: red"
        ret.loc[df.absolute_warning == "Yellow Alert", ["curr_perf", "absolute_warning"]] = "background-color: yellow"

    ret.loc[df.relative_warning == "Red Alert", ["drift_perc", "relative_warning"]] = "background-color: red"
    ret.loc[df.relative_warning == "Yellow Alert", ["drift_perc", "relative_warning"]] = "background-color: yellow"
    return ret
