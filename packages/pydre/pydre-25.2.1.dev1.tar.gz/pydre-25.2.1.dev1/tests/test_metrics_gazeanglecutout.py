import polars as pl
import io
import pytest
import pydre.core
from pydre.filters.gazeangle import gazeAnglePreProcessing
from pydre.metrics.gazeanglecutout import (
    gazeCutoutAngleDuration,
    gazeCutoutAngleRatio,
    gazeCutoutAngleViolations,
)


@pytest.fixture
def sample_drivedata():
    # .dat file structure for debugging
    dat_content = """
    DatTime GAZE_HEADING GAZE_PITCH FILTERED_GAZE_OBJ_NAME
    0.00 0.01 0.01 WindScreen
    0.05 0.03 0.02 WindScreen
    0.10 0.06 0.04 None
    0.15 0.09 0.08 None
    0.20 0.12 0.09 WindScreen
    0.25 0.15 0.10 InteriorCabin
    0.30 0.18 0.12 None
    0.35 0.22 0.15 DrvrSideMirror
    """

    df = pl.read_csv(io.StringIO(dat_content), separator=" ", has_header=True)

    dd = pydre.core.DriveData()
    dd.data = df
    dd.metadata = {"ParticipantID": "debug-metric"}
    return dd


@pytest.mark.parametrize(
    "target_name, expected_nonzero", [(None, False), ("WindScreen", True)]
)
def test_gaze_metrics(sample_drivedata, target_name, expected_nonzero):
    result = gazeAnglePreProcessing(
        sample_drivedata, half_angle_deg=5.0, target_name=target_name
    )

    duration = gazeCutoutAngleDuration(result)
    ratio = gazeCutoutAngleRatio(result)
    violations = gazeCutoutAngleViolations(result)

    print(
        f"\n[{target_name}] Duration={duration:.3f}, Ratio={ratio:.3f}, Violations={violations}"
    )

    if expected_nonzero:
        assert duration > 0.0
        assert 0.0 < ratio <= 1.0
        assert violations >= 1
    else:
        assert duration == 0.0
        assert ratio == 0.0
        assert violations == 0
