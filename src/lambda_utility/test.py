import pandas as pd
import numpy as np
import math
import bisect
import data
import log
from abc import ABC, abstractmethod


class SimulationTest(ABC):
    def __init__(self, load_path: str):
        self._load_path = load_path
        self._log = pd.Series()

    @abstractmethod
    def ds(self):
        pass

    @abstractmethod
    def int_check(self):
        pass

    def compare_profile(self, simple_dat: str, hfdibrans_dat: str, profile: str, profile_value: float):
        # read data
        simple = pd.read_csv(self._load_path+simple_dat)
        hfdibrans = pd.read_csv(self._load_path+hfdibrans_dat)
        # get needed values
        simple = self._sort_and_trim(simple, profile, profile_value)
        hfdibrans = self._sort_and_trim(hfdibrans, profile, profile_value)
        # sort
        simple.sort_values(by=profile)
        hfdibrans.sort_values(by=profile)
        return simple, hfdibrans

    # get value from dataframe closest to input
    def _get_closest(self, series: pd.Series, input: float):
        lower = bisect.bisect_left(series.values, input)
        return lower
    
    # get values correspoding to input value
    def _sort_and_trim(self, df: pd.DataFrame, profile: str, input: float):
        if profile == "x":
            key = self._get_closest(self, df["y"], input)
            df = df.loc[df["y"] == key]
        elif profile == "y":
            key = self._get_closest(self, df["x"], input)
            df = df.loc[df["x"] == key]
        return df
    
    def _mag_2D(self, df: pd.DataFrame):
        s = np.sqrt(df["x"].pow(2) + df["y"].pow(2))
        return s


class BfsTest(SimulationTest):
    def __init__(self, load_path: str, int_info: str, n_cells_y: int):
        super().__init__(load_path)
        # load data
        self._lambda_x, self._lambda_y = data.BfsData(
                                        load_path, int_info, n_cells_y
                                        ).return_data()

    def ds(self, x_step: float, y_step: float):
        # calculate ds difference for cells in x-dir
        self._lambda_x["ds"] = ((self._lambda_x["xCellCenter"] - self._lambda_x["xIntPoint1"])
                                -(self._lambda_x["xCellCenter"] - x_step))
        # reduce dataframe
        x = self._lambda_x.loc[:, ["cellI", "ds"]]
        # replace and drop empty rows
        x["ds"] = x["ds"].replace(0, np.nan)
        x = x.dropna()

        # calculate ds difference for cells in y-dir
        self._lambda_y["ds"] = ((self._lambda_y["yCellCenter"] - self._lambda_y["yIntPoint1"])
                               -(self._lambda_y["yCellCenter"] - y_step))
        # reduce dataframe
        y = self._lambda_y.loc[:, ["cellI", "ds"]]
        # replace and drop empty rows
        y["ds"] = y["ds"].replace(0, np.nan)
        y = y.dropna()

        # log output
        out_log = log.DsLog()
        out_log.concat(x)
        out_log.concat(y)
        out_log.write("log.ds")

        
    def int_check(self):
        vec1 = pd.DataFrame()
        # calculate the distance between first and last point in x-dir
        vec1["x"] = self._lambda_x["xIntPoint3"].subtract(self._lambda_x["xIntPoint1"])
        vec1["y"] = self._lambda_x["yIntPoint3"].subtract(self._lambda_x["yIntPoint1"])
        vec1["z"] = self._lambda_x["zIntPoint3"].subtract(self._lambda_x["zIntPoint1"])
        # repeat for y-dir --- TO-DO: GET RID OF LAMBDA_X, LAMBDA_Y
        temp_x = self._lambda_y["xIntPoint3"].subtract(self._lambda_y["xIntPoint1"])
        temp_y = self._lambda_y["yIntPoint3"].subtract(self._lambda_y["yIntPoint1"])
        temp_z = self._lambda_y["zIntPoint3"].subtract(self._lambda_y["zIntPoint1"])
        # concat frames, rename
        vec1 = pd.concat([vec1, pd.concat([temp_x, temp_y, temp_z], axis=1).rename(
            columns={0: "x", 1: "y", 2: "z"})]).reset_index(drop=True)
        
        # calculate normal
        mag = np.sqrt(np.square(vec1).sum(axis=1))
        # normalize vector
        vec1["x"] = vec1["x"].div(mag)
        vec1["y"] = vec1["y"].div(mag)
        vec1["z"] = vec1["z"].div(mag)

        # get surface normal for x-dir
        vec2 = self._lambda_x.loc[:, ["xSurfNorm", "ySurfNorm", "zSurfNorm"]]
        # repeat for y-dir
        vec2 = pd.concat([vec2, self._lambda_y[["xSurfNorm", "ySurfNorm", "zSurfNorm"]]]).reset_index(drop=True)
        # rename
        vec2 = vec2.rename(columns={"xSurfNorm": "x", "ySurfNorm": "y", "zSurfNorm": "z"})
        # compare vectors
        vec1 = vec1.subtract(vec2, axis=1)
        # get cell ids
        cell = pd.concat([self._lambda_x["cellI"], self._lambda_y["cellI"]]).reset_index(drop=True)
        
        # replace and drop empty rows
        vec1 = vec1.replace(0, np.nan)
        vec1 = vec1.loc[:, ["x", "y", "z"]].dropna(how="all")
        # concat cell ids and restructure
        vec1 = vec1.join(cell, how="left")
        vec1 = vec1.loc[:, ["cellI", "x", "y", "z"]]

        # log output
        out_log = log.IntLog()
        out_log.concat(vec1)
        out_log.write("log.int")