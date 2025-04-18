# external packages
import matplotlib.pyplot as plt
from typing import Callable
# internal packages
from .plot_utils import *


def naca_int_points(path: str,
                    df: str,
                    func: Callable[[], float]) -> None:
    # plot figure
    fig = plt.figure(figsize=(20, 12))
    #~ ax = plt.gca()
    #~ ax.set_aspect("equal")
    # plot points
    plt.scatter(df["xCellCenter"], df["yCellCenter"], marker="s", label="C")
    plt.scatter(df["xIntPoint1"], df["yIntPoint1"], label="1")
    plt.scatter(df["xIntPoint2"], df["yIntPoint2"], label="2")
    plt.scatter(df["xIntPoint3"], df["yIntPoint3"], label="3")

    # plot normal
    #~ for i in range(df.shape[0]):
    #~     plt.scatter(df.loc[i, "xCellCenter"]+self._df.loc[i, "xSurfNorm"],
    #~                 df.loc[i, "yCellCenter"]+self._df.loc[i, "ySurfNorm"], color="black")
    
    # plot naca outline
    outline(fig, df["xIntPoint1"], func)

    plt.legend()
    fig.savefig(path)
    plt.close(fig)