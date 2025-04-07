import pandas as pd
from abc import ABC, abstractmethod


class SimData(ABC):
    def __init__(self, load_path: str, int_info: str):
        self._df = pd.read_csv(load_path+int_info)
        self._data_manipulation()
    
    def return_data(self):
        return self._df

    def _data_manipulation(self):
        # split cellCenter into xyz coordinates
        data = self._df["cellCenter"].str.split(expand=True).rename(columns={
            0: "xCellCenter", 1: "yCellCenter", 2: "zCellCenter"})
        # repeat for intPoints
        data = data.join(self._df["intPoints"].str.split(expand=True)).rename(columns={
            0: "xIntPoint1", 1: "yIntPoint1", 2: "zIntPoint1",
            3: "xIntPoint2", 4: "yIntPoint2", 5: "zIntPoint2",
            6: "xIntPoint3", 7: "yIntPoint3", 8: "zIntPoint3"})
        # repeat for surface normal
        data = data.join(self._df["surfNorm"].str.split(expand=True)).rename(columns={
            0: "xSurfNorm", 1: "ySurfNorm", 2: "zSurfNorm"})
        # strip number of interpolation points
        data["xIntPoint1"] = data["xIntPoint1"].str.lstrip("3")
        # add cell ids
        data = data.join(self._df["cellI"])
        # strip brackets from all points
        data = data.applymap(lambda x: x.strip("()") if isinstance(x, str) else x, na_action="ignore")
        # convert from string to number
        data = data.apply(pd.to_numeric)
        # save as attribute
        self._df = data.copy()


class BfsData(SimData):
    def __init__(self, load_path: str, int_info: str, n_cells_y: int):
        super().__init__(load_path, int_info)
        # split dataframe into two frames based on geometry
        self.lambda_x = self._df[:n_cells_y-2].reset_index(drop=True).copy()
        self.lambda_y = self._df[n_cells_y:].reset_index(drop=True).copy()