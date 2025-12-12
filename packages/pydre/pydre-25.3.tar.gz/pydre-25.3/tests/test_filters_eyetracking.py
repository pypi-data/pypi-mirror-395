import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import polars as pl
from pydre.core import DriveData
from pydre.filters.eyetracking import smoothGazeData


class DummyDriveData(DriveData):
    def __init__(self, df: pl.DataFrame):
        super().__init__()
        self.data = df


def test_smooth_gaze_data_basic_case():
    df = pl.DataFrame(
        {
            "DatTime": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
            "FILTERED_GAZE_OBJ_NAME": [
                "WindScreen",
                "None",
                "DrvrSideMirror",
                "WindScreen",
                "RearViewMirror",
                "WindScreen",
                "InteriorCabin",
                "WindScreen",
            ],
        }
    )

    dd = DummyDriveData(df)
    result = smoothGazeData(dd)

    assert isinstance(result, DriveData)
    assert "onroad" in result.data.columns
    assert "gazenum" in result.data.columns

    onroad_values = result.data.get_column("onroad").unique().to_list()
    assert all(v in [0.0, 1.0] for v in onroad_values if v is not None)


def test_smooth_gaze_data_low_variation():
    df = pl.DataFrame(
        {"DatTime": [0.0, 0.1, 0.2], "FILTERED_GAZE_OBJ_NAME": ["None", "None", "None"]}
    )

    dd = DummyDriveData(df)
    result = smoothGazeData(dd)

    assert isinstance(result, DriveData)
    assert result.data.shape == dd.data.shape
