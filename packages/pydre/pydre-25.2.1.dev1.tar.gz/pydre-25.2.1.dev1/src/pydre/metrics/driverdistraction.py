import polars as pl
import pydre.core
from pydre.core import ColumnsMatchError
from pydre.metrics import registerMetric
import numpy as np
from scipy import signal


# These metrics were used in driving distraction evaluation. They have not been fully tested after conversion from
# Pandas to Polars.


@registerMetric()
def getTaskNum(drivedata: pydre.core.DriveData):
    required_col = ["TaskNum"]
    drivedata.checkColumnsNumeric(required_col)
    taskNum = drivedata.data.get_column("TaskNum").mode()
    if len(taskNum) > 0:
        return taskNum[0]
    else:
        return None


@registerMetric("errorPresses")
def numOfErrorPresses(drivedata: pydre.core.DriveData):
    required_col = ["SimTime", "TaskFail"]
    drivedata.checkColumnsNumeric(required_col)
    df = drivedata.data.select(required_col)
    df = df.unique(maintain_order=True).drop_nulls()
    presses = df.select((pl.col("TaskFail").shift() != pl.col("TaskFail")) > 0).sum()
    return presses


@registerMetric(
    columnnames=[
        "numOfGlancesOR",
        "numOfGlancesOR2s",
        "meanGlanceORDuration",
        "sumGlanceORDuration",
    ]
)
def gazeNHTSA(drivedata: pydre.core.DriveData):
    required_col = ["VidTime", "gaze", "gazenum", "TaskFail", "taskblocks", "PartID"]
    drivedata.checkColumns(required_col)

    numofglances = 0

    df = drivedata.data.select(required_col).unique(maintain_order=True).drop_nulls()

    # construct table with columns [glanceduration, glancelocation, error]
    gr = df.group_by("gazenum")

    glancelist = gr.agg(
        durations=(pl.col("VidTime").max() - pl.col("VidTime").min()),
        locations=pl.col("gaze")
        .first()
        .fill_null("offroad")
        .replace(
            ["car.WindScreen", "car.dashPlane", "None"],
            ["onroad", "offroad", "offroad"],
        ),
        error_list=pl.col("TaskFail").any(),
        TaskID=pl.col("TaskID").min(),
        taskblock=pl.col("taskblocks").min(),
        Subject=pl.col("PartID").min(),
    )

    # appendDFToCSV_void(glancelist_aug, "glance_list.csv")

    # table constructed, now find metrics
    # glancelist['over2s'] = glancelist['duration'] > 2

    num_over_2s_offroad_glances = glancelist[
        (glancelist["duration"] > 2) & (glancelist["locations"] == "offroad")
    ]["duration"].count()

    num_offroad_glances = glancelist[(glancelist["locations"] == "offroad")][
        "duration"
    ].count()

    total_time_offroad_glances = glancelist[(glancelist["locations"] == "offroad")][
        "duration"
    ].sum()

    mean_time_offroad_glances = glancelist[(glancelist["locations"] == "offroad")][
        "duration"
    ].mean()

    # print(">2s glances: {}, num glances: {}, total time glances: {}, mean time glances {}".format(
    # num_over_2s_offroad_glances, num_offroad_glances, total_time_offroad_glances, mean_time_offroad_glances))

    return [
        num_offroad_glances,
        num_over_2s_offroad_glances,
        mean_time_offroad_glances,
        total_time_offroad_glances,
    ]


@registerMetric(
    columnnames=[
        "numOfGlancesOffR",
        "numOfGlancesOffR2s",
        "meanGlanceOffRDuration",
        "sumGlanceOffRDuration",
    ]
)
def gazeNHTSATask(
    drivedata: pydre.core.DriveData,
    gazetype_col="onroad",
    gazenum_col="gazenum",
    time_col="DatTime",
):
    try:
        drivedata.checkColumns([gazenum_col, gazetype_col, time_col])
    except ColumnsMatchError:
        return [None, None, None, None]

    # construct table with columns [glanceduration, glancelocation, error]
    gr = drivedata.data.group_by("gazenum")

    glancelist = gr.agg(
        duration=(pl.col(time_col).max() - pl.col(time_col).min()),
        location=pl.col(gazetype_col).first(),
    )

    # table constructed, now find metrics

    num_over_2s_offroad_glances = glancelist.filter(
        (pl.col("duration") > 2) & (pl.col("location") == 0)
    ).height

    num_offroad_glances = glancelist.filter(pl.col("location") == 0).height

    total_time_offroad_glances = (
        glancelist.filter(pl.col("location") == 0).get_column("duration").sum()
    )

    mean_time_offroad_glances = (
        glancelist.filter(pl.col("location") == 0).get_column("duration").mean()
    )

    # print(">2s glances: {}, num glances: {}, total time glances: {}, mean time glances {}".format(
    # num_over_2s_offroad_glances, num_offroad_glances, total_time_offroad_glances, mean_time_offroad_glances))

    return [
        num_offroad_glances,
        num_over_2s_offroad_glances,
        mean_time_offroad_glances,
        total_time_offroad_glances,
    ]


