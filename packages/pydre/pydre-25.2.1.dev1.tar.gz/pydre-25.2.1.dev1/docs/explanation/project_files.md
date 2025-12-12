---
title: Project Files
---

# Project Files

Project files define the processing steps applied to the dataset. This is how users of the software specify the filters, regions of interest, and metrics that are run to get the final processed CSV output. Project files are written in [TOML](https://toml.io/).

# Anatomy of a project file

```toml title="test1_pf.toml"
[config]
outputfile = "Anasazi_output.csv"
datafiles = ["E:/work/data/Anasazi/*.dat"]

[filters.XPos_zscore]
function = "zscoreCol"
col = "Velocity"
newcol = "Velocity_zscore"

[rois.CruiseButtons]
type = "column"
columnname = "CruiseButtons"

[metrics.meanZscoreVel]
function = "colMean"
var = "Velocity_zscore"

[metrics.meanYPos]
function = "colMean"
var = "YPos"
```

Project files have four types of elements: config, filters, ROIs and metrics. For the latter three, In the TOML file, the start of each element is in the format `[elementtype.elementname]` where *elementtype* is one of "filters", "rois", or "metrics" and *elementname* is the name of the element. Names must be unique between elements of the same type. For filters and ROIs, the names are just for reference, but for the metrics, the name of the element defines the name of the output column where the metric results are placed. 

Below the start of each element, fields for the element are defined. Filters and metrics both have a mandatory *function* field. This field is the [metric function](../reference/metrics.md) or [filter function](../reference/filters.md) that is called internally during data processing. Each filter or metric has additional fields that may or must be defined to run correctly. 

[ROIs](../explanation/rois.md) can also be defined, and aid in computing repeated measures experiments or in any experiments where it is useful to partition each datafile into different parts before metrics are run. 

The config section of the project file is used to define any global variables that are used in the project file. Currently, you can define the input data directory and the output file name in the config section. You can also define the
[custom metrics and custom filter directories](../tutorial/custom_metrics.md) in the config section.
