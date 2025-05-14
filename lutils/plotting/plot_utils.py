# external packages
import matplotlib.figure
from matplotlib import pyplot as plt
import pandas as pd
import bisect
from typing import Callable, Union
#internal packages
from ..core.test_utils import get_closest


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
