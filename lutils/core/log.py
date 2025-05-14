# external packages
import pandas as pd
from abc import ABC, abstractmethod
#internal packages
from ..utils import check_dir


class BaseLogClass(ABC):
    def __init__(self,
                 log_dir="./logs/") -> None:
        self._log = pd.Series()
        self._log_dir = log_dir

        # check and create directory
        check_dir(self._log_dir)

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
    def write(self,
              file: str) -> None:
        pass


class DsLog(BaseLogClass):
    def __init__(self,
                 log_dir="./logs/") -> None:
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


class IntLog(BaseLogClass):
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


class ProfileLog(BaseLogClass):
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
