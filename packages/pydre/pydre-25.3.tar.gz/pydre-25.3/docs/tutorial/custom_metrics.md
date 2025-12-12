# Writing Custom Metrics for Pydre

Custom metrics in Pydre allow you to extract meaningful data from driving simulation data. Here's how to create one:

## Basic Metric Structure

A custom metric is a function decorated with `@registerMetric()` that takes a `DriveData` object as its first parameter and returns a numeric value or collection of values.

```python
from pydre.metrics import registerMetric
import pydre.core

@registerMetric()
def myCustomMetric(drivedata: pydre.core.DriveData, param1: str = "default") -> float:
    """Brief description of what this metric calculates
    
    Parameters:
        param1: Description of this parameter
        
    Note: Requires data columns
        - Column1: Description of required column
        - Column2: Description of another required column
        
    Returns:
        Description of return value
    """
    # Check for required columns
    required_cols = ["Column1", "Column2"]
    drivedata.checkColumns(required_cols)
    
    # Verify columns are numeric
    try:
        drivedata.checkColumnsNumeric(required_cols)
    except pydre.core.ColumnsMatchError:
        return None
        
    # Process data and compute the metric value
    result = some_calculation(drivedata.data)
    
    return result
```

## Advanced Metrics

### Multiple Return Values

For metrics that return multiple values, specify column names in the decorator:

```python
@registerMetric(columnnames=["value1", "value2"])
def multiValueMetric(drivedata: pydre.core.DriveData) -> list[float]:
    # ...
    return [value1, value2]
```

### Custom Metric Names

Override the function name for metric registration:

```python
@registerMetric(metricname="betterMetricName")
def internal_function_name(drivedata: pydre.core.DriveData) -> float:
    # ...
```

## Best Practices

1. Always validate required columns exist before processing
2. Use robust error handling with clear log messages
3. Return `None` when calculation fails rather than raising exceptions
4. Include comprehensive docstrings with parameter descriptions
5. Use polars operations when possible for performance

## Step-by-Step Guide

### 1. Create a Custom Metrics Directory

Create a directory for your custom metrics (outside the Pydre repository):

```
my_project/
├── custom_metric/
│   └── custom.py
├── data/
│   └── drive_data.dat
└── custom_test.toml
```

### 2. Set up your directory to use pydre

```bash
cd my_project
rye add pydre
rye sync
```

This will initialize the directory like a python package using *rye* and the pydre package. This will use the latest [published version of *pydre*](https://pypi.org/project/pydre/) from PyPI. If you want to use the latest development version of *pydre*, you can clone the repository and add it as a dependency instead.

### 3. Write Your Custom Metrics

Create a Python file (e.g., `custom.py`) in your custom metrics directory. Your metrics should use the `@registerMetric()` decorator:

```python title="custom_metric/custom.py"
from typing import Optional

import polars as pl
import pydre.core
from pydre.core import ColumnsMatchError
from pydre.metrics import registerMetric
from loguru import logger

@registerMetric()
def testMean(
    drivedata: pydre.core.DriveData, var: str, cutoff: Optional[float] = None
) -> Optional[float]:

    try:
        drivedata.checkColumnsNumeric([var])
    except ColumnsMatchError:
        return None
    if cutoff is not None:
        return (
            drivedata.data.get_column(var)
            .filter(drivedata.data.get_column(var) >= cutoff)
            .mean()
        )
    else:
        return drivedata.data.get_column(var).mean()

```

### 4. Configure Your Project File

Include your custom metrics directory in the config section of your project file. 

```toml title="custom_test.toml"
[config]
custom_metrics_dirs = ["custom_metric"]

[metrics.custom_test]
function = "testMean"
var = "XPos"

```

### 4. Run Pydre with Your Custom Metrics

Run Pydre with your project file:

```bash
rye run pydre -p examples/custom_project/custom_test.toml -d examples/custom_project/data/Experimenter_S1_Tutorial_11002233.dat -o custom.csv
```

## How It Works

1. Pydre loads all metrics defined in its core library
2. It then searches the directory paths specified in `custom_metrics_dirs`
3. For each Python file in those directories, it dynamically imports the metrics
4. The `@registerMetric()` decorator automatically registers your custom metrics with *pydre*
5. Your metrics become available for use in the project configuration

## Tips

- Ensure your custom metrics follow the same pattern as built-in metrics
- Add proper docstrings to document required columns and return values
- Always include error handling for missing columns using `checkColumns` or `checkColumnsNumeric`
- Use type hints to document your function parameters and return values

With this approach, you can maintain your custom metrics separately from the Pydre codebase while still using them in your projects.


# Custom filters

Custom filters can be created in a similar way to custom metrics. the search path for custom filters is similar to the custom metrics search path: "custom_filters_dirs". Additionally, `@registerFilter()` instead of `@registerMetric()` is used as the decorator.

## Example

```toml 
[config]
datafiles = ["data/drive_data.dat"]
outputfile = "results.csv"
custom_metrics_dirs = ["custom_metrics"]
custom_filters_dirs = ["custom_filters"]
```