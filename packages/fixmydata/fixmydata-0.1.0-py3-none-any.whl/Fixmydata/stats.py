# stats.py

import numpy as np
import pandas as pd

def calculate_mean(data: pd.Series) -> float:
    """Calculates the mean of a given pandas Series."""
    return data.mean()

def calculate_median(data: pd.Series) -> float:
    """Calculates the median of a given pandas Series."""
    return data.median()

def calculate_mode(data: pd.Series):
    """Calculates the mode of a given pandas Series."""
    return data.mode()[0]

def calculate_std_dev(data: pd.Series) -> float:
    """Calculates the standard deviation of a given pandas Series."""
    return data.std()

def correlation(data: pd.DataFrame, col1: str, col2: str) -> float:
    """Calculates the Pearson correlation coefficient between two columns."""
    return data[col1].corr(data[col2])

def z_score_outliers(data: pd.DataFrame, threshold: float = 3) -> pd.DataFrame:
    """Detects outliers using Z-score method. Returns the rows that do not contain outliers."""
    z_scores = np.abs((data - data.mean()) / data.std())
    return data[(z_scores < threshold).all(axis=1)]

def iqr_outliers(data: pd.DataFrame) -> pd.DataFrame:
    """Detects outliers using the Interquartile Range (IQR) method."""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    return data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]
