import math
import polars as pl
import pydre.core
from pydre.filters import registerFilter


@registerFilter()
def gazeAnglePreProcessing(
    drivedata: pydre.core.DriveData,
    timeColName: str = "DatTime",
    headingColName: str = "GAZE_HEADING",
    pitchColName: str = "GAZE_PITCH",
    targetColName: str = "FILTERED_GAZE_OBJ_NAME",
    half_angle_deg: float = 5.0,
    target_name: str | None = None,
) -> pydre.core.DriveData:
    """
    Compute gaze angle magnitude and mark whether gaze is off-target (cutout).

    Parameters
    ----------
    drivedata : pydre.core.DriveData
        Input DriveData object containing raw gaze columns.
    timeColName : str
        Column name for time stamps (default: 'DatTime').
    headingColName : str
        Column name for horizontal gaze component (default: 'GAZE_HEADING').
    pitchColName : str
        Column name for vertical gaze component (default: 'GAZE_PITCH').
    targetColName : str
        Column name for object gaze classification (default: 'FILTERED_GAZE_OBJ_NAME').
    half_angle_deg : float, optional
        Default cutout half-angle threshold, in degrees. Default is 5.0°.
    target_name : str | None, optional
        Optional target object name to check against FILTERED_GAZE_OBJ_NAME.

    Returns
    -------
    pydre.core.DriveData
        DriveData with new columns:
            - gaze_angle : float (radians)
            - gaze_cutout : bool
            - off_target : bool
    """

    required_cols = [timeColName, headingColName, pitchColName, targetColName]
    drivedata.checkColumns(required_cols)

    df = drivedata.data

    # Compute gaze angle magnitude (radians)
    df = df.with_columns(
        ((pl.col(headingColName) ** 2 + pl.col(pitchColName) ** 2).sqrt()).alias(
            "gaze_angle"
        )
    )

    # Convert threshold from degrees to radians
    half_angle_rad = math.radians(half_angle_deg)

    # Mark if gaze exceeds half-angle cutoff
    df = df.with_columns(
        (pl.col("gaze_angle").abs() > half_angle_rad)
        .cast(pl.Boolean)
        .alias("gaze_cutout")
    )

    # Determine off-target samples
    if target_name:
        off_target_mask = (pl.col(targetColName).is_null()) | (
            pl.col(targetColName) != target_name
        )
    else:
        off_target_mask = pl.col(targetColName).is_null()

    df = df.with_columns(off_target_mask.alias("off_target"))

    drivedata.data = df

    return drivedata
