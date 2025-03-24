import pandas as pd
import numpy as np
import math
import bisect
import src.lambdaUtility.data as data
import src.lambdaUtility.log as log
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

    def compare_profile(self, simple_dat: str, hfdibrans_dat: str, profile: str, profile_value: float, variable: str):
        simple = pd.read_csv(self._load_path+simple_dat)
        hfdibrans = pd.read_csv(self._load_path+hfdibrans_dat)

        simple = self._sort_and_trim(simple, profile, profile_value)
        hfdibrans = self._sort_and_trim(hfdibrans, profile, profile_value)

        simple.sort_values(by=profile)
        hfdibrans.sort_values(by=profile)

        return simple, hfdibrans

    def _get_closest(self, series, input):
        lower = bisect.bisect_left(series.values, input)
        return lower
    
    def _sort_and_trim(self, df, profile, input):
        if profile == "x":
            key = self._get_closest(self, df["y"], input)
            df = df.loc[df["y"] == key]
        elif profile == "y":
            key = self._get_closest(self, df["x"], input)
            df = df.loc[df["x"] == key]
        
        return df


class BfsTest(SimulationTest):
    def __init__(self, load_path: str, int_info: str, n_cells_y: int):
        super().__init__(load_path)
        self._lambda_x, self._lambda_y = data.BfsData(
                                        load_path, int_info, n_cells_y
                                        ).return_data()

    def ds(self, x_step: float, y_step: float):
        self._lambda_x["ds"] = ((self._lambda_x["xCellCenter"] - self._lambda_x["xIntPoint1"])
                                -(self._lambda_x["xCellCenter"] - x_step))
        x = self._lambda_x.loc[:, ["cellI", "ds"]]
        x["ds"] = x["ds"].replace(0, np.nan)
        x = x.dropna()

        self._lambda_y["ds"] = ((self._lambda_y["yCellCenter"] - self._lambda_y["yIntPoint1"])
                               -(self._lambda_y["yCellCenter"] - y_step))
        y = self._lambda_y.loc[:, ["cellI", "ds"]]
        y["ds"] = y["ds"].replace(0, np.nan)
        y = y.dropna()

        out_log = log.DsLog()
        out_log.concat(x)
        out_log.concat(y)
        out_log.write("log.ds")

        
    def int_check(self):
        vec1 = pd.DataFrame()
        vec1["x"] = self._lambda_x["xIntPoint3"].subtract(self._lambda_x["xIntPoint1"])
        vec1["y"] = self._lambda_x["yIntPoint3"].subtract(self._lambda_x["yIntPoint1"])
        vec1["z"] = self._lambda_x["zIntPoint3"].subtract(self._lambda_x["zIntPoint1"])
        temp_x = self._lambda_y["xIntPoint3"].subtract(self._lambda_y["xIntPoint1"])
        temp_y = self._lambda_y["yIntPoint3"].subtract(self._lambda_y["yIntPoint1"])
        temp_z = self._lambda_y["zIntPoint3"].subtract(self._lambda_y["zIntPoint1"])
        vec1 = pd.concat([vec1, pd.concat([temp_x, temp_y, temp_z], axis=1).rename(
            columns={0: "x", 1: "y", 2: "z"})]).reset_index(drop=True)
        
        mag = np.sqrt(np.square(vec1).sum(axis=1))
        vec1["x"] = vec1["x"].div(mag)
        vec1["y"] = vec1["y"].div(mag)
        vec1["z"] = vec1["z"].div(mag)

        vec2 = self._lambda_x.loc[:, ["xSurfNorm", "ySurfNorm", "zSurfNorm"]]
        vec2 = pd.concat([vec2, self._lambda_y[["xSurfNorm", "ySurfNorm", "zSurfNorm"]]]).reset_index(drop=True)
        vec2 = vec2.rename(columns={"xSurfNorm": "x", "ySurfNorm": "y", "zSurfNorm": "z"})
        vec1 = vec1.subtract(vec2, axis=1)

        cell = pd.concat([self._lambda_x["cellI"], self._lambda_y["cellI"]]).reset_index(drop=True)
        
        vec1 = vec1.replace(0, np.nan)
        vec1 = vec1.loc[:, ["x", "y", "z"]].dropna(how="all")
        vec1 = vec1.join(cell, how="left")
        vec1 = vec1.loc[:, ["cellI", "x", "y", "z"]]

        out_log = log.IntLog()
        out_log.concat(vec1)
        out_log.write("log.int")