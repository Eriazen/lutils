import pandas as pd
import numpy as np
import bisect
import src.lambda_utility.data as data
import src.lambda_utility.log as log
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

    def compare_profile(self, simple_dat: str, hfdibrans_dat: str, profile: str,
                        profile_value: float, out: bool = False):
        # read data
        simple = pd.read_csv(self._load_path+simple_dat)
        hfdibrans = pd.read_csv(self._load_path+hfdibrans_dat)
        # get needed values
        simple = self._sort_and_trim(simple, profile, profile_value)
        hfdibrans = self._sort_and_trim(hfdibrans, profile, profile_value)
        # sort
        simple.sort_values(by=profile)
        hfdibrans.sort_values(by=profile)
        # output log
        out_log = log.ProfileLog()
        out_log.concat(simple)
        out_log.concat(hfdibrans)
        out_log.write("log.profile")

        if out:
            return simple, hfdibrans
        
    def int_check(self):
        vec1 = pd.DataFrame()
        # calculate the distance between first and last point in x-dir
        vec1["x"] = self._df["xIntPoint3"].subtract(self._df["xIntPoint1"])
        vec1["y"] = self._df["yIntPoint3"].subtract(self._df["yIntPoint1"])
        vec1["z"] = self._df["zIntPoint3"].subtract(self._df["zIntPoint1"])
        
        # calculate normal
        mag = self._mag(vec1)
        # normalize vector
        vec1 = vec1.div(mag, axis=0)

        # get surface normal for x-dir
        vec2 = self._df.loc[:, ["xSurfNorm", "ySurfNorm", "zSurfNorm"]]
        # rename
        vec2 = vec2.rename(columns={"xSurfNorm": "x", "ySurfNorm": "y", "zSurfNorm": "z"})
        # compare normals
        vec1 = vec1.subtract(vec2, axis=1)
        
        # replace and drop empty rows
        vec1 = vec1.replace(0, np.nan)
        vec1 = vec1.loc[:, ["x", "y", "z"]].dropna(how="all")
        # concat cell ids and restructure
        vec1 = vec1.join(self._df["cellI"], how="left")
        vec1 = vec1.loc[:, ["cellI", "x", "y", "z"]]

        # log output
        out_log = log.IntLog()
        out_log.concat(vec1)
        out_log.write("log.int")

    # get value from series closest to input
    def _get_closest(self, series: pd.Series, input: float):
        lower = bisect.bisect_left(series.values, input)
        val = series[lower]
        return val
    
    # get rows correspoding to input value
    def _sort_and_trim(self, df: pd.DataFrame, profile: str, input: float):
        if profile == "x":
            key = self._get_closest(df["y"], input)
            df = df.loc[df["y"] == key]
        elif profile == "y":
            key = self._get_closest(df["x"], input)
            df = df.loc[df["x"] == key]
        return df
    
    # calculate vector magnitude
    def _mag(self, df: pd.DataFrame):
        s = np.sqrt(np.square(df).sum(axis=1))
        return s


class BFSTest(SimulationTest):
    def __init__(self, load_path: str, int_info: str, n_cells_y: int):
        super().__init__(load_path)
        # load data
        self._n_cells_y = n_cells_y
        self._df = data.SimulationData(self._load_path, int_info).return_data()

    def ds(self, x_step: float, y_step: float):
        # initialize lambda
        lambda_x = self._df[:self._n_cells_y-2].reset_index(drop=True)
        lambda_y = self._df[self._n_cells_y:].reset_index(drop=True)
        # calculate ds difference for cells in x-dir
        lambda_x["ds"] = ((lambda_x["xCellCenter"] - lambda_x["xIntPoint1"])
                                -(lambda_x["xCellCenter"] - x_step))
        # reduce dataframe
        x = lambda_x.loc[:, ["cellI", "ds"]]
        # replace and drop empty rows
        x["ds"] = x["ds"].replace(0, np.nan)
        x = x.dropna()

        # calculate ds difference for cells in y-dir
        lambda_y["ds"] = ((lambda_y["yCellCenter"] - lambda_y["yIntPoint1"])
                               -(lambda_y["yCellCenter"] - y_step))
        # reduce dataframe
        y = lambda_y.loc[:, ["cellI", "ds"]]
        # replace and drop empty rows
        y["ds"] = y["ds"].replace(0, np.nan)
        y = y.dropna()

        # log output
        out_log = log.DsLog()
        out_log.concat(x)
        out_log.concat(y)
        out_log.write("log.ds")

    
class NACATest(SimulationTest):
    def __init__(self, load_path):
        super().__init__(load_path)

    def ds(self):
        pass
