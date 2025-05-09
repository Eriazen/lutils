# external packages
import matplotlib.pyplot as plt
from typing import Callable, Union
# internal packages
from ..core import data
from ..utils import check_dir
from .plot_utils import values_in_range, Field
from .plot_bfs import *
from .plot_naca import *

plot_path = "./plots/"
class PlotPostProcessing:
    def __init__(self,
                 plot_dir: str = "./plots/") -> None:
        self._plot_dir = plot_dir
        self._plot_data = {}

        check_dir(self._plot_dir)

    def add_data(self,
                 file_path: str,
                 field_name: str,
                 label: str) -> None:
        self._plot_data[label] = Field(file_path, field_name)

    def del_data(self,
                 label: str) -> None:
        del self._plot_data[label]

    def set_params(self,
                   profile_values: list):
        self.profile_values = profile_values

    def plot_profile(self,
                     out_file_name: str,
                     profile: str,
                     profile_value: float,
                     title: str = None,
                     xlabel: str = None,
                     ylabel: str = None,
                     fig_id: Union[str, int] = None) -> None:
        if fig_id != None:
            figure = plt.figure(fig_id, figsize=(20, 12))
        else:
            figure = plt.figure(figsize=(20, 12))

        if title != None:
            plt.title(title, fontsize=22)

        if xlabel != None:
            plt.xlabel(xlabel, fontsize=18)

        if ylabel != None:
            plt.ylabel(ylabel, fontsize=18)

        for key, value in self._plot_data.items():
            value.trim_data(profile, profile_value)
            plt.scatter(value.get_profile(profile), value.field, label=key)

        figure.legend(fontsize=18)

        try:
            figure.savefig(self._plot_dir+out_file_name)
        except:
            raise TypeError("Invalid file format in {out_file_name}.")
        
def plot_profile(filename: str,
                 simple: pd.DataFrame,
                 hfdibrans: pd.DataFrame,
                 profile: str,
                 field: str,
                 title: str = None,
                 label1: str = "simple",
                 label2: str = "hfdibrans",
                 grid: bool = False) -> None:
    check_dir(plot_path)
    # plot figure
    fig = plt.figure(figsize=(20, 12))
    plt.scatter(simple[profile], simple[field], label=label1)
    plt.scatter(hfdibrans[profile], hfdibrans[field], label=label2)
    plt.legend(fontsize=18)
    plt.xlabel(profile, fontsize=18)
    plt.ylabel(field, fontsize=18)
    plt.title(title, fontsize=22)
    if grid:
        plt.grid()
    # save figure
    fig.savefig(plot_path+filename)
    plt.close(fig)


def plot_int_points(data_object: Union[data.BFSData, data.NACAData],
                    filename: str,
                    range_start: float = 0,
                    range_stop: float = 1,
                    x_step: float = 1.0,
                    y_step: float = 0.01,
                    func: Callable[[float], float] = None) -> None:
    # check if dir exists
    check_dir(plot_path)
    
    if isinstance(data_object, data.BFSData):
        # select values based on input range
        df = values_in_range(data_object.df.sort_values(by="xCellCenter"),
                                    "xCellCenter", range_start, range_stop)
        df = df.reset_index(drop=True)
        # plot
        bfs_int_points(plot_path+filename, df, range_stop, x_step, y_step)
    elif isinstance(data_object, data.NACAData):
        # select values based on input range
        df = values_in_range(data_object.df, "yCellCenter", range_start, range_stop)
        # plot
        naca_int_points(plot_path+filename, df, func)
    else:
        raise TypeError("Incorrect data object input.")
