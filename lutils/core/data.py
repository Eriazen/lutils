import os
import numpy as np

from ..io.loader import load_internal_field
from ..utils.utils import get_of_version, check_dir
from .types import DataFrame


class FoamCase:
    '''
    Base class representing one OpenFOAM case. Contains data relevant for post processing.
    '''
    def __init__(self,
                 case_path: str,
                 label: str,
                 log_dir: str = './logs/',
                 of_version: int = 0) -> None:
        '''
        Initialize the FoamCase class.

        Parameters:
            - case_path: path to OpenFOAM case folder
            - label: case label used in e.g. plot labels
            - of_version: version of OpenFOAM used, leave at 0 to autocheck log files
        '''
        self._case_path = case_path
        self._log_dir = log_dir
        self.label = label
        self.fields = {}

        # Check if log folder exists, otherwise create
        check_dir(os.path.join(self._case_path, self._log_dir))

        # Set speficied version, else try to get version from logs
        if of_version != 0:
            self.of_version = of_version
        else:
            self.of_version = get_of_version(self._case_path)

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
        del self.fields[field_name]


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


class ResidualsData:
    pass


class InterpolationData:
    pass


class GeometryData:
    pass
