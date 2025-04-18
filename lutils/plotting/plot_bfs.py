import matplotlib.pyplot as plt
from .plot_utils import *


def bfs_int_points(path: str,
                   df: pd.DataFrame,
                   range_stop: float) -> None:
    # plot figure
    fig = plt.figure(figsize=(20, 12))
    # plot points
    plt.scatter(df["xCellCenter"], df["yCellCenter"], marker="s")
    plt.scatter(df["xIntPoint1"], df["yIntPoint1"])
    plt.scatter(df["xIntPoint2"], df["yIntPoint2"])
    plt.scatter(df["xIntPoint3"], df["yIntPoint3"])
    # plot normal
    #~ for i in range(df.shape[0]):
    #~     plt.plot(df.loc[i, "xCellCenter"]+self._df.loc[i, "xSurfNorm"],
    #~                 df.loc[i, "yCellCenter"]+self._df.loc[i, "ySurfNorm"], color="black")

    # plot step outline
    plt.hlines(0.01, df["xIntPoint1"].min(), df["xIntPoint1"].max(), color="black")
    if range_stop >= 1.0:
        plt.vlines(1.0, df["yIntPoint1"].min(), df["yIntPoint1"].max(), color="black")
    fig.savefig(path)
    plt.close(fig)