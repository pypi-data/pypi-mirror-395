import re
import pathlib

import polars as pl
from loguru import logger

import pydre.core
from pydre.filters import registerFilter

THISDIR = pathlib.Path(__file__).resolve().parent


@registerFilter()
def modifyCriticalEventsCol(drivedata: pydre.core.DriveData):
    ident = drivedata.metadata["ParticipantID"]
    ident_groups = re.match(r"(\d)(\d)(\d)(\d\d\d\d)[wW](\d)", ident)
    if ident_groups is None:
        logger.warning("Could not parse R2D ID " + ident)
        return [None]
    week = ident_groups.group(5)
    scenario = drivedata.metadata["ScenarioName"]
    if week == "1" and scenario == "Load, Event":
        # between the x positions, change the critical event status to 1
        drivedata.data = drivedata.data.with_columns(
            pl.when(2165 < pl.col("XPos"), pl.col("XPos") < 2240)
            .then(1)
            .when(pl.col("CriticalEventStatus") == 1)
            .then(1)
            .otherwise(0)
            .alias("CriticalEventStatus")
        )
    return drivedata


@registerFilter()
def ValidateDataStartEnd(
    drivedata: pydre.core.DriveData, dataFile="", tol=100, trim_data=False
):
    """
    Ensure that the end of the drive data fits into the expected
    format - by distance & time.

    "early" - when xPos is less than expected
    "late" - when xPos is greater than expected
    "valid" - when all xPos fall within tolerance range

    :arg: dataFile: source of truth for start/end - csv filepath
    :arg: tol: tolerance of distance that permits "valid"
    """
    ident = drivedata.metadata["ParticipantID"]
    scenario = drivedata.metadata["ScenarioName"]
    # (control=5/case=3)(UAB=1/OSU=2)(Male=1/Female=2)(R2D_ID)w(Week Num)
    ident_groups = re.match(r"(\d)(\d)(\d)(\d\d\d\d)[wW](\d)", ident)
    if ident_groups is None:
        logger.warning("Could not parse R2D ID " + ident)
        return [None]
    week = ident_groups.group(5)
    df = drivedata.data

    if dataFile != "":
        merge_df = pl.read_csv(source=dataFile)
        merge_df = merge_df.filter(
            merge_df.get_column("Scenario") == scenario,
            merge_df.get_column("Week") == week,
        )
    else:
        raise Exception(
            "Datafile start/end definition not present - cannot merge w/o source of truth."
        )

    if len(merge_df) > 0:
        status = []
        expected_start = merge_df["Start Pos"][0]
        expected_end = merge_df["End Pos"][0]
        actual_start = df["XPos"][0]
        actual_end = df["XPos"][-1]

        if actual_start is None:
            logger.warning(
                f"Start point in data is null for {ident}. See data for issue."
            )

        if actual_end is None:
            logger.warning(
                f"End point in data is null for {ident}. See data for issue."
            )

        if actual_start < expected_start - tol:
            status.append("earlyStart")
        elif actual_start > expected_start + tol:
            status.append("lateStart")

        if actual_end < expected_end - tol:
            status.append("earlyEnd")
        elif actual_end > expected_end + tol:
            status.append("lateEnd")

        if not status:
            status.append("valid")

        status_value = "&".join(status)
        df = df.with_columns(pl.lit(status_value).alias("validityCheck"))
        if trim_data:
            start_shape = df.shape
            df = df.filter(df.get_column("XPos") >= expected_start)
            clipped_shape = df.shape
            start_rows_clip = start_shape[0] - clipped_shape[0]
            df = df.filter(df.get_column("XPos") <= expected_end)
            end_rows_clip = clipped_shape[0] - df.shape[0]
            # make valid determination & assign deterministic flags that we assess & sort on
            # stopsLate, stopsEarly, startEarly, startLate, valid
            df = df.with_columns(
                pl.lit(start_rows_clip).alias("rowsClippedAtStart"),
                pl.lit(end_rows_clip).alias("rowsClippedAtEnd"),
                pl.lit(actual_start).alias("preClipStartPos"),
                pl.lit(actual_end).alias("preClipEndPos"),
            )
    else:
        logger.warning(f"No start/end values for {ident} in {dataFile}.")
        return [None]

    drivedata.data = df
    return drivedata


@registerFilter()
def BinaryColReverse(
    drivedata: pydre.core.DriveData, old_col: str, new_col="MinusOneCol"
):
    """
    'reverses' a binary column's values.
    old value 1 --> new value 0 & vice versa
    """
    df = drivedata.data
    drivedata.data = df.with_columns((1 - pl.col(old_col)).alias(new_col))

    return drivedata


