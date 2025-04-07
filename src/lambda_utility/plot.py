import pandas as pd
import bisect
import numpy as np
import src.lambda_utility.test as test
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class SimPlot(ABC):
    def __init__(self, test_obj: test.SimTest):
        self._test = test_obj
        self._df = test_obj._df
    
    @abstractmethod
    def plot_int_points(self, range_start, range_stop):
        pass

    def plot_ds(self):
        pass
    
    def plot_profile(self, simple_dat: str, hfdibrans_dat: str, profile: str, profile_value: float, field: str):
        # get dataframes
        simple, hfdibrans = self._test.compare_profile(simple_dat, hfdibrans_dat,
                                                       profile, profile_value, out=True)

        # plot figure
        fig = plt.figure(2, figsize=(20, 12))
        plt.scatter(simple[profile], simple[field])
        plt.scatter(hfdibrans[profile], hfdibrans[field])

        fig.savefig("profile_test.png")

    def _values_in_range(self, df: pd.DataFrame, col: str,start: float, stop: float):
        lower = bisect.bisect_left(df[col], start)
        higher = bisect.bisect_right(df[col], stop)
        return df.loc[lower:higher-1, :].copy()
    
class BFSPlot(SimPlot):
    def __init__(self, bfs_obj: test.BFSTest):
        super().__init__(bfs_obj)

    def plot_int_points(self, range_start: float = 0, range_stop: float = 1):
        # select values based on input range
        df = self._values_in_range(self._df.sort_values(by="xCellCenter").reset_index(drop=True),
                                   "xCellCenter", range_start, range_stop)
        # plot figure
        fig = plt.figure(0, figsize=(20, 12))
        # plot points
        plt.scatter(df["xCellCenter"], df["yCellCenter"], marker="s")
        plt.scatter(df["xIntPoint1"], df["yIntPoint1"])
        plt.scatter(df["xIntPoint2"], df["yIntPoint2"])
        plt.scatter(df["xIntPoint3"], df["yIntPoint3"])
        # plot normal
        
        # plot step outline
        plt.hlines(0.01, df["xIntPoint1"].min(), df["xIntPoint1"].max(), color="black")
        if range_stop >= 1.0:
            plt.vlines(1.0, df["yIntPoint1"].min(), df["yIntPoint1"].max(), color="black")
        fig.savefig("int_test.png")


class NACAPlot(SimPlot):
    def __init__(self, test_obj: test.NACATest):
        super().__init__(test_obj)

    def plot_int_points(self, range_start, range_stop, func):
        # select values based on input range
        df = self._values_in_range(self._df.reset_index(drop=True),
                                   "yCellCenter", range_start, range_stop)
        # plot figure
        fig = plt.figure(0, figsize=(20, 12))
        # plot points
        plt.scatter(df["xCellCenter"], df["yCellCenter"], marker="s", label="C")
        plt.scatter(df["xIntPoint1"], df["yIntPoint1"], label="1")
        plt.scatter(df["xIntPoint2"], df["yIntPoint2"], label="2")
        plt.scatter(df["xIntPoint3"], df["yIntPoint3"], label="3")

        # plot normal
        # for i in range(df.shape[0]):
        #     plt.scatter(df.loc[i, "xCellCenter"]+self._df.loc[i, "xSurfNorm"], df.loc[i, "yCellCenter"]+self._df.loc[i, "ySurfNorm"], color="black")
        
        # plot naca outline
        y = df["xIntPoint1"].sort_values().apply(func)
        plt.plot(df["xIntPoint1"].sort_values(), y, color="black")
        plt.plot(df["xIntPoint1"].sort_values(), -y, color="black")

        plt.legend()
        fig.savefig("int_naca.png")