# external packages
import matplotlib.figure
from matplotlib import pyplot as plt
import pandas as pd
import bisect
from typing import Callable, Union
#internal packages
from ..core.data import get_data
from ..core.test_utils import get_closest


class Field:
    def __init__(self,
                 file_path: str,
                 field_name: str):
        data = get_data(file_path)

        self.x = data["x"].copy().reset_index(drop=True)
        self.y = data["y"].copy().reset_index(drop=True)
        self.z = data["z"].copy().reset_index(drop=True)
        self.field = data[field_name].copy().reset_index(drop=True)

    def get_profile(self,
                    profile: str) -> pd.Series:

        if profile == "x":
            return self.x
        elif profile == "y":
            return self.y
        elif profile == "z":
            return self.z
        else:
            raise TypeError("Incorrect profile value. Valid inputs are [x, y, z].")

    def trim_data(self,
                  profile: str,
                  profile_value: float):
        key = get_closest(self.x, profile_value)
        index = self.x.loc[self.x == key].index
        
        self.y = self.y.loc[index]
        self.field = self.field.loc[index]


# returns rows from df corresponding to input value
def values_in_range(df: pd.DataFrame, col: str, start: float, stop: float) -> pd.DataFrame:
    lower = bisect.bisect_left(df[col], start)
    higher = bisect.bisect_right(df[col], stop)
    return df.loc[lower:higher-1, :].copy()

# return ys of an outline based on xs
def outline(fig: Union[int, str, matplotlib.figure.Figure, matplotlib.figure.SubFigure],
            x: pd.Series, func: Callable[[float], float]) -> None:
    plt.figure(fig)
    y = x.sort_values().apply(func)
    plt.plot(x.sort_values(), y, color="black")
    plt.plot(x.sort_values(), -y, color="black")
