import polars as pl
from loguru import logger

import pydre.core
from pydre.filters import registerFilter

# The following functions need to be revised to work with polars rather than pandas

#
# @registerFilter()
# def smarteyeTimeSync(drivedata: pydre.core.DriveData, smarteye_vars: List[str]):
#     # TODO: switch to using polars
#
#     dt = drivedata.data.to_pandas()
#     # REALTIME_CLOCK is the 64-bit integer timestamp from SmartEye
#     # The clock data from SimObserver is in two different 32-bit integer values:
#     # hiFileTime encodes the high-order bits of the clock data
#     # lowFileTime encodes the low-order bits of the clock data
#     dt["SimCreatorClock"] = np.vectorize(mergeSplitFiletime)(
#         dt["hiFileTime"], dt["lowFileTime"]
#     )
#     dt["SimCreatorClock"] = dt["SimCreatorClock"].apply(filetimeToDatetime)
#     dt["SmartEyeClock"] = np.vectorize(filetimeToDatetime)(dt["REALTIME_CLOCK"])
#
#     # make a new data table with only the smarteye vars, for preparation for realignment
#     # first we should check if all the varables we want to shift are actually in the data
#     orig_columns = set(dt.columns)
#     smarteye_columns = set(smarteye_vars)
#
#     if not smarteye_columns.issubset(orig_columns):
#         logger.error(
#             "Some columns defined in the filter parameters are not in the DriveData: {}"
#             % [smarteye_columns - orig_columns]
#         )
#         # there is probably a cleaner way to do this operation.
#         # We want to keep only the smarteye data columns that are actually in the data file
#         smarteye_columns = smarteye_columns - (smarteye_columns - orig_columns)
#
#     smarteye_columns.add("SmartEyeClock")
#     smarteye_data = dt[smarteye_columns]
#     simcreator_data = dt[orig_columns - smarteye_columns]
#     drivedata.data = pl.from_pandas(
#         pandas.merge_asof(
#             simcreator_data,
#             smarteye_data,
#             left_on="SimCreatorClock",
#             right_on="SmartEyeClock",
#         )
#     )
#     return drivedata
#
#
# @registerFilter()
# def smoothGazeData(
#     drivedata: pydre.core.DriveData,
#     timeColName: str = "DatTime",
#     gazeColName: str = "FILTERED_GAZE_OBJ_NAME",
#     latencyShift=6,
# ):
#     # Right now this is just converting to a pandas DataFrame, doing the old computation and converting back
#     # TODO: convert to actually use polars
#
#     required_col = [timeColName, gazeColName]
#     diff = drivedata.checkColumns(required_col)
#
#     dt = drivedata.data.to_pandas()
#     cat_type = CategoricalDtype(
#         categories=[
#             "None",
#             "localCS.dashPlane",
#             "localCS.WindScreen",
#             "localCS.CSLowScreen",
#             "onroad",
#             "offroad",
#         ]
#     )
#     dt["gaze"] = dt[gazeColName].astype(cat_type)
#
#     # dt['gaze'].replace(['None', 'car.dashPlane', 'car.WindScreen'], ['offroad', 'offroad', 'onroad'], inplace=True)
#     dt["gaze"].replace(
#         ["None", "localCS.dashPlane", "localCS.WindScreen", "localCS.CSLowScreen"],
#         ["offroad", "offroad", "onroad", "offroad"],
#         inplace=True,
#     )
#
#     if len(dt["gaze"].unique()) < 2:
#         print("Bad gaze data, not enough variety. Aborting")
#         return None
#
#     # smooth frame blips
#     gaze_same = (
#         (dt["gaze"].shift(-1) == dt["gaze"].shift(1))
#         & (dt["gaze"].shift(-2) == dt["gaze"].shift(2))
#         & (dt["gaze"].shift(-2) == dt["gaze"].shift(-1))
#         & (dt["gaze"] != dt["gaze"].shift(1))
#     )
#     # print("{} frame blips".format(gaze_same.sum()))
#     dt.loc[gaze_same, "gaze"] = dt["gaze"].shift(-1)
#
#     # adjust for 100ms latency
#     dt["gaze"] = dt["gaze"].shift(-latencyShift)
#     dt["timedelta"] = pandas.to_timedelta(dt[timeColName].astype(float), unit="s")
#     dt.set_index("timedelta", inplace=True)
#
#     # filter out noise from the gaze column
#     # SAE J2396 defines fixations as at least 0.2 seconds,
#     min_delta = pandas.to_timedelta(0.2, unit="s")
#     # so we ignore changes in gaze that are less than that
#
#     # find list of runs
#     dt["gazenum"] = (dt["gaze"].shift(1) != dt["gaze"]).astype(int).cumsum()
#     n = dt["gazenum"].max()
#     dt = dt.reset_index()
#     # breakpoint()
#     durations = (
#         dt.groupby("gazenum")["timedelta"].max()
#         - dt.groupby("gazenum")["timedelta"].min()
#     )
#
#     # print("{} gazes before removing transitions".format(n))
#     short_gaze_count = 0
#     dt.set_index("gazenum")
#
#     short_duration_indices = durations[durations.lt(min_delta)].index.values
#     short_gaze_count = len(short_duration_indices)
#     dt.loc[dt["gazenum"].isin(short_duration_indices), "gaze"] = np.nan
#
#     # for x in trange(durations.index.min(), durations.index.max()):
#     # if durations.loc[x] < min_delta:
#     # short_gaze_count += 1
#     # dt['gaze'].where(dt['gazenum'] != x, inplace=True)
#     # dt.loc[x,'gaze']  = np.nan
#     # dt.loc[dt['gazenum'] == x, 'gaze'] = np.nan
#     dt.reset_index()
#     # print("{} transition gazes out of {} gazes total.".format(short_gaze_count, n))
#     dt["gaze"].fillna(method="bfill", inplace=True)
#     dt["gazenum"] = (dt["gaze"].shift(1) != dt["gaze"]).astype(int).cumsum()
#     # print("{} gazes after removing transitions.".format(dt['gazenum'].max()))
#
#     drivedata.data = polars.from_pandas(dt)
#     return drivedata


