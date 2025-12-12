import re
from typing import Optional

import polars as pl
from loguru import logger

import pydre.core
from pydre.core import ColumnsMatchError
from pydre.metrics import registerMetric


@registerMetric(
    "R2DIDColumns", ["ParticipantID", "MatchID", "Case", "Location", "Gender", "Week"]
)
def R2DIDColumns(drivedata: pydre.core.DriveData):
    ident = drivedata.metadata["ParticipantID"]
    ident_groups = re.match(r"(\d)(\d)(\d)(\d\d\d\d)[wW](\d)", ident)
    if ident_groups is None:
        logger.warning("Could not parse R2D ID " + ident)
        return [None, None, None, None, None, None]
    participant_id = (
        ident_groups.group(1)
        + ident_groups.group(2)
        + ident_groups.group(3)
        + ident_groups.group(4)
    )
    case = ident_groups.group(1)
    if case == "3":
        case = "Case"
    elif case == "5":
        case = "Control"
    elif case == "7":
        case = "Enrolled"
    location = ident_groups.group(2)
    if location == "1":
        location = "UAB"
    elif location == "2":
        location = "OSU"
    elif location == "3":
        location = "UA"
    gender = ident_groups.group(3)
    if gender == "1":
        gender = "Male"
    elif gender == "2":
        gender = "Female"
    match_id = ident_groups.group(4)
    week = ident_groups.group(5)
    return participant_id, match_id, case, location, gender, week


@registerMetric()
def throttleReactionTime(drivedata: pydre.core.DriveData) -> Optional[float]:
    """Calculates the time it takes to accelerate once follow car brakes (r2d)

    Note: Requires data columns
        - SimTime: Simulation time in seconds
        - FollowCarBraking Status: Whether the follow car is braking
        - LonAccel: Longitude acceleration
        - Brake: Whether the ownship is braking

    Returns:
        Time in seconds from when the follow car braked to when the ownship started accelerating forward.
    """
    drivedata.data = drivedata.data.with_columns(
        drivedata.data["SimTime"].cast(pl.Float64)
    )

    required_col = ["FollowCarBrakingStatus", "LonAccel", "SimTime", "Brake"]

    try:
        drivedata.checkColumnsNumeric(required_col)
    except pl.exceptions.PolarsError:
        return None

    df = drivedata.data.select(
        [
            pl.col("FollowCarBrakingStatus"),
            pl.col("SimTime"),
            pl.col("LonAccel"),
            pl.col("Brake"),
            pl.col("Throttle"),
        ]
    )

    if df.height < 1:
        return None

    initial_time = df.get_column("SimTime").item(0)

    try:
        df = df.filter(
            pl.col("SimTime")
            > df.filter(pl.col("Brake") > 3.0).get_column("SimTime").item(0)
        )
    except IndexError:
        logger.warning(
            f"No braking detected for roi {drivedata.roi} in file {drivedata.sourcefilename}"
        )
        return None

    df_after_brake = df.filter(pl.col("Brake") == 0)

    try:
        time_of_accel = (
            df_after_brake.filter(pl.col("LonAccel") > 0).get_column("SimTime").item(0)
        )
    except IndexError:
        logger.warning(
            f"No subsequent acceleration detected for roi {drivedata.roi} in file {drivedata.sourcefilename}"
        )
        return None

    throttle_reaction_time = time_of_accel - initial_time
    return throttle_reaction_time


@registerMetric()
def eventSpeedRecoveryTime(
    drivedata: pydre.core.DriveData, op_speed=15.64, tolerance=4
) -> Optional[float]:
    """Calculates the time it takes to accelerate back up to 'operational speed' (op_speed)
    tolerance allows for proper classification of subject behavior variation
    (defaults parameterized for R2D study processing)

    Note: Requires data columns
        - SimTime: Simulation time in seconds
        - Velocity: m/s directional speed of Subject

    Returns:
        Time in seconds from the start of the CE to when the Subject returned to (operational speed - tolerance)
    """
    drivedata.data = drivedata.data.with_columns(
        drivedata.data["SimTime"].cast(pl.Float64)
    )
    required_col = ["SimTime", "Velocity"]
    lower_bound = op_speed - tolerance

    try:
        drivedata.checkColumnsNumeric(required_col)
    except pl.exceptions.PolarsError:
        return None

    df = drivedata.data.select(
        [pl.col("Velocity"), pl.col("SimTime"), pl.col("Brake"), pl.col("EventName")]
    )

    non_event_detect = df.filter(pl.col("EventName") == "")

    if non_event_detect.is_empty():
        # filter df, so we take recovery time after initial slow-down
        try:
            df = df.filter(
                pl.col("SimTime")
                > df.filter(pl.col("Velocity") < lower_bound)
                .get_column("SimTime")
                .item(0)
            )
        except IndexError:
            logger.warning(
                f"Velocity doesn't drop below {lower_bound} m/s for roi {drivedata.roi} in file {drivedata.sourcefilename}"
            )
            return "NoSlowDown"

        # initial time once velocity reading below lower threshold
        initial_time = df.get_column("SimTime").item(0)

        recover_cond = pl.col("Velocity") >= lower_bound
        recover_time = df.filter(recover_cond).select(pl.col("SimTime").first()).item()

        if recover_time is not None:
            return recover_time - initial_time
        else:
            max_velo = df.select(pl.max("Velocity").first()).item()
            logger.warning(
                f"No recovery detected during this event - returned to max speed of {max_velo} m/s"
            )
            return "NoRecover"
    else:
        return "NoEvent"


