import os
import numpy as np
from abc import ABC

from .misc import check_dir


class BaseLog(ABC):
    '''
    Base class for logging OpenFOAM case data to NumPy array and writing them to a formatted text file.
    '''
    def __init__(self,
                 log_name: str,
                 dtype: np.dtype,
                 case_path: str,
                 log_dir: str = 'logs/') -> None:
        '''
        Initialize the BaseLog object, create internal log array and ensure log directory exists.

        Parameters:
        - log_name: name of the log
        - dtype: NumPy structured dtype for log entries
        - case_path: path to OpenFOAM case folder
        - log_dir: directory to store logs, relative to case_path

        '''
        self.name = log_name
        self._log_dtype = dtype
        self._log_dir = os.path.join(case_path, log_dir)
        self._log = np.empty((0,), dtype=self._log_dtype)

        check_dir(self._log_dir)

    def add_entry(self,
                  row: tuple) -> None:
        '''
        Add a signle row to the log.

        Parameters:
            - row: a tuple matching the log dtype
        '''
        self._log = np.append(self._log, np.array(row, dtype=self._log_dtype))

    def add_batch(self,
                  batch: np.ndarray) -> None:
        '''
        Add multiple rows to the log.

        Parameters:
            - batch: structured NumPy array matching the log dtype
        '''
        self._log = np.concatenate((self._log, batch))

    def write(self,
              file_name: str,
              header: str | None = None) -> None:
        '''
        Write the logged data to a text file in a table format.

        Parameters:
            - file_name: name of the output file
            - header: optional header at the top of the log file
        '''
        path = os.path.join(self._log_dir, file_name)

        with open(path, 'w') as f:
            if header:
                f.write(f'{header}\n\n')
            f.write(self._format_table())

    def _format_table(self) -> str:
        '''
        Convert the internal log array to a readable table format.

        Returns:
            - str: formatted table as a string
        '''
        lines = []
        col_names = self._log_dtype.names
        col_widths = [max(len(col), 10) for col in col_names]

        header = ' '.join(f'{col:<{w}}' for col, w in zip(col_names, col_widths))
        lines.append(header)
        lines.append('-' * len(header))
        
        if self._log.shape[0] <= 1:
            row = self._log
            line = ' '.join(f'{row[0][i]:<{w}.6g}' if isinstance(row[0][i], float) else f'{row[0][i]:<{w}}'
                            for i, w in enumerate(col_widths))
            lines.append(line)
        else:
            for row in self._log:
                line = ' '.join(f'{row[i]:<{w}.6g}' if isinstance(row[i], float) else f'{row[i]:<{w}}'
                                for i, w in enumerate(col_widths))
                lines.append(line)

        return '\n'.join(lines)
