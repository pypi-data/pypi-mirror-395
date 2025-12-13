"""Data cleaning utilities for the fixmydata package."""
from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd


class DataCleaner:
    """Perform common data cleaning tasks on a pandas DataFrame.

    Each operation mutates a copy of the provided DataFrame and returns the
    cleaned data to allow chaining or immediate inspection.
    """

    def __init__(self, data: pd.DataFrame):
        self._data = data.copy()

    def _ensure_column_exists(self, column: str) -> None:
        if column not in self._data.columns:
            raise KeyError(f"Column '{column}' is not present in the dataframe.")

    def remove_duplicates(self, subset: Optional[Iterable[str]] = None, keep: str = "first") -> pd.DataFrame:
        """Remove duplicate rows.

        Args:
            subset: Optional list of columns to consider when identifying duplicates.
            keep: Which duplicate to keep; passed directly to ``DataFrame.drop_duplicates``.
        """

        self._data = self._data.drop_duplicates(subset=subset, keep=keep)
        return self._data

    def drop_missing(self, columns: Optional[Iterable[str]] = None, how: str = "any", thresh: Optional[int] = None) -> pd.DataFrame:
        """Drop rows with missing values.

        Args:
            columns: Optional iterable of column names to check for missing values.
            how: ``any`` to drop if any value is missing, ``all`` if all values are missing.
            thresh: Require at least this many non-null values; overrides ``how`` when provided.
        """

        if columns is not None:
            for column in columns:
                self._ensure_column_exists(column)

        if thresh is not None:
            self._data = self._data.dropna(subset=columns, thresh=thresh)
        else:
            self._data = self._data.dropna(subset=columns, how=how)
        return self._data

    def fill_missing(self, column: str, value) -> pd.DataFrame:
        """Fill missing values in a column with a provided value."""

        self._ensure_column_exists(column)
        self._data[column] = self._data[column].fillna(value)
        return self._data

    def drop_columns(self, columns: Iterable[str]) -> pd.DataFrame:
        """Drop specified columns from the DataFrame."""

        for column in columns:
            self._ensure_column_exists(column)
        self._data = self._data.drop(columns=columns)
        return self._data

    def standardize_whitespace(self, columns: Iterable[str]) -> pd.DataFrame:
        """Strip leading/trailing whitespace from string columns."""

        for column in columns:
            self._ensure_column_exists(column)
            if not pd.api.types.is_string_dtype(self._data[column]):
                raise TypeError(f"Column '{column}' must be a string dtype to standardize whitespace.")
            self._data[column] = self._data[column].str.strip()
        return self._data

    @property
    def data(self) -> pd.DataFrame:
        """Return the current state of the cleaned DataFrame."""

        return self._data.copy()