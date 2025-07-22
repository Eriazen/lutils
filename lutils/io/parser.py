import os
import numpy as np


def parse_internal_field(case_path: str,
                         file_path: str) -> tuple[list[str], np.ndarray]:
    '''
    Parses a CSV-style file output from readAndWrite functions into Python.
    
    Parameters:
        - case_path: path to OpenFOAM case folder
        - file_path: path to file in case folder

    Returns:
        - header: list of column names
        - data: structured NumPy array
    '''
    # Concatenate path
    path = os.path.join(case_path, file_path)
    # Open and parse file
    with open(path) as f:
        lines = f.readlines()
        # Separate header
        header = lines[0].strip().split(',')
        data = []
        for line in lines[1:]:
            # Skip empty lines
            if not line.strip():
                continue
            values = line.strip().split(',')
            # Convert to float, convert to np.nan for empty cells
            row = [float(x) if x else np.nan for x in values]
            data.append(row)
    # Convert the list into np.ndarray
    arr = np.array(data)
    return header, arr


def parse_residuals(case_path: str,
                    file_path: str) -> tuple[list[str], np.ndarray]:
    '''
    Parses an OpenFOAM residuals file into Python.

    Parameters:
        - case_path: path to OpenFOAM case folder
        - file_path: path to file in case folder
    Returns:
        - header: list of column names
        - data: structured NumPy array
    '''
    # Concatenate path
    path = os.path.join(case_path, file_path)
    # Open and parse file
    with open(path) as f:
        lines = f.readlines()
        # Separate header
        header = lines[1].strip('#').split()
        data = []
        for line in lines[2:]:
            # Skip empty lines
            if not line.strip():
                continue
            values = line.strip().split()
            # Convert to float, if non convertable leave as is, covnert to np.nan for empty cells
            row = []
            for x in values:
                if x:
                    try:
                        row.append(float(x))
                    except:
                        row.append(x)
                else:
                    row.append(np.nan)
            data.append(row)
    # Convert the list into np.ndarray
    arr = np.array(data)
    return header, arr
