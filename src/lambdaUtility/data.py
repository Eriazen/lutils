import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class SimulationData(ABC):
    def __init__(self, load_path: str, int_info: str):
        self._df = pd.read_csv(load_path+int_info)
        self.data_manipulation()

    def data_manipulation(self):
        data = self._df["cellCenter"].str.split(expand=True).rename(columns={
            0: "xCellCenter", 1: "yCellCenter", 2: "zCellCenter"})
        data = data.join(self._df["intPoints"].str.split(expand=True)).rename(columns={
            0: "xIntPoint1", 1: "yIntPoint1", 2: "zIntPoint1",
            3: "xIntPoint2", 4: "yIntPoint2", 5: "zIntPoint2",
            6: "xIntPoint3", 7: "yIntPoint3", 8: "zIntPoint3"})
        data = data.join(self._df["surfNorm"].str.split(expand=True)).rename(columns={
            0: "xSurfNorm", 1: "ySurfNorm", 2: "zSurfNorm"})
        data["xIntPoint1"] = data["xIntPoint1"].str.lstrip("3")
        data = data.join(self._df["cellI"])
        
        data = data.applymap(lambda x: x.strip("()") if isinstance(x, str) else x, na_action="ignore")
        data = data.apply(pd.to_numeric)

        self._df = data
    
    @abstractmethod
    def drop(self):
        pass


class BfsData(SimulationData):
    def __init__(self, load_path: str, int_info: str, n_cells_y: int):
        super().__init__(load_path, int_info)
        self.n_cells_y = n_cells_y
        self._lambda_x = self._df[:n_cells_y-2].reset_index(drop=True)
        self._lambda_y = self._df[n_cells_y:].reset_index(drop=True)
    
    def drop(self, row=None, column=None):
        if row == None and column != None:
            self._lambda_x = self._lambda_x.drop(column, axis=1)
            self._lambda_y = self._lambda_y.drop(column, axis=1)

        elif row != None and column == None:
            self._lambda_x = self._lambda_x.drop(row, axis=0)
            self._lambda_y = self._lambda_y.drop(row, axis=0)

        else:
            self._lambda_x = self._lambda_x.replace([row, column], np.NaN)
            self._lambda_y = self._lambda_y.replace([row, column], np.NaN)

        self._lambda_x = self._lambda_x.dropna()
        self._lambda_y = self._lambda_y.dropna()

    def return_data(self):
        return self._lambda_x, self._lambda_y