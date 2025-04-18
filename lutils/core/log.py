import pandas as pd
import os
from abc import ABC, abstractmethod


class Log(ABC):
    def __init__(self,
                 log_dir="./logs/") -> None:
        self._log = pd.Series()
        self._log_dir = log_dir

        # check and create directory
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)

    # concatenate info onto log
    def concat(self,
               data: pd.Series) -> None:
        self._log = pd.concat([self._log, data], ignore_index=True)
        self._log = self._log.dropna(axis=1)

    # convert cell ids from float to int
    def _cellid_to_int(self) -> None:
        if "cellI" in self._log:
            self._log["cellI"] = self._log["cellI"].astype(int)
    
    @abstractmethod
    def write(self) -> None:
        pass


class DsLog(Log):
    def __init__(self,
                 log_dir="./logs/"):
        super().__init__(log_dir)

    def write(self,
              file: str) -> None:
        self._cellid_to_int()
        # convert dataframe to string
        out = self._log.to_string(index=False)
        # open out stream and write
        with open(self._log_dir+file, "w") as f:
            f.write("-------------ds difference-------------\n")
            f.write(out)
            f.write("\nTotal number of inconsistent cells: %i" % self._log.shape[0])


class IntLog(Log):
    def __init__(self,
                 log_dir="./logs/") -> None:
        super().__init__(log_dir)

    def write(self,
              file: str) -> None:
        self._cellid_to_int()
        # covert dataframe to string
        out = self._log.to_string(index=False)
        # open out stream and write
        with open(self._log_dir+file, "w") as f:
            f.write("-------------intPoint inconsistency-------------\n")
            f.write(out)
            f.write("\nTotal number of inconsistent cells: %i" % self._log.shape[0])


class ProfileLog(Log):
    def __init__(self,
                 log_dir="./logs/") -> None:
        super().__init__(log_dir)

    def write(self,
              file: str) -> None:
        self._cellid_to_int()
        # covert dataframe to string
        out = self._log.to_string(index=False)
        # open out stream and write
        with open(self._log_dir+file, "w") as f:
            f.write("-------------profile values-------------\n")
            f.write(out)
            f.write("\nTotal number of points: %i" % self._log.shape[0])