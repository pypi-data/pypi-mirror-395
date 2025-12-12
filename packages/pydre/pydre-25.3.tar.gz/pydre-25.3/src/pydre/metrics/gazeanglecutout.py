import polars as pl
import pydre.core
from pydre.core import ColumnsMatchError
from pydre.metrics import registerMetric


def _check_and_prepare(drivedata: pydre.core.DriveData) -> pl.DataFrame:
    """
    Validate required columns and compute dt (Δt) between DatTime samples.
    """

    required_cols = ["DatTime", "gaze_cutout", "off_target"]
    try:
        drivedata.checkColumns(required_cols)
    except ColumnsMatchError:
        return pl.DataFrame({col: [] for col in required_cols})

    df = drivedata.data.select(required_cols).drop_nulls()

    # Compute Δt (time difference between consecutive DatTime entries)
    df = df.with_columns(
        (pl.col("DatTime").shift(-1) - pl.col("DatTime"))
        .fill_null(0.0)
        .clip(lower_bound=0.0)
        .alias("dt")
    )

    # combined mask for cutout + off-target
    df = df.with_columns(
        (
            pl.col("gaze_cutout").fill_null(False).cast(pl.Boolean)
            & pl.col("off_target").fill_null(False).cast(pl.Boolean)
        ).alias("mask")
    )

    return df


@registerMetric("gazeCutoutAngleDuration")
def gazeCutoutAngleDuration(drivedata: pydre.core.DriveData) -> float:
    """
    Returns the total duration (seconds) that the gaze was both
    outside the cutout angle AND off-target.
    """
    df = _check_and_prepare(drivedata)
    if df.is_empty():
        return 0.0

    mask_expr = pl.when(pl.col("mask")).then(pl.col("dt")).otherwise(0.0)
    duration = df.select(mask_expr.sum().alias("duration")).item()
    return float(duration or 0.0)


@registerMetric("gazeCutoutAngleRatio")
def gazeCutoutAngleRatio(drivedata: pydre.core.DriveData) -> float:
    """
    Fraction of total time spent outside the cutout angle (and off-target).
    Returns 0 if DatTime is missing or total duration = 0.
    """
    df = _check_and_prepare(drivedata)
    if df.is_empty():
        return 0.0

    total_time = df.select(pl.sum("dt")).item() or 0.0
    if total_time <= 0.0:
        return 0.0

    mask_expr = pl.when(pl.col("mask")).then(pl.col("dt")).otherwise(0.0)
    off_time = df.select(mask_expr.sum().alias("off_time")).item() or 0.0

    return float(off_time / total_time)


@registerMetric("gazeCutoutAngleViolations")
def gazeCutoutAngleViolations(drivedata: pydre.core.DriveData) -> int:
    """
    Counts the number of contiguous segments where the gaze was
    outside the cutout angle and off-target.

    A new violation is counted when mask transitions from False → True.
    """
    df = _check_and_prepare(drivedata)
    if df.is_empty():
        return 0

    df = df.with_columns(pl.col("mask").shift(1).fill_null(False).alias("prev_mask"))

    violation_expr = (
        pl.when((pl.col("mask") == True) & (pl.col("prev_mask") == False))
        .then(1)
        .otherwise(0)
    )
    violations = df.select(violation_expr.sum().alias("violations")).item() or 0

    return int(violations)
