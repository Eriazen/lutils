import pandas as pd
import numpy as np
import bisect


# get value from series closest to input
def get_closest(series: pd.Series, input: float):
    lower = bisect.bisect_left(series.values, input)
    val = series[lower]
    return val

# get rows correspoding to input value
def sort_and_trim(df: pd.DataFrame, profile: str, input: float):
    if profile == "x":
        key = get_closest(df["y"], input)
        df = df.loc[df["y"] == key]
    elif profile == "y":
        key = get_closest(df["x"], input)
        df = df.loc[df["x"] == key]
    return df

# calculate vector magnitude
def magnitude(df: pd.DataFrame):
    s = np.sqrt(np.square(df).sum(axis=1))
    return s

# replace values close to zero with nan
def isclose_replace(data):
    if isinstance(data, pd.DataFrame):
        data = data.applymap(lambda x: np.nan if np.isclose(x, 0) else x, na_action="ignore")
    elif isinstance(data, pd.Series):
        data = data.apply(lambda x: np.nan if np.isclose(x, 0) else x)
    return data