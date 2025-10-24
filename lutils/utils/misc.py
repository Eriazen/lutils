import os
from pathlib import Path
import re


# Check if path exists, create dir if not
def check_dir(path: Path) -> None:
    '''
    Check if path exists, create directory if not.
    '''
    if not path.exists():
        Path.mkdir(path)


def is_list_str(key) -> bool:
    '''
    Check if input key is a list of strings.

    Parameters:
        - key: key to check

    Returns:
        - bool
    '''
    if not isinstance(key, list):
        return False
    if not all(isinstance(k, str) for k in key):
        return False
    return True

def get_of_version(case_path: Path) -> int | None:
    '''
    Get version of OpenFOAM used in speficied case. Version is extracted from solver log file.

    Parameters:
        - case_path: path to OpenFOAM case folder

    Returns:
        - int: if version found
        - None: if version not found
    '''
    dict_path = 'system/controlDict'
    ver = re.compile(r'Version:\s+(\S+)')
    # Check if controlDict exists, find solver name
    if Path(case_path / dict_path).exists():
        solver_log = find_in_file(case_path, dict_path, 'application')
    else:
        raise ValueError('Invalid file path: controlDict not found.')
    # Check if solver name found, join path
    if solver_log:
        log_path = Path(case_path, f'log.{solver_log.strip(';')}')
    else:
        raise ValueError('Solver name not found in controlDict')
    # Open solver log and find OpenFOAMa version
    with log_path.open() as f:
        # Regex OpenFOAM version
        for line in f:
            found = ver.search(line)
            # If found, return version cast to int, else raise exception
            if found:
                return int(found.group(1))
        return None

def find_in_file(case_path: Path,
                 file_path: Path,
                 str_id: str,
                 return_next: bool = True) -> bool | str | None:
    '''
    Find arbitrary string in specified file.

    Parameters:
        - case_path: path to OpenFOAM case folder
        - file_path: path to file in case folder
        - str_id: desired string, supports regex
        - return_next: switch between str and bool return

    Returns:
        - str: if str found
        - None: if str not found
    '''
    path = Path(case_path / file_path)
    # Precompile regex to save time
    regex = re.compile(str_id)
    next = re.compile(r'\S+')

    with path.open() as f:
        for line in f:
            # Search file for input string
            match = regex.search(line)
            if match:
                if return_next:
                    # If return_next, search for the next str and return
                    rest = line[match.end():]
                    next_match = next.search(rest)
                    return next_match.group() if next_match else None
                return True
    # If no match return None or False
    return None if return_next else False
