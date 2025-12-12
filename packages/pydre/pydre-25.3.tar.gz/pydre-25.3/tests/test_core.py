from pathlib import Path
import pytest
import polars as pl
from pydre.core import DriveData, ColumnsMatchError

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_data"


@pytest.mark.datafiles(
    FIXTURE_DIR / "test_datfiles" / "ExampleProject_Sub_1_Drive_1.dat"
)
def test_init_old_rti(datafiles):
    """Test initialization of DriveData using old RTI format."""
    file_path = datafiles / "ExampleProject_Sub_1_Drive_1.dat"

    drive_data = DriveData.init_old_rti(file_path)

    assert drive_data.sourcefilename == file_path
    assert drive_data.sourcefiletype == "old SimObserver"
    assert drive_data.metadata["ParticipantID"] == "1"
    assert drive_data.metadata["DriveID"] == "1"


@pytest.mark.datafiles(
    FIXTURE_DIR / "test_datfiles" / "ExampleProject_Sub_1_Drive_1.dat"
)
def test_init_test(datafiles):
    """Test initialization with test data."""
    df = pl.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    file_path = datafiles / "ExampleProject_Sub_1_Drive_1.dat"

    drive_data = DriveData.init_test(df, file_path)

    assert drive_data.sourcefilename == file_path
    assert drive_data.data.equals(df)


def test_init_from_existing():
    """Test creating DriveData from existing DriveData."""
    original = DriveData()
    original.sourcefilename = Path("test.dat")
    original.sourcefiletype = "test"
    original.roi = "test_roi"
    original.metadata = {"key": "value"}

    # Test with default parameters
    copy = DriveData(original)
    assert copy.sourcefilename == original.sourcefilename
    assert copy.sourcefiletype == original.sourcefiletype
    assert copy.roi == original.roi
    assert copy.metadata == original.metadata

    # Test with new data
    new_df = pl.DataFrame({"A": [1, 2, 3]})
    copy_with_data = DriveData(original, new_df)
    assert copy_with_data.data.equals(new_df)


@pytest.mark.datafiles(
    FIXTURE_DIR / "test_datfiles" / "ExampleProject_Sub_1_Drive_1.dat"
)
def test_load_datfile(datafiles):
    """Test loading data from datfile."""
    file_path = datafiles / "ExampleProject_Sub_1_Drive_1.dat"

    drive_data = DriveData.init_old_rti(file_path)
    drive_data.loadData()

    assert not drive_data.data.is_empty()
    assert "VidTime" in drive_data.data.columns
    assert "SimTime" in drive_data.data.columns


@pytest.mark.datafiles(
    FIXTURE_DIR / "test_datfiles" / "ExampleProject_Sub_1_Drive_1.dat"
)
def test_copy_metadata(datafiles):
    """Test copying metadata between DriveData objects."""
    file_path = datafiles / "ExampleProject_Sub_1_Drive_1.dat"

    source = DriveData.init_old_rti(file_path)
    source.roi = "test_roi"
    source.metadata["TestKey"] = "TestValue"

    target = DriveData()
    target.copyMetaData(source)

    assert target.sourcefilename == source.sourcefilename
    assert target.sourcefiletype == source.sourcefiletype
    assert target.roi == source.roi
    assert target.metadata == source.metadata


@pytest.mark.datafiles(
    FIXTURE_DIR / "test_datfiles" / "ExampleProject_Sub_1_Drive_1.dat"
)
def test_check_columns(datafiles):
    """Test column validation."""
    file_path = datafiles / "ExampleProject_Sub_1_Drive_1.dat"

    drive_data = DriveData.init_old_rti(file_path)
    drive_data.loadData()

    # Should not raise for existing columns
    drive_data.checkColumns(["VidTime", "SimTime"])

    # Should raise for missing columns
    with pytest.raises(ColumnsMatchError) as exc_info:
        drive_data.checkColumns(["NonExistentColumn"])

    assert "NonExistentColumn" in str(exc_info.value)
    assert "NonExistentColumn" in exc_info.value.missing_columns


