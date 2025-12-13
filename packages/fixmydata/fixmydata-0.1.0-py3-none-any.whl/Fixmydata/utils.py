# utils.py

import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)

def save_to_csv(data: pd.DataFrame, file_path: str):
    """Saves a pandas DataFrame to a CSV file."""
    data.to_csv(file_path, index=False)

def clean_column_names(data: pd.DataFrame):
    """Cleans column names by making them lowercase and replacing spaces with underscores."""
    data.columns = [col.lower().replace(" ", "_") for col in data.columns]
    return data

def check_nulls(data: pd.DataFrame):
    """Checks for missing values in the DataFrame and returns a boolean mask."""
    return data.isnull().sum()

def display_data_info(data: pd.DataFrame):
    """Displays basic information about the DataFrame (shape, columns, and types)."""
    print(f"Shape: {data.shape}")
    print(f"Columns: {data.columns}")
    print(f"Data Types: \n{data.dtypes}")
