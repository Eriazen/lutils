# external packages
import pandas as pd
import bisect
from typing import Union


class BaseDataClass:
    def __init__(self,
                 file_path: str) -> None:
        self.data = pd.read_csv(file_path)

    def get_data(self) -> pd.DataFrame:
        return self.data.copy()

    def update_data(self,
                    column: Union[str, int],
                    correction: float) -> None:
        self.data[column] = self.data[column]*correction

    def get_value(self,
                  value: str) -> pd.Series:
        try:
            return self.data.loc[:, value]
        except:
            raise NameError("Invalid value name.")


class Field(BaseDataClass):
    def __init__(self,
                 file_path: str) -> None:
        super().__init__(file_path)

    def get_trimmed(self,
                    profile: str,
                    across: str,
                    profile_value: float) -> pd.DataFrame:
        key = self._get_closest(self.get_value(across), profile_value)
        df = self.data.loc[self.data[across] == key].copy()
        df = df.sort_values(by=profile)
        return df

    def _get_closest(self,
                     series: pd.Series,
                     value: float) -> float:
        lower = bisect.bisect_left(series.values, value)
        return series.loc[lower]


class InterpolationInfo(BaseDataClass):
    def __init__(self,
                 file_path: str):
        super().__init__(file_path)
        self._data_manipulation()

    def get_split(self,
                  number_of_cells: int):
        df1 = self.data.loc[:number_of_cells-2, :].reset_index(drop=True)
        df2 = self.data.loc[number_of_cells:, :].reset_index(drop=True)
        return df1.copy(), df2.copy()


    def _data_manipulation(self) -> None:
        # split cellCenter into xyz coordinates
        df = self.data["cellCenter"].str.split(expand=True).rename(columns={
            0: "xCellCenter", 1: "yCellCenter", 2: "zCellCenter"})
        # repeat for intPoints
        df = df.join(self.data["intPoints"].str.split(expand=True)).rename(columns={
            0: "xIntPoint1", 1: "yIntPoint1", 2: "zIntPoint1",
            3: "xIntPoint2", 4: "yIntPoint2", 5: "zIntPoint2",
            6: "xIntPoint3", 7: "yIntPoint3", 8: "zIntPoint3"})
        # repeat for surface normal
        df = df.join(self.data["surfNorm"].str.split(expand=True)).rename(columns={
            0: "xSurfNorm", 1: "ySurfNorm", 2: "zSurfNorm"})
        # strip number of interpolation points
        df["xIntPoint1"] = df["xIntPoint1"].str.lstrip("3")
        # add cell ids
        df = df.join(self.data["cellI"])
        # strip brackets from all points
        df = df.map(lambda x: x.strip("()") if isinstance(x, str) else x, na_action="ignore")
        # convert from string to number
        df = df.apply(pd.to_numeric)
        # save as attribute
        self.data = df.copy()
