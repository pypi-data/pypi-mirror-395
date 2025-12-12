"""
Unit tests for SpaceROI class in pydre.rois.
Covers:
  - Successful splitting of points inside/outside an ROI
  - Malformed CSV definitions (invalid or missing columns)
  - Logging behavior when no data or bad datatypes occur
"""

import re
import polars as pl
import pytest
from pydre.core import DriveData
from pydre.rois import SpaceROI


@pytest.fixture
def basic_points_df():
    """Return a DataFrame with XPos,YPos pairs for testing."""
    return pl.DataFrame(
        {
            "XPos": [1.0, 2.0, 4.0, 5.0],
            "YPos": [1.0, 2.0, 4.0, 5.0],
        }
    )


@pytest.fixture
def simple_roi_csv(tmp_path):
    """Create a CSV file defining a single ROI covering X:[1,3], Y:[1,3]."""
    df = pl.DataFrame(
        {
            "roi": ["valid_roi"],
            "X1": [1],
            "X2": [3],
            "Y1": [1],
            "Y2": [3],
        }
    )
    path = tmp_path / "simple_space_roi.csv"
    df.write_csv(str(path))
    return path


@pytest.mark.parametrize(
    "columns,row",
    [
        # Completely wrong columns → no 'roi', X1, X2, Y1, Y2
        (["wrong", "columns"], [1, 2]),
        # Missing Y1, Y2 keys
        (["roi", "X1", "X2"], ["bad_roi", 0, 2]),
    ],
)
def test_space_roi_malformed_csv(tmp_path, columns, row):
    """
    SpaceROI should raise ValueError if the CSV is missing required columns.
    """
    # Build a malformed ROI CSV
    roi_df = pl.DataFrame({col: [val] for col, val in zip(columns, row)})
    path = tmp_path / "malformed_space_roi.csv"
    roi_df.write_csv(str(path))

    # Expect ValueError on initialization
    with pytest.raises(ValueError):
        SpaceROI(str(path))


def test_space_roi_split_valid_range(simple_roi_csv, basic_points_df):
    """
    Verify that SpaceROI correctly filters points within the ROI.
    Only the points (1.0,1.0) and (2.0,2.0) should fall inside [1,3]×[1,3].
    """
    dd = DriveData.init_test(basic_points_df, "dummy.dat")
    dd.metadata["ParticipantID"] = "Tester"

    roi = SpaceROI(str(simple_roi_csv))
    results = roi.split(dd)

    # We expect one DriveData with exactly two rows
    assert len(results) == 1
    data = results[0].data
    assert data.height == 2
    # ROI name is set correctly
    assert results[0].roi == "valid_roi"


def test_space_roi_rectangle_out_of_bounds_logs_warning(
    tmp_path, basic_points_df, caplog
):
    """
    When no points fall inside the ROI, split should still return one DriveData
    but produce a warning indicating no data for that SubjectID.
    """
    roi_df = pl.DataFrame(
        {
            "roi": ["offbounds"],
            "X1": [100],
            "X2": [200],
            "Y1": [100],
            "Y2": [200],
        }
    )
    path = tmp_path / "offbounds_space_roi.csv"
    roi_df.write_csv(str(path))

    dd = DriveData.init_test(basic_points_df, "dummy.dat")
    dd.metadata["ParticipantID"] = "TestSubject"

    with caplog.at_level("WARNING"):
        roi = SpaceROI(str(path))
        results = roi.split(dd)

    # Expect one result with zero rows
    assert len(results) == 1
    assert results[0].data.height == 0
    # Check the warning text with regex for full message structure
    assert re.search(
        r"No data for SubjectID: TestSubject, Source: dummy\.dat,  ROI: offbounds",
        caplog.text,
    )


def test_space_roi_invalid_type_logs_error(tmp_path, basic_points_df, caplog):
    """
    When ROI CSV contains non-numeric coordinate, split should return empty list
    and log an ERROR about bad datatype.
    """
    roi_df = pl.DataFrame(
        {
            "roi": ["invalid"],
            "X1": ["not-a-number"],
            "X2": [2],
            "Y1": [0],
            "Y2": [3],
        }
    )
    path = tmp_path / "invalid_space_roi.csv"
    roi_df.write_csv(str(path))

    dd = DriveData.init_test(basic_points_df, "dummy.dat")

    roi = SpaceROI(str(path))
    with caplog.at_level("ERROR"):
        results = roi.split(dd)

    assert results == []
    # Look for 'bad datatype' substring in error log
    assert re.search(r"bad datatype", caplog.text.lower())


# TODO: Implement tests for correct input handling in the ROIs tests. At the moment, only error scenarios are tested. (Use test files for validation)
"""
Unit tests for correct handling of SpaceROI with valid inputs:
  - multiple ROI definitions in one CSV
  - inclusion of boundary points in each ROI
  - exclusion of points outside any ROI
"""


@pytest.fixture
def test_points():
    """Return a DataFrame of test points with XPos and YPos columns."""
    return pl.DataFrame(
        {
            "XPos": [0, 1, 2, 3, 5],
            "YPos": [0, 1, 2, 3, 5],
        }
    )


@pytest.fixture
def drive_data_with_metadata(test_points):
    """
    Initialize DriveData with test_points and
    set metadata["ParticipantID"] to 'Tester'.
    """
    dd = DriveData.init_test(test_points, "dummy.dat")
    dd.metadata["ParticipantID"] = "Tester"
    return dd


def test_space_roi_multiple_rois_and_boundaries(tmp_path, drive_data_with_metadata):
    """
    Verify that SpaceROI correctly splits points among multiple ROIs,
    including points exactly on the boundary.
    """
    # Create a CSV file defining two ROIs:
    # - roiA covers X in [0,2] and Y in [0,2]
    # - roiB covers X in [2,4] and Y in [2,4]
    roi_definitions = pl.DataFrame(
        {
            "roi": ["roiA", "roiB"],
            "X1": [0, 2],
            "X2": [2, 4],
            "Y1": [0, 2],
            "Y2": [2, 4],
        }
    )
    roi_csv_path = tmp_path / "multi_space_roi.csv"
    roi_definitions.write_csv(str(roi_csv_path))

    # Perform the split operation using the fixture-provided DriveData
    results = SpaceROI(str(roi_csv_path)).split(drive_data_with_metadata)

    # Expect two output DriveData objects, one per ROI
    returned_rois = sorted([r.roi for r in results])
    assert returned_rois == ["roiA", "roiB"]

    # Check that the row counts match expected:
    # - roiA should have 3 rows (points at (0,0), (1,1), and (2,2))
    # - roiB should have 2 rows (points at (2,2) and (3,3))
    counts = {r.roi: r.data.height for r in results}
    assert counts["roiA"] == 3
    assert counts["roiB"] == 2
