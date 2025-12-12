# Developer notes

## Development environment

If you want to create your own metrics or filters, we recommend
setting up a local development environment. 

The recommended way to set up your local 
environment to run Pydre is to use [Rye](https://rye.astral.sh/):

1. Install Rye.
2. Either clone the Git repository to a local directory or unzip a release package of Pydre
3. Navigate to the Pydre directory in the terminal.
4. Run `rye sync`

This will download the appropriate python packages needed to run Pydre.

## DriveData objects

This is the primary unit of data storage for the module. DriveData objects are initially created from dat files, and then they are split by the ROI functions. 

  - SubjectID: Unique identifier for this object. Any file loaded into a DriveData object should ONLY be data from this subject number, however, this is not currently enforced
  - roi: Singular string denoting the region of interest of the particular DriveData. There can currently only be one region of interest per DriveData object
  - data: Polars dataframe containing the rows of the drive data
  - sourcefilename: The filename of where the data originally came from
  

# Project objects

This is where the processing actually takes place. A project is constructed by reading in a project file. 

## Tips for Writing New Metrics

Metrics are used to calculate values from the data, and the calculations are done after the data is filtered.

Everytime you want to make a new metric, you need to use the `@registerMetric` decorator followed by the function definition.

Generally, every metric begins with the same two lines:  
```
required_col = [array of column names]  
try:
    drivedata.checkColumnsNumeric(required_col)
except pl.exceptions.PolarsError:
    return None  
```
This is to ensure that the columns you need in order to calculate your metric are part of the dataset.  

As metrics calculate some value, every metric has a return statement.  
If no output is specified, the return value gets outputted in an out.csv file under a column titled the metrics name.  
If the data is sectioned into multiple regions of interests (rois), the metric will be processed on each roi and produce
a row for each roi in the output file.  