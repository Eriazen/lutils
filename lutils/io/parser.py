import os
import numpy as np


def parse_internal_field(case_path: str,
                         file_path: str) -> tuple[list[str], np.ndarray]:
    '''
    Parses a CSV-style file output from readAndWrite functions into Python.

    Returns:
        - header: list of column names
        - data: structured NumPy array

    '''
    # concatenate path
    path = os.path.join(case_path, file_path)
    with open(path) as f:
        lines = f.readlines()
        header = lines[0].strip().split(',') # seperate header

        data = []
        for line in lines[1:]:
            if not line.strip(): # skip empty lines
                continue
            values = line.strip().split(',')
            row = [float(x) if x else np.nan for x in values] # convert to float, np.nan for empty values
            data.append(row)

    arr = np.array(data) # convert to array
    return header, arr
