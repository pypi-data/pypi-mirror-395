# Getting Started

Pydre is a Python application, run from the command line. 

# pydre.run

The main entry point to run Pydre is `pydre`. This application that allows the user to analyze data using command line arguments.

The user must enter the path for the project file and data file in order to aggregate the data. The user has the option of specifying an output file name, to which the test results will be saved. If no output file name is given the output will save to _"out.csv"_ by default. A brief description of the aforementioned arguments is offered below.

!!! info "Command Line Arguments for `pydre`"

    * Project File [-p]: The project file specifies a file for the regions of interest from which the data should be aggregated. It also specifies a list of metrics (the type of data) that will be aggregated from the regions of interest. 

    * Data File [-d]: The data file contains the raw metrics obtained from the simulation. This argument supports wildcards.
    
    * Output File [-o]: After the script has executed, the output file will display the aggregated metrics from the regions of interests that were both specified in the project file. The output file will be saved in the same folder as the script. 
    
    * Logger level [-l]: This defines the level the logger will print out. The default is 'warning'. Options include debug, info, warning, error, and critical.
  
Command Line Syntax:

If pydre is installed via `rye` (similar for `uv`):

```
rye run pydre -p [project file path] -d [data file path] 
    -o [output file name] -l [warning level]
```


If pydre is installed via `pip`:

```
pydre -p [project file path] -d [data file path] 
    -o [output file name] -l [warning level]
```

Example execution: 
```
rye run pydre -p examples/tutorial/tutorial.toml -d examples/tutorial/Experimenter_S1_Tutorial_11002233.dat -o tutorial.csv
```

You can download the example files [here](examples.zip).

# Example data processing

## Data files

We'll walk through the creation of a project file and running that project file on an [example data file](Experimenter_S1_Tutorial_11002233.dat).  

| DatTime | SimTime | MediaTime | LonAccel | LatAccel | Throttle | Brake | Gear | Heading  | HeadwayDistance | HeadwayTime | Lane | LaneOffset | RoadOffset | Steer    | Velocity | XPos      | YPos  | GazeObj           |
|---------|---------|-----------|----------|----------|----------|-------|------|----------|-----------------|-------------|------|------------|------------|----------|----------|-----------|-------|-------------------|
| 1.1     | 9.1     | 5.2       | 0.014943 | 0.020915 | 0        | 0     | 3    | 0.116032 | 10000           | 486.5342    | 2    | 0.1        | 5.1        | 0.003261 | 20.55353 | \-6470.89 | 14.6  | InstrumentCluster |
| 2.1     | 10.1    | 6.2       | 0.017797 | 0.020037 | 0        | 0     | 3    | 0.116593 | 10000           | 486.5269    | 2    | 0.12       | 5.12       | 0.003104 | 20.55384 | \-6460    | 15.1  | InstrumentCluster |
| 3.1     | 11.1    | 7.2       | 0.019815 | 0.019082 | 9.814428 | 0     | 3    | 0.117187 | 10000           | 486.5185    | 2    | 0.15       | 5.15       | 0.002947 | 20.5542  | \-6449.11 | 14.6  | None              |
| 4.1     | 12.1    | 8.2       | 0.02161  | 0.017984 | 9.814428 | 0     | 3    | 0.11781  | 10000           | 486.5088    | 2    | 0.2        | 5.2        | 0.002633 | 20.55461 | \-6438.21 | 14.65 | None              |
| 5.1     | 13.1    | 9.2       | 0.023096 | 0.016835 | 0        | 4.3   | 3    | 0.118379 | 10000           | 486.4993    | 2    | 0.2        | 5.2        | 0.002319 | 20.55501 | \-6427.32 | 15.2  | None              |


The example file is only five rows of a data file, where real data files are tens of thousands of lines. Also, this is synthetic data, for example purposes only, not real data from a driving simulator run.

## Project file

Say you wanted to find the standard deviation of lane position (SDLP) for this data. Pydre comes with a [standard deviation metric function](../reference/metrics.md#pydre.metrics.common.colSD), so you can use that. To do that, you would write a project file like so:

```toml title="tutorial.toml"
[metrics.SDLP]
function = "colSD"
var = "LaneOffset"
```

The `[metrics.SDLP]` section title shows the type of object we're defining (a metric) and the name of the metric ("SDLP").  The [`colSD` function](../reference/metrics.md#pydre.metrics.common.colSD) requires a parameter `var` that is the column name in the data files to calculate the standard deviation over.

After saving the project file, you can then run:

```bash

rye run pydre -p examples/tutorial/tutorial.toml -d examples/tutorial/Experimenter_S1_Tutorial_11002233.dat -o tutorial.csv
```

This will run the project commands on the specified data file and out the result in `tutorial.csv`. If you wanted to run on multiple data files, you could enter `-d ../datafiles/tutorialdata/*.dat` or something similar. Since we have no ROIs, the output csv will contain one row per input data file:

| Subject | Mode         | ScenarioName | UniqueID | ROI | SDLP                |
|---------|--------------|--------------|----------|-----|---------------------|
| S1      | Experimenter | Tutorial     | 11002233 |     | 0.04560701700396553 |

In this example, ROI is blank since we did not specify any ROIs. The metric column header is "SDLP", since we defined it under the category "metrics.**SDLP**" in the TOML project file. 

