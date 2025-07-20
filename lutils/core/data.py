import numpy as np

from ..io.loader import load_internal_field
from .types import DataFrame


class FoamCase:
    '''
    Base class representing one OpenFOAM case. Contains data relevant for post processing.
    '''
    def __init__(self,
                 case_path: str) -> None:
        '''
        Initialize the FoamCase class.

        Parameters:
            - case_path: path to OpenFOAM case folder
        '''
        self.case_path = case_path
        self.fields: dict[str, FieldData] = {}

    def add_field(self,
                  file_path: str,
                  field_name: str) -> None:
        '''
        Loads a field of specified name from a specified file, which can be used for further post processing.

        Parameters:
            - file_path: path to file in case folder
            - field_name: str key of desired field
        '''
        self.fields[field_name] = FieldData(self.case_path, file_path, field_name)

    def del_field(self,
                  field_name: str) -> None:
        '''
        Deletes a specified field from the case class.

        Parameters:
            - field_name: str key of desired field
        '''
        del self.fields[field_name]


class BaseDataClass:
    '''
    Base class used to implement specific data classes and class functions.
    '''
    def __init__(self,
                 case_path: str,
                 file_path: str) -> None:
        '''
        Initializes the BaseDataClass

        Parameters:
            - case_path: path to OpenFOAM case folder
            - file_path: path to file in case folder
        '''
        self.internal_field = load_internal_field(case_path, file_path)


class FieldData(BaseDataClass):
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
        super().__init__(case_path, file_path)

        self.name = field_name
        keys = ['x', 'y', 'z', self.name]
        self.data = DataFrame(keys, self.internal_field[keys])


class ResidualsData:
    pass


class InterpolationData:
    pass


class GeometryData:
    pass
