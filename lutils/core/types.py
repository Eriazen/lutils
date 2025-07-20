from collections.abc import Mapping, Iterator
import numpy as np

from ..utils.utils import is_list_str


class DataFrame(Mapping):
    def __init__(self,
                 header: list[str],
                 data: np.ndarray) -> None:
        '''
        Initializes the DataFrame.

        Parameters:
            - header: list of str, column names
            - data: 2D NumPy array of shape (rows, columns)
        '''
        self._header = header
        self._data = data
        self._map = {name: idx for idx, name in enumerate(header)}

    def __getitem__(self, key):
        '''
        Return a column, row, cell or multiple columns depending on key type.

        Parameters:
            - key: str, int, tuple or list[str]

        Returns:
            - str: column as a NumPy array
            - int: row as NumPy array
            - tuple: value in a cell at [row, column]
            - list[str]: multiple columns as a NumPy array

        '''
        # Column access using str key
        if isinstance(key, str):
            col_idx = self._map[key]
            return self._data[:, col_idx]
        # Row access using int key
        elif isinstance(key, int):
            return self._data[key]
        # Cell access using tuple key
        elif isinstance(key, tuple):
            row, col = key
            col_idx = self._map[col] if isinstance(col, str) else col
            return self._data[row, col_idx]
        # List of columns using list[str]
        elif is_list_str(key):
            col_idx = []
            for col in key:
                col_idx.append(self._map[col])
            col_idx.sort()
            return self._data[:, col_idx]
        # Raise type error
        else:
            raise TypeError('Invalid key type. Try again with str, int, tuple or list[str].')

    def __iter__(self) -> Iterator[str]:
        '''
        Returns an iterator over column names.
        '''
        return iter(self._header)

    def __repr__(self) -> str:
        '''
        Returns string representation of the DataFrame.
        '''
        return f'{self._header}\n{self._data}'

    def __len__(self) -> int:
        '''
        Returns the number of columns in the DataFrame.
        '''
        return len(self._header)

    def shape(self):
        '''
        Returns the shape of the DataFrame as (rows, columns).
        '''
        return self._data.shape
