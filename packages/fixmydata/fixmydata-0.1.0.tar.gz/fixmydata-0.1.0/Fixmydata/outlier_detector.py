# outlier_detector.py
from __future__ import annotations

import numpy as np
import pandas as pd


class OutlierDetector:
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def _numeric_data(self) -> pd.DataFrame:
        numeric = self._data.select_dtypes(include=[np.number])
        if numeric.empty:
            raise ValueError("Outlier detection requires at least one numeric column.")
        return numeric

    def z_score_outliers(self, threshold: float = 3) -> pd.DataFrame:
        """Detect outliers using the Z-score method while ignoring non-numeric columns."""
        numeric = self._numeric_data()
        std = numeric.std(ddof=0).replace(0, np.nan)
        z_scores = np.abs((numeric - numeric.mean()) / std)
        mask = (z_scores < threshold).all(axis=1)
        return self._data[mask.fillna(False)]

    def iqr_outliers(self) -> pd.DataFrame:
        """Detect outliers using the Interquartile Range (IQR) method."""
        numeric = self._numeric_data()
        q1 = numeric.quantile(0.25)
        q3 = numeric.quantile(0.75)
        iqr = q3 - q1
        mask = ~((numeric < (q1 - 1.5 * iqr)) | (numeric > (q3 + 1.5 * iqr))).any(axis=1)
        return self._data[mask]
