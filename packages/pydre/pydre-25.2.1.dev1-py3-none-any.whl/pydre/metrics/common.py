from typing import Optional

import polars as pl
from polars import exceptions
import pydre.core
from pydre.core import ColumnsMatchError
from pydre.metrics import registerMetric
from loguru import logger
import numpy as np

from scipy import signal

# metrics defined here take a list of DriveData objects and return a single floating point value

# not registered & incomplete

# @registerMetric()
# def findFirstTimeAboveVel(drivedata: pydre.core.DriveData, cutoff: float = 25):
#     required_col = ["Velocity"]
#     drivedata.checkColumns(required_col)
#     timestepID = -1
#     # TODO: reimplement with selection and .head(1)
#
#     for i, row in drivedata.data.iterrows():
#         if row.Velocity >= cutoff:
#             timestepID = i
#             break
#
#     return timestepID


@registerMetric()
def colMean(
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


@registerMetric()
def colMedian(
    drivedata: pydre.core.DriveData, var: str, cutoff: Optional[float] = None
) -> Optional[float]:
    """Calculates the median of the specified column

    If `cutoff` is not `None`, then all values less than `cutoff` are ignored.
    If column is not numeric, `None` is returned.

    Parameters:
        var: The column name to process. Must be numeric.
        cutoff: Lower bound on data processed.

    Returns:
        Median of selected column.
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
            .median()
        )
    else:
        return drivedata.data.get_column(var).median()


@registerMetric()
def colSD(
    drivedata: pydre.core.DriveData, var: str, cutoff: Optional[float] = None
) -> Optional[float]:
    """Calculates the standard deviation of the specified column

    Uses Bessel's correction (denominator of N-1) for SD calculation.

    Parameters:
        var: The column name to process. Must be numeric.
        cutoff: Lower bound on data processed.

    Returns:
        Standard deviation of selected column.
            If `cutoff` is not `None`, then all values less than `cutoff` are ignored.
            If column is not numeric, `None` is returned.
    """
    try:
        drivedata.checkColumnsNumeric([var])
    except ColumnsMatchError as e:
        logger.warning(f"Columns not numeric: {e.missing_columns}")
        return None
    if cutoff is not None:
        return (
            drivedata.data.get_column(var)
            .filter(drivedata.data.get_column(var) >= cutoff)
            .std()
        )
    else:
        return drivedata.data.get_column(var).std()


@registerMetric()
def colMax(drivedata: pydre.core.DriveData, var: str) -> Optional[float]:
    """Calculates the maximum of the specified column

    Parameters:
        var: The column name to process. Must be numeric.

    Returns:
        Maximum value of selected column.
    """
    try:
        drivedata.checkColumnsNumeric([var])
    except ColumnsMatchError:
        return None
    return drivedata.data.get_column(var).max()


@registerMetric()
def colMin(drivedata: pydre.core.DriveData, var: str) -> Optional[float]:
    """Calculates the minimum of the specified column

    Parameters:
        var: The column name to process. Must be numeric.

    Returns:
        Minimum value of selected column.
    """
    try:
        drivedata.checkColumnsNumeric([var])
    except ColumnsMatchError:
        return None
    return drivedata.data.get_column(var).min()


@registerMetric()
def colFirst(drivedata: pydre.core.DriveData, var: str) -> Optional[float]:
    """Returns the first value of the specified column

    Parameters:
        var: The column name to process.

    Returns:
        First value of selected column.
    """

    try:
        drivedata.checkColumns([var])
    except ColumnsMatchError:
        return None
    return drivedata.data.get_column(var).head(1).item()


@registerMetric()
def colLast(drivedata: pydre.core.DriveData, var: str) -> Optional[float]:
    """Returns the last value of the specified column

    Parameters:
        var: The column name to process

    Returns:
        Last value of selected column.
    """
    try:
        drivedata.checkColumns([var])
    except ColumnsMatchError:
        return None
    return drivedata.data.get_column(var).tail(1).item()


@registerMetric()
def timeAboveSpeed(
    drivedata: pydre.core.DriveData, cutoff: float = 0, percentage: bool = False
) -> Optional[float]:
    """Returns the amount of seconds travelling above the specified speed

    Parameters:
        cutoff: Speed threshold value
        percentage: If true, return the percentage of total time in the DriveData object where the speed was
            above the cutoff.

    Note: Requires data columns
        - SimTime: Time in seconds
        - Velocity: Speed

    Returns:
        Number of seconds travelling above the specified speed.
    """
    required_col = ["SimTime", "Velocity"]
    # to verify if column is numeric
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None
    drivedata.checkColumns(required_col)

    df = drivedata.data.select(
        [
            pl.col("SimTime"),
            pl.col("Velocity"),
            pl.col("SimTime").diff().clip(lower_bound=0).alias("Duration"),
        ]
    )

    time = df.get_column("Duration").filter(df.get_column("Velocity") >= cutoff).sum()
    try:
        total_time: float = float(df.get_column("SimTime").max()) - float(
            df.get_column("SimTime").min()
        )
    except TypeError:
        return None
    if percentage:
        out: float = time / total_time
    else:
        out: float = time
    return out


@registerMetric()
def timeWithinSpeedLimit(
    drivedata: pydre.core.DriveData, lowerlimit: float = 0, percentage: bool = False
) -> Optional[float]:
    """Returns the amount of seconds travelling below the speed limit

    Parameters:
        lowerlimit: Filter out all velocities lower than this value.
        percentage: If true, return the percentage of total time in the DriveData object where the speed was under the limit

    Note: Requires data columns
        - SimTime: Time in seconds
        - Velocity: Speed in meters per second
        - SpeedLimit: Speed limit in miles per hour

    Returns:
        Number of seconds travelling above the specified speed.
    """
    required_col = ["SimTime", "Velocity", "SpeedLimit"]
    # to verify if column is numeric
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    df = drivedata.data.select(
        [
            pl.col("SimTime"),
            pl.col("Velocity"),
            pl.col("Velocity").mul(2.23694).alias("VelocityMPH"),
            pl.col("SimTime").diff().clip(lower_bound=0).alias("Duration"),
            pl.col("SpeedLimit"),
        ]
    )

    time = (
        df.filter(
            (pl.col("VelocityMPH") <= pl.col("SpeedLimit"))
            & (pl.col("VelocityMPH") >= lowerlimit)
        )
        .get_column("Duration")
        .sum()
    )

    if percentage:
        total_time = float(df.get_column("SimTime").max()) - float(
            df.get_column("SimTime").min()
        )
        output = time / total_time
    else:
        output = time
    return output


@registerMetric()
def stoppingDist(
    drivedata: pydre.core.DriveData, roadtravelposition="XPos"
) -> Optional[float]:
    """Returns the position of the first complete stop of the vehicle, relative to the center position of the
    DriveData object, as measured by the `roadtravelposition` column.

    This metric is designed to be used with the position-based ROI to define ROIs that have the stop line for a
    stop sign or stop light as the middle value in the direction of travel.

    Parameters:
        roadtravelposition: column name of increasing distance of travel, in meters

    Note: Requires data columns
        - Velocity: Speed in meters per second

    Returns:
        Number of meters the detected stop is away from the stop line. If no stops detected, return `10000`
    """
    required_col = [roadtravelposition, "Velocity"]
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    df = drivedata.data.select([pl.col(roadtravelposition), pl.col("Velocity")])
    if df.height == 0:
        return None
    # filtering the data to remove any negative velocities and only focus on velocities below 0.01 (chosen epsilon)
    velocities = df.filter(
        (df.get_column("Velocity") >= 0.0) & (df.get_column("Velocity") < 0.01)
    )

    lineposition = (
        float(df.get_column(roadtravelposition).min())
        + float(df.get_column(roadtravelposition).max())
    ) / 2

    if velocities.height == 0:
        # hard coding a "bad" value for stopposition if vehicle never stopped
        return 10000
    else:
        # finding the furthest position where velocity was close to zero
        stopposition = velocities.item(velocities.height - 1, 0)
    return lineposition - stopposition


@registerMetric()
def maxdeceleration(
    drivedata: pydre.core.DriveData, cutofflimit: float = 1
) -> Optional[float]:
    """Returns the maximum deceleration value

    Parameters:
        cutofflimit: all rows with velocities less than this value will be removed

    Note: Requires data columns
        - LonAccel: Acceleration value in the direction of travel, in meters per second per second
        - Velocity: Speed in meters per second

    Returns:
        maximum negative acceleration value (i.e. minimum acceleration value)
    """
    required_col = ["LonAccel", "Velocity"]
    # to verify if column is numeric
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    df = drivedata.data.select([pl.col("LonAccel"), pl.col("Velocity")])

    # filtering data to take out all rows with velocities less than cutoff value
    dfupdated = df.filter(df.get_column("Velocity") > cutofflimit)
    decel = dfupdated.filter(dfupdated.get_column("LonAccel") < 0)

    maxdecel = decel.get_column("LonAccel").min()
    return maxdecel


@registerMetric()
def maxacceleration(
    drivedata: pydre.core.DriveData, cutofflimit: int = 1
) -> Optional[float]:
    """Returns the maximum acceleration value

    Parameters:
        cutofflimit: all rows with velocities less than this value will be removed

    Note: Requires data columns
        - LonAccel: Acceleration value in the direction of travel, in meters per second per second
        - Velocity: Speed in meters per second

    Returns:
        maximum acceleration value
    """
    required_col = ["LonAccel", "Velocity"]
    # to verify if column is numeric
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    df = drivedata.data.select([pl.col("LonAccel"), pl.col("Velocity")])
    dfupdated = df.filter(df.get_column("Velocity") > cutofflimit)
    accel = dfupdated.filter(dfupdated.get_column("LonAccel") > 0)
    maxaccel = accel.filter(
        accel.get_column("LonAccel") == accel.get_column("LonAccel").max()
    )

    return maxaccel


@registerMetric()
def numbrakes(
    drivedata: pydre.core.DriveData, cutofflimit: float = 1
) -> Optional[float]:
    """Returns the number of times the brakes were pressed

    Parameters:
        cutofflimit: minimum velocity at which braking should be considered

    Note: Requires data columns
        - BrakeStatus: Column indicating braking. 0: no braking, greater than 0: braking
        - Velocity: Speed

    Returns:
        number of separate braking events
    """
    required_col = ["Brake", "Velocity"]
    # to verify if column is numeric
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    df = drivedata.data.select(
        [
            pl.col("Brake"),
            pl.col("Brake").gt(0).cast(pl.Float32).diff().alias("BrakeStatus"),
            pl.col("Velocity"),
        ]
    )
    dfupdated = df.filter(df.get_column("Velocity") > cutofflimit)

    numberofbrakes = (
        dfupdated.filter(dfupdated.get_column("BrakeStatus") > 0)
        .select(pl.count())
        .item(0, 0)
    )

    return numberofbrakes


def _calculateReversals(df):
    k = 1
    n = 0
    threshold = 0.0523598776 * 2
    for l in range(2, len(df)):
        if df[l] - df[k] >= threshold:
            n = n + 1
            k = l
        elif df[l] <= df[k]:
            k = l
    return n


@registerMetric()
def steeringReversals(drivedata: pydre.core.DriveData) -> float:
    """Steering reversals, as a count

    Note: Requires data columns
        - SimTime: simulation time
        - Steer: orientation of steering wheel in radians

    Returns:
        total reversals in this ROI

    """

    required_col = ["SimTime", "Steer"]
    # to verify if column is numeric
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    df = drivedata.data.select([pl.col("SimTime"), pl.col("Steer")])
    # convert to numpy and resample data to have even time steps (of 32Hz)
    df = df.slice(1, None)
    numpy_df = df.to_numpy()
    original_time = numpy_df[:, 0]
    original_steer = numpy_df[:, 1]

    # 32Hz = 0.03125seconds
    new_time = np.arange(original_time[0], original_time[-1], 0.03125)
    new_steer = np.interp(new_time, original_time, original_steer)
    numpy_df = np.column_stack((new_time, new_steer))

    # apply second order butterworth filter at 6z frequency
    sos = signal.butter(2, 6, output="sos", fs=32)
    theta_i = signal.sosfilt(sos, numpy_df[:, 1], zi=None)

    # calcuate thetaI
    theta_prime_i = np.diff(theta_i)
    theta_prime_i = np.append(0, theta_prime_i)

    # make column for i and combine with theta_prime_i column
    i = np.arange(1, len(theta_prime_i) + 1)
    df_with_theta = np.column_stack((i, theta_prime_i, theta_i))

    # find all values of i where theta_prime_i is 0
    df = pl.from_numpy(
        df_with_theta, schema=["i", "thetaPrimeI", "thetaI"], orient="row"
    )
    df_except_one = df.filter(df.get_column("i") > 1)
    zeros = df_except_one.filter(df_except_one.get_column("thetaPrimeI") == 0).drop(
        "thetaPrimeI"
    )

    # find values of i where difference between consequential signs of theta_prime_i is 2
    sign_diff = df.with_columns(
        df.get_column("thetaPrimeI").sign().diff(-1).alias("SignDiff")
    )
    diff_two = sign_diff.filter(
        (sign_diff.get_column("SignDiff") == 2)
        | (sign_diff.get_column("SignDiff") == -2)
    ).drop(["SignDiff", "thetaPrimeI"])

    # merge list of i's to get one sorted list of i's
    set_of_i = zeros.merge_sorted(diff_two, key="i").to_numpy()

    # calculate total reversals
    n_upwards = _calculateReversals(set_of_i[:, 1])
    set_of_i_down = np.multiply(set_of_i[:, 1], -1)
    n_downwards = _calculateReversals(set_of_i_down)
    reversals = n_upwards + n_downwards

    return reversals


@registerMetric()
def steeringReversalRate(drivedata: pydre.core.DriveData) -> float:
    """Steering reversal rate

    As defined in [SAE j2944](https://www.auto-ui.org/docs/sae_J2944_appendices_PG_130212.pdf)

    Note: Requires data columns
        - SimTime: simulation time
        - Steer: orientation of steering wheel in radians

    Returns:
        reversals per minute

    """
    required_col = ["SimTime", "Steer"]

    # to verify if column is numeric
    drivedata.checkColumnsNumeric(required_col)
    drivedata.checkColumns(required_col)

    df = drivedata.data.select([pl.col("SimTime"), pl.col("Steer")])
    # convert to numpy and resample data to have even time steps (of 32Hz)
    df = df.slice(1, None)
    numpy_df = df.to_numpy()
    original_time = numpy_df[:, 0]
    original_steer = numpy_df[:, 1]

    # 32Hz = 0.03125seconds
    new_time = np.arange(original_time[0], original_time[-1], 0.03125)
    new_steer = np.interp(new_time, original_time, original_steer)
    numpy_df = np.column_stack((new_time, new_steer))

    # apply second order butterworth filter at 6z frequency
    sos = signal.butter(2, 6, output="sos", fs=32)
    theta_i = signal.sosfilt(sos, numpy_df[:, 1], zi=None)

    # calcuate thetaI
    theta_prime_i = np.diff(theta_i)
    theta_prime_i = np.append(0, theta_prime_i)

    # make column for i and combine with theta_prime_i column
    i = np.arange(1, len(theta_prime_i) + 1)
    df_with_theta = np.column_stack((i, theta_prime_i, theta_i))

    # find all values of i where theta_prime_i is 0
    df = pl.from_numpy(
        df_with_theta, schema=["i", "thetaPrimeI", "thetaI"], orient="row"
    )
    df_except_one = df.filter(df.get_column("i") > 1)
    zeros = df_except_one.filter(df_except_one.get_column("thetaPrimeI") == 0).drop(
        "thetaPrimeI"
    )

    # find values of i where difference between consequential signs of theta_prime_i is 2
    sign_diff = df.with_columns(
        df.get_column("thetaPrimeI").sign().diff(-1).alias("SignDiff")
    )
    diff_two = sign_diff.filter(
        (sign_diff.get_column("SignDiff") == 2)
        | (sign_diff.get_column("SignDiff") == -2)
    ).drop(["SignDiff", "thetaPrimeI"])

    # merge list of i's to get one sorted list of i's
    set_of_i = zeros.merge_sorted(diff_two, key="i").to_numpy()

    # calculate total reversals
    n_upwards = _calculateReversals(set_of_i[:, 1])
    set_of_i_down = np.multiply(set_of_i[:, 1], -1)
    n_downwards = _calculateReversals(set_of_i_down)
    reversals = n_upwards + n_downwards

    # reversal rate as reversals/ minute
    reversal_rate = reversals / ((np.max(original_time) - np.min(original_time)) / 60)
    return reversal_rate


# mean dip time
# number of dips
# median dip time
@registerMetric(
    columnnames=[
        "meanDipTime",
        "numDips",
        "medianDipTime",
    ]
)
def biopticDipMeasure(drivedata: pydre.core.DriveData):
    required_col = ["SimTime", "hpBinary", "HeadPitch", "DipRegions"]
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        logger.warning("columns dont match in bioptics metric")
        return [None, None, None]

    df = drivedata.data.select(
        [
            pl.col("SimTime"),
            pl.col("hpBinary"),
            pl.col("DipRegions"),
            pl.col("HeadPitch"),
        ]
    )

    numDips = df.filter(df["hpBinary"] < 1).get_column("DipRegions").n_unique()

    zeros_df = df.filter(pl.col("hpBinary") < 1)

    duration_df = zeros_df.group_by("DipRegions").agg(
        [(pl.col("SimTime").max() - pl.col("SimTime").min()).alias("Duration")]
    )

    meanDipTime = duration_df.get_column("Duration").mean()

    medianDipTime = duration_df.get_column("Duration").median()
    return [
        meanDipTime,
        numDips,
        medianDipTime,
    ]


@registerMetric()
def maxAcceleration(drivedata: pydre.core.DriveData) -> Optional[float]:
    required_col = ["LatAccel", "LonAccel"]

    drivedata.checkColumnsNumeric(required_col)
    # issue with R2D part: 5210006w1 Load, No Event. SimTime is col type "str".
    drivedata.checkColumns(["SimTime"])

    df = drivedata.data.select(
        [pl.col("LatAccel"), pl.col("LonAccel"), pl.col("SimTime")]
    )

    df = df.with_columns(
        ((pl.col("LonAccel") ** 2) + (pl.col("LatAccel") ** 2))
        .sqrt()
        .alias("Total_Accel")
    )
    return df.get_column("Total_Accel").max()


# laneExits
# Will compute the number of transitions from the lane number specified to (lane+1) or (lane-1)
# the 'sign' function will remove transitions from (lane+1) to (lane+2) or similar
@registerMetric()
def laneExits(drivedata: pydre.core.DriveData, lane=2, lane_column="Lane"):
    drivedata.checkColumnsNumeric([lane_column])
    return (
        drivedata.data.select((pl.col(lane_column) - lane).sign().diff().abs())
        .sum()
        .item()
    )


@registerMetric()
def laneViolations(
    drivedata: pydre.core.DriveData,
    offset: str = "LaneOffset",
    lane: int = 2,
    lane_column: str = "Lane",
    lane_width: float = 3.65,
    car_width: float = 2.1,
):
    df = drivedata.data
    # df.checkColumnsNumeric([lane_column])
    # tolerance is the maximum allowable offset deviation from 0
    tolerance = lane_width / 2 - car_width / 2
    # Determine which rows are violations
    df = df.with_columns(
        ((pl.col(offset) > tolerance) | (pl.col(offset) < -tolerance)).alias(
            "violation"
        )
    )

    df = df.with_columns(
        (pl.col("violation") != pl.col("violation").shift(1)).alias("transition")
    )

    # Filter to keep only the rows where a transition occurs
    transitions = df.filter(pl.col("transition") == True)

    # Count the number of transitions from non-violation to violation
    violation_starts = transitions.filter(pl.col("violation") == True).shape[0]

    return violation_starts


def laneViolationDuration(
    drivedata: pydre.core.DriveData,
    offset: str = "LaneOffset",
    lane: int = 2,
    lane_column: str = "Lane",
    lane_width: float = 3.65,
    car_width: float = 2.1,
):
    required_col = [offset, lane_column, "LaneDuration", "SimTime", "Duration"]
    # to verify if column is numeric
    drivedata.checkColumnsNumeric(required_col)

    tolerance = lane_width / 2 - car_width / 2
    lane_data = drivedata.data.filter(pl.col(lane_column) == 2)
    lane_data = lane_data.select(
        [
            pl.col(offset).abs().alias("LaneViolations") > tolerance,
            pl.col("SimTime").diff().clip(lower_bound=0).alias("Duration"),
        ]
    )

    return lane_data.select(pl.col("LaneViolations") * pl.col("Duration")).sum().item()


@registerMetric()
def roadExits(drivedata: pydre.core.DriveData):
    required_col = ["SimTime", "RoadOffset", "Velocity"]
    # to verify if column is numeric
    drivedata.checkColumnsNumeric(required_col)
    drivedata.checkColumns(required_col)

    # assuming a two lane road, determine the amount of time they were not in the legal roadway
    # Lane width 3.6m, car width 1.8m

    df = drivedata.data.select(
        [
            pl.col("SimTime"),
            pl.col("RoadOffset"),
            pl.col("Velocity"),
            pl.col("SimTime")
            .diff()
            .alias("Duration")
            .clip(
                0, 0.5
            ),  # any duration outside this range is bad data (maybe from a splice)
        ]
    )

    outtimes = df.filter(
        (~pl.col("RoadOffset").is_between(0, 7.2)) & (pl.col("Velocity") > 1)
    )

    return outtimes.get_column("Duration").sum()


@registerMetric()
def roadExitsY(drivedata: pydre.core.DriveData):
    required_col = ["SimTime", "YPos", "Velocity"]
    # to verify if column is numeric
    drivedata.checkColumnsNumeric(required_col)
    drivedata.checkColumns(required_col)

    # assuming a two lane road, determine the amount of time they were not in the legal roadway
    # Lane width 3.6m, car width 1.8m

    df = drivedata.data.select(
        [
            pl.col("SimTime"),
            pl.col("RoadOffset"),
            pl.col("Velocity"),
            pl.col("SimTime")
            .diff()
            .alias("Duration")
            .clip(
                0, 0.5
            ),  # any duration outside this range is bad data (maybe from a splice)
        ]
    )

    outtimes = df.filter(
        pl.col("RoadOffset").is_between(0.9, 6.3) & (pl.col("Velocity") > 1)
        # TODO: double check offsets
    )

    return outtimes.get_column("Duration").sum()


# cutoff doesn't work
@registerMetric()
def steeringEntropy(drivedata: pydre.core.DriveData, cutoff: float = 0):
    required_col = ["SimTime", "Steer"]
    # to verify if column is numeric
    drivedata.checkColumnsNumeric(required_col)
    drivedata.checkColumns(required_col)

    out = []
    df = drivedata.data.select([pl.col("SimTime"), pl.col("Steer")])
    df = df.unique(
        subset=["Steer"], maintain_order=True
    )  # remove nans and drop duplicates

    if df.select(pl.count()).item(0, 0) == 0:
        return None

    # downsample the array to change the time step to every 0.15 seconds
    # based on article "Development of a Steering Entropy Method For Evaluating Driver Workload"
    df = df.slice(1, None)
    numpy_df = df.to_numpy()
    original_time = numpy_df[:, 0]
    original_steer = numpy_df[:, 1]

    new_time = np.arange(original_time[0], original_time[-1], 0.15)
    new_steer = np.interp(new_time, original_time, original_steer)

    numpy_df = np.column_stack((new_time, new_steer))
    df = pl.from_numpy(numpy_df, schema=["SimTime", "Steer"], orient="row")

    # calculate predicted angle
    # pAngle(n) = angle(n-1) + (angle(n-1) - angle(n-2)) + 0.5*( (angle(n-1) - angle(n-2)) - (angle(n-2) - angle(n-3)))
    end_index = df.height - 1

    angle_minus_one = df.get_column("Steer").slice(2, end_index - 2).to_numpy()
    angle_minus_two = df.get_column("Steer").slice(1, end_index - 2).to_numpy()
    angle_minus_three = df.get_column("Steer").slice(0, end_index - 2).to_numpy()
    pAngle = (
        angle_minus_one
        + (angle_minus_one - angle_minus_two)
        + 0.5
        * ((angle_minus_one - angle_minus_two) - (angle_minus_two - angle_minus_three))
    )
    pAngle = pl.from_numpy(pAngle, schema=["Steer"], orient="row")

    # calculate error
    error = df.get_column("Steer").slice(3, None) - pAngle.get_column("Steer")

    # TIYA - stopped making edits to this function this point onwards
    out.append(error)

    # concatenate out (list of np objects) into a single list
    if len(out) == 0:
        return None
    error = np.concatenate(out)
    # 90th percentile of error
    alpha = np.nanpercentile(error, 90)

    # divide into 9 bins with edges: -5a,-2.5a,-a,a,2.5,5a
    binnedError = np.histogram(
        error,
        bins=[
            -10 * abs(alpha),
            -5 * abs(alpha),
            -2.5 * abs(alpha),
            -abs(alpha),
            -0.5 * abs(alpha),
            0.5 * abs(alpha),
            abs(alpha),
            2.5 * abs(alpha),
            5 * abs(alpha),
            10 * abs(alpha),
        ],
    )

    # calculate H
    binnedArr = np.asarray(binnedError[0])
    binnedArr = binnedArr.astype(float)

    # check out calc of p
    p = np.divide(binnedArr, np.sum(binnedArr))
    Hp = np.multiply(np.multiply(-1, p), (np.log(p) / np.log(9)))
    Hp = Hp[~np.isnan(Hp)]
    Hp = np.sum(Hp)

    return Hp


@registerMetric()
def closeFollowing(
    drivedata: pydre.core.DriveData,
    threshold: float = 2,
    percentage: bool = False,
    minvelocity: Optional[float] = None,
) -> Optional[float]:
    """Close following is the amount of time where the headway time was lower than a threshold

    Very close following is sometimes called tailgating

    Parameters:
        threshold: maximum following time to collision, in seconds
        percentage: flag to output a percentage of total time spent
            following closely, rather than the number of seconds
        minvelocity: minimum velocity to consider rows as part of total time.
            If None, consider all times

    Note: Requires data columns:
        - SimTime: Simulation time in seconds
        - HeadwayTime: Headway time in seconds. This is the headway distance multiplied by the current
            speed of the vehicle.

    Returns:
        number of seconds or percentage of close following, under the specified threshold

    """
    # to verify if column is numeric
    required_col = ["SimTime", "HeadwayTime"]
    if minvelocity:
        required_col.append("Velocity")

    try:
        drivedata.checkColumnsNumeric(required_col)
    except pl.exceptions.PolarsError:
        return None

    following_df = drivedata.data.with_columns(
        pl.col("SimTime").diff().alias("delta_t")
    )

    # find all tailgating instances where the delta time is reasonable.
    # this ensures we don't get screwy data from merged files
    following_df = following_df.filter(pl.col("delta_t").is_between(0, 0.5))

    if minvelocity:
        following_df = following_df.filter(pl.col("Velocity") >= minvelocity)

    tail_time = (
        following_df.filter(
            pl.col("HeadwayTime").is_between(0, threshold, closed="none")
        )
        .select("delta_t")
        .sum()
        .item()
    )

    total_time = following_df.select("delta_t").sum().item()

    if percentage:
        if total_time > 0:
            return tail_time / total_time
        else:
            return None
    else:
        return tail_time


# determines when the ownship collides with another vehicle by examining headway distance as threshold
@registerMetric()
def leadVehicleCollision(
    drivedata: pydre.core.DriveData, cutoff: float = 2.85
) -> Optional[float]:
    """Number of collisions between the ownship and the lead vehicle.

    Parameters:
        cutoff: number of meters below wich the headway distance is considered "collided".
            Since headway distance is measured center-to-center of the two vehicles, 2.85m is used
            as the default value based on the size of sedans in the simulation.

    Note: Requires data columns
        - SimTime: Simulation time in seconds
        - HeadwayDistance: distance between the ownship and the lead vehicle in meters

    Returns:
        number of collision events

    """
    required_col = ["SimTime", "HeadwayDistance"]
    # to verify if column is numeric
    try:
        drivedata.checkColumnsNumeric(required_col)
    except pl.exceptions.PolarsError:
        return None

    # find contiguous instances of headway distance < the cutoff
    collision_table = drivedata.data.select(
        (pl.col("HeadwayDistance") <= cutoff).alias("CollisionZone")
    )
    collisions = (
        collision_table.select(pl.col("CollisionZone").cast(pl.Int32).diff().clip(0, 1))
        .sum()
        .item()
    )
    return collisions


def _firstOccurrence(df: pl.DataFrame, column: str):
    try:
        output = df[column].head(1)
        return output.index[0]
    except pl.PolarsError:
        return None


@registerMetric()
def timeFirstTrue(
    drivedata: pydre.core.DriveData, var: str, timecol: str = "SimTime"
) -> Optional[float]:
    """Time of the first true (>0) value in the specified variable column

    Parameters:
        var: column to check for first true value
        timecol: column to use for for time

    Returns:
        earliest value of the time column when the var column is true (above 0). None is returned if
            the var column is never true or if there is a error in processing.

    """

    required_col = [var, timecol]
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    try:
        df = drivedata.data.filter(pl.col(var) > 0)
    except pl.exceptions.ComputeError:
        logger.warning(
            "Failure processing timeFirstTrue metric for variable {} in file {}".format(
                var, drivedata.sourcefilename
            )
        )
        return None
    if df.height == 0:
        return None
    return (
        df.select("SimTime").head(1).item()
        - drivedata.data.select("SimTime").head(1).item()
    )


@registerMetric()
def reactionBrakeFirstTrue(
    drivedata: pydre.core.DriveData, var: str
) -> Optional[float]:
    required_col = [var, "SimTime"]
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    try:
        df = drivedata.data.filter(pl.col(var) > 5)
    except pl.exceptions.ComputeError:
        logger.warning("Brake value non-numeric in {}".format(drivedata.sourcefilename))
        return None
    if drivedata.data.height == 0 or df.height == 0:
        return None
    return (
        df.select("SimTime").head(1).item()
        - drivedata.data.select("SimTime").head(1).item()
    )


@registerMetric()
def reactionTimeEventTrue(drivedata: pydre.core.DriveData, var1: str, var2: str):
    required_col = [var1, var2, "SimTime"]
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None
    break_reaction = reactionBrakeFirstTrue(drivedata, var1)

    if break_reaction:
        return break_reaction
    else:
        df = drivedata.data.filter(abs(pl.col(var2)) >= 0.2)
        if drivedata.data.height == 0 or df.height == 0:
            return None
        return (
            df.select("SimTime").head(1).item()
            - drivedata.data.select("SimTime").head(1).item()
        )


@registerMetric()
def timeToOutsideThreshold(
    drivedata: pydre.core.DriveData,
    var: str,
    threshold_low: float = -100000,
    threshold_high: float = 100000,
):
    """
    Checks a column "var" values to ensure they are within range
    [threshold_low: threshold_high]

    threshold_low &  threshold_high are set to extreme numbers by default to
    ensure users don't have to define irrelevant bounds. Calculates a reaction
    time for the first occurrence of a threshold violation.

    :arg var: column name to check for reaction
    :arg threshold_low: the value that defines a reaction
        for the given column, if lower
    :arg threshold_high: the value that defines a reaction
        for the given column, if higher
    """
    required_col = [var, "SimTime"]
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None
    try:
        df = drivedata.data.filter(pl.col(var) < threshold_low)
    except pl.exceptions.ComputeError as e:
        logger.warning(f"{var} value non-numeric in {drivedata.sourcefilename} --> {e}")
        return None
    # no lower threshold violation, check upper threshold
    if drivedata.data.height == 0 or df.height == 0:
        df = drivedata.data.filter(pl.col(var) > threshold_high)
        if df.height == 0:
            # no threshold violations for given bounds
            return None
    return (
        df.select("SimTime").head(1).item()
        - drivedata.data.select("SimTime").head(1).item()
    )


"""
TBI Reaction algorithm
To find the braking reaction time to the event (for each Section):
    Only look at values after the event E (Activation = 1)
    Find the first timestep X where:
		X is after the Event (Activation=1)
			AND
		BrakeForce(X) – BrakeForce(E) > 0
    Reaction time is Time(X) – Time(First timestep where Activation = 1)


To find the throttle reaction time to the event (for each Section):
    Only look at values after the event E (Activation = 1)
    Find the first timestep X where:
		X is after the Event (Activation=1)
			AND
		Throttle(X) – Throttle(X-1) > SD([Throttle for all X in Section where Activation !=1]).
    Reaction time is Time(X) – Time(First timestep where Activation = 1)


Then you average the two throttle reaction times and the two brake reaction times for each of the 4 DriveIDs.
This results in 8 reaction times per participant.
"""


@registerMetric()
def reactionTime(drivedata: pydre.core.DriveData, brake_cutoff=1, steer_cutoff=0.2):
    required_col = ["SimTime", "Brake", "Steer", "XPos", "HeadwayDistance"]
    # to verify if column is numeric
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    df = drivedata.data.select(
        [
            pl.col("SimTime"),
            pl.col("Steer"),
            pl.col("Brake"),
            pl.col("XPos"),
            pl.col("HeadwayDistance"),
        ]
    )

    event_start_time = df.get_column("SimTime").item(0)
    # calculate braking reaction time
    brake_df = df.filter(df.get_column("Brake") > brake_cutoff)
    if brake_df.is_empty():
        brake_reaction = 50
    else:
        first_brake = brake_df.get_column("SimTime").item(0)
        brake_reaction = first_brake - event_start_time
    # calculate swerving reaction time
    first_steer = df.get_column("Steer").item(0)
    try:
        df_steer = df.with_columns(
            (pl.col("Steer") - first_steer).alias("SteerDiff").abs()
        )
        df_steer = df_steer.filter(df_steer.get_column("SteerDiff") > steer_cutoff)
    except exceptions.InvalidOperationError:
        return None

    if df_steer.is_empty():
        steer_reaction = 50
    else:
        steer_reaction = df_steer.get_column("SimTime").item(0) - event_start_time

    if steer_reaction > 10 and brake_reaction > 10:
        reactionTime = None
    else:
        reactionTime = min(steer_reaction, brake_reaction)
    return reactionTime
