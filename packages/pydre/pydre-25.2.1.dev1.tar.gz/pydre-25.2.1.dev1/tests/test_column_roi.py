import pydre.core
import pydre.rois
import polars as pl
import pytest
from pathlib import Path
from pydre.core import DriveData
from pydre.rois import ColumnROI

# Define the directory that contains test CSV data
FIXTURE_DIR = Path(__file__).parent.resolve() / "test_data" / "test_roi_files"


@pytest.mark.datafiles(
    FIXTURE_DIR / "test_column_roi.csv"
)  # This file is not used in this test but kept for consistency
def test_column_roi_split(datafiles):
    # Create sample drive data with a column "Task" used for ROI
    df = pl.DataFrame(
        {
            "SimTime": [0, 1, 2, 3, 4, 5],
            "Task": [1, 1, 2, 2, 3, 3],
            "Speed": [10, 20, 30, 40, 50, 60],
        }
    )

    # Metadata is required by DriveData, even if simple
    metadata = {"ParticipantID": "Test01"}
    drive_data = pydre.core.DriveData()
    drive_data.data = df
    drive_data.metadata = metadata
    drive_data.sourcefilename = "dummy"

    # Instantiate a ColumnROI using the "Task" column
    roi = pydre.rois.ColumnROI("Task")
    results = roi.split(drive_data)

    # Expecting 3 distinct ROIs (1, 2, 3)
    assert len(results) == 3

    # ROI labels should match
    roi_names = {d.roi for d in results}
    assert roi_names == {"1", "2", "3"}

    # Each result should be a valid DriveData object
    for d in results:
        assert isinstance(d, pydre.core.DriveData)


def test_column_roi_with_null_group():
    df = pl.DataFrame({"ROI": ["A", None, "B"], "Value": [1, 2, 3]})
    dd = DriveData.init_test(df, "test.dat")
    processor = ColumnROI("ROI")
    result = processor.split(dd)

    cleaned_rois = set(d.roi for d in result if d.roi not in (None, "None"))
    assert cleaned_rois == {"A", "B"}


def test_column_roi_missing_column_logs_error(caplog):
    df = pl.DataFrame({"UnrelatedCol": [1, 2, 3]})
    dd = DriveData.init_test(df, "file.dat")

    roi = ColumnROI("MissingCol")
    with caplog.at_level("ERROR"):
        with pytest.raises(KeyError):
            list(roi.split(dd))
    assert "missingcol" in caplog.text.lower()


def test_column_roi_columnname_none():
    df = pl.DataFrame({"Task": ["A", "B"]})
    dd = DriveData.init_test(df, "sim.dat")
    with pytest.raises(TypeError):
        roi = ColumnROI(columnname=None)
        roi.split(dd)


def test_column_roi_columnname_numeric():
    with pytest.raises(TypeError):
        _ = ColumnROI(123)


def test_column_roi_grouping_returns_empty():
    df = pl.DataFrame({"Task": [None, None, None]})
    dd = DriveData.init_test(df, "sim.dat")
    roi = ColumnROI("Task")
    result = roi.split(dd)
    assert result == []


def test_column_roi_missing_column_keyerror(caplog):
    df = pl.DataFrame({"Other": ["x", "y"]})
    dd = DriveData.init_test(df, "sim.dat")
    roi = ColumnROI("MissingCol")

    with caplog.at_level("ERROR"):
        with pytest.raises(KeyError):
            _ = roi.split(dd)

    assert "not found in data" in caplog.text


def test_column_roi_sets_metadata_and_roi_field():
    roi_df = pl.DataFrame({"roi": ["Zone1", "Zone2"], "column_value": ["A", "B"]})

    df = pl.DataFrame({"column_value": ["A", "B", "C"], "other_col": [1, 2, 3]})
    drive_data = DriveData.init_test(df, "dummy_drive.csv")

    roi = ColumnROI("column_value")
    roi.roi_column_df = roi_df

    result_list = roi.split(drive_data)

    roi_names = [res.metadata.get("ROIName", "") for res in result_list]

    assert "Zone1" in roi_names
    assert "Zone2" in roi_names


def test_column_roi_split_with_no_matching_values(caplog):
    roi_df = pl.DataFrame({"roi": ["ZoneA"], "column_value": ["Z"]})

    df = pl.DataFrame({"column_value": ["X", "Y"], "other_col": [10, 20]})
    drive_data = DriveData.init_test(df, "drive.csv")

    roi = ColumnROI("column_value")
    roi.roi_column_df = roi_df

    with caplog.at_level("WARNING"):
        split_results = roi.split(drive_data)

    assert any(
        "ROI value Z not found in data" in message for message in caplog.messages
    )

    for result in split_results:
        assert "ROIName" not in result.metadata
