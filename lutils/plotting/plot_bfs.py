# external packages
import matplotlib.pyplot as plt
import pandas as pd


def bfs_int_points(path: str,
                   df: pd.DataFrame,
                   range_stop: float,
                   x_step:float,
                   y_step: float) -> None:
    # plot figure
    fig = plt.figure(figsize=(20, 12))
    # plot points
    plt.scatter(df["xCellCenter"], df["yCellCenter"], marker="s")
    plt.scatter(df["xIntPoint1"], df["yIntPoint1"])
    plt.scatter(df["xIntPoint2"], df["yIntPoint2"])
    plt.scatter(df["xIntPoint3"], df["yIntPoint3"])
    # plot normal
    for i in range(df.shape[0]):
        # get normal start point
        x = df.loc[i, "xCellCenter"]
        y = y_step
        # x_step correction
        if df.loc[i, "xCellCenter"] >= x_step:
            x = x_step
            y = df.loc[i, "yCellCenter"]
        # add surface normal and plot
        x_norm = x + df.loc[i, "xSurfNorm"]*(df.loc[i, "xIntPoint3"]-x_step)
        y_norm = y + df.loc[i, "ySurfNorm"]*(df.loc[i, "yIntPoint3"]-y_step)
        plt.plot([x, x_norm], [y, y_norm], color="black")
    # plot step outline
    plt.hlines(y_step, df["xIntPoint1"].min(), df["xIntPoint1"].max(), color="black")
    if range_stop >= x_step:
        plt.vlines(x_step, df["yIntPoint1"].min(), df["yIntPoint1"].max(), color="black")
    fig.savefig(path)
    plt.close(fig)
