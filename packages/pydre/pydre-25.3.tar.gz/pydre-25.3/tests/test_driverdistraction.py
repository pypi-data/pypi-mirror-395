import pytest
import polars as pl
from pydre.core import DriveData
from pydre.metrics import driverdistraction


# Helper function to create a mock DriveData object
def make_drive_data(df_dict, metadata={}):
    df = pl.DataFrame(df_dict)
    d = DriveData()
    d.data = df
    d.metadata = metadata
    d.sourcefilename = "test"
    return d


# ---- getTaskNum ----
def test_get_task_num():
    df = {"TaskNum": [1, 2, 2, 3]}
    data = make_drive_data(df)
    result = driverdistraction.getTaskNum(data)
    assert result == 2


def test_get_task_num_empty():
    # Must explicitly specify data type for empty series
    df = {"TaskNum": pl.Series("TaskNum", [], dtype=pl.Int64)}
    data = make_drive_data(df)
    result = driverdistraction.getTaskNum(data)
    assert result is None


# ---- numOfErrorPresses ----
def test_num_of_error_presses():
    df = {"SimTime": [0, 1, 2], "TaskFail": [0, 1, 1]}
    data = make_drive_data(df)
    result = driverdistraction.numOfErrorPresses(data)
    assert result.shape == (1, 1)


# ---- gazeNHTSATask: missing column fallback ----
def test_gaze_nhtsa_task_missing_col():
    df = {"gazenum": [0, 0], "DatTime": [1.0, 3.5]}  # Missing 'onroad'
    data = make_drive_data(df)
    result = driverdistraction.gazeNHTSATask(data)
    assert result == [None, None, None, None]


# ---- speedLimitMatchTime: increasing speed ----
def test_speed_limit_match_time_increasing():
    df = {
        "DatTime": [0, 1, 2, 3],
        "Velocity": [5, 10, 15, 20],
        "SpeedLimit": [10, 10, 20, 20],
    }
    data = make_drive_data(df)
    result = driverdistraction.speedLimitMatchTime(
        data, mpsBound=1.0, speedLimitCol="SpeedLimit"
    )
    assert isinstance(result, (float, int))


# ---- speedLimitMatchTime: no speed limit change (should raise IndexError or return None)
def test_speed_limit_match_time_none():
    df = {"DatTime": [0, 1, 2], "Velocity": [2, 2, 2], "SpeedLimit": [10, 10, 10]}
    data = make_drive_data(df)
    with pytest.raises(IndexError):
        driverdistraction.speedLimitMatchTime(data, 2.0, "SpeedLimit")
