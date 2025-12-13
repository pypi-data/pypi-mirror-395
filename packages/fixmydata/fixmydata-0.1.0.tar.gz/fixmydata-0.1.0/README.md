# Fixmydata

Fixmydata is a lightweight helper library built on top of pandas for cleaning, validating, and inspecting tabular datasets. It provides quick, chainable utilities for removing common data issues so you can focus on analysis.

## Installation

The project targets Python 3.7+ and depends on pandas and numpy. You can install the package from source by cloning the repository and installing with pip:

```bash
pip install -e .
```

## Features

- **Cleaning**: Deduplicate rows, drop or fill missing values, remove columns, and trim whitespace with `DataCleaner`.
- **Validation**: Assert value ranges and check for missing or empty data with `DataValidator`.
- **Outlier filtering**: Identify inliers using Z-score or IQR methods while ignoring non-numeric columns via `OutlierDetector`.
- **Utilities**: CSV load/save helpers, column name normalization, null counting, and quick DataFrame introspection.

## Quickstart

```python
import pandas as pd
from Fixmydata import DataCleaner, DataValidator, OutlierDetector

raw = pd.DataFrame({
    "id": [1, 1, 2, 3],
    "city": ["  New York", "Boston  ", "Chicago", None],
    "value": [10.5, 9.7, 11.2, 13.0],
})

# Clean data
cleaner = DataCleaner(raw)
cleaner.remove_duplicates(subset=["id"])
cleaner.drop_missing(columns=["city"])
cleaner.standardize_whitespace(["city"])
clean = cleaner.data

# Validate data
validator = DataValidator(clean)
validator.validate_range("value", 0, 15)
validator.validate_non_empty()

# Filter outliers
outlier_detector = OutlierDetector(clean)
inliers = outlier_detector.z_score_outliers(threshold=2.5)
print(inliers)
```

## Modules

- `Fixmydata.cleaning.DataCleaner`: Common cleaning operations that mutate an internal copy and expose the cleaned `data` property for reuse.
- `Fixmydata.data_validator.DataValidator`: Range and completeness checks with clear errors on schema mismatches.
- `Fixmydata.outlier_detector.OutlierDetector`: Z-score and IQR inlier filters with safeguards for missing numeric data.
- `Fixmydata.utils`: CSV I/O helpers, column name normalization, null counting, and DataFrame info display.
- `Fixmydata.stats`: Basic descriptive statistics and standalone outlier helpers.

## Contributors

| Name                  | Role / Position | Main Contribution                           |
| --------------------- | --------------- | ------------------------------------------- |
| Johann Lloyd Megalbio | Leader          | Project management and overall coordination |
| Albrien Dealino       | Developer       | Core coding and development tasks           |
| Rafael John Calingin  | Developer       | Coding and implementation of key features   |
| Shawn Bolores Sillote | Developer       | Development of system modules and functions |
