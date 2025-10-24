from pathlib import Path

from .parser import parse_internal_field, parse_residuals
from ..core import types

def load_internal_field(case_path: Path,
                        file_path: str) -> types.DataFrame:
    '''
    Loads parsed OpenFOAM data into custom DataFrame.

    Parameters:
        - case_path: path to OpenFOAM case folder
        - file_path: path to file in case folder

    Returns:
        - DataFrame compromised of header and values
    '''
    # Parse OpenFOAM file
    header, values = parse_internal_field(case_path, file_path)

    return types.DataFrame(header, values)

def load_residuals(case_path: Path,
                   file_path: str) -> types.DataFrame:
    '''
    Loads parsed OpenFOAM data into custom DataFrame.

    Parameters:
        - case_path: path to OpenFOAM case folder
        - file_path: path to file in case folder

    Returns:
        - DataFrame compromised of header 
    '''
    # Parse OpenFOAM file
    header, values = parse_residuals(case_path, file_path)

    return types.DataFrame(header, values)
