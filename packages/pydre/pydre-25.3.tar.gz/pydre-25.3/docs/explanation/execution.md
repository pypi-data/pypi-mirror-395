---
title: Execution of the pydre package from the command line
---

The `pydre` entrypoint provides a command-line interface for processing driving data through project files and generating analysis results.

## Command Line Usage

If installed via `rye` (similarly for `uv`):

```
rye run pydre -p PROJECT_FILE [-d DATAFILES [DATAFILES ...]] [-o OUTPUT_FILE] [-l LOG_LEVEL]
```

If installed via `pip` or another situation where `pydre` is in your `PATH`:

```
pydre -p PROJECT_FILE [-d DATAFILES [DATAFILES ...]] [-o OUTPUT_FILE] [-l LOG_LEVEL]
```

### Required Arguments

- `-p, --projectfile`: Path to the project configuration file (TOML or JSON format)
  - Defines filters, ROIs (Regions of Interest), metrics, and configuration settings

### Optional Arguments

- `-d, --datafiles`: One or more data files to process
  - Can be specified as a space-separated list
  - Overrides or adds to any data files defined in the project file
  
- `-o, --outputfile`: Name of the output file (CSV format)
  - Default: `out.csv`
  - Overrides the output file name specified in the project file
  
- `-l, --warninglevel`: Logging level
  - Valid options: `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`
  - Default: `WARNING`

## Examples

### Basic Usage

Process a project file with the data files defined in it:

```
pydre -p projects/analysis.toml
```

### Specifying Data Files

Process specific data files with a project file:

```
pydre -p projects/analysis.toml -d data/drive1.dat data/drive2.dat
```

### Changing Output File

Save results to a custom output file:

```
pydre -p projects/analysis.toml -o results/custom_output.csv
```

### Verbose Logging

Use INFO level logging for more detailed information:

```
pydre -p projects/analysis.toml -l INFO
```

## Process Flow

1. The program loads the project file (TOML or JSON)
2. If specified, additional data files are added to the project
3. For each data file:
   - Data is loaded
   - Filters are applied in the order defined in the project
   - ROIs are processed to split data into relevant segments
   - Metrics are calculated for each ROI
4. Results are aggregated and saved to the output CSV file

## Return Codes

- `0`: Successful execution
- `1`: Error occurred during execution (check logs for details)

