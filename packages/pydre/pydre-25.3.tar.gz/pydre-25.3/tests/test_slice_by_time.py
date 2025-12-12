import polars as pl
from pydre.rois import sliceByTime


def test_slice_by_time_invalid_column():
    df = pl.DataFrame({"WrongTime": [0, 1, 2]})
    result = sliceByTime(0.0, 1.0, "NoSuchColumn", df)
    assert result.equals(df)
