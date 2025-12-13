# data_validator.py
from __future__ import annotations

import pandas as pd
from pandas.api import types as pd_types


class DataValidator:
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def _ensure_column_exists(self, column: str) -> None:
        if column not in self._data.columns:
            raise KeyError(f"Column '{column}' is not present in the dataframe.")

    def validate_range(self, column: str, min_val: float, max_val: float) -> pd.DataFrame:
        """Ensure values in a column are within the specified range."""
        self._ensure_column_exists(column)
        if not pd_types.is_numeric_dtype(self._data[column]):
            raise TypeError(f"Column '{column}' must be numeric to validate a range.")
        if not self._data[column].between(min_val, max_val).all():
            raise ValueError(f"Values in {column} are out of the specified range.")
        return self._data

    def validate_non_empty(self) -> pd.DataFrame:
        """Ensure there are no empty or null values in the dataframe."""
        if self._data.isnull().any().any():
            raise ValueError("Data contains missing values.")
        if self._data.empty:
            raise ValueError("Dataframe is empty.")
        return self._data
