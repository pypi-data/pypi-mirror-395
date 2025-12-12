
# Merge Tool

Merge Tool is a program designed to effectively merge SimObserver data in the event that a
participant's drive is interrupted. This often occurs due to study interruptions such as
SimCreator shut downs. Merge Tools is run on these separate data files from the same participant's drives and
merges them into one file to ensure a uniform presentation of the data. 
	  
For example, if during a study, called 'ExampleProject', Participant 3's original drive 1 was interrupted  
prematurely two times, there would be 3 separate data files created, with different drive IDs. These 
drive files could be merged to create a single drive file for further processing.

## Merge Types
   Merge Tool has two different kinds of merge options. This section will highlight each of them.
   
### Sequential

Sequential Merge is a file merge based on time. Once all the files in the 
`merge directory (-d)` have been processed by the program, Merge Tool will use the SimCreator's recorded
`SimTime` metric to concatenate the files. This is accomplished by iterating 
through every `SimTime` column, reading the last `SimTime` value of the current data file, and adding that
value as a constant through the next data file's `SimTime` column. 
   
### Spatial
   Spatial Merge is a file merge based on X & Y coordinate positions. Much like the `Sequential`
   merge, Spatial Merge will perform the same `SimTime` corrections as multiple drives for the same participant are merged.
   However, along with the time correction, Spatial Merge also analyzes SimCreator's recorded `XPos` and `YPos` metrics.
   `out_frame` is the variable name in which all the merged data will end up, before a csv is created. For every 
   `next_frame` (files that comes after the first for the participant), the row with the minimum distance from the 
   last position in `out_frame` will be the starting index of the data that is appended to `out_frame`.
   
	
## Usage

This section covers how Merge Tool is executed as well as the command line parameters that the user is expected to supply.
   - Command Line execution
        - Ran from where pydre is ran from
        - Ex: `python pydre_merge.py -d 'exampleMergeDirectory' -t 'spatial or sequential'`
   - Two Args. 
		1. -d (DataFile directory). The directory to be merged, is occupied by multiple drives for at least one participant.
		2. -t (Merge Type). Chosen as either "Spatial" or "Sequential", determines which type of merge will be performed.


## Testing

Within the `pydre` folder, there will be a `test` directory with a sub-directory called 
`MergeTools`. This sub-directory contains all the materials for testing `pydre_merge.py`.
To run the tests, navigate to the pydre module directory (top level) and use the command:
`python -m unittest tests\MergeTools\test_merge.py`. 
	  
### Testing Explanation

- There are two, primary functions to test within `merge_tool.py`, one for each merge 
		  type (`Sequential` and `Spatial`). These two functions are found at (considering 
		  `pydre.merge_tool` as `p_merge`) `p_merge.MergeTool.sequential_merge()` and 
		  `p_merge.MergeTool.spatial_merge()`(see `Overview` above for merge-type
		   explanations).
		
- To properly test each of these, the testing functions must supply the two,
		  required parameters without using the command line (refer to `Usage` above).
		  Briefly, below will address how each argument is supplied in the testing. <br>

1. Merge Directory (-d) - Within `MergeTools\test_dats_to_merge\` there are a host of 
directories. Each of these directories is unique per test
case and will contain particular data files to simulate the 
intended use of the program.
		
2. Merge Type (-t) - Supplied as a string within the test case, unique to the target 
`MergeTool()` function of the current test.
		 
#### Results and Expected
This section will cover the results from running the program, the expected
results, and how the two will be compared for the sake of testing.

Results:

After calling the target function (either `Sequential` or `Spatial`) with the two
parameters from the test case, the program, after running successfully, will create
a `.csv` file per participant found in the `Merge Directory (-d)`. This `.csv` file(s)
can always be found in `MergeTools\test_dats_to_merge\current-dir\MergedData\`. With that, using the
`pandas` module for Python, it is easy to recover the contents of the `.csv`.
			
Expected:

Within `MergeTools\expected_csv` there will be a sub-directory for every test.
Each of these sub-directories will be named with the prefix `expected_` followed
by the `Merge Directory (-d)` name. (Ex: with "-d test_dats_to_merge/ref_dir"
the expected csv will be found at `MergeTools\expected_csv\expected_ref_dir\`).
These directories and their contents must be prepared prior to testing, as these 
`.csv` files' are recovered using `pandas` as well.

With both the results and expected results in the testing program, the contents
of both `.csv` files will be compared. In order for the `MergeTool()` function
to pass the test, it must produce a `.csv` file that is exactly the same as the
corresponding file found in `expected_csv`.

Note: For streamlined testing, `MergedData` is completely removed after
each test case. This ensures `test_merge.py` will have easy access to only the
pertinent results of the current, running test case.