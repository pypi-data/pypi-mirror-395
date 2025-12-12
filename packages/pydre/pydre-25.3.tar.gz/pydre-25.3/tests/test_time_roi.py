import polars as pl
import pytest
from pathlib import Path
from pydre.core import DriveData
from pydre.rois import TimeROI, sliceByTime

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_data"


def test_parse_timestamp_valid_formats():
    """
    parseTimeStamp should correctly parse H:M:S, M:S, and pure seconds inputs.
    """
    hours, minutes, seconds = 1, 15, 10
    # "1:15:10" -> 1h + 15m + 10s
    assert TimeROI.parseTimeStamp("1:15:10") == hours * 3600 + minutes * 60 + seconds

    hours, minutes, seconds = 12, 12, 0
    # "12:12:00" -> 12h + 12m + 0s
    assert TimeROI.parseTimeStamp("12:12:00") == hours * 3600 + minutes * 60 + seconds

    minutes, seconds = 12, 59
    # "12:59" -> 12m + 59s
    assert TimeROI.parseTimeStamp("12:59") == minutes * 60 + seconds

    minutes, seconds = 0, 1
    # "00:01" -> 0m + 1s
    assert TimeROI.parseTimeStamp("00:01") == minutes * 60 + seconds

    # Pure seconds input
    assert TimeROI.parseTimeStamp("10.5") == 10.5


def test_parse_timestamp_invalid_formats():
    """
    parseTimeStamp should raise ValueError for malformed inputs.
    """
    with pytest.raises(ValueError):
        TimeROI.parseTimeStamp("1:2:3:4")
    with pytest.raises(ValueError):
        TimeROI.parseTimeStamp("not-a-time")


@pytest.mark.datafiles(FIXTURE_DIR / "test_roi_files")
def test_time_roi_builds_rois_dict(datafiles):
    """
    TimeROI should read CSV and populate the 'rois' dictionary correctly.
    """
    csv_path = datafiles / "test_time_2.csv"
    time_roi = TimeROI(csv_path, timecol="DatTime")
    expected = {
        "roi_1:Practice": {
            "ScenarioName": "Practice",
            "time_start": 0.0,
            "time_end": 180.0,
        },
        "roi_2:Practice": {
            "ScenarioName": "Practice",
            "time_start": 180.0,
            "time_end": 300.0,
        },
    }
    assert time_roi.rois == expected
    assert isinstance(time_roi, TimeROI)


@pytest.mark.datafiles(FIXTURE_DIR / "test_roi_files")
def test_time_roi_splits_into_segments(datafiles):
    """
    TimeROI.split() should produce one DriveData per defined ROI segment.
    """
    roi = TimeROI(datafiles / "test_time_2.csv", timecol="DatTime")
    df = pl.DataFrame(
        {
            "DatTime": [0.0, 90.0, 179.9, 180.0, 240.0, 299.9],
            "Indicator": [1, 2, 3, 4, 5, 6],
        }
    )
    dd = DriveData.init_test(df, "drive.dat")
    dd.metadata = {"ScenarioName": "Practice"}

    segments = roi.split(dd)
    assert len(segments) == 2

    seg1 = next(s for s in segments if s.roi.startswith("roi_1"))
    assert seg1.data["DatTime"].to_list() == [0.0, 90.0, 179.9]

    seg2 = next(s for s in segments if s.roi.startswith("roi_2"))
    assert seg2.data["DatTime"].to_list() == [180.0, 240.0, 299.9]


def test_time_roi_skips_on_metadata_mismatch(tmp_path):
    """
    TimeROI.split() should skip ROI segments when metadata does not match.
    """
    roi_df = pl.DataFrame(
        {
            "ROI": ["RegionA"],
            "time_start": ["00:00"],
            "time_end": ["00:10"],
            "ScenarioName": ["Expected"],
        }
    )
    path = tmp_path / "roi.csv"
    roi_df.write_csv(str(path))

    dd = DriveData.init_test(pl.DataFrame({"SimTime": [1.0]}), "drive.dat")
    dd.metadata = {"ScenarioName": "Actual"}

    results = TimeROI(str(path)).split(dd)
    assert results == []


def test_time_roi_warns_when_no_data_matches(tmp_path, caplog):
    """
    TimeROI.split() should log a WARNING when no data falls within any ROI.
    """
    roi_df = pl.DataFrame(
        {"ROI": ["EmptyRegion"], "time_start": ["00:00"], "time_end": ["00:01"]}
    )
    path = tmp_path / "empty.csv"
    roi_df.write_csv(str(path))

    dd = DriveData.init_test(pl.DataFrame({"DatTime": []}), "drive.dat")
    dd.metadata = {}

    with caplog.at_level("WARNING"):
        result = TimeROI(str(path)).split(dd)
    assert result == []
    assert "fails to qualify" in caplog.text.lower()


def test_slice_by_time_valid_range():
    """
    sliceByTime() should include rows where time_column is in [begin, end).
    """
    df = pl.DataFrame({"SimTime": [0.0, 0.5, 1.0, 1.5], "Value": [10, 20, 30, 40]})
    result = sliceByTime(0.5, 1.5, "SimTime", df)
    assert result.to_dicts() == [
        {"SimTime": 0.5, "Value": 20},
        {"SimTime": 1.0, "Value": 30},
    ]


@pytest.mark.parametrize(
    "df, time_column",
    [
        # Case A: only a non-matching column present
        (
            pl.DataFrame({"OtherTime": [0.1, 0.2, 0.3], "Value": [10, 20, 30]}),
            "SimTime",
        ),
        # Case B: time column exists but the name is wrong
        (pl.DataFrame({"SimTime": [0.1, 0.2, 0.3]}), "NotAColumn"),
    ],
)
def test_slice_by_time_missing_column_logs_error_and_returns_original(
    df, time_column, caplog
):
    """
    When the specified time_column does not exist:
      1) sliceByTime() must return the original DataFrame unchanged.
      2) An ERROR log containing 'Problem in applying Time ROI' is emitted.
    """
    with caplog.at_level("ERROR"):
        result = sliceByTime(0.0, 1.0, time_column, df)

    # Should return original rows
    assert result.to_dicts() == df.to_dicts()

    # Should log an error about the missing time column
    assert "Problem in applying Time ROI".lower() in caplog.text.lower()
