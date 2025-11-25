import matplotlib.pyplot as plt
import matplotlib.figure as fgr
from pathlib import Path

from lutils.core.data import FoamCase
from lutils.utils.misc import check_dir


class FoamPlot:
    '''
    Base class for plotting OpenFOAM post processing data.
    '''

    def __init__(self,
                 plot_dir: str = './plots/') -> None:
        '''
        Initializes the FoamPlot class.

        Parameters:
            - plot_dir: directory to store plots
        '''
        self._plot_dir = Path(plot_dir)
        self._plot_data = {}

        check_dir(self._plot_dir)

    def add_data(self,
                 case: FoamCase,
                 field_name: str,
                 label: str) -> None:
        '''
        Loads plot data from specified case object.

        Parameters:
            - case: FoamCase object containing desired field
            - field_name: str key of desired field
            - label: plot data label, used for plotting
        '''
        self._plot_data[label] = case.fields[field_name]

    def del_data(self,
                 label: str) -> None:
        '''
        Deletes specified plot data from the FoamPlot class.

        Parameters:
            - label: plot data label

        '''
        try:
            del self._plot_data[label]
        except:
            raise ValueError('Plot data with specified label does not exist.')

    def plot_profile(self,
                     output_file: str,
                     field_name: str,
                     data_axis: str,
                     position_axis: str,
                     position_value: float,
                     position_tol: float,
                     title: str | None = None,
                     xlabel: str | None = None,
                     ylabel: str | None = None,
                     fig_id: str | int | None = None,
                     csv: bool = True) -> None:
        '''
        Plot all data stored in FoamPlot instance over a line in specified direction.

        Parameters:
            - output_file: name of output file
            - field_name: name of plotted field
            - across: 
            - profile: 
            - profile_value:
            - title: plot title
            - xlabel: plot x label
            - ylabel: plot y label
            - fig_id: plot figure id
        '''
        figure = self._fig_exists(fig_id)

        if title != None:
            plt.title(title, fontsize=22)

        if xlabel != None:
            plt.xlabel(xlabel, fontsize=18)

        if ylabel != None:
            plt.ylabel(ylabel, fontsize=18)

        for key, value in self._plot_data.items():
            trimmed = value._get_cells(
                position_axis, position_value, data_axis, position_tol)
            plt.scatter(trimmed[data_axis],
                        trimmed[field_name], label=key)
            if csv:
                trimmed.to_csv(self._plot_dir / str(key+'.csv'))

        figure.legend(fontsize=18)

        figure.savefig(self._plot_dir / output_file)

    def _fig_exists(self,
                    fig_id: str | int | None) -> fgr.Figure:
        '''
        Checks if figure with specified id already exists, creates one if not.

        Parameters:
            - fig_id: figure id of type int or str

        Returns:
            - plt.figure: new or existing matplotlib.figure.Figure
        '''
        if fig_id == None:
            return plt.figure(figsize=(20, 12))
        elif plt.fignum_exists(fig_id):
            return plt.figure(fig_id)
        else:
            return plt.figure(fig_id, figsize=(20, 12))
