from collections.abc import MutableMapping, Iterator
import numpy as np
import csv

from lutils.utils.misc import is_list_str


class DataFrame(MutableMapping):
    """
    A custom DataFrame implementation backed by NumPy arrays.

    This class provides a dictionary-like interface for managing 2D tabular data,
    supporting column access via string keys, row access via integer indices,
    and cell access via tuples.

    Parameters
    ----------
    header : list[str]
        A list of strings representing the column names.
    data : np.ndarray
        A 2D NumPy array containing the table data. The shape must be
        (rows, len(header)).
    """

    def __init__(self,
                 header: list[str],
                 data: np.ndarray) -> None:
        self._header = header
        self._data = data
        self._map = {name: idx for idx, name in enumerate(header)}

    def filter_rows(self,
                    column: str,
                    value: float) -> np.ndarray:
        """
        Selects rows where the specified column matches a value.

        This method uses `np.isclose` to compare floating point values.

        Parameters
        ----------
        column : str
            The name of the column to filter by.
        value : float
            The target value to compare against.

        Returns
        -------
        np.ndarray
            A new NumPy array containing only the rows that match the criteria.
        """
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
        """
        Retrieves data from the DataFrame based on the key type.

        Parameters
        ----------
        key : str, int, tuple, or list[str]
            - **str**: Returns the column as a 1D array.
            - **int**: Returns the row as a 1D array.
            - **tuple (row, col)**: Returns the scalar value at the specific cell.
            - **list[str]**: Returns a subset of columns as a 2D array.

        Returns
        -------
        np.ndarray or scalar
            The requested data slice or value.

        Raises
        ------
        TypeError
            If the key type is not supported.
        KeyError
            If a column string is provided that does not exist in the header.
        """
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
        else:
            raise TypeError(
                'Invalid key type. Try again with str, int, tuple or list[str].')

    def __setitem__(self,
                    key,
                    value) -> None:
        """
        Modifies data at the specified location.

        Parameters
        ----------
        key : str, int, tuple, or list[str]
            The location to modify (column, row, cell, or multiple columns).
        value : scalar or array_like
            The value(s) to assign to the specified location.
        """
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
        """
        Exports the DataFrame to a CSV file.

        Parameters
        ----------
        path : str
            The destination file path.
        """
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self._header)
            writer.writerows(self._data)

    def __delitem__(self,
                    key) -> None:
        """
        Masks the specified data with NaN (Not a Number).

        Note: This does not remove the row or column from the array structure;
        it merely invalidates the data at the specified key.

        Parameters
        ----------
        key : str, int, tuple, or list[str]
            The location to mask with NaN.
        """
        self._data[key] = np.nan

    def __iter__(self) -> Iterator[str]:
        """
        Returns an iterator over the column names.

        Yields
        ------
        str
            The next column name in the header.
        """
        return iter(self._header)

    def __repr__(self) -> str:
        """Returns the string representation of the DataFrame."""
        return f'{self._header}\n{self._data}'

    def __len__(self) -> int:
        """
        Returns the number of columns in the DataFrame.

        Returns
        -------
        int
            The length of the header list.
        """
        return len(self._header)

    def shape(self):
        """
        Returns the dimensions of the DataFrame.

        Returns
        -------
        tuple[int, int]
            A tuple representing (number_of_rows, number_of_columns).
        """
        return self._data.shape
