import os
import re
from typing import Union


# Check if path exists, create dir if not
def check_dir(path: str) -> None:
    '''
    Check if path exists, create directory if not.
    '''
    if not os.path.exists(path):
        os.makedirs(path)


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

def get_of_version(case_path: str) -> Union[int, None]:
    '''
    Get version of OpenFOAM used in speficied case. Version is extracted from solver log file.

    Parameters:
        - case_path: path to OpenFOAM case folder

    Returns:
        - int: if version found
        - None: if version not found
    '''
    # Get list of files in case folder
    for file in os.listdir(case_path):
        # Look for solver log files
        if file.startswith('log.') and file.endswith('Foam'):
            path = os.path.join(case_path, file)
            with open(os.path.join(path), 'r') as f:
                # Regex OpenFOAM version
                for line in f:
                    found = re.search(r'Version:\s+(\S+)', line)
                    # If found, return version cast to int, else raise exception
                    if found:
                        return int(found.group(1))
    # If no logs found, raise error
    raise ValueError('No logs found to get OpenFOAM version. Specify version manually in FoamCase.')

def find_in_log(case_path: str,
                log_name: str,
                str_id: str) -> Union[str, None]:
    '''
    Find arbitrary string in specified log.

    Parameters:
        - case_path: path to OpenFOAM case folder
        - log_name: name of log to search in
        - str_id: desired string

    Returns:
        - str: if str found
        - None: if str not found
    '''
    fileName = os.path.join(case_path, log_name)
    with open(fileName,'r') as file:
        data = file.readlines()
    to_return = None

    for line in data:
        if str_id in line:
            to_return = line[:-1]

    return to_return
