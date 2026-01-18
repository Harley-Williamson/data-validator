# Flawed Data Report Generator

## Overview
This script usese the pandas library to check a file for errors.

It is designed to:
- Accept Commands from the Command Line:
    - Input File
    - Output File
    - Silent(Optional) 
    - Issues_Only(Optional)
- Automatically detects file extension, and file type
- Checks Rows and Columns for missing fields
- Checks date field for invalid date format
- Prints a summary to the screen
- Outputs a new file, which includes a column that lists issues for each row (Either outputs all rows, or just those with issues depending on flags)

## Requirements
- Python 3.12.3+
- Standard Libraries (pathlib, argparse, datetime)
- pandas library

## Usage
From the parent directory

python3 pandas_data_cleaner.py input_file output_file --silent --issues_only

example:
python3 pandas_data_cleaner.py data.csv issues.csv --silent --issues_only

## Output
- A Summary of work done to the screen. (Unless --silent flag is used.)
- An output file which includes a new column listing issues in the file. (Only if --issues_only flag isn't used.)
- An output file with only the rows that contain issues, includes an added column listing issues. (Only if --issues_only flag is used.)