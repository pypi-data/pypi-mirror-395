import pydre.core
import polars as pl
import pytest
import warnings
import pydre.metrics
import pydre.metrics.common


def test_colMean():
    # Create a sample Polars DataFrame

    data = {"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]}
    df = pl.DataFrame(data)
    dd = pydre.core.DriveData.init_test(df, "test.dat")

    # Test cases
    assert pydre.metrics.common.colMean(dd, var="A") == 3.0
    assert pydre.metrics.common.colMean(dd, var="B") == 30.0

    # Test cases with cutoff
    assert pydre.metrics.common.colMean(dd, var="A", cutoff=2.5) == 4.0
    assert pydre.metrics.common.colMean(dd, var="B", cutoff=25) == 40.0

    # Test for an invalid column name
    assert pydre.metrics.common.colMean(dd, var="InvalidColumn") is None


def test_colMedian():
    # Create a sample Polars DataFrame
    data = {"A": [-1, 2, 3, 4, 5], "B": [-10, 20, 30, 40, 50]}
    df = pl.DataFrame(data)
    dd = pydre.core.DriveData.init_test(df, "test.dat")

    # Test cases
    assert pydre.metrics.common.colMedian(dd, var="A") == 3.0
    assert pydre.metrics.common.colMedian(dd, var="B") == 30.0

    assert pydre.metrics.common.colMedian(dd, var="A", cutoff=2.5) == 4.0
    assert pydre.metrics.common.colMedian(dd, var="B", cutoff=25) == 40.0

    # Test for an invalid column name
    assert pydre.metrics.common.colMedian(dd, var="InvalidColumn") is None


def test_colSD():
    # Create a sample Polars DataFrame
    data = {"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]}
    df = pl.DataFrame(data)
    dd = pydre.core.DriveData.init_test(df, "test.dat")

    # Test cases
    assert pytest.approx(pydre.metrics.common.colSD(dd, var="A"), 0.01) == 1.58
    assert pytest.approx(pydre.metrics.common.colSD(dd, var="B"), 0.01) == 15.8

    # Test for an invalid column name
    assert pydre.metrics.common.colSD(dd, var="InvalidColumn") is None


def test_colMax():
    # Create a sample Polars DataFrame
    data = {"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]}
    df = pl.DataFrame(data)
    dd = pydre.core.DriveData.init_test(df, "test.dat")

    # Test cases
    assert pydre.metrics.common.colMax(dd, var="A") == 5
    assert pydre.metrics.common.colMax(dd, var="B") == 50

    # Test for an invalid column name
    assert pydre.metrics.common.colMax(dd, var="InvalidColumn") is None


def test_colMin():
    # Create a sample Polars DataFrame
    data = {"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]}
    df = pl.DataFrame(data)
    dd = pydre.core.DriveData.init_test(df, "test.dat")

    # Test cases
    assert pydre.metrics.common.colMin(dd, var="A") == 1
    assert pydre.metrics.common.colMin(dd, var="B") == 10

    # Test for an invalid column name
    assert pydre.metrics.common.colMin(dd, var="InvalidColumn") is None


def test_timeAboveSpeed():
    # Create sample Polars DataFrames for testing
    data1 = {"SimTime": [0, 1, 2, 3, 4], "Velocity": [10, 20, 30, 40, 50]}
    df1 = pl.DataFrame(data1)
    dd1 = pydre.core.DriveData.init_test(df1, "test1.dat")

    data2 = {"SimTime": [0, 1, 2, 3], "Velocity": [5, 15, 25, 35]}  # Shorter duration
    df2 = pl.DataFrame(data2)
    dd2 = pydre.core.DriveData.init_test(df2, "test2.dat")

    # Test cases with various cutoffs and percentage options
    assert pydre.metrics.common.timeAboveSpeed(dd1) == 4
    assert (
        pydre.metrics.common.timeAboveSpeed(dd1, cutoff=30) == 3
    )  # 3 seconds above 30
    assert (
        pydre.metrics.common.timeAboveSpeed(dd1, cutoff=30.1) == 2
    )  # 2 seconds above 30.1
    assert pydre.metrics.common.timeAboveSpeed(dd1, cutoff=25, percentage=True) == (
        3 / 4
    )
    assert pydre.metrics.common.timeAboveSpeed(dd2, cutoff=20) == 2
    assert pydre.metrics.common.timeAboveSpeed(dd2, cutoff=40) == 0  # No time above 40

    # Test with a cutoff that results in no time above
    assert pydre.metrics.common.timeAboveSpeed(dd1, cutoff=60) == 0

    # Test with missing required columns
    data3 = {"SimTime": [0, 1, 2], "OtherColumn": [1, 2, 3]}
    df3 = pl.DataFrame(data3)
    dd3 = pydre.core.DriveData.init_test(df3, "test3.dat")
    assert pydre.metrics.common.timeAboveSpeed(dd3) is None

    # Test with non-numeric columns (assuming it raises ColumnsMatchError)
    data4 = {"SimTime": [0, 1, 2], "Velocity": ["slow", "medium", "fast"]}
    df4 = pl.DataFrame(data4)
    dd4 = pydre.core.DriveData.init_test(df4, "test4.dat")
    assert pydre.metrics.common.timeAboveSpeed(dd4) is None


def test_timeWithinSpeedLimit():
    # Create sample Polars DataFrames for testing
    data1 = {
        "SimTime": [0, 1, 2, 3, 4],
        "Velocity": [10, 12, 18, 20, 25],  # in meters per second
        "SpeedLimit": [35, 35, 35, 50, 50],  # in miles per hour
    }
    df1 = pl.DataFrame(data1)
    dd1 = pydre.core.DriveData.init_test(df1, "test1.dat")

    data2 = {"SimTime": [0, 1, 2], "Velocity": [5, 5, 25], "SpeedLimit": [30, 30, 60]}
    df2 = pl.DataFrame(data2)
    dd2 = pydre.core.DriveData.init_test(df2, "test2.dat")

    # Test cases with various lower limits and percentage options
    assert pydre.metrics.common.timeWithinSpeedLimit(dd1, lowerlimit=0) == 2
    assert (
        pydre.metrics.common.timeWithinSpeedLimit(dd1, lowerlimit=20, percentage=True)
        == 0.5
    )
    assert pydre.metrics.common.timeWithinSpeedLimit(dd2, lowerlimit=10) == 2
    assert pydre.metrics.common.timeWithinSpeedLimit(dd2, lowerlimit=20) == 1

    # Test with a lower limit that results in no time within limit
    assert pydre.metrics.common.timeWithinSpeedLimit(dd1, lowerlimit=100) == 0

    # Test with missing required columns
    data3 = {"SimTime": [0, 1, 2], "Velocity": [10, 20, 30]}
    df3 = pl.DataFrame(data3)
    dd3 = pydre.core.DriveData.init_test(df3, "test3.dat")
    assert pydre.metrics.common.timeWithinSpeedLimit(dd3) is None

    # Test with non-numeric columns
    data4 = {
        "SimTime": [0, 1, 2],
        "Velocity": ["slow", "medium", "fast"],
        "SpeedLimit": [30, 30, 40],
    }
    df4 = pl.DataFrame(data4)
    dd4 = pydre.core.DriveData.init_test(df4, "test4.dat")
    assert pydre.metrics.common.timeWithinSpeedLimit(dd4) is None


def test_colFirst():
    df = pl.DataFrame({"Speed": [10, 20, 30]})
    dd = pydre.core.DriveData.init_test(df, "test_colFirst.dat")
    assert pydre.metrics.common.colFirst(dd, var="Speed") == 10
    assert pydre.metrics.common.colFirst(dd, var="InvalidColumn") is None


def test_colLast():
    df = pl.DataFrame({"Speed": [10, 20, 30]})
    dd = pydre.core.DriveData.init_test(df, "test_colLast.dat")
    assert pydre.metrics.common.colLast(dd, var="Speed") == 30
    assert pydre.metrics.common.colLast(dd, var="InvalidColumn") is None


def test_stoppingDist():
    df = pl.DataFrame(
        {"Velocity": [10.0, 5.0, 0.005, 0.0, 0.0], "XPos": [0, 10, 20, 25, 30]}
    )
    dd = pydre.core.DriveData.init_test(df, "test_stoppingDist.dat")
    result = pydre.metrics.common.stoppingDist(dd)
    assert isinstance(result, float)

    df_no_stop = pl.DataFrame({"Velocity": [10.0, 10.0, 10.0], "XPos": [0, 10, 20]})
    dd_no_stop = pydre.core.DriveData.init_test(df_no_stop, "test_no_stop.dat")
    assert pydre.metrics.common.stoppingDist(dd_no_stop) == 10000


def test_maxdeceleration():
    df = pl.DataFrame({"Velocity": [5, 4, 3, 2], "LonAccel": [-1.5, -2.0, -3.0, -0.5]})
    dd = pydre.core.DriveData.init_test(df, "test_maxdecel.dat")
    assert pydre.metrics.common.maxdeceleration(dd) == -3.0

    df_no_decel = pl.DataFrame({"Velocity": [5, 6, 7], "LonAccel": [0.5, 0.6, 0.7]})
    dd2 = pydre.core.DriveData.init_test(df_no_decel, "test_no_decel.dat")
    assert pydre.metrics.common.maxdeceleration(dd2) is None


def test_numbrakes():
    df = pl.DataFrame({"Brake": [0, 1, 1, 0, 1], "Velocity": [5, 5, 5, 5, 5]})
    dd = pydre.core.DriveData.init_test(df, "test_numbrakes.dat")
    assert pydre.metrics.common.numbrakes(dd) == 2

    df_none = pl.DataFrame({"Brake": [0, 0, 0], "Velocity": [2, 2, 2]})
    dd2 = pydre.core.DriveData.init_test(df_none, "test_numbrakes_none.dat")
    assert pydre.metrics.common.numbrakes(dd2) == 0


def test_colMax():
    df = pl.DataFrame({"A": [1, 7, 3]})
    dd = pydre.core.DriveData.init_test(df, "test_colMax.dat")
    assert pydre.metrics.common.colMax(dd, var="A") == 7


def test_colMin():
    df = pl.DataFrame({"A": [1, -4, 3]})
    dd = pydre.core.DriveData.init_test(df, "test_colMin.dat")
    assert pydre.metrics.common.colMin(dd, var="A") == -4


def test_colMean():
    df = pl.DataFrame({"A": [1, 2, 3, 4]})
    dd = pydre.core.DriveData.init_test(df, "test_colMean.dat")
    assert pydre.metrics.common.colMean(dd, var="A") == 2.5


def test_colSD():
    df = pl.DataFrame({"A": [1.0, 2.0, 3.0, 4.0]})
    dd = pydre.core.DriveData.init_test(df, "test_colSD.dat")
    result = pydre.metrics.common.colSD(dd, var="A")
    assert round(result, 5) == round(df["A"].std(), 5)


def test_colMedian():
    df = pl.DataFrame({"A": [1, 3, 5]})
    dd = pydre.core.DriveData.init_test(df, "test_colMedian.dat")
    assert pydre.metrics.common.colMedian(dd, var="A") == 3


def test_maxacceleration():
    df = pl.DataFrame({"Velocity": [2, 4, 6], "LonAccel": [0.1, 2.5, 1.2]})
    dd = pydre.core.DriveData.init_test(df, "test_maxacceleration.dat")
    result = pydre.metrics.common.maxacceleration(dd)
    assert result.shape[0] == 1
    assert result["LonAccel"].item() == 2.5


def test_maxAcceleration():
    df = pl.DataFrame(
        {"LatAccel": [0.0, 3.0], "LonAccel": [4.0, 0.0], "SimTime": [0.0, 1.0]}
    )
    dd = pydre.core.DriveData.init_test(df, "test_maxAcceleration.dat")
    result = pydre.metrics.common.maxAcceleration(dd)
    assert round(result, 2) == 4.0  # √(0² + 4²)


def test_laneExits():
    df = pl.DataFrame({"Lane": [2, 3, 2, 1, 2]})
    dd = pydre.core.DriveData.init_test(df, "test_laneExits.dat")
    assert pydre.metrics.common.laneExits(dd, lane=2) == 4


def test_steeringReversals():
    simtime = [i * 0.05 for i in range(10)]
    steer = [0.0, 0.2, 0.0, -0.2, 0.0, 0.2, 0.0, -0.2, 0.0, 0.2]
    df = pl.DataFrame({"SimTime": simtime, "Steer": steer})
    dd = pydre.core.DriveData.init_test(df, "test_steeringReversals.dat")
    result = pydre.metrics.common.steeringReversals(dd)
    assert isinstance(result, int)
    assert result > 0


def test_timeFirstTrue():
    df = pl.DataFrame({"SimTime": [0.0, 1.0, 2.0, 3.0], "Signal": [0, 0, 1, 1]})
    dd = pydre.core.DriveData.init_test(df, "test_timeFirstTrue.dat")

    result = pydre.metrics.common.timeFirstTrue(dd, var="Signal")
    assert result == 2.0

    df2 = pl.DataFrame({"SimTime": [0.0, 1.0, 2.0], "Signal": [0, 0, 0]})
    dd2 = pydre.core.DriveData.init_test(df2, "test_timeFirstTrue_none.dat")
    result_none = pydre.metrics.common.timeFirstTrue(dd2, var="Signal")
    assert result_none is None


def test_reactionBrakeFirstTrue():
    df = pl.DataFrame(
        {"SimTime": [0.0, 1.0, 2.0, 3.0], "BrakeSignal": [2.0, 4.0, 6.5, 7.0]}
    )
    dd = pydre.core.DriveData.init_test(df, "test_reactionBrakeFirstTrue.dat")

    result = pydre.metrics.common.reactionBrakeFirstTrue(dd, var="BrakeSignal")
    assert result == 2.0

    df_none = pl.DataFrame({"SimTime": [0.0, 1.0, 2.0], "BrakeSignal": [1.0, 2.0, 3.0]})
    dd_none = pydre.core.DriveData.init_test(
        df_none, "test_reactionBrakeFirstTrue_none.dat"
    )
    result_none = pydre.metrics.common.reactionBrakeFirstTrue(
        dd_none, var="BrakeSignal"
    )
    assert result_none is None


def test_reactionTimeEventTrue():
    df = pl.DataFrame(
        {
            "SimTime": [0.0, 1.0, 2.0, 3.0],
            "BrakeSignal": [0.0, 2.0, 5.5, 7.0],
            "Steering": [0.0, 0.1, 0.3, 0.2],
        }
    )
    dd = pydre.core.DriveData.init_test(df, "test_reactionTimeEventTrue_brake.dat")
    result = pydre.metrics.common.reactionTimeEventTrue(
        dd, var1="BrakeSignal", var2="Steering"
    )
    assert result == 2.0

    df2 = pl.DataFrame(
        {
            "SimTime": [0.0, 1.0, 2.0, 3.0],
            "BrakeSignal": [0.0, 0.1, 0.2, 0.3],
            "Steering": [0.0, 0.1, 0.25, 0.5],
        }
    )
    dd2 = pydre.core.DriveData.init_test(df2, "test_reactionTimeEventTrue_steer.dat")
    result2 = pydre.metrics.common.reactionTimeEventTrue(
        dd2, var1="BrakeSignal", var2="Steering"
    )
    assert result2 == 2.0  # SimTime at Steering >= 0.2

    df3 = pl.DataFrame(
        {
            "SimTime": [0.0, 1.0, 2.0],
            "BrakeSignal": [1.0, 1.5, 2.0],
            "Steering": [0.0, 0.1, 0.15],
        }
    )
    dd3 = pydre.core.DriveData.init_test(df3, "test_reactionTimeEventTrue_none.dat")
    result3 = pydre.metrics.common.reactionTimeEventTrue(
        dd3, var1="BrakeSignal", var2="Steering"
    )
    assert result3 is None


def test_reactionTime():
    df1 = pl.DataFrame(
        {
            "SimTime": [0.0, 1.0, 2.0],
            "Brake": [0.5, 1.2, 0.8],
            "Steer": [0.0, 0.05, 0.08],
            "XPos": [0, 1, 2],
            "HeadwayDistance": [10.0, 9.0, 8.0],
        }
    )
    dd1 = pydre.core.DriveData.init_test(df1, "test_reactionTime_brake.dat")
    assert pydre.metrics.common.reactionTime(dd1) == 1.0

    df2 = pl.DataFrame(
        {
            "SimTime": [0.0, 1.0, 2.0],
            "Brake": [0.5, 0.5, 0.5],
            "Steer": [0.0, 0.05, 0.25],
            "XPos": [0, 1, 2],
            "HeadwayDistance": [10.0, 9.0, 8.0],
        }
    )
    dd2 = pydre.core.DriveData.init_test(df2, "test_reactionTime_steer.dat")
    assert pydre.metrics.common.reactionTime(dd2) == 2.0

    df3 = pl.DataFrame(
        {
            "SimTime": [0.0, 1.0, 2.0],
            "Brake": [0.5, 1.2, 1.5],  # brake at t=1
            "Steer": [0.0, 0.3, 0.1],
            "XPos": [0, 1, 2],
            "HeadwayDistance": [10.0, 9.0, 8.0],
        }
    )
    dd3 = pydre.core.DriveData.init_test(df3, "test_reactionTime_both.dat")
    assert pydre.metrics.common.reactionTime(dd3) == 1.0

    df4 = pl.DataFrame(
        {
            "SimTime": [0.0, 5.0, 11.0],
            "Brake": [0.1, 0.1, 0.1],
            "Steer": [0.0, 0.05, 0.08],
            "XPos": [0, 1, 2],
            "HeadwayDistance": [10.0, 9.0, 8.0],
        }
    )
    dd4 = pydre.core.DriveData.init_test(df4, "test_reactionTime_none.dat")
    assert pydre.metrics.common.reactionTime(dd4) is None


def test_closeFollowing():
    df1 = pl.DataFrame(
        {
            "SimTime": [0.0, 0.1, 0.2, 0.3, 0.4],
            "HeadwayTime": [3.0, 1.5, 1.0, 2.0, 3.5],
            "Velocity": [10, 10, 10, 10, 10],
        }
    )
    dd1 = pydre.core.DriveData.init_test(df1, "test_closeFollowing.dat")

    # only index 1, 2 meet HeadwayTime < 2.0
    # → delta_t = 0.1 + 0.1 = 0.2
    assert (
        pytest.approx(pydre.metrics.common.closeFollowing(dd1, threshold=2), 0.01)
        == 0.2
    )


def test_steeringReversalRate():
    simtime = [i * 0.05 for i in range(20)]
    steer = [
        0.0,
        0.3,
        0.0,
        -0.3,
        0.0,
        0.3,
        0.0,
        -0.3,
        0.0,
        0.3,
        0.0,
        -0.3,
        0.0,
        0.3,
        0.0,
        -0.3,
        0.0,
        0.3,
        0.0,
        -0.3,
    ]
    df = pl.DataFrame({"SimTime": simtime, "Steer": steer})
    dd = pydre.core.DriveData.init_test(df, "test_steeringReversalRate.dat")

    result = pydre.metrics.common.steeringReversalRate(dd)

    assert isinstance(result, float)
    assert result > 0


def test_leadVehicleCollision():
    df = pl.DataFrame(
        {
            "SimTime": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            "HeadwayDistance": [3.5, 2.5, 2.4, 2.9, 2.0, 3.0],
        }
    )
    dd = pydre.core.DriveData.init_test(df, "test_leadVehicleCollision.dat")
    result = pydre.metrics.common.leadVehicleCollision(dd)
    assert result == 2

    df_none = pl.DataFrame(
        {"SimTime": [0.0, 0.1, 0.2], "HeadwayDistance": [3.0, 3.1, 3.2]}
    )
    dd_none = pydre.core.DriveData.init_test(
        df_none, "test_leadVehicleCollision_none.dat"
    )
    result_none = pydre.metrics.common.leadVehicleCollision(dd_none)
    assert result_none == 0


def test_steeringEntropy():
    simtime = [i * 0.1 for i in range(10)]
    steer = [-1.0, -0.7, -0.4, -0.1, 0.0, 0.1, 0.4, 0.7, 1.0, 0.3]

    df = pl.DataFrame({"SimTime": simtime, "Steer": steer})
    dd = pydre.core.DriveData.init_test(df, "test_steeringEntropy.dat")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        result = pydre.metrics.common.steeringEntropy(dd)

    assert isinstance(result, float)
    assert result >= 0


def test_biopticDipMeasure():
    df = pl.DataFrame(
        {
            "SimTime": [0.0, 0.5, 1.0, 1.5, 2.0],
            "hpBinary": [1, 0, 0, 1, 0],
            "DipRegions": [0, 1, 1, 0, 2],
            "HeadPitch": [0.0, -5.0, -4.5, -2.0, -6.0],
        }
    )
    dd = pydre.core.DriveData.init_test(df, "test_biopticDipMeasure.dat")

    result = pydre.metrics.common.biopticDipMeasure(dd)
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[1] == 2  # numDips
    assert result[0] > 0  # meanDipTime
    assert result[2] > 0  # medianDipTime

    # missing required columns case
    df_bad = pl.DataFrame(
        {
            "SimTime": [0.0, 0.5, 1.0],
            "hpBinary": [0, 0, 0],
            "DipRegions": [1, 1, 2],
            # missing "HeadPitch"
        }
    )
    dd_bad = pydre.core.DriveData.init_test(df_bad, "test_biopticDipMeasure_bad.dat")
    result_bad = pydre.metrics.common.biopticDipMeasure(dd_bad)
    assert result_bad == [None, None, None]


def test_roadExits_safe():
    df = pl.DataFrame(
        {
            "SimTime": [0.0, 0.1, 0.2, 0.3],
            "RoadOffset": [3.0, 4.0, 6.0, 7.1],
            "Velocity": [0.5, 0.8, 1.0, 1.0],
        }
    )
    dd = pydre.core.DriveData.init_test(df, "test_roadExits_safe.dat")
    result = pydre.metrics.common.roadExits(dd)
    assert result == 0.0


def test_laneViolations():
    df = pl.DataFrame(
        {"LaneOffset": [0.0, 1.5, 2.0, 1.0, 2.5, 1.0], "Lane": [2, 2, 2, 2, 2, 2]}
    )
    dd = pydre.core.DriveData.init_test(df, "test_laneViolations.dat")
    result = pydre.metrics.common.laneViolations(dd)
    assert isinstance(result, int)
    assert result > 0


def test_laneViolationDuration():
    df = pl.DataFrame(
        {
            "LaneOffset": [0.0, 2.0, 3.0, 0.5],
            "Lane": [2, 2, 2, 2],
            "LaneDuration": [1.0, 1.0, 1.0, 1.0],  # not directly used
            "SimTime": [0.0, 1.0, 2.0, 3.0],
            "Duration": [1.0, 1.0, 1.0, 1.0],
        }
    )
    dd = pydre.core.DriveData.init_test(df, "test_laneViolationDuration.dat")
    result = pydre.metrics.common.laneViolationDuration(dd)
    assert isinstance(result, float)
    assert result > 0


def test_roadExitsY():
    df = pl.DataFrame(
        {
            "SimTime": [0.0, 0.2, 0.4, 0.6],
            "YPos": [0.0, 3.0, 8.0, 3.5],
            "RoadOffset": [0.5, 2.0, 8.0, 3.0],
            "Velocity": [2.0, 2.0, 2.0, 2.0],
        }
    )
    dd = pydre.core.DriveData.init_test(df, "test_roadExitsY.dat")
    result = pydre.metrics.common.roadExitsY(dd)
    assert isinstance(result, float)
    assert result > 0


def test_timeToOutsideThreshold():
    df = pl.DataFrame({"SimTime": [0.0, 1.0, 2.0, 3.0], "Steer": [0.0, 0.1, 0.2, 0.6]})
    dd = pydre.core.DriveData.init_test(df, "test_timeToOutsideThreshold.dat")
    result = pydre.metrics.common.timeToOutsideThreshold(
        dd, var="Steer", threshold_high=0.5
    )
    assert result == 3.0

    df2 = pl.DataFrame({"SimTime": [0.0, 1.0, 2.0], "Steer": [0.0, 0.1, 0.2]})
    dd2 = pydre.core.DriveData.init_test(df2, "test_timeToOutsideThreshold_none.dat")
    result2 = pydre.metrics.common.timeToOutsideThreshold(
        dd2, var="Steer", threshold_high=0.5
    )
    assert result2 is None
