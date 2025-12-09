import matplotlib.pyplot as plt
import matplotlib.figure as fgr
from pathlib import Path

from lutils.core.data import FoamCase
from lutils.utils.misc import check_dir
from lutils.io.parser import parse_yaml_config


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

    @property
    def title(self):
        return self._title

    @property
    def xlabel(self):
        return self._xlabel

    @property
    def ylabel(self):
        return self._ylabel

    def _setup_plot(self,
                    label_path: str,
                    style: str) -> None:
        '''
        Sets matplotlib style and plot labels.

        Parameters:
            - label_path: path to YAML file with labels or preset label name
            - style: style name
        '''
        # get and set labels
        labels = parse_yaml_config(label_path)
        self._title = labels['title']
        self._xlabel = labels['xlabel']
        self._ylabel = labels['ylabel']
        # set style
        plt.style.use(style)

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
        except KeyError:
            print(f'Plot data with label "{label}" not found.')

    def plot_profile(self,
                     output_file: str,
                     field: str,
                     data_axis: str,
                     position_axis: str,
                     position_value: float,
                     position_tol: float,
                     labels: str = 'velocity',
                     style: str = 'lutils.plt_cfg.lutils',
                     figure_id: str | int | None = None,
                     out_csv: bool = True) -> None:
        '''
        Plot all data over a line in a specified direction.

        Parameters:
            - output_file: output file name
            - field: plot field 
            - data_axis: data axis
            - position_axis: profile axis
            - position_value: profile value
            - position_tol: profile value tolerance
            - labels: path to YAML file with labels
            - style: matplotlib style
            - figure_id: figure id
            - out_csv: if true, output a csv file with data
        '''

        # get label and style
        self._setup_plot(labels, style)

        # init figure
        figure = self._setup_figure(figure_id)

        # set labels
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # plot all plot data entries
        for key, value in self._plot_data.items():
            trimmed = value._get_cells(
                position_axis, position_value, data_axis, position_tol)
            plt.scatter(trimmed[data_axis],
                        trimmed[field], label=key)
            if out_csv:
                trimmed.to_csv(self._plot_dir / str(key+'.csv'))

        figure.legend()

        figure.savefig(self._plot_dir / output_file)

    def _setup_figure(self,
                      figure_id: str | int | None) -> fgr.Figure | fgr.FigureBase:
        '''
        Gets an existing figure with specified id, otherwise creates one.

        Parameters:
            - figure_id: figure id of type int or str

        Returns:
            - plt.figure: new or existing matplotlib figure
        '''
        if not figure_id:
            return plt.figure()

        return plt.figure(figure_id)
