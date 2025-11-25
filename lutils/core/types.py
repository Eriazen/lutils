from collections.abc import MutableMapping, Iterator
import numpy as np
import csv

from lutils.utils.misc import is_list_str


class DataFrame(MutableMapping):
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

    def filter_rows(self,
                    column: str,
                    value: float) -> np.ndarray:
        '''
        Gets rows where column values are close to specified value.

        Parameters:
            - column: column name
            - value: value for comparison

        Returns:
            - filtered np.ndarray
        '''
        # Get id of column
        idx = self._map[column]

        arr = []
        # Check if value in columns is close to specified value for each row
        for row in self._data:
            if np.isclose(row[idx], value):
                arr.append(row)

        return np.array(arr)

    def __getitem__(self,
                    key):
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
            raise TypeError(
                'Invalid key type. Try again with str, int, tuple or list[str].')

    def __setitem__(self,
                    key,
                    value) -> None:
        '''
        Modify a specified value based on key type.

        Parameters:
            - key: str, int, tuple or list[str]
            - value: value to be stored at key
        '''
        # Overwrite column
        if isinstance(key, str):
            self._data[:, key] = value
        # Overwrite row
        elif isinstance(key, int):
            self._data[key] = value
        # Overwrite cell value
        elif isinstance(key, tuple):
            row, col = key
            self._data[row, col] = value
        # Overwrite multiple columns
        elif is_list_str(key):
            for col in key:
                self._data[col] = value

    def to_csv(self,
               path: str) -> None:
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self._header)
            writer.writerows(self._data)

    def __delitem__(self,
                    key) -> None:
        '''
        Set a specified value as np.nan.

        Parameters:
            - key: str, int, tuple or list[str]
        '''
        self._data[key] = np.nan

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
