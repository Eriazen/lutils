# external packages
import matplotlib.pyplot as plt
from typing import Callable, Union
# internal packages
from ..core import data
from ..utils import *
from .plot_utils import *
from .plot_bfs import *
from .plot_naca import *

plot_path = "./plots/"

def plot_profile(filename: str,
                 simple: str,
                 hfdibrans: str,
                 profile: str,
                 field: str,
                 grid: bool = False) -> None:
    check_dir(plot_path)
    # plot figure
    fig = plt.figure(figsize=(20, 12))
    plt.scatter(simple[profile], simple[field], label="simple")
    plt.scatter(hfdibrans[profile], hfdibrans[field], label="hfdibrans")
    plt.legend()
    if grid:
        plt.grid()
    # save figure
    fig.savefig(plot_path+filename)
    plt.close(fig)


def plot_int_points(data_obj: Union[data.BFSData, data.NACAData],
                    filename: str,
                    range_start: float = 0,
                    range_stop: float = 1,
                    func: Callable[[], float] = None):
    # check if dir exists
    check_dir(plot_path)
    
    if isinstance(data_obj, data.BFSData):
        # select values based on input range
        df = values_in_range(data_obj.df.sort_values(by="xCellCenter"),
                                    "xCellCenter", range_start, range_stop)
        df = df.reset_index(drop=True)
        # plot figure
        bfs_int_points(plot_path+filename, df, range_stop)
    elif isinstance(data_obj, data.NACAData):
        # select values based on input range
        df = values_in_range(data_obj.df, "yCellCenter", range_start, range_stop)
        # plot figure
        naca_int_points(plot_path+filename, df, func)
    else:
        print("Incorrect data object as input")