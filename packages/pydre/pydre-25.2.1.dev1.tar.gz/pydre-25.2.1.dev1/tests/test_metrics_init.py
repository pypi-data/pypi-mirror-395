import pytest
import polars as pl
from pathlib import Path
import pydre.metrics as metrics_module

from pydre.metrics import registerMetric, metricsList, metricsColNames
from pydre.core import DriveData


@pytest.fixture
def dummy_drive_data():
    data = pl.DataFrame({"speed": [10, 20, 30]})
    return DriveData.init_test(data, Path("dummyfile.dat"))


def test_register_metric_adds_to_dict(dummy_drive_data):
    @registerMetric("my_test_metric", ["mean_speed"])
    def calc_mean_speed(data: DriveData):
        return data.data["speed"].mean()

    assert "my_test_metric" in metricsList
    assert callable(metricsList["my_test_metric"])
    assert metricsColNames["my_test_metric"] == ["mean_speed"]
    assert metricsList["my_test_metric"](dummy_drive_data) == 20.0


def test_register_metric_defaults_to_func_name(dummy_drive_data):
    @registerMetric()
    def speed_range(data: DriveData):
        return data.data["speed"].max() - data.data["speed"].min()

    assert "speed_range" in metricsList
    assert metricsColNames["speed_range"] == ["speed_range"]
    assert metricsList["speed_range"](dummy_drive_data) == 20


def test_check_data_columns_decorator_logs(monkeypatch):
    log_msgs = []

    monkeypatch.setattr(
        metrics_module.logger, "debug", lambda msg: log_msgs.append(msg)
    )

    @metrics_module.check_data_columns(None)
    def double_value(x):
        return x * 2

    result = double_value(7)
    assert result == 14
    assert any("called with" in str(m) for m in log_msgs)
    assert any("return value" in str(m) for m in log_msgs)


def teardown_module(module):
    metricsList.clear()
    metricsColNames.clear()
