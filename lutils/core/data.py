from pathlib import Path
import subprocess
import petl

from lutils.io.parser import (parse_internal_field,
                              parse_residuals,
                              parse_interpolation)
from lutils.utils.misc import get_of_version, check_dir
from lutils.core.types import DataFrame


class FoamCase:
    """
    A base class representing an OpenFOAM case.

    This class manages the case directory structure, handles script execution,
    and facilitates the loading and storage of post-processing data.

    Parameters
    ----------
    case_path : str
        The file path to the OpenFOAM case directory.
    label : str
        A unique label or identifier for the case.
    log_dir : str, optional
        The directory name where logs will be stored, relative to `case_path`.
        Default is 'logs/'.
    of_version : int, optional
        The specific OpenFOAM version used. If 0, the version is auto-detected
        from existing logs. Default is 0.

    Attributes
    ----------
    of_version : int
        The OpenFOAM version number.
    of_version_type : str
        The type of OpenFOAM distribution ('com' for ESI/OpenCFD, 'org' for Foundation).
        A dictionary mapping field names to their corresponding FieldData objects.
    """

    def __init__(self,
                 case_path: str,
                 label: str,
                 log_dir: str = 'logs/',
                 of_version: int = 0) -> None:
        if not Path(case_path).is_dir():
            raise FileNotFoundError(
                f'Case path not found or in not a directory.')
        self._case_path = Path(case_path)
        self._log_dir = log_dir
        self._label = label
        self._fields = {}

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

    @property
    def case_path(self):
        """Path: The absolute path to the case directory."""
        return self._case_path

    @property
    def label(self):
        """str: The case label."""
        return self._label

    @property
    def fields(self):
        """dict[str, FieldData]: A dictionary mapping field names to their corresponding FieldData objects. """
        return self._fields

    def run_script(self,
                   file_name: str) -> None:
        """
        Executes an arbitrary script within the context of the OpenFOAM case.

        Parameters
        ----------
        file_name : str
            The path to the script file. If a relative path is provided, it is
            resolved relative to the case directory. Absolute paths are used as-is.

        Raises
        ------
        FileNotFoundError
            If the script file does not exist at the resolved path.
        RuntimeError
            If the script execution fails (returns a non-zero exit code) or if an
            unexpected error occurs during execution.
        """
        script_path = Path(file_name)

        # Check if script_path is absolute, else run relative to dir case
        if script_path.is_absolute():
            command = str(script_path)

            if not script_path.exists():
                raise FileNotFoundError(
                    f'Script file not found at absolute path: {script_path}')
        else:
            full_script_path = self.case_path / script_path

            if not full_script_path.exists():
                raise FileNotFoundError(
                    f'Script file not found inside case directory: {full_script_path}')

            command = f'./{file_name}'

        try:
            # Run script inside case directory
            subprocess.run(command, cwd=self.case_path, check=True)
        except subprocess.CalledProcessError as e:
            err_msg = (
                f'Script execution failed for case "{self.label}" at path: {self.case_path}.')
            raise RuntimeError(err_msg) from e
        except Exception as e:
            raise RuntimeError(
                f'An unexpected error occured while trying to run script "{file_name}" for case "{self.label}": {e}')

    def add_field(self,
                  file_path: str,
                  field_name: str) -> None:
        """
        Loads field data from a file and registers it to the case.

        Parameters
        ----------
        file_path : str
            The path to the data file, relative to the case directory.
        field_name : str
            The unique name (key) to assign to this field data.
        """
        self.fields[field_name] = FieldData(
            self.case_path, file_path, field_name)

    def del_field(self,
                  field_name: str) -> None:
        """
        Removes a specified field from the case.

        Parameters
        ----------
        field_name : str
            The name of the field to delete.
        """
        try:
            del self.fields[field_name]
        except ValueError:
            print(
                f'Field "{field_name}" not "{self.label}" fields. Skipping deletion.')

    def add_residuals(self,
                      file_path: str,
                      fields: list[str] = []) -> None:
        """
        Loads residual data from a specified file.

        Parameters
        ----------
        file_path : str
            The path to the residuals file, relative to the case directory.
        fields : list[str], optional
            A list of specific residual fields to load. If empty, all available
            fields are loaded. Default is an empty list.
        """
        self.residuals = ResidualsData(
            self.case_path, file_path, fields)


class FieldData:
    """
    A container for field data loaded from OpenFOAM output files.

    Parameters
    ----------
    case_path : Path
        The root path of the OpenFOAM case.
    file_path : str
        The path to the specific data file, relative to `case_path`.
    field_name : str
        The name identifying this field.
    """

    def __init__(self,
                 case_path: Path,
                 file_path: str,
                 field_name: str) -> None:
        # Parse data into DataFrame
        raw_table = parse_internal_field(case_path / file_path)
        self._name = field_name

        # Filter relevant columns
        self._data = petl.cut(raw_table, 'x', 'y', 'z', self._name)

    @property
    def name(self):
        """str: The field name."""
        return self._name

    @property
    def data(self):
        """petl.Table: A petl.Table containing the parsed internal field data."""
        return self._data

    def get_cells(self,
                  position_axis: str,
                  position_value: float,
                  data_axis: str,
                  tol: float) -> petl.Table:
        """
        Extracts a subset of cells near a specific coordinate and sorts them.

        Parameters
        ----------
        position_axis : str
            The axis name to filter by (e.g., 'x', 'y', or 'z').
        position_value : float
            The target coordinate value along `position_axis`.
        data_axis : str
            The column name to use for sorting the resulting data.
        tol : float
            The tolerance radius around `position_value` for cell selection.

        Returns
        -------
        petl.Table
            A petl.Table containing the filtered cells, sorted by `data_axis`.
        """
        def is_near(row):
            val = row[position_axis]
            if val is None:
                return False
            return abs(val - position_value) < tol

        res = (self._data.select(is_near).sort(data_axis))

        return res


class ResidualsData:
    """
    A container for residual data loaded from OpenFOAM output files.

    Parameters
    ----------
    case_path : Path
        The root path of the OpenFOAM case.
    file_path : str
        The path to the residuals file, relative to `case_path`.
    fields : list[str], optional
        A list of specific residual fields to extract. If empty, all fields are loaded.
        Default is an empty list.
    """

    def __init__(self,
                 case_path: Path,
                 file_path: str,
                 fields: list[str] = []) -> None:
        # Load residuals
        residuals = parse_residuals(case_path / file_path)

        # If no fields given load all, else select provided
        if not fields:
            self._data = residuals
        else:
            self._data = DataFrame(fields, residuals[fields])

    @property
    def data(self):
        """DataFrame: A DataFrame containing the parsed residuals."""
        return self._data


class InterpolationData:
    def __init__(self,
                 case_path: Path,
                 file_path: str,
                 fields: list[str] = []) -> None:
        interpolation = parse_interpolation(case_path / file_path)

        if not fields:
            self._data = interpolation
        else:
            self._data = DataFrame(fields, interpolation[fields])

        HEADER = ['cellCenter', 'surfNorm', 'intPoints', 'intCells']

        for col in HEADER:
            try:
                res = self._data[col]
                print(res)
            except KeyError:
                continue


class GeometryData:
    pass