def test_columns_match_error():
    """Test ColumnsMatchError class."""
    error = ColumnsMatchError("Custom message", ["col1", "col2"])
    assert "Custom message" in str(error)
    assert error.missing_columns == ["col1", "col2"]

    # Test default message generation
    error = ColumnsMatchError("", ["col3", "col4"])
    assert "Columns in DriveData object not as expected" in str(error)
    assert "col3" in str(error)
    assert "col4" in str(error)


def test_init_rti_and_load_data(tmp_path):
    file_path = tmp_path / "DX_Alice_City_42.dat"
    file_path.write_text("VidTime SimTime\n1 1\n2 2\n3 3")

    drive_data = DriveData.init_rti(file_path)
    drive_data.loadData()

    assert drive_data.sourcefiletype == "SimObserver r2"
    assert not drive_data.data.is_empty()


def test_init_scanner_and_load_data(tmp_path):
    file_path = tmp_path / "p001v01d02.txt"
    file_path.write_text("colA\tcolB\n1\t2\n3\t4")

    drive_data = DriveData.init_scanner(file_path)
    drive_data.loadData()

    assert drive_data.sourcefiletype == "Scanner"
    assert "colA" in drive_data.data.columns


def test_check_columns_numeric_valid():
    df = pl.DataFrame({"A": [1, 2, 3], "B": [4.5, 5.5, 6.5]})
    dd = DriveData.init_test(df, Path("dummy.dat"))
    dd.checkColumnsNumeric(["A", "B"])  # Should not raise


def test_check_columns_numeric_invalid_type():
    df = pl.DataFrame({"A": ["x", "y", "z"]})
    dd = DriveData.init_test(df, Path("dummy.dat"))
    with pytest.raises(ColumnsMatchError) as exc_info:
        dd.checkColumnsNumeric(["A"])
    assert "not numeric" in str(exc_info.value)


def test_check_columns_numeric_missing():
    df = pl.DataFrame({"A": [1, 2, 3]})
    dd = DriveData.init_test(df, Path("dummy.dat"))
    with pytest.raises(ColumnsMatchError):
        dd.checkColumnsNumeric(["B"])  # Missing column


def test_drive_data_copy():
    df = pl.DataFrame({"X": [10, 20]})
    dd = DriveData.init_test(df, Path("sample.dat"))
    dd.metadata["a"] = "b"

    copy_dd = dd.copy()
    assert copy_dd.data.equals(dd.data)


def test_columns_match_error_default_message():
    error = ColumnsMatchError("", ["MissingCol"])
    assert "Columns in DriveData object not as expected" in str(error)
    assert "MissingCol" in str(error)


def test_simobserver_r2_loads_datfile(tmp_path):
    file_path = tmp_path / "DX_Alice_City_42.dat"
    file_path.write_text("VidTime SimTime\n1 1\n2 2\n3 3")  # space-separated
    dd = DriveData.init_rti(file_path)
    dd.loadData()
    assert not dd.data.is_empty()
    assert "VidTime" in dd.data.columns


def test_scanner_loads_scannerfile(tmp_path):
    file_path = tmp_path / "p001v01d02.dat"
    file_path.write_text("col1\tcol2\n1\t2\n3\t4")  # tab-separated
    dd = DriveData.init_scanner(file_path)
    dd.loadData()
    assert not dd.data.is_empty()
    assert "col1" in dd.data.columns


def test_check_columns_numeric_missing_column_logged():
    df = pl.DataFrame({"speed": [10, 20, 30]})
    dd = DriveData.init_test(df, Path("fake.dat"))
    with pytest.raises(ColumnsMatchError) as exc_info:
        dd.checkColumnsNumeric(["not_a_column"])
    assert "not numeric" in str(exc_info.value)