@registerFilter()
def CropStartPosition(drivedata: pydre.core.DriveData):
    """
    Ensure that drive data starts from consistent point between sites.
    This code was decoupled from merge filter to zero UAB start points.
    """
    ident = drivedata.metadata["ParticipantID"]
    # (control=5/case=3)(UAB=1/OSU=2)(Male=1/Female=2)(R2D_ID)w(Week Num)
    ident_groups = re.match(r"(\d)(\d)(\d)(\d\d\d\d)[wW](\d)", ident)
    if ident_groups is None:
        logger.warning("Could not parse R2D ID " + ident)
        return [None]
    site = int(ident_groups.group(2))
    # copy values from datTime into simTime
    df = drivedata.data

    # only used to apply this to UAB, but applies to all sites
    df = df.with_columns(pl.col("DatTime").alias("SimTime"))
    df = df.with_columns(pl.col("XPos").cast(pl.Float32).diff().abs().alias("PosDiff"))
    df_actual_start = df.filter(df.get_column("PosDiff") > 500)
    if not df_actual_start.is_empty():
        start_time = df_actual_start.get_column("SimTime").item(0)
        df = df.filter(df.get_column("SimTime") > start_time)
        logger.warning(f"Trimming {ident}: time value of split: {start_time}")

    drivedata.data = df
    return drivedata


@registerFilter()
def MergeCriticalEventPositions(
    drivedata: pydre.core.DriveData,
    dataFile="",
    analyzePriorCutOff=False,
    criticalEventDist=250.0,
    cutOffDist=150.0,
    cutInDist=50.0,
    cutInStart=200.0,
    cutOffStart=200.0,
    cutInDelta=2.5,
    headwayThreshold=250.0,
):
    """
    :arg: dataFile: the file name of the csv that maps CE positions.
        -> required cols:
        'Week','ScenarioName','Event','maneuver pos','CENum'
    :arg: analyzePriorCutOff: True: analyze Subject's reaction before cut-In CE
                            False: analyze Subject's reaction after cut-In CE
    :arg: criticalEventDist: determines how many meters on the X-axis
        is determined to be "within the critical event duration"
    :arg: cutOffDist: distance modifier in meters for cut-off range
    :arg: cutInDist: distance modifier in meters for cut-in range
    :arg: cutInStart: offset for cut-in event execution start
    :arg: cutOffStart: offset for cut-off event execution start
    :arg: cutInDelta: time, in seconds, to account for subject
        reaction inclusion to ROI for Cut-Off Critical Event.
    :arg: headwayThreshold: determines whether Subject is following a vehicle

    with defaults:
    cut-in: range=300m; start_offset=200
    cut-off: range=400m; start_offset=200
    trashtip: range=250m; start_offset=0

    Imports specified csv dataFile for use in XPos-based filtering,
    using 'manuever pos'. dataFile also determines additional columns
    in the filtered result:
        - CriticalEventNum
        - EventName
    """
    ident = drivedata.metadata["ParticipantID"]
    scenario = drivedata.metadata["ScenarioName"]
    # (control=5/case=3)(UAB=1/OSU=2)(Male=1/Female=2)(R2D_ID)w(Week Num)
    ident_groups = re.match(r"(\d)(\d)(\d)(\d\d\d\d)[wW](\d)", ident)
    if ident_groups is None:
        logger.warning("Could not parse R2D ID " + ident)
        return [None]
    week = ident_groups.group(5)
    df = drivedata.data
    df = df.with_columns(
        pl.lit(-1).alias("CriticalEventNum"), pl.lit("").alias("EventName")
    )
    if "No Event" not in scenario:
        # adding cols with meaningless values for later CE info, ensuring shape
        if dataFile != "":
            merge_df = pl.read_csv(source=dataFile)
            merge_df = merge_df.filter(
                merge_df.get_column("ScenarioName") == scenario,
                merge_df.get_column("Week") == week,
            )
        else:
            raise Exception("Datafile not present - cannot merge w/o source of truth.")

        ceInfo_df = merge_df.select(
            pl.col("manuever pos"), pl.col("CENum"), pl.col("Event")
        )
        filter_df = df.clear()

        for ceRow in ceInfo_df.rows():
            # critical event position, number, and name
            cePos = ceRow[0]
            ceNum = ceRow[1]
            event = ceRow[2]

            # Activation vs manuever execution dictates need for range adjust
            if "cut-in" in event.lower():
                criticalEventDist += cutInDist
                cePos += cutInStart
            elif "cut-off" in event.lower():
                criticalEventDist += cutOffDist
                cePos += cutOffStart

            # xPos based bounding, consider
            ceROI = df.filter(
                df.get_column("XPos") >= cePos,
                df.get_column("XPos") < cePos + criticalEventDist,
            )
            # update existing columns with Critical Event values
            ceROI = ceROI.with_columns(
                pl.lit(ceNum).alias("CriticalEventNum"),
                pl.lit(event).alias("EventName"),
            )

            # cut-off/in need better filtering, based on headway check
            if "trash" not in event.lower():
                headwayROI = ceROI.filter(
                    ceROI.get_column("HeadwayDistance") <= headwayThreshold
                )
                if not headwayROI.is_empty():
                    logger.debug(f"{event} recovery detected in data.")
                    # rewind and/or expand timeframe for cut-off timings
                    if "cut-off" in event.lower():
                        simTimeStart = headwayROI.get_column("SimTime").head(1).item()
                        simTimeEnd = headwayROI.get_column("SimTime").tail(1).item()
                        if analyzePriorCutOff:
                            ceROI = df.filter(
                                df.get_column("SimTime") >= simTimeStart - cutInDelta,
                                df.get_column("SimTime") <= simTimeEnd,
                            )
                        else:
                            ceROI = df.filter(
                                df.get_column("SimTime") >= simTimeStart,
                                df.get_column("SimTime") <= simTimeEnd + cutInDelta,
                            )
                        ceROI = ceROI.with_columns(
                            pl.lit(ceNum).alias("CriticalEventNum"),
                            pl.lit(event).alias("EventName"),
                        )
                else:
                    logger.warning(
                        f"{event} Event for {ident} in scenario '{scenario}' does not display expected headway behavior."
                    )

            filter_df.extend(ceROI)
            drivedata.data = filter_df
        if ceInfo_df.shape[0] == 0:
            logger.warning("No imported merge info - no known CE positions.")
    else:
        logger.warning(
            "Attempting to run 'Event' filtering on scenario with no Events - don't filter."
        )
        drivedata.data = df
    return drivedata


