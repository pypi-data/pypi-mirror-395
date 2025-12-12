import polars as pl
import pydre.core
from pydre.metrics import registerMetric


@registerMetric()
def averageBoxReactionTime(drivedata: pydre.core.DriveData):
    required_col = ["ReactionTime"]
    drivedata.checkColumns(required_col)

    # Filter all reaction times that are positive (hit boxes)
    df = drivedata.data.filter(pl.col("ReactionTime") > 0).select("ReactionTime")

    if df.is_empty():
        return 0

    return df.mean().item()


@registerMetric()
def sdBoxReactionTime(drivedata: pydre.core.DriveData):
    required_col = ["ReactionTime"]
    drivedata.checkColumns(required_col)

    df = drivedata.data.filter(pl.col("ReactionTime") > 0).select("ReactionTime")

    if df.is_empty():
        return 0

    return df.std().item()


def countBoxHits(drivedata: pydre.core.DriveData, cutoff=5):
    required_col = ["ReactionTime"]
    diff = drivedata.checkColumns(required_col)
    return drivedata.data.filter(
        pl.col("ReactionTime").is_between(0, cutoff, closed="both")
    ).height


@registerMetric()
def percentBoxHits(drivedata: pydre.core.DriveData, cutoff=5):
    required_col = ["ReactionTime"]
    drivedata.checkColumns(required_col)
    df = drivedata.data.select(pl.col("ReactionTime")).drop_nulls()
    if df.is_empty():
        return 0
    return (
        df.filter(pl.col("ReactionTime").is_between(0, cutoff, closed="both")).height
        / df.height
    ) * 100


# negative reaction time from the filter indicates a missed box
def countBoxMisses(drivedata: pydre.core.DriveData):
    required_col = ["ReactionTime"]
    diff = drivedata.checkColumns(required_col)
    return drivedata.data.filter(pl.col("ReactionTime") < 0).height


@registerMetric()
def percentBoxMisses(drivedata: pydre.core.DriveData):
    required_col = ["ReactionTime"]
    drivedata.checkColumns(required_col)
    df = drivedata.data.select(pl.col("ReactionTime")).drop_nulls()
    if df.is_empty():
        return 0
    return (df.filter(pl.col("ReactionTime") < 0).height / df.height) * 100


#
# @registerMetric()
# def boxMetrics(drivedata: pydre.core.DriveData, cutoff: float = 0, stat: str = "count"):
#     required_col = ["SimTime", "FeedbackButton", "BoxAppears"]
#     diff = drivedata.checkColumns(required_col)
#
#     total_boxclicks = pandas.Series(dtype="float64")
#     # original code here: total_boxclicks = pandas.Series()
#     # Got this warning on pandas 1.2.4: " DeprecationWarning: The default dtype for empty Series will be 'object'
#     # instead of 'float64' in a future version. Specify a dtype explicitly to silence this warning."
#     # Plz change it back to the original code if the current one leads to an issue
#     time_boxappeared = 0.0
#     time_buttonclicked = 0.0
#     hitButton = 0
#     df = pandas.DataFrame(drivedata.data, columns=required_col)  # drop other columns
#     df = pandas.DataFrame.drop_duplicates(
#         df.dropna(axis=0, how="any")
#     )  # remove nans and drop duplicates
#     if len(df) == 0:
#         return None
#     boxAppearsdf = df["BoxAppears"]
#     simTimedf = df["SimTime"]
#     boxOndf = boxAppearsdf.diff(1)
#     indicesBoxOn = boxOndf[boxOndf.values > 0.5].index[0:]
#     indicesBoxOff = boxOndf[boxOndf.values < 0.0].index[0:]
#     feedbackButtondf = df["FeedbackButton"]
#     reactionTimeList = list()
#     for counter in range(0, len(indicesBoxOn)):
#         boxOn = int(indicesBoxOn[counter])
#         boxOff = int(indicesBoxOff[counter])
#         startTime = simTimedf.loc[boxOn]
#         buttonClickeddf = feedbackButtondf.loc[boxOn:boxOff].diff(1)
#         buttonClickedIndices = buttonClickeddf[buttonClickeddf.values > 0.5].index[0:]
#
#         if len(buttonClickedIndices) > 0:
#             indexClicked = int(buttonClickedIndices[0])
#             clickTime = simTimedf.loc[indexClicked]
#             reactionTime = clickTime - startTime
#             reactionTimeList.append(reactionTime)
#         else:
#             if counter < len(indicesBoxOn) - 1:
#                 endIndex = counter + 1
#                 endOfBox = int(indicesBoxOn[endIndex])
#                 buttonClickeddf = feedbackButtondf.loc[boxOn : endOfBox - 1].diff(1)
#                 buttonClickedIndices = buttonClickeddf[
#                     buttonClickeddf.values > 0.5
#                 ].index[0:]
#                 if len(buttonClickedIndices) > 0:
#                     indexClicked = int(buttonClickedIndices[0])
#                     clickTime = simTimedf.loc[indexClicked]
#                     reactionTime = clickTime - startTime
#                     reactionTimeList.append(reactionTime)
#         sum = feedbackButtondf.loc[boxOn:boxOff].sum()
#         if sum > 0.000:
#             hitButton = hitButton + 1
#     if stat == "count":
#         return hitButton
#     elif stat == "mean":
#         mean = np.mean(reactionTimeList, axis=0)
#         return mean
#     elif stat == "sd":
#         sd = np.std(reactionTimeList, axis=0)
#         return sd
#     else:
#         print("Can't calculate that statistic.")
#     return hitButton