@registerMetric(
    columnnames=[
        "numOfGlancesOR",
        "numOfGlancesOR2s",
        "meanGlanceORDuration",
        "sumGlanceORDuration",
    ]
)
def gazeNHTSA(drivedata: pydre.core.DriveData):
    required_col = ["VidTime", "gaze", "gazenum", "TaskFail", "taskblocks", "PartID"]
    drivedata.checkColumns(required_col)

    numofglances = 0

    df = drivedata.data.select(required_col).unique(maintain_order=True).drop_nulls()

    # construct table with columns [glanceduration, glancelocation, error]
    gr = df.group_by("gazenum")

    glancelist = gr.agg(
        durations=(pl.col("VidTime").max() - pl.col("VidTime").min()),
        locations=pl.col("gaze")
        .first()
        .fill_null("offroad")
        .replace(
            ["car.WindScreen", "car.dashPlane", "None"],
            ["onroad", "offroad", "offroad"],
        ),
        error_list=pl.col("TaskFail").any(),
        TaskID=pl.col("TaskID").min(),
        taskblock=pl.col("taskblocks").min(),
        Subject=pl.col("PartID").min(),
    )

    # appendDFToCSV_void(glancelist_aug, "glance_list.csv")

    # table constructed, now find metrics
    # glancelist['over2s'] = glancelist['duration'] > 2

    num_over_2s_offroad_glances = glancelist[
        (glancelist["duration"] > 2) & (glancelist["locations"] == "offroad")
    ]["duration"].count()

    num_offroad_glances = glancelist[(glancelist["locations"] == "offroad")][
        "duration"
    ].count()

    total_time_offroad_glances = glancelist[(glancelist["locations"] == "offroad")][
        "duration"
    ].sum()

    mean_time_offroad_glances = glancelist[(glancelist["locations"] == "offroad")][
        "duration"
    ].mean()

    # print(">2s glances: {}, num glances: {}, total time glances: {}, mean time glances {}".format(
    # num_over_2s_offroad_glances, num_offroad_glances, total_time_offroad_glances, mean_time_offroad_glances))

    return [
        num_offroad_glances,
        num_over_2s_offroad_glances,
        mean_time_offroad_glances,
        total_time_offroad_glances,
    ]


# not working
def addVelocities(drivedata: pydre.core.DriveData):
    df = pl.DataFrame(drivedata.data)
    # add column with ownship velocity
    g = np.gradient(df.XPos.values, df.SimTime.values)
    df.insert(len(df.columns), "OwnshipVelocity", g, True)
    # add column with leadcar velocity
    headwayDist = df.HeadwayTime * df.OwnshipVelocity
    # v = df.OwnshipVelocity+np.gradient(headwayDist, df.SimTime.values)
    df.insert(len(df.columns), "LeadCarPos", headwayDist + df.XPos.values, True)
    df.insert(len(df.columns), "HeadwayDist", headwayDist, True)
    v = np.gradient(headwayDist + df.XPos.values, df.SimTime.values)
    df.insert(len(df.columns), "LeadCarVelocity", v, True)
    return df


@registerMetric()
def crossCorrelate(drivedata: pydre.core.DriveData):
    df = drivedata.data
    if "OwnshipVelocity" not in df.columns or "LeadCarVelocity" not in df.columns:
        df = addVelocities(drivedata)
        print("calling addVelocities()")

    v2 = df.LeadCarVelocity
    v1 = df.OwnshipVelocity
    cor = signal.correlate(v1 - v1.mean(), v2 - v2.mean(), mode="same")
    # cor-An N-dimensional array containing a subset of the discrete linear cross-correlation of in1 with in2.
    # delay index at the max
    df.insert(len(df.columns), "CrossCorrelations", cor, True)
    delayIndex = np.argmax(cor)
    if delayIndex > 0:
        v2 = df.LeadCarVelocity.iloc[delayIndex : df.columns.__len__()]
        v1 = df.OwnshipVelocity.iloc[delayIndex : df.columns.__len__()]
    # normalize vectors
    v1_norm = v1 / np.linalg.norm(v1)
    v2_norm = v2 / np.linalg.norm(v2)
    cor = np.dot(v1_norm, v2_norm)
    if cor > 0:
        return cor
    else:
        return 0.0


# find relative time where speed is within [mpsBound] of new speed limit
# 0 is when the car is crossing the sign.
# Returns None if the speed is never within 2
@registerMetric()
def speedLimitMatchTime(
    drivedata: pydre.core.DriveData, mpsBound: float, speedLimitCol: str
):
    required_col = ["DatTime", speedLimitCol, "Velocity"]
    diff = drivedata.checkColumns(required_col)

    speed_limit = drivedata.data.get_column(speedLimitCol).tail(1).item() * 0.44704
    starting_speed_limit = (
        drivedata.data.get_column(speedLimitCol).head(1).item() * 0.44704
    )

    if speed_limit == 0 or starting_speed_limit == 0:
        return None

    if speed_limit > starting_speed_limit:
        # increasing speed
        match_speed_block = drivedata.data.filter(
            pl.col("Velocity") >= (speed_limit - mpsBound)
        )
    else:
        match_speed_block = drivedata.data.filter(
            pl.col("Velocity") <= (speed_limit + mpsBound)
        )

    if match_speed_block.height > 0:
        time = match_speed_block.item(0, "DatTime")
    else:
        time = drivedata.data.tail(1).get_column("DatTime").item()

    sign_time = drivedata.data.filter(
        abs(pl.col(speedLimitCol) * 0.44704 - starting_speed_limit) > 0.1
    ).item(0, "DatTime")

    if time is None:
        return None
    else:
        # print( starting_speed_limit, speed_limit, time, sign_time)
        return time - sign_time
