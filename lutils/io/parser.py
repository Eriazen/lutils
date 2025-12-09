from pathlib import Path
import numpy as np
import yaml

from lutils.core.types import DataFrame
from lutils.plt_cfg.labels import Labels


def parse_internal_field(path: Path) -> DataFrame:
    '''
    Parses a CSV-style file output from readAndWrite functions into Python.

    Parameters:
        - case_path: path to OpenFOAM case folder
        - file_path: path to file in case folder

    Returns:
        - DataFrame: DataFrame instance with residuals data
    '''
    # Open and parse file
    with path.open() as f:
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

    return DataFrame(header, arr)


def parse_residuals(path: Path) -> DataFrame:
    '''
    Parses an OpenFOAM residuals file into Python.

    Parameters:
        - case_path: path to OpenFOAM case folder
        - file_path: path to file in case folder
    Returns:
        - DataFrame: DataFrame instance with residuals data
    '''
    # Open and parse file
    with path.open() as f:
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

    return DataFrame(header, arr)


def parse_yaml_config(cfg_path: str) -> dict[str, str]:
    '''
    Gets preset labels, otherwise parses labels from file.

    Parameters:
        - cfg_path: preset label name or file path
                    valid preset labels are [velocity, k, nut, epsilon, omega]
    Returns:
        - dict[str, str]: dictionary with [key, label]
    '''
    # check if input matches any preset labels
    labels = Labels()
    match cfg_path:
        case 'velocity':
            return labels.velocity
        case 'k':
            return labels.k
        case 'nut':
            return labels.nut
        case 'epsilon':
            return labels.epsilon
        case 'omega':
            return labels.omega
        case _:
            pass

    # otherwise load labels from file
    path = Path(cfg_path)
    if not path.exists():
        raise FileNotFoundError(f'Config file not found at path: {path}')

    with path.open() as f:
        config = yaml.safe_load(f)

    return config
