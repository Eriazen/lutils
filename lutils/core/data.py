import os
import numpy as np

from ..io.loader import load_internal_field, load_residuals
from ..utils.misc import get_of_version, check_dir
from .types import DataFrame


class FoamCase:
    '''
    Base class representing the OpenFOAM case. Contains data relevant for post processing.
    '''
    def __init__(self,
                 case_path: str,
                 label: str | None = None,
                 log_dir: str = 'logs/',
                 of_version: int = 0,
                 auto_load: bool = True) -> None:
        '''
        Initialize the FoamCase class.

        Parameters:
            - case_path: path to OpenFOAM case folder
            - label: optional case label
            - log_dir: directory to store logs
            - of_version: version of OpenFOAM used, leave at 0 to autocheck log files
            - auto_load: if true, tries to automatically load files from default paths
        '''
        self._case_path = case_path
        self._log_dir = log_dir
        self.label = label
        self.fields = {}

        # Check if log folder exists, otherwise create
        check_dir(os.path.join(self._case_path, self._log_dir))

        # Set speficied version, else try to get version from logs
        if of_version:
            self.of_version = of_version
        else:
            self.of_version = get_of_version(self._case_path)

        # Run autoload if true
        if auto_load:
            self._auto_load()

    def add_field(self,
                  file_path: str,
                  field_name: str) -> None:
        '''
        Loads a field of specified name from a specified file, which can be used for further post processing.

        Parameters:
            - file_path: path to file in case folder
            - field_name: str key of desired field
        '''
        self.fields[field_name] = FieldData(self._case_path, file_path, field_name)

    def del_field(self,
                  field_name: str) -> None:
        '''
        Deletes a specified field from the case class.

        Parameters:
            - field_name: str key of desired field
        '''
        try:
            del self.fields[field_name]
        except:
            raise ValueError('Field with specified name does not exist.')

    def add_residuals(self,
                      file_path: str,
                      fields: list[str] = []) -> None:
        '''
        Load residuals from a specified file.

        Parameters:
            - file_path: path to file in case folder
            - fields: list of field names to load
        '''
        self.residuals = ResidualsData(self._case_path, file_path, fields)

    def _auto_load(self) -> None:
        '''
        Tries to automatically load residuals based on the used OpenFOAM version.
        '''
        if self.of_version == 2312:
            default_path = 'postProcessing/residuals/0/solverInfo.dat'
        elif self.of_version == 8:
            default_path = 'postProcessing/residuals/0/residuals.dat'
        else:
            raise ValueError('You are using an unsupported OpenFOAM version.')

        path = os.path.join(self._case_path, default_path)
        if os.path.exists(path):
            self.residuals = ResidualsData(self._case_path, default_path)
        else:
            print('Auto load failed: default residuals path not found. Please load residuals with the add_residuals function.')


class FieldData:
    '''
    Stores the field data loaded from OpenFOAM files.
    '''
    def __init__(self,
                 case_path: str,
                 file_path: str,
                 field_name: str) -> None:
        '''
        Initializes the FieldData class.

        Parameters:
            - case_path: path to OpenFOAM case folder
            - file_path: path to file in case folder
            - field_name: str key of desired field
        '''
        self._internal_field = load_internal_field(case_path, file_path)

        self.name = field_name
        keys = ['x', 'y', 'z', self.name]
        self.data = DataFrame(keys, self._internal_field[keys])

    def _trim(self,
             position_axis: str,
             position_value: float,
             data_axis: str):
        '''
        Get data with values close to the specified value and sort by desired column.

        Parameters:
            - position_axis: name of horizontal axis
            - position_value: value of horizontal axis
            - data_axis: name of vertical axis

        Returns:
            - np.ndarray sorted by data_axis
        '''
        # Get position axis values
        column_names = self.data._header
        data_axis_values = self.data[position_axis]

        # Find the column value close to position value
        near_idx = np.argmin(np.abs(data_axis_values-position_value))
        near_val = data_axis_values[near_idx]

        # Filter data
        filtered = self.data.filter_rows(position_axis, near_val)

        # Sort filtered data by data axis
        col_idx = self.data._map[data_axis]
        sorted_idx = np.argsort(filtered[:, col_idx])
        sorted = filtered[sorted_idx]

        return DataFrame(column_names, sorted)


class ResidualsData:
    '''
    Stores the residuals loaded from OpenFOAM files.
    '''
    def __init__(self,
                 case_path: str,
                 file_path: str,
                 fields: list[str] = []) -> None:
        '''
        Initializes the ResidualsData class.

        Parameters:
            - case_path: path to OpenFOAM case folder
            - file_path: path to file in case folder
            - fields: list of field names to load
        '''
        # Load residuals
        residuals = load_residuals(case_path, file_path)

        # If no fields given load all, else select provided
        if not fields:
            self.data = residuals
        else:
            self.data = DataFrame(fields, residuals[fields])

class InterpolationData:
    pass


class GeometryData:
    pass
