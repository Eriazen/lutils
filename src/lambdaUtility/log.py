import pandas as pd
import os
from abc import ABC, abstractmethod


class Log(ABC):
    def __init__(self, log_dir="./logs/"):
        self._log = pd.Series()
        self._log_dir = log_dir

        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)

    def concat(self, data: pd.Series):
        self._log = pd.concat([self._log, data], ignore_index=True)

    def _cellid_to_int(self):
        if "cellI" in self._log:
            self._log["cellI"] = self._log["cellI"].astype(int)
    
    @abstractmethod
    def write(self):
        pass


class DsLog(Log):
    def __init__(self, log_dir="./logs/"):
        super().__init__(log_dir)

    def write(self, file: str):
        self._log = self._log.dropna(axis=1)
        self._cellid_to_int()
        out = self._log.to_string(index=False)
        with open(self._log_dir+file, "w") as f:
            f.write("-------------ds difference-------------\n")
            f.write(out)
            f.write("\nTotal number of inconsistent cells: %i" % self._log.shape[0])


class IntLog(Log):

    def __init__(self, log_dir="./logs/"):
        super().__init__(log_dir)

    def write(self, file: str):
        self._log = self._log.dropna(axis=1)
        self._cellid_to_int()
        out = self._log.to_string(index=False)
        with open(self._log_dir+file, "w") as f:
            f.write("-------------intPoint inconsistency-------------\n")
            f.write(out)
            f.write("\nTotal number of inconsistent cells: %i" % self._log.shape[0])