@registerFilter()
def DesignateNonEventRegions(drivedata: pydre.core.DriveData, dataFile=""):
    """
    Imports specified csv dataFile for use in XPos-based filtering,
    using each start-end x range. dataFile also determines additional columns

    Parameters:
    dataFile: the file name of the csv that maps Non Event regions.

    Note: Requires data columns:
        'Week','Scenario','Event', 'startX1', 'endX1', 'startX2', 'endX2', 'startX3', 'endX3'

    Returns:
        Original DriveData object with additional column *NonEventRegion* with values of 0-3
        0 indicates non-designated region, 1-3 are the designated regions.

    """
    ident = drivedata.metadata["ParticipantID"]
    scenario = drivedata.metadata["ScenarioName"]
    # (control=5/case=3)(UAB=1/OSU=2)(Male=1/Female=2)(R2D_ID)w(Week Num)
    ident_groups = re.match(r"(\d)(\d)(\d)(\d\d\d\d)[wW](\d)", ident)
    if ident_groups is None:
        logger.warning("Could not parse R2D ID " + ident)
        return [None]
    week = ident_groups.group(5)
    df = drivedata.data

    # adding cols with meaningless values for later region filtering, ensures shape
    df = df.with_columns(
        pl.lit(-1).alias("NonEventRegion"),
    )
    if dataFile != "":
        merge_df = pl.read_csv(source=dataFile)
        merge_df = merge_df.filter(
            merge_df.get_column("Scenario") == scenario,
            merge_df.get_column("Week") == week,
        )
        filter_df = df.clear()
    else:
        raise Exception("Datafile not present - cannot merge w/o source of truth.")

    if merge_df.shape[0] > 0:
        # week/scenario match, have actual coordinates
        startx1 = merge_df["startX1"][0]
        endx1 = merge_df["endX1"][0]
        startx2 = merge_df["startX2"][0]
        endx2 = merge_df["endX2"][0]
        startx3 = merge_df["startX3"][0]
        endx3 = merge_df["endX3"][0]

        region1 = df.filter(
            df.get_column("XPos") >= startx1, df.get_column("XPos") <= endx1
        )
        region1 = region1.with_columns(pl.lit(1).alias("NonEventRegion"))

        region2 = df.filter(
            df.get_column("XPos") >= startx2, df.get_column("XPos") <= endx2
        )
        region2 = region2.with_columns(pl.lit(2).alias("NonEventRegion"))

        region3 = df.filter(
            df.get_column("XPos") >= startx3, df.get_column("XPos") <= endx3
        )
        region3 = region3.with_columns(pl.lit(3).alias("NonEventRegion"))

        filter_df.extend(region1)
        filter_df.extend(region2)
        filter_df.extend(region3)
        drivedata.data = filter_df
    else:
        logger.warning(
            f"Do not have non-event regions for {scenario}, w{week} combo. Skipping.."
        )
        drivedata.data = df
    return drivedata
