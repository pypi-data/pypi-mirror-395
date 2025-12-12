import polars as pl
import pytest
from pydre.core import DriveData
import pydre.metrics.box as box


@pytest.fixture
def sample_data():
    df = pl.DataFrame({"ReactionTime": [1.2, 2.4, 0.8, None, 3.0]})
    return DriveData.init_test(data=df, sourcefilename="dummy.dat")


def test_average_box_reaction_time(sample_data):
    values = [1.2, 2.4, 0.8, 3.0]
    expected = sum(values) / len(values)
    result = box.averageBoxReactionTime(sample_data)
    assert abs(result - expected) < 1e-6


def test_sd_box_reaction_time(sample_data):
    values = [1.2, 2.4, 0.8, 3.0]
    expected_std = pl.Series(values).std()
    result = box.sdBoxReactionTime(sample_data)
    assert abs(result - expected_std) < 1e-6


def test_count_box_hits(sample_data):
    result = box.countBoxHits(sample_data)
    assert result == 4


def test_percent_box_hits(sample_data):
    result = box.percentBoxHits(sample_data, cutoff=5)
    expected = (4 / 4) * 100
    assert abs(result - expected) < 1e-6


def test_count_box_misses(sample_data):
    result = box.countBoxMisses(sample_data)
    assert result == 0


def test_percent_box_misses(sample_data):
    result = box.percentBoxMisses(sample_data)
    expected = (0 / 4) * 100
    assert abs(result - expected) < 1e-6


def test_metrics_with_empty_data():
    empty_df = pl.DataFrame({"ReactionTime": []})
    empty_data = DriveData.init_test(data=empty_df, sourcefilename="empty.dat")

    assert box.countBoxHits(empty_data) == 0
    assert box.percentBoxHits(empty_data) == 0
    assert box.countBoxMisses(empty_data) == 0
    assert box.percentBoxMisses(empty_data) == 0
    assert box.averageBoxReactionTime(empty_data) == 0
    assert box.sdBoxReactionTime(empty_data) == 0
