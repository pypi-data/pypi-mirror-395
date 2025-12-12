import pytest
from pathlib import Path
import argparse

from pydre.run import parse_arguments, setup_logging, run_project, main

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_data"


# Fixtures for common mocks
@pytest.fixture
def mock_project(mocker):
    """Mock Project class and instance"""
    mock_project_class = mocker.patch("pydre.project.Project")
    mock_instance = mocker.MagicMock()
    mock_project_class.return_value = mock_instance
    return mock_project_class, mock_instance


@pytest.fixture
def mock_logger(mocker):
    """Mock logger functions"""
    return {
        "remove": mocker.patch("loguru.logger.remove"),
        "add": mocker.patch("loguru.logger.add"),
        "warning": mocker.patch("loguru.logger.warning"),
        "error": mocker.patch("loguru.logger.error"),
    }


def test_parse_arguments_minimal():
    """Test argument parsing with only required arguments."""
    args = parse_arguments(["-p", "project.toml"])
    assert args.projectfile == "project.toml"
    assert args.datafiles is None
    assert args.outputfile == "out.csv"
    assert args.warninglevel == "WARNING"


def test_parse_arguments_full():
    """Test argument parsing with all arguments provided."""
    args = parse_arguments(
        [
            "-p",
            "project.toml",
            "-d",
            "file1.dat",
            "file2.dat",
            "-o",
            "output.csv",
            "-l",
            "DEBUG",
        ]
    )
    assert args.projectfile == "project.toml"
    assert args.datafiles == ["file1.dat", "file2.dat"]
    assert args.outputfile == "output.csv"
    assert args.warninglevel == "DEBUG"


def test_parse_arguments_missing_required():
    """Test argument parsing with missing required arguments."""
    with pytest.raises(SystemExit):
        parse_arguments([])


def test_setup_logging_valid(mock_logger):
    """Test logging setup with valid log level."""
    result = setup_logging("INFO")

    mock_logger["remove"].assert_called_once()
    mock_logger["add"].assert_called_once()
    assert mock_logger["add"].call_args[1]["level"] == "INFO"
    assert result == "INFO"


def test_setup_logging_invalid(mock_logger):
    """Test logging setup with invalid log level."""
    result = setup_logging("INVALID")

    mock_logger["remove"].assert_called_once()
    mock_logger["add"].assert_called_once()
    assert mock_logger["add"].call_args[1]["level"] == "WARNING"
    mock_logger["warning"].assert_called_once_with(
        "Command line log level (-l) invalid. Defaulting to WARNING"
    )
    assert result == "WARNING"


def test_run_project_basic(mock_project):
    """Test basic project run functionality."""
    mock_project_class, mock_instance = mock_project

    result = run_project("project.toml", ["data.dat"], "output.csv")

    mock_project_class.assert_called_once_with(
        "project.toml", ["data.dat"], "output.csv"
    )
    mock_instance.processDatafiles.assert_called_once_with(numThreads=12)
    mock_instance.saveResults.assert_called_once()
    assert result == mock_instance


def test_run_project_custom_threads(mock_project):
    """Test project run with custom thread count."""
    mock_project_class, mock_instance = mock_project

    run_project("project.toml", ["data.dat"], "output.csv", num_threads=4)

    mock_instance.processDatafiles.assert_called_once_with(numThreads=4)


def test_run_project_missing_file(mocker):
    """Test project run with missing file."""
    mocker.patch(
        "pydre.project.Project", side_effect=FileNotFoundError("File not found")
    )

    with pytest.raises(FileNotFoundError):
        run_project("nonexistent.toml", ["data.dat"], "output.csv")


def test_main_success(mocker):
    """Test successful execution of main function."""
    mock_parse_args = mocker.patch("pydre.run.parse_arguments")
    mock_setup_logging = mocker.patch("pydre.run.setup_logging")
    mock_run_project = mocker.patch("pydre.run.run_project")

    mock_parse_args.return_value = argparse.Namespace(
        projectfile="project.toml",
        datafiles=["data.dat"],
        outputfile="output.csv",
        warninglevel="INFO",
    )

    result = main(["dummy"])

    mock_parse_args.assert_called_once_with(["dummy"])
    mock_setup_logging.assert_called_once_with("INFO")
    mock_run_project.assert_called_once_with("project.toml", ["data.dat"], "output.csv")
    assert result == 0


def test_main_project_error(mocker, mock_logger):
    """Test main function with project processing error."""
    mock_parse_args = mocker.patch("pydre.run.parse_arguments")
    mock_setup_logging = mocker.patch("pydre.run.setup_logging")
    mocker.patch(
        "pydre.run.run_project", side_effect=FileNotFoundError("File not found")
    )

    mock_parse_args.return_value = argparse.Namespace(
        projectfile="project.toml",
        datafiles=["data.dat"],
        outputfile="output.csv",
        warninglevel="INFO",
    )

    result = main([])

    assert result == 1
    mock_logger["error"].assert_called_once()
    assert "File not found" in mock_logger["error"].call_args[0][0]
