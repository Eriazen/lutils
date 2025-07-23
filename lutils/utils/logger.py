import os
import numpy as np
from abc import ABC

from .utils import check_dir


class BaseLog(ABC):
    '''

    '''
    def __init__(self,
                 log_name: str,
                 dtype: np.dtype,
                 case_path: str,
                 log_dir: str = 'logs/') -> None:
        '''

        '''
        self.name = log_name
        self._log_dtype = dtype
        self._log_dir = os.path.join(case_path, log_dir)
        self._log = np.empty((0,), dtype=self._log_dtype)

        check_dir(self._log_dir)

    def add_entry(self,
                  row: tuple) -> None:
        '''

        '''
        self._log = np.append(self._log, np.array(row, dtype=self._log_dtype))

    def add_batch(self,
                  batch: np.ndarray) -> None:
        '''

        '''
        self._log = np.concatenate((self._log, batch))

    def write(self,
              file_name: str,
              header: str | None = None):
        '''

        '''
        path = os.path.join(self._log_dir, file_name)

        with open(path, 'w') as f:
            if header:
                f.write(f'{header}\n\n')
            f.write(self._format_table())

    def _format_table(self):
        '''

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