# external packages
import matplotlib.figure
from matplotlib import pyplot as plt
import pandas as pd
import bisect
from typing import Callable, Union


def values_in_range(df: pd.DataFrame, col: str, start: float, stop: float) -> None:
        lower = bisect.bisect_left(df[col], start)
        higher = bisect.bisect_right(df[col], stop)
        return df.loc[lower:higher-1, :].copy()

def outline(fig: Union[int, str, matplotlib.figure.Figure, matplotlib.figure.SubFigure],
            x: pd.Series, func: Callable) -> None:
    plt.figure(fig)
    y = x.sort_values().apply(func)
    plt.plot(x.sort_values(), y, color="black")
    plt.plot(x.sort_values(), -y, color="black")