@registerFilter()
def smoothGazeData(
    drivedata: pydre.core.DriveData,
    timeColName: str = "DatTime",
    gazeColName: str = "FILTERED_GAZE_OBJ_NAME",
    latencyShift=6,
):
    required_col = [timeColName, gazeColName]
    drivedata.checkColumns(required_col)

    # adjust for 100ms latency
    dt = drivedata.data.with_columns(pl.col(gazeColName).shift(-6))

    mapping = {
        "None": 0,
        "WindScreen": 1,
        "InstrumentCluster": 0,
        "InteriorCabin": 0,
        "BottomCenterDisplay": 0,
        "TopCenterDisplay": 0,
        "DrvrSideMirror": 0,
        "RearViewMirror": 0,
        "PassSideMirror": 0,
    }
    dt = dt.with_columns(
        pl.col(gazeColName)
        .replace(mapping, default=0, return_dtype=pl.Float32)
        .alias("onroad")
    )

    if dt.get_column("onroad").n_unique() < 2:
        logger.error("Gaze data not of sufficient variety. Skipping filtering.")
        return drivedata

    # smooth frame blips
    dt = dt.with_columns(
        pl.col("onroad").rolling_median(window_size=5, center=True).alias("onroad")
    )

    # find list of runs
    dt = dt.with_columns(
        (pl.col("onroad").shift() != pl.col("onroad")).cum_sum().alias("gazenum")
    )

    durations = dt.group_by("gazenum").agg(
        glance_duration=pl.col(timeColName).max() - pl.col(timeColName).min()
    )

    # SAE J2396 defines fixations as at least 0.2 seconds,
    # so we ignore changes in gaze that are less than that
    sub200msGazes = durations.filter(pl.col("glance_duration") < 0.2).get_column(
        "gazenum"
    )

    dt = dt.with_columns(
        pl.when(pl.col("gazenum").is_in(sub200msGazes))
        .then(None)
        .otherwise(pl.col("onroad"))
        .alias("onroad")
    )

    dt = dt.with_columns(pl.col("onroad").fill_null(strategy="backward"))

    # find list of runs with short fixations removed
    dt = dt.with_columns(
        (pl.col("onroad").shift() != pl.col("onroad")).cum_sum().alias("gazenum")
    )

    drivedata.data = dt

    return drivedata
