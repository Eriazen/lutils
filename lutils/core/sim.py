# external packages
import matplotlib.figure as fgr
import matplotlib.pyplot as plt
from typing import Optional, Union
# internal packages
from .data import Field, InterpolationInfo
from ..utils import check_dir


class Simulation:
    # DATA MANIPLATION METHODS
    def __init__(self,
                 plot_dir: str = "./plots/",
                 log_dir: str = "./logs/",
                 label: Optional[str] = None) -> None:
        self.fields = {}
        self.interpolation_info = {}
        self.label = label
        self._plot_dir = plot_dir
        self._log_dir = log_dir

        check_dir(self._plot_dir)

    def __str__(self) -> str:
        if self.label == None:
            return "None"
        else:
            return self.label

    def add_field(self,
                  file_path: str,
                  name: str) -> None:
        self.fields[name] = Field(file_path)

    def del_field(self,
                  name: str) -> None:
        try:
            del self.fields[name]
        except:
            raise ValueError("No field to delete.")

    def add_int_info(self,
                     file_path: str,
                     name: str) -> None:
        self.interpolation_info[name] = InterpolationInfo(file_path)

    def del_int_info(self,
                     name: str) -> None:
        try:
            del self.interpolation_info[name]
        except:
            raise ValueError("No interpolation info to delete.")

    # TEST METHODS
    def check_intetpolation(self):
        pass
