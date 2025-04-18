# external packages
import matplotlib.pyplot as plt
from typing import Callable, Union
# internal packages
from ..core import data
from ..utils import *
from .plot_utils import *


def plot_profile(filename: str,
                 simple: str,
                 hfdibrans: str,
                 profile: str,
                 field: str,
                 grid: bool = False) -> None:
    check_dir("./plots")
    # plot figure
    fig = plt.figure(figsize=(20, 12))
    plt.scatter(simple[profile], simple[field], label="simple")
    plt.scatter(hfdibrans[profile], hfdibrans[field], label="hfdibrans")
    plt.legend()
    if grid:
        plt.grid()

    fig.savefig(filename)
    plt.close(fig)


def plot_int_points(data_obj: Union[data.BFSData, data.NACAData],
                    filename: str,
                    range_start: float = 0,
                    range_stop: float = 1,
                    func: Callable = None):
    check_dir("./plots")
    
    if isinstance(data_obj, data.BFSData):
        # select values based on input range
        df = values_in_range(data_obj.df.sort_values(by="xCellCenter"),
                                    "xCellCenter", range_start, range_stop)
        df = df.reset_index(drop=True)
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
        fig.savefig(filename)

    if isinstance(data_obj, data.NACAData):
        # select values based on input range
        df = values_in_range(data_obj.df.reset_index(drop=True),
                                   "yCellCenter", range_start, range_stop)
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
        fig.savefig(filename)
    else:
        print("Incorrect data object as input")