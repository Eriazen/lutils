# external packages
import matplotlib.pyplot as plt
import matplotlib.figure as fgr
from typing import Union, Optional
# internal packages
from ..core import sim
from ..utils import check_dir
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
                 simulation: sim.Simulation,
                 field_name: str,
                 label: str) -> None:
        self._plot_data[label] = simulation.fields[field_name]

    def del_data(self,
                 label: str) -> None:
        try:
            del self._plot_data[label]
        except:
            raise ValueError("No data to delete.")

    def plot_profile(self,
                     out_file_name: str,
                     field_name: str,
                     across: str,
                     profile: str,
                     profile_value: float,
                     title: Optional[str] = None,
                     xlabel: Optional[str] = None,
                     ylabel: Optional[str] = None,
                     fig_id: Optional[Union[str, int]] = None) -> None:
        figure = self._fig_exists(fig_id)

        if title != None:
            plt.title(title, fontsize=22)

        if xlabel != None:
            plt.xlabel(xlabel, fontsize=18)

        if ylabel != None:
            plt.ylabel(ylabel, fontsize=18)

        for key, value in self._plot_data.items():
            trimmed = value.get_trimmed(profile, across, profile_value)
            plt.scatter(trimmed[profile],
                        trimmed[field_name], label=key)

        figure.legend(fontsize=18)

        try:
            figure.savefig(self._plot_dir+out_file_name)
        except:
            raise TypeError("Invalid file format in {out_file_name}.")

    def _fig_exists(self,
                    fig_id: Optional[Union[str, int]]) -> fgr.FigureBase:
        if fig_id == None:
            return plt.figure(figsize=(20, 12))
        elif plt.fignum_exists(fig_id):
            return plt.figure(fig_id)
        else:
            return plt.figure(fig_id, figsize=(20, 12))

# def plot_int_points(data_object: Union[data.BFSData, data.NACAData],
#                     filename: str,
#                     range_start: float = 0,
#                     range_stop: float = 1,
#                     x_step: float = 1.0,
#                     y_step: float = 0.01,
#                     func: Callable[[float], float] = None) -> None:
#     # check if dir exists
#     check_dir(plot_path)
#
#     if isinstance(data_object, data.BFSData):
#         # select values based on input range
#         df = values_in_range(data_object.df.sort_values(by="xCellCenter"),
#                                     "xCellCenter", range_start, range_stop)
#         df = df.reset_index(drop=True)
#         # plot
#         bfs_int_points(plot_path+filename, df, range_stop, x_step, y_step)
#     elif isinstance(data_object, data.NACAData):
#         # select values based on input range
#         df = values_in_range(data_object.df, "yCellCenter", range_start, range_stop)
#         # plot
#         naca_int_points(plot_path+filename, df, func)
#     else:
#         raise TypeError("Incorrect data object input.")