@registerMetric()
def eventRecenterRecoveryTime(
    drivedata: pydre.core.DriveData, tolerance=0.65, event_detect="Trash"
) -> Optional[float]:
    """Calculates the time it takes to recenter in lane after specific event occurences
    tolerance allows for proper classification of subject behavior variation

    Note: Requires data columns
        - EventName: The name of the critical event for this region
        - LaneOffset: meters of Subject from center of their lane
        - SimTime: Simulation time in seconds

    Returns:
        Time in seconds from when the Subject left (lane_offset +- tolerance )
        to when the Subject returned to (lane_offset +- tolerance)
    """
    drivedata.data = drivedata.data.with_columns(
        drivedata.data["SimTime"].cast(pl.Float64)
    )
    required_col = ["LaneOffset", "SimTime"]

    try:
        drivedata.checkColumns(required_col)
    except pl.exceptions.PolarsError:
        return None

    df = drivedata.data.select(
        [pl.col("EventName"), pl.col("LaneOffset"), pl.col("SimTime")]
    )

    contains_trash = df.filter(pl.col("EventName").str.contains(event_detect))

    if contains_trash.height > 0:
        # filter df, breach "tolerance"
        try:
            df = df.filter(
                pl.col("SimTime")
                > df.filter(pl.col("LaneOffset").abs() > tolerance)
                .get_column("SimTime")
                .item(0)
            )
        except IndexError:
            logger.warning(
                f"Subject does not breach {tolerance} m lane offset for roi {drivedata.roi} in file {drivedata.sourcefilename}"
            )
            return "NoSwerve"

        # initial time once velocity reading below lower threshold
        initial_time = df.get_column("SimTime").item(0)
        recover_cond = pl.col("LaneOffset").abs() <= tolerance
        recover_time = df.filter(recover_cond).select(pl.col("SimTime").first()).item()

        if recover_time is not None:
            return recover_time - initial_time
        else:
            min_offset = df.select(pl.col("LaneOffset").abs().min().first()).item()
            logger.warning(
                f"No recovery detected during this event - returned to min offset of {min_offset} m"
            )
            return "NoRecover"
    else:
        non_event_detect = df.filter(pl.col("EventName") == "")
        if non_event_detect.is_empty():
            return "NoTrashTip"  # situation not Trashtip event, ignore
        else:
            return "NoEvent"  # situation is non event


@registerMetric()
def reactionCheckVarVal(
    drivedata: pydre.core.DriveData, var: str, val: float
) -> Optional[float]:
    required_col = [var, "SimTime"]
    drivedata.data = drivedata.data.with_columns(
        drivedata.data["SimTime"].cast(pl.Float64)
    )
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None

    try:
        df = drivedata.data.filter(pl.col(var) < val)
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
def reactionTimeEventTrueR2D(
    drivedata: pydre.core.DriveData, var1: str, var2: str, val1: float, val2: float
):
    required_col = [var1, var2, "SimTime"]
    drivedata.data = drivedata.data.with_columns(
        drivedata.data["SimTime"].cast(pl.Float64)
    )
    try:
        drivedata.checkColumnsNumeric(required_col)
    except ColumnsMatchError:
        return None
    first_metric_reaction = reactionCheckVarVal(drivedata, var1, val1)

    if first_metric_reaction:
        return first_metric_reaction
    else:
        df = drivedata.data.filter(abs(pl.col(var2)) >= val2)
        if drivedata.data.height == 0 or df.height == 0:
            return None
        return (
            df.select("SimTime").head(1).item()
            - drivedata.data.select("SimTime").head(1).item()
        )


@registerMetric("criticalEventStartPos", ["ceName", "ceStartPos"])
def criticalEventStartPos(drivedata: pydre.core.DriveData):
    required_col = ["XPos"]
    # to verify if column is numeric
    drivedata.checkColumnsNumeric(required_col)
    required_col.append("EventName")
    drivedata.checkColumns(required_col)
    df = drivedata.data
    return df.get_column("XPos").item(0), df.get_column("EventName").item(0)


@registerMetric("criticalEventEndPos", ["ceName", "ceEndPos"])
def criticalEventEndPos(drivedata: pydre.core.DriveData):
    required_col = ["XPos"]
    # to verify if column is numeric
    drivedata.checkColumnsNumeric(required_col)
    required_col.append("EventName")
    drivedata.checkColumns(required_col)

    df = drivedata.data
    return df.get_column("XPos").item(-1), df.get_column("EventName").item(-1)
