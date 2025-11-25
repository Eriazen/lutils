import numpy as np
from pathlib import Path

from lutils.io.loader import load_internal_field, load_residuals
from lutils.utils.misc import get_of_version, check_dir
from lutils.core.types import DataFrame


class FoamCase:
    '''
    Base class representing the OpenFOAM case.
    Contains data relevant for management and post processing.
    '''

    def __init__(self,
                 case_path: str,
                 label: str | None = None,
                 log_dir: str = 'logs/',
                 of_version: int = 0) -> None:
        '''
        Initialize the FoamCase class.

        Parameters:
            - case_path: path to OpenFOAM case folder
            - label: optional case label
            - log_dir: directory to store logs
            - of_version: version of OpenFOAM used
        '''
        self._case_path = Path(case_path)
        self._log_dir = log_dir
        self.label = label
        self.fields = {}

        # Check if log folder exists, otherwise create new one
        check_dir(self._case_path / self._log_dir)

        # Set speficied version, else try to get version from logs
        if of_version:
            self.of_version = of_version
        else:
            self.of_version = get_of_version(self._case_path)

        if len(str(self.of_version)) == 4:
            self.of_version_type = 'com'
        else:
            self.of_version_type = 'org'

    def add_field(self,
                  file_path: str,
                  field_name: str) -> None:
        '''
        Loads a field of specified name from a specified file, which can be used for further post processing.

        Parameters:
            - file_path: path to file in case folder
            - field_name: str key of desired field
        '''
        self.fields[field_name] = FieldData(
            self._case_path, file_path, field_name)

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
        self.residuals = ResidualsData(
            self._case_path, self.of_version_type, file_path, fields)


class FieldData:
    '''
    Stores the field data loaded from OpenFOAM files.
    '''

    def __init__(self,
                 case_path: Path,
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
              data_axis: str) -> DataFrame:
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

    def _get_cells(self,
                   position_axis: str,
                   position_value: float,
                   data_axis: str,
                   tol: float) -> DataFrame:
        # Get position axis values
        column_names = self.data._header
        data_axis_values = self.data[position_axis]

        # Find all cells close to position value
        sub = np.abs(data_axis_values-position_value)
        near_idx = np.where(sub < tol)[0]

        # Filter data
        filtered = self.data._data[near_idx]
        # Sort filtered data
        col_idx = self.data._map[data_axis]

        return DataFrame(column_names, filtered)


class ResidualsData:
    '''
    Stores the residuals loaded from OpenFOAM files.
    '''

    def __init__(self,
                 case_path: Path,
                 of_version_type: str,
                 file_path: str | None = None,
                 fields: list[str] = []) -> None:
        '''
        Initializes the ResidualsData class.

        Parameters:
            - case_path: path to OpenFOAM case folder
            - file_path: path to file in case folder
            - fields: list of field names to load
        '''
        # Load residuals
        if file_path:
            residuals = load_residuals(case_path, file_path)
        else:
            if of_version_type == 'com':
                residuals = load_residuals(
                    case_path, 'postProcessing/resiuals/0/solverInfo.dat')
            else:
                residuals = load_residuals(
                    case_path, 'postProcessign/residuals/0/residuals.dat')

        # If no fields given load all, else select provided
        if not fields:
            self.data = residuals
        else:
            self.data = DataFrame(fields, residuals[fields])


class InterpolationData:
    pass


class GeometryData:
    pass
