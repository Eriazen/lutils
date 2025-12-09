from pathlib import Path
import re
import subprocess


# load provided OpenFoam version
def load_of(of_bin: str) -> None:
    """
    Sources or executes the specified OpenFOAM binary/environment script.

    Parameters
    ----------
    of_bin : str
        The file path to the OpenFOAM binary or sourcing script.
    """
    subprocess.run(of_bin)


# Check if path exists, create dir if not
def check_dir(path: Path) -> None:
    """
    Ensures that a directory exists, creating it if necessary.

    Parameters
    ----------
    path : Path
        The directory path to check or create.
    """
    if not path.exists():
        Path.mkdir(path)


# Check if input is of type list
def is_list_str(key) -> bool:
    """
    Validates if the input key is a list composed exclusively of strings.

    Parameters
    ----------
    key : Any
        The object to validate.

    Returns
    -------
    bool
        True if `key` is a list of strings, False otherwise.
    """
    return isinstance(key, list) and all(isinstance(k, str) for k in key)


# find OpenFOAM version based on log.* files
def get_of_version(case_path: Path) -> int | None:
    """
    Extracts the OpenFOAM version number from the case's solver log.

    This function first identifies the solver used via 'system/controlDict',
    then searches the corresponding log file for the version string.

    Parameters
    ----------
    case_path : Path
        The root directory of the OpenFOAM case.

    Returns
    -------
    int or None
        The major version number if found (e.g., 2312, 11), otherwise None.

    Raises
    ------
    ValueError
        If 'system/controlDict' is missing or if the solver name cannot be found within it.
    """
    path = case_path / 'system/controlDict'
    # Precompile regex to save time
    ver = re.compile(r'Version:\s+(\S+)')
    # Check if controlDict exists, find solver name
    if path.exists():
        solver_log = find_in_file(path, 'application')
    else:
        raise ValueError('Invalid file path: controlDict not found.')
    # Check if solver name found, join path
    if solver_log:
        log_path = Path(case_path / f'log.{solver_log.strip(';')}')
    else:
        raise ValueError('Solver name not found in controlDict')
    # Open solver log and find OpenFOAMa version
    with log_path.open() as f:
        # Regex OpenFOAM version
        for line in f:
            found = ver.search(line)
            # If found, return version cast to int
            if found:
                return int(found.group(1))
        return None


def find_in_file(path: Path,
                 str_id: str,
                 return_next: bool = True) -> bool | str | None:
    """
    Searches for a specific string pattern within a file.

    Parameters
    ----------
    path : Path
        The path to the target file.
    str_id : str
        The string pattern or regex to search for.
    return_next : bool, optional
        If True, returns the non-whitespace string immediately following the match.
        If False, returns True immediately upon finding a match. Default is True.

    Returns
    -------
    str or bool or None
        - If `return_next` is True: The string following the match, or None if not found.
        - If `return_next` is False: True if the match exists, False otherwise.
    """
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
