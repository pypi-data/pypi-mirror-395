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
    """Calculates the mean of the specified column

    If `cutoff` is not `None`, then all values less than `cutoff` are ignored.
    If column is not numeric, `None` is returned.

    Parameters:
        var: The column name to process. Must be numeric.
        cutoff: Lower bound on data processed.

    Returns:
        Mean of selected column.
            If `cutoff` is not `None`, then all values less than `cutoff` are ignored.
            If column is not numeric, `None` is returned.
    """
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
